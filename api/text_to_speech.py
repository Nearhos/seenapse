import os
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
import tempfile
import subprocess

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY not found in environment variables")

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def speak_text(text):
    try:
        # Try ElevenLabs first
        from elevenlabs import generate, play, set_api_key
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise Exception("No ElevenLabs API key found")
        set_api_key(api_key)
        audio = generate(text=text, voice="Rachel", model="eleven_multilingual_v2")
        play(audio)
    except Exception as e:
        print(f"ElevenLabs failed: {e}. Falling back to Windows TTS.")
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e2:
            print(f"Windows TTS also failed: {e2}")

