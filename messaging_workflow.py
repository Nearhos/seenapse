import os
from datetime import datetime
from text_to_speech import speak_text
from twilio.rest import Client  # Now enabled for testing

def send_message_workflow(message_text=None):
    """Send a quick message to a specific contact"""
    
    print("💬 Starting message workflow...")
    
    # Default message if none provided
    if not message_text:
        message_text = "Hi! Just checking in. Hope you're doing well!"
    
    # Speak what we're doing
    speak_text(f"Sending message: {message_text}")
    
    # Set Twilio credentials directly for testing
    account_sid = "ACdc98fda075d039d46598b4c54462b5f3"
    auth_token = "ca0ab5df258db91e2ea2b1b8ab7ba6a5"
    
    if account_sid and auth_token:
        client = Client(account_sid, auth_token)
        from_number = "+14159807815"  # Your Twilio number
        target_contact = "+16478668110"  # Your frequent contact
        
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
    else:
        print("❌ Twilio credentials not configured")
    
    
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
