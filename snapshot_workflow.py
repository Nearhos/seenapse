import cv2
import numpy as np
from mss import mss
from datetime import datetime
import google.generativeai as genai
from PIL import Image
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Direct import from root level
from text_to_speech import speak_text

# Configuration constants (inline since no config file)
SCREEN_CAPTURE = {"top": 140, "left": 25, "width": 400, "height": 600}
GEMINI_MODEL = "gemini-1.5-flash"

# Configure Gemini API from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=GEMINI_API_KEY)

def capture_screenshot():
    """Capture a screenshot of the specific screen area and save it as an image file"""
    
    # Set up screen capture using config settings
    sct = mss()
    monitor = SCREEN_CAPTURE
    
    # Take screenshot
    screenshot = sct.grab(monitor)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.jpg"
    
    # Save the image
    cv2.imwrite(filename, frame)
    print(f"📸 Screenshot saved as: {filename}")
    
    return filename

def analyze_image_enhanced(image_path):
    """Enhanced image analysis using optimized prompt from partner's code"""
    
    # Initialize the model using config
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    # Open and prepare the image
    image = Image.open(image_path)
    
    # Enhanced prompt from partner's snapshot.py (more focused and effective)
    prompt = """
        You are a compact multimodal assistant used in a real-time Snapshot tool.

        Select ONE best task:

        1) Math: solve and return only the final answer. If there are multiple parts, list each on its own line as (a), (b), ...
        2) Translation: detect language and return the full English translation only. No extra commentary.
        3) Image understanding: explain what the image shows and clarify likely confusing elements. 
        If the image contains text or equations, transcribe the relevant parts and, if applicable, solve or translate them.

        Rules:
        - Be concise (ideally ≤ 3 sentences unless multiple sub-answers are required).
        - No preamble, no markdown, no apologies, no chain-of-thought.
        - Preserve technical symbols, numbers, and proper nouns.
        - For math: include units; avoid unnecessary rounding; if assumptions are required, state them in one short sentence at the end.
        - For translation: output the translated text only.
        - For image: prioritize what the user likely cares about (main subjects, relationships, actions, anomalies, UI labels). Include one brief clarification note only if ambiguity would mislead.

        Output format:
        - Math → just the final answer (and label parts if needed).
        - Translation → just the English translation.
        - Image → 1–3 concise sentences (add a single "Note: ..." line only if essential).
        """
    
    response = model.generate_content([prompt, image])
    return response.text.strip()

def snapshot_workflow():
    """Complete snapshot workflow: capture + analyze + speak"""
    
    print("🔍 Starting snapshot workflow...")
    
    # Step 1: Capture screenshot from your specific screen area
    image_path = capture_screenshot()
    
    # Step 2: Analyze with enhanced Gemini prompt
    print("🤖 Analyzing with enhanced Gemini...")
    
    try:
        analysis = analyze_image_enhanced(image_path)
        print(f"\n✅ Analysis:")
        print("-" * 50)
        print(analysis)
        print("-" * 50)
        
        # Step 3: Speak the results
        print("🔊 Converting to speech...")
        speak_text(analysis)
        
        print("✅ Snapshot workflow complete!")
        return analysis
        
    except Exception as e:
        error_msg = f"❌ Error in snapshot workflow: {e}"
        print(error_msg)
        speak_text("Error occurred during analysis")
        return None

if __name__ == "__main__":
    snapshot_workflow()
