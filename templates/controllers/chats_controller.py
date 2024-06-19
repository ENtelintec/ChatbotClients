# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 13/jun./2024  at 17:04 $'

import json
from datetime import datetime

from static.extensions import format_timestamps
from templates.database.connection import execute_sql


def insert_chat(context: list, sender_id: str, client_id: str, platform: str, thread_id: str):
    """
    Inserts a new chat into the database.

    :param context: <list> list of dictionaries with the context of the conversation
    :param sender_id: <string> id of the sender
    :param client_id: <string> id of the receiver
    :param platform: <string> platform of the conversation
    :param thread_id: <string> id of the thread
    """
    timestamp = datetime.now().strftime(format_timestamps)
    metadata = {
        "platform": platform,
        "thread_id": thread_id,
        "timestamp_start": timestamp,
        "sender_id": sender_id,
        "timestamp_end": "",
        "is_alive": 1
    }
    sql = "INSERT INTO telintec_clts_chats.chats " \
          "(content, metadata, client_id) " \
          "VALUES (%s, %s, %s)"
    val = (json.dumps(context), json.dumps(metadata), client_id)
    flag, error, result = execute_sql(sql, val, 3)
    if not flag:
        print("Error: {}".format(error))
    else:
        print("Insert successful")


def upd_chats_msg(chat_id: str, context: list, sender_id: str, client_id: str, platform: str, thread_id: str):
    """
    Updates the chat message in the database.

    :param chat_id: <string> id of the chat
    :param context: <list> list of dictionaries with the context of the conversation
    :param sender_id: <string> id of the sender
    :param client_id: <string> id of the receiver
    :param platform: <string> platform of the conversation
    :param thread_id: <string> id of the thread
    """
    timestamp = datetime.now().strftime(format_timestamps)
    metadata = {
        "platform": platform,
        "thread_id": thread_id,
        "timestamp_end": timestamp,
        "sender_id": sender_id,
        "is_alive": 0
    }
    sql = "UPDATE telintec_clts_chats.chats " \
          "SET content = %s, metadata = %s " \
          "WHERE chat_id = %s"
    val = (json.dumps(context), json.dumps(metadata), chat_id)
    flag, error, result = execute_sql(sql, val, 3)
    if not flag:
        print("Error: {}".format(error))
        print("Update failed")
        return False
    else:
        print("Update successful")
        return True

