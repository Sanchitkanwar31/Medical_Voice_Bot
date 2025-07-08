import os
import elevenlabs
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
from dotenv import load_dotenv
load_dotenv()

import subprocess
import platform
import tempfile

ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
def convert_mp3_to_wav(mp3_path, wav_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

def text_to_speech(in_text, file_path):
    client = ElevenLabs(api_key=ELEVEN_LABS_API_KEY)
    audio = client.generate(
        text=in_text,
        voice="Aria",
        model="eleven_turbo_v2",
        output_format="mp3_22050_32"
    )
    elevenlabs.save(audio,file_path)

    #2 to setup a system that will make doctor speak as it get save/automatic
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', file_path])
            
        elif os_name == "Windows":  # Windows

           # Convert MP3 to temporary WAV file wothout saving
            sound = AudioSegment.from_mp3(file_path)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                wav_path = tmp_wav.name
                sound.export(wav_path, format="wav")
            
            subprocess.run(['powershell', '-c',f'(New-Object Media.SoundPlayer "{wav_path.replace("/", "\\\\")}").PlaySync();'], check=True)
        
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', file_path])  # Alternative: use 'mpg123' or 'ffplay'
        
        else:
            raise OSError("Unsupported operating system")
        
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

#text_to_speech("Hello, this is a test of the Doctor new version voicetext-to-speech system.", "output_voice.mp3")


'''import subprocess
import platform
#==FOR GTTS SYSYTEM==
def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


input_text="Hi this is Ai with Hassan, autoplay testing!"
# #text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")'''
