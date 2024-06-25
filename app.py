from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from static.extensions import api, secrets, client_id
from templates.Functions_Aux import parse_message, retrieve_conversation, message_handler, send_reply_whatsapp
from templates.controllers.chats_controller import upd_chats_msg, insert_chat, finalize_chat

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/IA/api/v1/hello')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/.well-known/pki-validation/<path:path>", methods=["GET"])
def server_static(path):
    return send_from_directory('./', path)


@app.route("/IA/api/v1/whatsapp", methods=["POST", "GET"])
def whatsapp_webhook_handler():
    # hub challenge verification
    print(secrets['VERIFY_TOKEN_WA'])
    if request.method == "GET":
        print(request.args.get('hub.verify_token'))
        with open("log.txt", "a") as f:
            f.write("request detected: " + str(request.args.get('hub.verify_token')) + "\n")
        if request.args.get('hub.verify_token') == secrets['VERIFY_TOKEN_WA']:
            with open("log.txt", "a") as f:
                f.write("request accepted: " + str(request.args.get('hub.challenge')) + "\n")
            return request.args.get('hub.challenge')
        else:
            return "Error de autentificación", 403
    elif request.method == 'POST':
        data = request.get_json()
        # parse message
        txt = ""
        try:
            sender_id, msg_txt, timestamp, attachment, is_status = parse_message(data, "whatsapp")
            if is_status:
                print("Empty message")
                return jsonify({"status": "success", "message": "Empty"}), 200
            if msg_txt is None:
                print("No message")
                return jsonify({"status": "success", "message": "No message"}), 200
            # retrieve the chat_id and context from the database
            chat_id, content, metadata, flag_create = retrieve_conversation(sender_id)
            # update context for chat
            content.append({'role': 'user',
                            'content': f"{msg_txt}"})
            txt += msg_txt+"\n"
            # get response from chatbot
            response, command, context, thread_id, assistant_id, flags = message_handler(msg_txt, content, chat_id, sender_id)
            # update the database with the new context and timestamp
            context.append({'role': 'assistant',
                            'content': f"{response}"})
            txt += response+"\n"
            if flag_create:
                flag, error, result, metadata = insert_chat(
                    context, sender_id, client_id, "whatsapp", thread_id, assistant_id)
            else:
                flag, error, result = upd_chats_msg(chat_id, context, metadata)
            txt += f"flag: {flag}, error: {error}, result: {result}\n"
            print("ChatGPT response: ", response)
            # send the response to the user
            send_reply_whatsapp(sender_id, response)
            txt += "reply sent in whatsapp\n"
            # handle an end flag
            if "is_end" in flags:
                if flags["is_end"]:
                    flag, error, result = finalize_chat(chat_id, metadata)
                    txt += f"finalize chat------flag: {flag}, error: {error}, result: {result}\n"
            with open("log.txt", "a") as f:
                f.write("-----------------stesps-----------------\n")
                f.write(txt)
            return jsonify({"status": "success"}), 200
        except KeyError as e:
            print("keyError of:" + str(e))
            return jsonify({"status": "error"}), 200
    else:
        return jsonify({"status": "ok", "message": "Not a permitted method"}), 405


api.init_app(app, doc='/IA/doc')

if __name__ == '__main__':
    app.run()
