import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import tempfile
import subprocess

# Load environment variables
load_dotenv()

# Initialize ElevenLabs client
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
    
    print(f"🔊 Speaking with ElevenLabs: {text[:50]}...")
    
    try:
        # Generate audio using ElevenLabs
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",  # High quality multilingual model
            output_format="mp3_44100_128",
        )
        
        # Convert generator to bytes
        audio_bytes = b"".join(audio_generator)
        
        # Save to temporary file and play
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        # Play using macOS afplay command
        subprocess.run(['afplay', tmp_file_path], check=True)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        print("✅ Speech completed successfully!")
        
    except Exception as e:
        print(f"❌ Error with ElevenLabs TTS: {e}")
        # Fallback to macOS built-in TTS if ElevenLabs fails
        print("🔄 Falling back to macOS built-in speech...")
        clean_text = text.replace('"', '\\"').replace('`', '').replace('$', '')
        os.system(f'say -v Alex "{clean_text}"')

def get_available_voices():
    """Get list of available voices from ElevenLabs"""
    try:
        response = client.voices.search()
        print("🎤 Available ElevenLabs voices:")
        for voice in response.voices:
            print(f"  - {voice.name} (ID: {voice.voice_id})")
        return response.voices
    except Exception as e:
        print(f"❌ Error fetching voices: {e}")
        return []

def speak_text_with_voice_name(text, voice_name="Rachel"):
    """
    Convert text to speech using voice name instead of ID
    
    Args:
        text (str): The text to convert to speech
        voice_name (str): Name of the voice (e.g., "Rachel", "Sarah", "Drew", "Dave")
    """
    
    try:
        # Get all voices and find the one with matching name
        response = client.voices.search()
        voice_id = None
        
        for voice in response.voices:
            if voice.name.lower() == voice_name.lower():
                voice_id = voice.voice_id
                break
        
        if voice_id:
            speak_text(text, voice_id)
        else:
            print(f"❌ Voice '{voice_name}' not found. Using default voice.")
            speak_text(text)
            
    except Exception as e:
        print(f"❌ Error finding voice by name: {e}")
        speak_text(text)  # Fallback to default

if __name__ == "__main__":
    # Test the ElevenLabs text-to-speech
    print("🧪 Testing ElevenLabs Text-to-Speech...")
    
    # Test basic functionality
    test_text = "Hello! This is a test of the ElevenLabs text to speech integration for your mental health AI assistant."
    
    print("Testing main speak_text function...")
    speak_text(test_text)
    
    # Show available voices
    print("\nFetching available voices...")
    get_available_voices()
    
    # Test with voice name
    print("\nTesting with voice name...")
    speak_text_with_voice_name("This is Sarah speaking!", "Sarah")
    
    print("✅ ElevenLabs TTS test completed!")
