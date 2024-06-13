# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 13/jun./2024  at 16:55 $'

import json
import re
import time
from datetime import datetime
from heyoo import WhatsApp
from static.extensions import secrets
from templates.database.connection import execute_sql


def search_handler(command: str, currency) -> str:
    """
    Search in the database according to the command input by the chatbot.
    :param currency:
    :param command: <string>
    :return: Response with the list of products or a none result response
    :rtype: str
    """
    res = ""
    if command != "":
        my_result = search_sql(command)
        print(my_result)
        if my_result.__len__() != 0:
            res = present_list(my_result, currency)
        else:
            res = "No se encontraron  resultados"
    else:
        print("no matched command search")
    if res.__contains__("ERROR:root:Response"):
        res = "Restart the conversation"
    return res


def send_reply_whatsapp(phone, answer):
    """
    Sends a reply to the user.
    :param phone: <string> phone number of the user
    :param answer: <string> answer to the user
    """
    message_wa = WhatsApp(secrets.get("TOKEN_WA"),
                          secrets.get("ID_PHONE_NUMBER_WA"))
    phone = phone.replace("521", "52")
    message_wa.send_message(answer, phone)


def command_handler(command: str, context: list, chat_id: str, sender_id: str) -> tuple[str, list | None]:
    """
    Handles the command received from a chat.
    :param sender_id: id of the sender
    :param chat_id: chat id in the database
    :param context: chain of messages
    :param command: <string> command received
    :return: <tuple> (response, context)
    response: <string> response to the command
    context: <list> context of the conversation
    """
    res = ""
    print("data from: ", str(chat_id) + "+" + str(sender_id))
    match command:
        case "start":
            if len(context) > 2:
                res = context[2]["content"]
                context = context[0:2]
            else:
                res = "Bienvenido"
                context = context[0]
                context.append({"role": "User", "content": "Hola"})
        case "stop":
            pass
        case "close":
            pass
        case "end":
            # send_ListData_generator("hola2", chat_id, sender_id)
            res = "end"
            pass
    return res, context


def command_simplifier(cmd_tag: str) -> str:
    """
    Returns a command output (string) based on the tag.

    :param cmd_tag: tag name of the command.
    :return: output (string).
    """
    # cmd_tag = nltk.word_tokenize(cmd_tag)[0]
    commands = {
        "start": "start",
        "stop": "stop",
        "close": "close",
        "end": "end"
    }
    return commands.get(cmd_tag, "default")


def extract_command(res: str) -> list:
    """
    Extract the command from the response
    :param res: <string> response
    :return: <list> [<command>, <response>]
    """
    command = ""
    flag_search = False
    match_command = re.search("/search: *", res)
    match_command2 = re.search(r"'''.*?'''", res)
    if match_command is not None and match_command2 is not None:
        print("extrayendo comando")
        index_0 = match_command.regs[0][0]
        index_1 = match_command2.regs[0][1]
        command = res[index_0 - 3:index_1]
        res = res[:index_0 - 3]
        flag_search = True
    return [command, res, flag_search]


def message_handler(msg: str, context: list, chat_id: str, sender_id: str) -> tuple:
    """
    Obtains an answer from the chatbot based on the message received.
    :param sender_id: id of the sender
    :param chat_id: chat id in the database
    :param context: chain of messages
    :param msg: <string> message received
    :return : <tuple> (response, command, flag_search, context)
    response: <string> response to the message
    command: <string> command to the message
    flag_search: <bool> flag to search for the command
    context: <list> context of the conversation
    """
    flag_search = False
    if msg.startswith('/'):
        command = command_simplifier(msg[1:])
        res, context = command_handler(command, context, chat_id, sender_id)
        print("command: ", res)
    else:
        res = get_response(context)
        command, res, flag_search = extract_command(res)
        print("answer: {} command: {} flag_search: {}".format(res, command, flag_search))
    return res, command, flag_search, context


