# Author: Claude Petit-Frere
# Date: 11/14/24
# Desc: All the audio logic is stored here from playback, recording, transcription and generation.

import librosa
import torch
import warnings
import whisper
import numpy as np
from TTS.api import TTS
import time
import sounddevice as sd
import sys

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")

if device == "cpu":
    print("This project is currently using cpu to run it's models. \nWhile this is possible, it is slower than using NVIDIA's cuda toolkit(by a noticeable amount). \nIf you have a cuda capable NVIDIA graphics card, please consider installing a 12.+ cuda toolkit driver and the corresponding torch version for faster speeds.\n")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning, module="whisper") # Filter by module
    model = whisper.load_model("small").to(device)

def whisperTranscription(audio_data):
    """simple whisper transcription
    """
    audio_data = audio_data.astype(np.float32) / 32768.0
    resampled_audio = librosa.resample(audio_data.astype(np.float32), orig_sr=44100, target_sr=16000)
    if len(resampled_audio.shape) > 1:
        resampled_audio = resampled_audio.mean(axis=1)
    result = model.transcribe(resampled_audio, language='en', fp16=torch.cuda.is_available())
    print(f"User: {result["text"]}")
    return result["text"]


def generateAudio(textinput, speaker_file):
    """This is the function use to generate the TTS model audio using xtts_v2 wave and sounddevice
    """

    try:
        wav = tts.tts(text=textinput,
                    speaker_wav=speaker_file,
                    language="en")
        sd.play(wav, 26460)
    except Exception:
        print("Error generating assistant voice. \nIs your speaker_file path correct?")
        sys.exit(1)

        
def recordAudio():
    """Records audio with sounddevice after a volume threshold is passed and stops recording after a silence duration is exceeded
       Saves the file as whisper.wav
    """
    fs = 44100  
    silence_duration = 2.25
    chunk_size = 1024  
    started_recording = False
    silence_start = None
    volume_threshold = 10
    buffer = np.array([], dtype=np.float32)
    buffer_length = 1
    full_recording = np.array([], dtype=np.float32)
    
    with sd.InputStream(samplerate=fs, channels=1, dtype=np.float32, blocksize=chunk_size) as stream:
        while True:
            audio_data, _ = stream.read(chunk_size)
            volume = np.sqrt(np.mean(np.square(audio_data))) * 1000
            buffer = np.append(buffer, audio_data)

            if len(buffer) > int(buffer_length * fs):
                buffer = buffer[-int(buffer_length * fs):]

            if not started_recording:
                print("*Listening...*", end='\r')
                if volume > volume_threshold:
                    print("*Recording...*", end='\r')
                    sd.stop()
                    full_recording = np.append(full_recording, buffer)
                    started_recording = True
            elif started_recording:
                full_recording = np.append(full_recording, audio_data)
                if volume < volume_threshold:
                    if silence_start is None:
                        silence_start = time.time()
                    if (time.time() - silence_start) > silence_duration:
                        print("*Generating...*")
                        break
                else:
                    silence_start = None


    full_recording = np.int16(full_recording / np.max(np.abs(full_recording)) * 32767)
    return full_recording