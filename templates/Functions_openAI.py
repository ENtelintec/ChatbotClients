# -*- coding: utf-8 -*-
__author__ = 'Edisson Naula'
__date__ = '$ 26/dic./2023  at 14:35 $'

import json
import time
from typing import Any, Tuple

import openai
from openai import OpenAI

from static.extensions import secrets, AV_avaliable_tools_files
from templates.Function_tools_openAI import getInfoForSalesContact

client = OpenAI(api_key=secrets.get("OPENAI_API_KEY_DEMOS"))
openai.api_key = secrets["OPENAI_API_KEY_DEMOS"]

available_functions = {
    "getInfoForSalesContact": getInfoForSalesContact
}


def create_assistant_openai(model="gpt-4-1106-preview", files=None, instructions=None, tools=None):
    if tools is None:
        tools = [{"type": "code_interpreter"}, {"type": "retrieval"}]
    e = None
    file_ids = files if files is not None else []
    try:
        assistant = client.beta.assistants.create(
            name="Assistant",
            instructions=instructions,
            model=model,
            tools=tools,
            tool_resources={
                "code_interpreter": {
                    "file_ids": file_ids
                }
            }
        )
    except Exception as e:
        print(e)
        assistant = None
    return assistant, e


def create_thread_openai():
    e = None
    try:
        thread = client.beta.threads.create()
    except Exception as e:
        print(e)
        thread = None
    return thread, e


def create_message_openai(thread_id, msg, role):
    e = None
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=msg
        )
    except Exception as e:
        print(e)
        message = None
    return message, e


def run_thread_openai(thread_id, assistant_id):
    e = None
    try:
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id)
    except Exception as e:
        print(e)
        run = None
    return run, e


def get_tool_outputs(required_actions):
    outputs = []

    for tool in required_actions:
        print(tool)
        arguments = json.loads(tool.function.arguments)
        function_to_call = available_functions[tool.function.name]
        output = function_to_call(**arguments)
        outputs.append(
            {
                "tool_call_id": tool.id,
                "output": str(output),
            }
        )
    return outputs


def complete_required_actions(required_actions, thread_id, run_id):
    e = None
    try:
        complete_actions = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=get_tool_outputs(required_actions)
        )
    except Exception as e:
        print("catch error complete required tool: ", e)
        complete_actions = None
    return complete_actions, e


def retrieve_runs_openai(thread_id, run_id):
    e = None
    try:
        while True:
            runs = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            if runs.status == "requires_action":
                completed_actions, error = complete_required_actions(
                    runs.required_action.submit_tool_outputs.tool_calls, thread_id, run_id)
                if error is not None:
                    print("Error at completing required tool: ", error)
                    runs = None
                    e = error
                    break
            if runs.status == "completed":
                break
            time.sleep(0.5)
    except Exception as e:
        print("Error at retrieving runs ", e)
        runs = None
    return runs, e


def retrieve_messages_openai(thread_id):
    e = None
    try:
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
    except Exception as e:
        print(e)
        messages = None
    return messages, e


def get_response_chat_completion(messages: list) -> str:
    """
    Receives context and conversation with the bot and return a
    message from the bot.

    :param messages: chain of messages or context as a List[json].
    :return: answer (string)
    """
    # while 1:
    client_1 = OpenAI(api_key=secrets.get("OPENAI_API_KEY_1"))
    try:
        print(messages)
        out = client_1.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4-0613",
            messages=messages,
        )
        # break
    except Exception as e:
        print("Error at openAI: ", e)
        return "Error at openAI"
    return out.choices[0].message.content


def get_response_assistant(message: str, filename: str = None, files: list = None, instructions: str = None,
                           client_tag=None, thread_id=None, assistant_id=None) -> \
        tuple[list | Any, str, str | None | Any, str | Any]:
    """
    Receives context and conversation with the bot and return a
    message from the bot.

    :param assistant_id:
    :param thread_id:
    :param filename: file to use
    :param client_tag:
    :param instructions:
    :param files: list of files to upload
    :param message:message
    :return: answer (string)
    """
    # json.loads(open('context.json', encoding='utf-8').read())["context"]]
    data_av_tools_files = json.loads(open(AV_avaliable_tools_files[client_tag.lower()], encoding='utf-8').read())
    tools = data_av_tools_files["tools"]
    e = None
    answer = ""
    files_assistat_ids = []
    if files is None:
        files = data_av_tools_files["files"]
        for i, item in enumerate(files):
            files_assistat_ids.append(item["id"])
    else:
        if len(files) > 0:
            for i, item in enumerate(files):
                if item["name"] == filename:
                    files_assistat_ids.append(item["id"])
                    break
    first_flag = False
    if thread_id is None:
        first_flag = True
        try:
            assistant, error = create_assistant_openai(files=files_assistat_ids, instructions=instructions, tools=tools)
            assistant_id = assistant.id
            print("first time creation")
        except Exception as e:
            print("Error at creating assistant on openAI: ", e)
            return files, "Error at creating assistant on openAI", "None", "None"
    try:
        if first_flag:
            thread, error = create_thread_openai()
            thread_id = thread.id
            print("first time")
        message_obj, error = create_message_openai(thread_id, message, "user")
        run, error = run_thread_openai(thread_id, assistant_id)
        run, error = retrieve_runs_openai(thread_id, run.id)
        msgs, error = retrieve_messages_openai(thread_id)
        for msg in msgs.data:
            if msg.role == "user":
                continue
            answer = msg.content[0].text.value + "\n" if msg.role == "assistant" else ""
            break
        # answer = msgs
    except Exception as e:
        print("Catching Error at getting response on openAI: ", e)
        return files, f"Catching Error at getting response on openAI: {e}", "None", "None"
    return files, answer, thread_id, assistant_id


def get_files_list_openai():
    files = []
    e = None
    try:
        files_openai = client.files.list(purpose="assistants")
        files = files_openai.data
        if len(files) == 0:
            files = []
    except Exception as e:
        print("Error at getting files list on openAI: ", e)
    return files, e


def delete_file_openai(file_id):
    e = None
    try:
        res = client.files.delete(file_id=file_id)
        flag = res.deleted
    except Exception as e:
        flag = False
        print("Error at deleting file on openAI: ", e)
    return flag, e


def upload_file_openai(file_path: str):
    e = None
    try:
        file = client.files.create(
            file=open(file_path, "rb"),
            purpose="assistants"
        )
        while True:
            files, error = get_files_list_openai()
            if len(files) > 0:
                process = False
                for item in files:
                    if item.id == file.id:
                        if item.status == "processed":
                            print("File processed")
                            process = True
                            break
                        else:
                            print("File not processed yet")
                if process:
                    break
            time.sleep(2)
    except Exception as e:
        print(e)
        file = None
    return file, e
