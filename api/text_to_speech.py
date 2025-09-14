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

def speak_text(text, voice_id="21m00Tcm4TlvDq8ikWAM"):
    """
    Convert text to speech using ElevenLabs API and play it immediately
    
    Args:
        text (str): The text to convert to speech
        voice_id (str): ElevenLabs voice ID (default: Rachel - clear female voice)
                       Popular voices from your account:
                       - "21m00Tcm4TlvDq8ikWAM": Rachel (clear female voice)
                       - "EXAVITQu4vr4xnSDxMaL": Sarah (young female voice)
                       - "29vD33N1CtxCmqQRPOHJ": Drew (male voice)
                       - "CYw3kZ02Hs0563khs1Fj": Dave (male voice)
    """
    
    print(f"Speaking with ElevenLabs: {text[:50]}...")
    
    try:
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        
        audio_bytes = b"".join(audio_generator)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        subprocess.run(['afplay', tmp_file_path], check=True)
        os.unlink(tmp_file_path)
        
        print("Speech completed successfully!")
        
    except Exception as e:
        print(f"Error with ElevenLabs TTS: {e}")
        print("Falling back to macOS built-in speech...")
        clean_text = text.replace('"', '\\"').replace('`', '').replace('$', '')
        os.system(f'say -v Alex "{clean_text}"')

