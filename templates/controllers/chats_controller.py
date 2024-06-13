# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 13/jun./2024  at 17:04 $'

import json

from templates.database.connection import execute_sql


def upd_chats_msg(chat_id: str, context: list, timestamp: str,
                  is_end: bool, sender_id: str, receiver_id: str,
                  platform: str, f_create: bool):
    """
    Updates the database based on the parameter provided.
    If the conversation is finished, then the timestamp_end is updated.
    If the conversation is not finished, then the context is updated.
    If the conversation has finished and the register must be created,
    then a new register must be created.

    :param chat_id: <string> id of the conversation
    :param context: <list> list of dictionaries with the context of the conversation
    :param timestamp: <string> timestamp of the message
    :param is_end: <boolean> flag indicating if the conversation have finished
    :param sender_id: <string> id of the sender
    :param receiver_id: <string> id of the receiver
    :param platform: <string> platform of the conversation
    :param f_create: <boolean> flag indicating if the register must be created
    """
    if is_end:
        sql = "UPDATE chats " \
              "SET context = %s, timestamp_end = %s, is_alive = %s " \
              "WHERE chat_id = %s"
        val = (json.dumps(context), timestamp, '0', chat_id)
        flag, error, result = execute_sql(sql, val, 3)
        print(f"flag: {flag}")
        if not flag:
            print("Error: {}".format(error))
        else:
            print("Update successful")
    else:
        if f_create:
            sql = "INSERT INTO chats " \
                  "(context, timestamp_start, timestamp_end," \
                  " receiver_id, sender_id, platform, is_alive) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (json.dumps(context), timestamp, timestamp,
                   receiver_id, sender_id, platform, '1')
            flag, error, result = execute_sql(sql, val, 3)
            if not flag:
                print("Error: {}".format(error))
            else:
                print("Insert successful")
        else:
            sql = "UPDATE chats SET context = %s, timestamp_end = %s " \
                  "WHERE chat_id = %s"
            val = (json.dumps(context), timestamp, chat_id)
            print("trying to  update")
            flag, error, result = execute_sql(sql, val, 3)
            if not flag:
                print("Error: {}".format(error))
            else:
                print("Update successful")

