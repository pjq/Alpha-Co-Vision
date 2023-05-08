import os
import sys
import subprocess
import threading

import whispercpp
from whispercpp import Whisper

import config

def process_input_stream(callback):
    if not config.settings:
        whisper_cpp_path = "/Users/i329817/SAPDevelop/pythonProject/whisper.cpp"
    else:
        whisper_cpp_path = config.settings.whisper_cpp_path
    stream_command = f"{whisper_cpp_path}/stream -l auto -m ./models/ggml-base.en.bin -t 8 --step 500 --length 5000"
    print(f"{stream_command}")

    def capture_text(p):
        for line in iter(p.stdout.readline, b''):
            decoded_line = line.decode('utf-8').strip()
            if decoded_line:
                callback.notify(decoded_line)

    try:
        p = subprocess.Popen(
            stream_command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        capture_text(p)
    except Exception as e:
        print("Error capturing text: ", e)

class Callback:
    def notify(self, new_message):
        print(new_message)

def run_whispercpppythonbinding(callback):
    devices = whispercpp.utils.available_audio_devices()
    print(devices)
    # Found 2 audio capture devices:
    # - Device id 0: 'MacBook Pro Microphone'
    # - Device id 1: 'Microsoft Teams Audio'
    # w = Whisper.from_pretrained("tiny.en")
    w = Whisper.from_pretrained("base.en")
    # iterator = w.stream_transcribe(device_id=0, length_ms=5000, n_threads=8, step_ms=500, keep_ms=200)
    iterator = w.stream_transcribe(device_id=0)
    try:
        for it in iterator:
            print(it)
    except KeyboardInterrupt:
        print("Transcription")

    # print(["\nTranscription (line by line):\n"] + [f"{it}\n" for it in iterator])

def start_whispercpp():
    callback = Callback()

    # Start process_input_stream in a separate thread
    # t = threading.Thread(target=process_input_stream, args=(callback,))
    t = threading.Thread(target=run_whispercpppythonbinding, args=(callback,))
    t.start()
    return t

if __name__ == "__main__":
    t = start_whispercpp()

    # Main thread continues
    while True:
        if not t.is_alive():
            break
        # Main thread can perform other tasks here
