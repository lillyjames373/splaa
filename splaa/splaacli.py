import argparse
import asyncio
from .assistantInteraction import generateResponse
import os

def main():
    parser = argparse.ArgumentParser(description='splaa CLI')
    parser.add_argument('--model', default="qwen2.5:3b", help='ollama model to use')
    parser.add_argument('--assistant_name', default="Athena", help='Name of the assistant')
    parser.add_argument('--user_name', default="Unknown", help='Name of the user')
    parser.add_argument('--speaker_file', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "speaker.wav"), help='Path to the speaker file for TTS')
    parser.add_argument('--system_prompt', default="You are a very concise and to the point AI assistant", help='System prompt for the assistant')
    parser.add_argument('--command_permission', default=False, help='Determines whether the model can execute commands on your system. WARNING: COULD LEAD TO UNEXPECTED CATASTROPHIC RESULTS')
    args = parser.parse_args()
    asyncio.run(generateResponse(
        model=args.model,
        assistant_name=args.assistant_name,
        user_name=args.user_name,
        speaker_file=args.speaker_file,
        system_prompt=args.system_prompt,
        command_permission=args.command_permission
    ))


if __name__ == '__main__':
    main()