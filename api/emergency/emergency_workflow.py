import os
import requests
from datetime import datetime
import cv2
import numpy as np
from mss import mss
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def capture_emergency_screenshot():
    """Capture screenshot at the moment of emergency for context"""
    try:
        print("Capturing emergency screenshot...")
        
        sct = mss()
        monitor = {"top": 140, "left": 25, "width": 400, "height": 600}
        
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"emergency_screenshot_{timestamp}.jpg"
        
        cv2.imwrite(filename, frame)
        print(f"Emergency screenshot saved: {filename}")
        
        return filename
    
    except Exception as e:
        print(f"Error capturing emergency screenshot: {e}")
        return None

def get_location():
    """Get current location using IP-based geolocation"""
    try:
        token = os.getenv("IPINFO_TOKEN")
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
        print(f"Error getting location: {e}")

def send_emergency_sms(location_info, screenshot_path=None):
    """Send SOS SMS with location and screenshot to emergency contact"""
    
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")
    emergency_contact = os.getenv("EMERGENCY_CONTACT")
    
    if not all([account_sid, auth_token, from_number, emergency_contact]):
        print("Twilio credentials not set in environment variables")
        return
    
    client = Client(account_sid, auth_token)
    
    message_body = f"🚨 SOS ALERT 🚨\\nLocation: {location_info['lat']:.5f},{location_info['lon']:.5f}\\nCity: {location_info['city']}, {location_info['region']}, {location_info['country']}\\nTime: {location_info['timestamp']}\\nIP: {location_info['ip']}"
    
    try:
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=emergency_contact
        )
        print(f"SOS sent to {emergency_contact}")
        if screenshot_path and os.path.exists(screenshot_path):
            print(f"Screenshot saved locally: {screenshot_path}")
            
    except Exception as e:
        print(f"Failed to send SOS: {e}")

def trigger_vapi_call(phone_number, message="Emergency detected! Please respond."):
    """Trigger an outbound call via Vapi API"""
    vapi_api_key = os.getenv("VAPI_API_KEY")
    vapi_agent_id = os.getenv("VAPI_AGENT_ID")
    if not vapi_api_key or not vapi_agent_id:
        print("Vapi credentials not set in environment variables")
        return

    url = "https://api.vapi.dev/calls"
    headers = {
        "Authorization": f"Bearer {vapi_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "agent": vapi_agent_id,
        "phone": phone_number,
        "payload": {
            "type": "text",
            "text": message
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"Vapi call triggered to {phone_number}")
        else:
            print(f"Vapi call failed: {response.text}")
    except Exception as e:
        print(f"Error triggering Vapi call: {e}")


    '''
    log_file = f"emergency_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(log_file, 'w') as f:
        f.write(f"EMERGENCY LOG\n")
        f.write(f"Timestamp: {location_info['timestamp']}\n")
        f.write(f"Location: {location_info['lat']:.5f},{location_info['lon']:.5f}\n")
        f.write(f"Address: {location_info['city']}, {location_info['region']}, {location_info['country']}\n")
        f.write(f"IP: {location_info['ip']}\n")
        f.write(f"Screenshot: {screenshot_path if screenshot_path else 'None captured'}\n")
        f.write(f"Emergency Contact: +16478668110\n")
    '''

