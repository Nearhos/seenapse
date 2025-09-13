import cv2
import numpy as np
from mss import mss
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
from text_to_speech import speak_text

# Load environment variables
load_dotenv()

# Configure Gemini API from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=GEMINI_API_KEY)

def capture_screenshot():
    """Capture a screenshot of the test capture space and save it as an image file"""
    
    # Set up screen capture (same coordinates as your test_capture.py)
    sct = mss()
    monitor = {"top": 140, "left": 25, "width": 400, "height": 600}
    
    # Take screenshot
    screenshot = sct.grab(monitor)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.jpg"
    
    # Save the image
    cv2.imwrite(filename, frame)
    print(f"Screenshot saved as: {filename}")
    
    return filename

def analyze_image(image_path):
    """Send an image to Gemini API and get description"""
    
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Open and prepare the image
    image = Image.open(image_path)
    
    # Send to Gemini with the custom prompt
    prompt = (
        "You are an assistant.\n"
        "If a math problem is given, solve it and return the answer.\n"
        "If a non-English text is given, translate it to English and return the entire translation.\n"
        "If an image is given, explain what is in the image, what is going on, or anything that may be confusing to the user.\n"
        "Try to be as concise as possible while maintaining all the answers and accuracy.\n"
    )
    
    response = model.generate_content([prompt, image])
    
    return response.text

def capture_analyze_and_speak():
    """Complete workflow: Capture screenshot, analyze with Gemini, and speak the result"""
    
    print("Starting capture, analysis, and speech workflow...")
    
    # Step 1: Capture screenshot
    print("📸 Taking screenshot...")
    image_path = capture_screenshot()
    
    # Step 2: Analyze with Gemini
    print("🤖 Analyzing with Gemini...")
    
    try:
        description = analyze_image(image_path)
        print(f"\n✅ Gemini's analysis:")
        print("-" * 50)
        print(description)
        print("-" * 50)
        
        # Step 3: Convert to speech
        print("🔊 Converting to speech...")
        speak_text(description)
        
        print("✅ Workflow complete!")
        
    except Exception as e:
        print(f"❌ Error in workflow: {e}")

if __name__ == "__main__":
    capture_analyze_and_speak()