def retrieve_conversation(sender_id: str, receiver_id: str) -> tuple:
    """
    if a conversation is present in the database that complains with the
    sender_id and receiver_id, then it is returned the previous context.
    if not, then it is created a simple json context and a flag raised indicating
    a new register must be created in the database.

    :param sender_id: <string> sender identification
    :param receiver_id: <string> receiver identification
    :return: <list> [<chat_id>, <res>, <flag>]
        <chat_id>: <int> chat_id
        <res>: <list> json context
        <flag>: <bool> flag indicating if a new register must be created
        in the database
    """
    sql = "SELECT context, chat_id FROM chats " \
          "WHERE sender_id = %s AND receiver_id = %s " \
          "AND timestampdiff(MINUTE, timestamp_end, %s)<5 " \
          "AND is_alive = %s"
    time_now = time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime())
    val = (sender_id, receiver_id, time_now, '1')
    # my_cursor.execute(sql, val)
    # my_result = my_cursor.fetchall()
    my_result = execute_sql(sql, val, 2)
    chat_id = 0
    flag = True
    res = [json.loads(open('context_handler.json', encoding='utf-8').read())["context"]]
    if my_result is not None:
        if my_result.__len__() > 0:
            res = json.loads(my_result[0][0])
            chat_id = my_result[0][1]
            flag = False
    return chat_id, res, flag


def process_message_attachment(attachment: any):
    """
    Process attachments in the messages.
    :param attachment: <Any> attachment of the message
    :return: <string> response to the message
    """
    print("attachment: ", attachment)
    if attachment.get("type") == "image":
        return "image attachment supported"
    elif attachment.get("type") == "video":
        return "video attachment supported"
    elif attachment.get("type") == "audio":
        return "audio attachment supported"
    elif attachment.get("type") == "file":
        return "file attachment supported"
    else:
        return "no attachment supported"


def remove_prefix_str(string: str, prefix: str) -> str:
    size = len(prefix)
    return string[size:]


def check_syntax(sender_id):
    out = False
    if re.findall(r'^w', sender_id):
        sender_id = remove_prefix_str(sender_id, 'w')
        if re.findall(r'^\d+$', sender_id):
            return True
    return out


def parse_message(data, platform: str) -> tuple:
    """
    if message is a json, the msg is unpacked with necessary information provided
    by the API.
    :param data: json packaged information
    :param platform: <string> APIs platform name
    :return: <tuple> [<sender_id>, <text>, <timestamp>, <receiver_id>,
     <attachment>, <is_status>]
    """
    timestamp = time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime())
    receiver_id = "11"
    attachment = []
    txt = ""
    sender_id = ""
    is_status = False
    currency = "MXN"
    try:
        if platform == "facebook":
            print("message F-->", data)
            for event in data['entry']:
                messaging = event['messaging']
                for msg in messaging:
                    if msg.get('message'):
                        sender_id = msg['sender']['id']
                        if msg['message'].get('text'):
                            txt = msg['message']['text']
                        if msg['message'].get('attachments'):
                            attachment = process_message_attachment(
                                msg['message']['attachments'])
        elif platform == "whatsapp":
            print("message W -->", data)
            entry = data['entry'][0]['changes'][0]['value']
            if 'messages' in entry:
                sender_id = entry['messages'][0]['from']
                txt = entry['messages'][0]['text']['body']
                id_wa = entry['messages'][0]['id']
                timestamp = datetime.fromtimestamp(int(entry['messages'][0]['timestamp']))
                print("message sent from: %s at %s to  %s" % (sender_id, timestamp, id_wa))
            elif 'statuses' in entry:
                is_status = True
                status = entry['statuses'][0]['status']
                id_wa = entry['statuses'][0]['id']
                timestamp_status = datetime.fromtimestamp(int(entry['statuses'][0]['timestamp']))
                recipient_id = entry['statuses'][0]['recipient_id']
                print("Status changed to: %s from %s at %s when sender was %s" %
                      (status, recipient_id, timestamp_status, id_wa))
            else:
                is_status = True
                print("message Ws not recognized")
        elif platform == "telegram":
            print("message T-->", data)
            sender_id = data['message']['chat']['id']
            txt = data['message']['text']
        elif platform == "webchat":
            print("message WC-->", data)
            sender_id = data['chat_id']
            txt = data['message']
            if sender_id == "" or sender_id is None:
                is_status = True
            else:
                if not check_syntax(sender_id):
                    is_status = True
            try:
                currency = data['currency']
            except Exception as e:
                print("error: ", e)
                currency = "MXN"
        else:
            print("message O-->", data)
        return sender_id, txt, timestamp, receiver_id, attachment, is_status, currency
    except Exception as e:
        print("error: ", e)
        is_status = True
        return sender_id, txt, timestamp, receiver_id, attachment, is_status, currency
