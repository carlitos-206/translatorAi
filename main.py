from pydub import AudioSegment
import whisper 
import wave
import pyaudio
import speech_recognition as sr
from translate import Translator
from langdetect import detect
import pyttsx3

# # Loadind the MP3 File
# audio = AudioSegment.from_file("oracionSalvadorena.mp3", format="mp3")

# # Export the audio to a temporary WAV file
# tmp_wav_file = "temp.wav"
# audio.export(tmp_wav_file, format="wav")

# # Load the WAV file with whisper
# model = whisper.load_model("base")
# result = model.transcribe(tmp_wav_file, task= 'translate')


# This function parses the result -- unique function does not apply outside this script
def parseResult(data):
  for i in data:
    if data[i] == data['segments']:
      for j in data['segments']:
        if isinstance(j, dict):
          print("---------")
          for k in j:
            print(f"{k}: {j[k]}")
          print("---------")
    else:
      print(f"\n {i}: {data[i]} \n")

# parseResult(result)

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))


def audio_translator():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    
    # Setup PyAudio instance
    p = pyaudio.PyAudio()

    # Setup stream parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "outputt.wav"
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
        
    
    # Transcribe audio
    try:
        transcribed_audio = recognizer.recognize_google(audio)
        print("\nTranscribed Audio: ", transcribed_audio)
        
        if transcribed_audio == 'stop':
          print('Exiting Translator')
          return
        # Detect language
        detected_lang = detect(transcribed_audio)
        print("Detected language: ", detected_lang)

        # Translate the transcribed audio
        translator = Translator(from_lang=detected_lang, to_lang="en")
        translation = translator.translate(transcribed_audio)
        print("Translated Text: ", translation)

        # Convert translated text to speech
        engine = pyttsx3.init()
        engine.say(translation)
        engine.runAndWait()

    except Exception as e:
        print("\nSomething went wrong: ", str(e))

audio_translator()