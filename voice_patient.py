import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
#1
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

#To Record Audio from mic
def record_audio(file_path,timout=20,phrase_time_limit=None):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            
            logging.info("Recording Audio...")
            recognizer.adjust_for_ambient_noise(source,duration=1)#it is to remove background noise more than 1 second more accuracy
            logging.info("Please speak now...")

            #record audio start
            audio_data = recognizer.listen(source, timeout=timout, phrase_time_limit=phrase_time_limit)#if timeout time reaches 20 then timeout occur
            logging.info("Recording complete.")

            #save audio -->in file_path given in function
            wav_data=audio_data.get_wav_data()
            audio_segment=AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path,format="mp3",bitrate="128k")

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred while recording audio: {e}")

audio_filepath = "patient_voice.mp3"
#record_audio(file_path="patient_voice.mp3")


#2 -------Audio to text--------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


stt_model=  "whisper-large-v3"
def transcribe_audio(stt_model,audio_filepath,GROQ_API_KEY):
    client= Groq(api_key=GROQ_API_KEY)
    audio_file=open(audio_filepath, "rb")
    transcription = client.audio.transcriptions.create(
        model=stt_model,
        file=audio_file,
        language="en"
    )
    return transcription.text