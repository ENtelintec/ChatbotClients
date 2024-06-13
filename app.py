from flask import Flask, request, jsonify
from flask_cors import CORS

from static.extensions import api, secrets
from templates.Functions_Aux import parse_message, retrieve_conversation, message_handler, send_reply_whatsapp, \
    search_handler
from templates.controllers.chats_controller import upd_chats_msg
from templates.resources.resources_login import ns as ns_login

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/IA/api/v1/hello')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/IA/api/v1/whatsapp", methods=["POST", "GET"])
def whatsapp_webhook_handler():
    # hub challenge verification
    if request.method == "GET":
        if request.args.get('hub.verify_token') == secrets['VERIFY_TOKEN_WA']:
            return request.args.get('hub.challenge')
        else:
            return "Error de autentificación", 403
    elif request.method == 'POST':
        data = request.get_json()
        # parse message
        try:
            sender_id, msg_txt, timestamp, \
                receiver_id, attachment, is_status, currency = parse_message(data, "whatsapp")
            if not is_status:
                if msg_txt is not None:
                    # retrieve the chat_id and context from the database
                    chat_id, context, flag_create = retrieve_conversation(
                        sender_id, receiver_id)
                    # update context for chat
                    context.append({'role': 'user',
                                    'content': f"{msg_txt}"})
                    # get response from chatbot
                    response, command, flag_search, context = message_handler(msg_txt, context, chat_id, sender_id)
                    is_end = True if response == "end" else False
                    # update the database with the new context and timestamp
                    context.append({'role': 'assistant',
                                    'content': f"{response}"})
                    upd_chats_msg(chat_id, context, timestamp, is_end,
                                  sender_id, receiver_id,
                                  "whatsapp", flag_create)
                    print("ChatGPT response: ", response)
                    # send the response to the user
                    if not is_end:
                        send_reply_whatsapp(sender_id, response)
                    # do search if necessary
                    if flag_search:
                        res = search_handler(command, currency)
                        # update the database with the new context and timestamp
                        context.append({'role': 'assistant',
                                        'content': f"{res}"})
                        upd_chats_msg(chat_id, context, timestamp, is_end,
                                      sender_id, receiver_id,
                                      "whatsapp", flag_create)
                        print("ChatGPT search response: ", res)
                        # send the response to the user
                        send_reply_whatsapp(sender_id, res)
                    return jsonify({"status": "success"}), 200
                else:
                    print("Empty message")
                    return jsonify({"status": "success", "message": "Empty"}), 200
            else:
                print("Empty message")
                return jsonify({"status": "ok"}), 200
        except KeyError as e:
            print("keyError of:" + str(e))
            return jsonify({"status": "error"}), 200
    else:
        return jsonify({"status": "ok", "message": "Not a permitted method"}), 405


api.init_app(app)
api.add_namespace(ns_login)

if __name__ == '__main__':
    app.run()
