import os

def speak_text(text):
    """Convert text to speech using macOS built-in TTS with Alex voice"""
    
    print(f"🔊 Speaking: {text[:50]}...")
    
    # Clean the text and escape quotes for command line safety
    clean_text = text.replace('"', '\\"').replace('`', '').replace('$', '')
    
    # Use macOS built-in text-to-speech with Alex voice
    os.system(f'say -v Alex "{clean_text}"')

if __name__ == "__main__":
    # Test the text-to-speech
    test_text = "Hello! This is a test of the text to speech system."
    speak_text(test_text)

if __name__ == "__main__":
    # Test the text-to-speech
    test_text = "Hello! This is a test of the text to speech system."
    speak_text(test_text)
