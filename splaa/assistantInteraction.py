# Author: Claude Petit-Frere
# Date: 11/14/24
# Desc: This is where the main logic for the ollama inference is stored

from ollama import chat
from .audioFunctions import generateAudio, recordAudio, whisperTranscription
from . import helperFunctions


async def generateResponse(model, assistant_name, user_name, speaker_file, system_prompt, command_permission):
    if command_permission:
        helperFunctions.tools.append({"type": "function", "function": {"name": "executeCommand", "description": "Executes a command in the powershell terminal. eg start firefox, systeminfo ...ect", "parameters": {"type": "object", "properties": {"command": {"type": "string", "description": "The command to execute"}},"required": ["command"]}}})
        helperFunctions.available_functions['executeCommand']= helperFunctions.executeCommand
    history = [
    {'role': 'system', 'content': f"Rule: all outputs should be concise, english and in paragraph form. Your Name:{assistant_name}. Prompt: {system_prompt}. User Name:{user_name}."}
    ]
    response = chat(model, messages=history, tools=helperFunctions.tools)
    while True:
        user_text = whisperTranscription(recordAudio())
        if assistant_name.lower() in user_text.lower():
            history.append({'role': 'user', 'content': user_text})
            response = chat(model, messages=history, tools=helperFunctions.tools)
            if response['message'].get('tool_calls'):
                for tool in response['message']['tool_calls']:
                    print(f"Using {tool['function']['name']} tool")
                    function_to_call = helperFunctions.available_functions[tool['function']['name']]
                    function_response = await function_to_call(**tool['function']['arguments'])
                    history.append({'role': 'tool','content': function_response,})
                response = chat(model, messages=history, tools=helperFunctions.tools)
            generateAudio(response['message']['content'], speaker_file)
            print(f"Response: {response['message']['content']}")
            print("------------------", end="\n")
            history.append(response['message'])