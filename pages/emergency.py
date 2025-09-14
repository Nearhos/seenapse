import streamlit as st
from api.text_to_speech import speak_text

st.title("Emergency Workflow")

from emergency.emergency_workflow import capture_emergency_screenshot, get_location, send_emergency_sms, trigger_vapi_call

vapi_phone_number = "+528110518779"

screenshot_path = capture_emergency_screenshot()
location_info = get_location()

location_message = (
        f"Emergency detected. "
        f"Location: {location_info['city']}, {location_info['region']}, {location_info['country']}. "
        f"Coordinates: {location_info['lat']:.5f}, {location_info['lon']:.5f}. "
        f"Time: {location_info['timestamp']}"
    )

speak_text("Emergency workflow activated. Capturing screenshot, getting your location and alerting emergency contact.")

send_emergency_sms(location_info, screenshot_path)
trigger_vapi_call(vapi_phone_number, message=location_message)
