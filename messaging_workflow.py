import os
from datetime import datetime
from dotenv import load_dotenv
from text_to_speech import speak_text
from twilio.rest import Client

# Load environment variables
load_dotenv()

def send_message_workflow(message_text=None):
    """Send a quick message to a specific contact"""
    
    print("💬 Starting message workflow...")
    
    # Default message if none provided
    if not message_text:
        message_text = "Hi! Just checking in. Hope you're doing well!"
    
    # Speak what we're doing
    speak_text(f"Sending message: {message_text}")
    
    # Get credentials from environment variables
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")
    target_contact = os.getenv("EMERGENCY_CONTACT")
    
    if not all([account_sid, auth_token, from_number, target_contact]):
        print("❌ Twilio credentials not configured in environment variables")
        speak_text("Message sending failed - credentials not configured")
        return None
    
    client = Client(account_sid, auth_token)
    
    try:
        message = client.messages.create(
            body=message_text,
            from_=from_number,
            to=target_contact
        )
        print(f"✅ Message sent to {target_contact}")
        speak_text("Message sent successfully")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")
        speak_text("Message sending failed")
    
    
    # Log message for now
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = "message_log.txt"
    
    with open(log_file, 'a') as f:
        f.write(f"{timestamp}: {message_text}\n")
    
    print(f"📱 Message logged: {message_text}")
    print("✅ Message workflow complete!")
    
    return message_text

if __name__ == "__main__":
    send_message_workflow()
