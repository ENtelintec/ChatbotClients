# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 13/jun./2024  at 16:55 $'

import json
import re
import time
from datetime import datetime, timedelta
from heyoo import WhatsApp
from static.extensions import secrets, client_name, AV_avaliable_tools_files, format_timestamps
from templates.Functions_openAI import get_response_assistant
from templates.controllers.chats_controller import get_chats_msg


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


def message_handler(msg: str, context: list, chat_id: str, sender_id: str, assistant_id=None, thread_id=None) -> tuple:
    """
    Gets an answer from the chatbot based on the message received.
    :param thread_id:
    :param assistant_id:
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
    flags = None
    if msg.startswith('/'):
        command = command_simplifier(msg[1:])
        res, context = command_handler(command, context, chat_id, sender_id)
        print("command: ", res)
    else:
        data_av = json.loads(open(AV_avaliable_tools_files[client_name.lower()], encoding='utf-8').read())
        instructions = data_av["instructions"]
        files_av, res, thread_id, assistant_id, flags = get_response_assistant(
            msg, instructions=instructions, client_tag=client_name, thread_id=thread_id, assistant_id=assistant_id)
        command, res, flag_search = extract_command(res)
        print("answer: {} command: {} flag_search: {}".format(res, command, flag_search))
    flags = flags if flags is not None else {"is_end": False}
    return res, command, context, thread_id, assistant_id, flags


def retrieve_conversation(sender_id: str) -> tuple:
    """
    if a conversation is present in the database that complains with the
    sender_id and receiver_id, then it is returned the previous context.
    if not, then it is created a simple json context and a flag raised indicating
    a new register must be created in the database.
    :param sender_id: <string> sender identification
    :return: <list> [<chat_id>, <res>, <flag>]
        <chat_id>: <int> chat_id
        <res>: <list> json context
        <flag>: <bool> flag indicating if a new register must be created
        in the database
    """
    time_now = datetime.now()
    flag, error, my_result = get_chats_msg(sender_id)
    if flag and len(my_result) > 0:
        for item in my_result:
            chat_id = item[0]
            metadata = json.loads(item[2])
            content = json.loads(item[1])
            timestamp_end = metadata.get("timestamp_end")
            if timestamp_end == "":
                continue
            timestamp_end = datetime.strptime(timestamp_end, format_timestamps)
            if time_now < timestamp_end + timedelta(minutes=5):
                return chat_id, content, metadata, False
    return None, [], {}, True


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
    timestamp = time.strftime(format_timestamps, time.localtime())
    attachment = []
    txt = ""
    sender_id = ""
    is_status = False
    try:
        if platform == "whatsapp":
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
        else:
            print("message O-->", data)
        return sender_id, txt, timestamp, attachment, is_status
    except Exception as e:
        print("error: ", e)
        is_status = True
        return sender_id, txt, timestamp, attachment, is_status
