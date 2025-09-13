import cv2
import numpy as np
from mss import mss
from datetime import datetime
from PIL import Image
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

import cohere

# Load environment variables
load_dotenv()

# Direct import from root level
from text_to_speech import speak_text

# Configuration constants (inline since no config file)
SCREEN_CAPTURE = {"top": 140, "left": 25, "width": 400, "height": 600}

# Configure Cohere API from environment variable
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY not found in environment variables")
co = cohere.ClientV2(api_key=COHERE_API_KEY)

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
    """Enhanced image analysis using Cohere's vision model and optimized prompt."""
    import base64
    # Open and encode the image as base64 data URI
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        data_uri = f"data:image/jpeg;base64,{image_base64}"

    prompt = (
        "You are a compact multimodal assistant used in a real-time Snapshot tool.\n\n"
        "Select ONE best task:\n\n"
        "1) Math: solve and return only the final answer. If there are multiple parts, list each on its own line as (a), (b), ...\n"
        "2) Translation: detect language and return the full English translation only. No extra commentary.\n"
        "3) Image understanding: explain what the image shows and clarify likely confusing elements. "
        "If the image contains text or equations, transcribe the relevant parts and, if applicable, solve or translate them.\n\n"
        "Rules:\n"
        "- Be concise (ideally ≤ 3 sentences unless multiple sub-answers are required).\n"
        "- No preamble, no markdown, no apologies, no chain-of-thought.\n"
        "- Preserve technical symbols, numbers, and proper nouns.\n"
        "- For math: include units; avoid unnecessary rounding; if assumptions are required, state them in one short sentence at the end.\n"
        "- For translation: output the translated text only.\n"
        "- For image: prioritize what the user likely cares about (main subjects, relationships, actions, anomalies, UI labels). Include one brief clarification note only if ambiguity would mislead.\n\n"
        "Output format:\n"
        "- Math → just the final answer (and label parts if needed).\n"
        "- Translation → just the English translation.\n"
        "- Image → 1–3 concise sentences (add a single 'Note: ...' line only if essential)."
    )

    resp = co.chat(
        model="command-a-vision-07-2025",
        temperature=0.3,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": data_uri}},
            ],
        }],
    )
    return resp.message.content[0].text.strip()

def snapshot_workflow():
    """Complete snapshot workflow: capture + analyze + speak"""
    print("🔍 Starting snapshot workflow...")

    # Step 1: Capture screenshot from your specific screen area
    image_path = capture_screenshot()

    # Step 2: Analyze with enhanced Cohere vision prompt
    print("🤖 Analyzing with Cohere vision model...")

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
