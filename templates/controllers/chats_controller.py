# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 13/jun./2024  at 17:04 $'

import json
from datetime import datetime

from static.extensions import format_timestamps
from templates.database.connection import execute_sql


def insert_chat(context: list, sender_id: str, client_id: str, platform: str, thread_id: str, assistant_id: str):
    """
    Inserts a new chat into the database.

    :param assistant_id:
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
        "assistant_id": assistant_id,
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
        print(f"Error: {str(error)}")
    else:
        print("Insert successful")
    return flag, error, result, metadata


def upd_chats_msg(chat_id: str, content: list, metadata):
    """
    Updates the chat message in the database.

    :param chat_id: <string> id of the chat
    :param content: <list> list of dictionaries with the context of the conversation
    :param metadata: <dict> metadata of the chat
    """
    timestamp = datetime.now().strftime(format_timestamps)
    metadata["timestamp_end"] = timestamp

    sql = "UPDATE telintec_clts_chats.chats " \
          "SET content = %s, metadata = %s " \
          "WHERE chat_id = %s"
    val = (json.dumps(content), json.dumps(metadata), chat_id)
    flag, error, result = execute_sql(sql, val, 3)
    if not flag:
        print(f"Error: {str(error)}")
        print("Update failed")
    else:
        print("Update successful")
    return flag, error, result


def get_chats_msg(sender_id: str):
    """
    Retrieves the chat messages from the database.

    :param sender_id: <string> id of the receiver
    :return: <list> list of dictionaries with the chat messages
    """
    sql = ("SELECT telintec_clts_chats.chats.chat_id, content, metadata, client_id "
           "FROM telintec_clts_chats.chats "
           "WHERE metadata->'$.sender_id' = %s AND metadata->'$.is_alive' = 1")
    val = (sender_id,)
    flag, error, result = execute_sql(sql, val, 2)
    return flag, error, result


def finalize_chat(chat_id: str, metadata: dict):
    """
    Finalizes the chat in the database.

    :param chat_id: <string> id of the chat
    :param metadata: <dict> metadata of the chat
    """
    metadata["is_alive"] = 0
    sql = "UPDATE telintec_clts_chats.chats " \
          "SET metadata = %s " \
          "WHERE chat_id = %s"
    val = (json.dumps(metadata), chat_id)
    flag, error, result = execute_sql(sql, val, 3)
    if not flag:
        print(f"Error: {str(error)}")
    else:
        print("Finalize successful")
    return flag, error, result
