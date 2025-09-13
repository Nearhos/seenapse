import os
import requests
from datetime import datetime
import cv2
import numpy as np
from mss import mss
from dotenv import load_dotenv
from text_to_speech import speak_text
from twilio.rest import Client

# Load environment variables
load_dotenv()

def capture_emergency_screenshot():
    """Capture screenshot at the moment of emergency for context"""
    try:
        print("📸 Capturing emergency screenshot...")
        
        # Use the same screen capture settings as your main system
        sct = mss()
        monitor = {"top": 140, "left": 25, "width": 400, "height": 600}
        
        # Take screenshot
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        
        # Create emergency screenshot filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"emergency_screenshot_{timestamp}.jpg"
        
        # Save the emergency screenshot
        cv2.imwrite(filename, frame)
        print(f"📸 Emergency screenshot saved: {filename}")
        
        return filename
        
    except Exception as e:
        print(f"❌ Error capturing emergency screenshot: {e}")
        return None

def get_location():
    """Get current location using IP-based geolocation"""
    try:
        # IP-based geolocation (city-level, approximate)
        token = os.getenv("IPINFO_TOKEN")  # Optional: set this for better rate limits
        url = "https://ipinfo.io/json" + (f"?token={token}" if token else "")
        response = requests.get(url, timeout=4)
        j = response.json()
        lat, lon = map(float, j.get("loc", "0,0").split(","))
        
        return {
            "lat": lat,
            "lon": lon,
            "ip": j.get("ip"),
            "city": j.get("city"),
            "region": j.get("region"),
            "country": j.get("country"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        print(f"❌ Error getting location: {e}")
        return {
            "lat": 0,
            "lon": 0,
            "ip": "unknown",
            "city": "unknown",
            "region": "unknown", 
            "country": "unknown",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def send_emergency_sms(location_info, screenshot_path=None):
    """Send SOS SMS with location and screenshot to emergency contact"""
    
    # Get credentials from environment variables
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")
    emergency_contact = os.getenv("EMERGENCY_CONTACT")
    
    if not all([account_sid, auth_token, from_number, emergency_contact]):
        print("❌ Twilio credentials not set in environment variables")
        return
    
    client = Client(account_sid, auth_token)
    
    message_body = f"🚨 SOS ALERT 🚨\\nLocation: {location_info['lat']:.5f},{location_info['lon']:.5f}\\nCity: {location_info['city']}, {location_info['region']}, {location_info['country']}\\nTime: {location_info['timestamp']}\\nIP: {location_info['ip']}"
    
    try:
        # Send message without screenshot attachment (file URLs don't work with Twilio)
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=emergency_contact
        )
        print(f"✅ SOS sent to {emergency_contact}")
        if screenshot_path and os.path.exists(screenshot_path):
            print(f"📷 Screenshot saved locally: {screenshot_path}")
            
    except Exception as e:
        print(f"❌ Failed to send SOS: {e}")

def emergency_workflow():
    """Complete emergency workflow: screenshot + location + alerts + logging"""
    
    print("🚨 EMERGENCY WORKFLOW ACTIVATED 🚨")
    
    # Step 1: Immediately capture screenshot for context
    screenshot_path = capture_emergency_screenshot()
    
    # Step 2: Get current location
    print("📍 Getting location...")
    location_info = get_location()
    
    # Step 3: Create emergency message
    location_message = (
        f"Emergency detected. "
        f"Location: {location_info['city']}, {location_info['region']}, {location_info['country']}. "
        f"Coordinates: {location_info['lat']:.5f}, {location_info['lon']:.5f}. "
        f"Time: {location_info['timestamp']}"
    )
    
    # Step 4: Speak emergency alert
    print("🔊 Speaking emergency alert...")
    speak_text("Emergency workflow activated. Capturing screenshot, getting your location and alerting emergency contact.")
    
    # Step 5: Send alerts with screenshot (currently just logging)
    send_emergency_sms(location_info, screenshot_path)
    
    # Step 6: Log everything to file for record keeping
    log_file = f"emergency_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_file, 'w') as f:
        f.write(f"EMERGENCY LOG\n")
        f.write(f"Timestamp: {location_info['timestamp']}\n")
        f.write(f"Location: {location_info['lat']:.5f},{location_info['lon']:.5f}\n")
        f.write(f"Address: {location_info['city']}, {location_info['region']}, {location_info['country']}\n")
        f.write(f"IP: {location_info['ip']}\n")
        f.write(f"Screenshot: {screenshot_path if screenshot_path else 'None captured'}\n")
        f.write(f"Emergency Contact: +16478668110\n")
    
    print(f"📝 Emergency logged to: {log_file}")
    print("✅ Emergency workflow complete!")
    
    return {
        "location": location_info,
        "screenshot": screenshot_path,
        "emergency_contact": "+16478668110",
        "log_file": log_file
    }

if __name__ == "__main__":
    emergency_workflow()
