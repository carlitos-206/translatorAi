from pydub import AudioSegment
import whisper 
import wave
import pyaudio
import speech_recognition as sr
from translate import Translator
from langdetect import detect
import pyttsx3
import asyncio
import threading
# from multiprocessing import Process
import multiprocessing
import time
import os
import concurrent.futures

def speak(data:str):
  return 

def transcribe():
  try:
    wav_file = 'output.wav'
    model = whisper.load_model("base")
    result = model.transcribe(wav_file, task='translate')
    print(f"\n{result['text']}")
    engine = pyttsx3.init()
    engine.say(result['text'])
    engine.runAndWait()
    os.remove(wav_file)
    record()
  except:
    print("here")


def record():
  current_time_ms = int(time.time() * 1000)
   # Setup PyAudio instance
  p = pyaudio.PyAudio()
  # Setup stream parameters
  CHUNK = 1024
  FORMAT = pyaudio.paInt16
  CHANNELS = 1
  RATE = 44100
  RECORD_SECONDS = 5
  WAVE_OUTPUT_FILENAME = "output.wav"
      # Saving the audio in .wav format
  print("\nSTART>>>\n")
  stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      input_device_index= 3,
                      frames_per_buffer=CHUNK)
  frames = []
  for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
      
  print("\n>>>END\n")  
  stream.stop_stream()
  stream.close()
  wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(p.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  wf.writeframes(b''.join(frames))
  wf.close()
  transcribe()
  # asyncio.run(asyncio.gather(transcribe(WAVE_OUTPUT_FILENAME), record()))

# with concurrent.futures.ThreadPoolExecutor() as executor:  
#   if __name__ == '__main__':
#       p1 = executor.submit(record)
#       p2 = executor.submit(transcribe)

  
record()


# def transcribe():
#     try:
#         while True:
#             wav_file = 'test.wav'
#             model = whisper.load_model("base")
#             result = model.transcribe(wav_file, task='translate')
#             print(f"\n{result['text']}")
#             engine = pyttsx3.init()
#             engine.say(result['text'])
#             engine.runAndWait()
#             os.remove(wav_file)
#     except:
#         time.sleep(2)
#         print("here")
#         transcribe()

# def record():
#     try:
#         while True:
#             current_time_ms = int(time.time() * 1000)
#             # Setup PyAudio instance
#             p = pyaudio.PyAudio()
#             # Setup stream parameters
#             CHUNK = 1024
#             FORMAT = pyaudio.paInt16
#             CHANNELS = 1
#             RATE = 44100
#             RECORD_SECONDS = 5
#             WAVE_OUTPUT_FILENAME = f"test.wav"
            
#             # Saving the audio in .wav format
#             print("\nSTART>>>\n")
#             stream = p.open(format=FORMAT,
#                             channels=CHANNELS,
#                             rate=RATE,
#                             input=True,
#                             input_device_index=3,
#                             frames_per_buffer=CHUNK)
#             frames = []
#             for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#                 data = stream.read(CHUNK)
#                 frames.append(data)
                
#             print("\n>>>END\n")  
#             stream.stop_stream()
#             stream.close()
#             wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#             wf.setnchannels(CHANNELS)
#             wf.setsampwidth(p.get_sample_size(FORMAT))
#             wf.setframerate(RATE)
#             wf.writeframes(b''.join(frames))
#             wf.close()
#     except:
#         time.sleep(2)
#         print("here")
#         record()

# # Create threads for both functions
# transcribe_thread = threading.Thread(target=transcribe)
# record_thread = threading.Thread(target=record)

# # Start the threads
# transcribe_thread.start()
# record_thread.start()

# # Keep the main thread alive
# while True:
#     pass