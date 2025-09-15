import streamlit as st
from api.text_to_speech import speak_text
from api.emergency.emergency_workflow import (
    capture_emergency_screenshot,
    get_location,
    send_emergency_sms,
    trigger_vapi_call,
)
import time
import requests




st.set_page_config(page_title="SOS Workflow", page_icon="🚨", layout="centered")
st.title("🚨 SOS Workflow")


# Fetch data from endpoint every refresh
response = requests.get("https://bfe9d3f0313a.ngrok-free.app/latest/emergency")
if response.ok:
    data = response.json()
    st.write("Latest post:", data)
    if data and len(data) > 0:
        st.success("Executing main script logic!")
        # Place your main logic here
        # ...
else:
    st.error("Fetch error")

if (data and len(data) > 0):
    # Step 1: Capture Screenshot
    with st.spinner("Capturing emergency screenshot..."):
        screenshot_path = capture_emergency_screenshot()
        time.sleep(1)
    st.success("Image captured")
    st.image(screenshot_path, caption="Emergency Screenshot", width=300)

    st.divider()

    # Step 2: Get Location
    with st.spinner("Obtaining location..."):
        location_info = get_location()
        time.sleep(1)
    st.success(f"Location obtained: {location_info['city']}, {location_info['region']}, {location_info['country']}")

    # Show map with pinpoint
    if "lat" in location_info and "lon" in location_info:
        st.map(
            data=[{"lat": location_info["lat"], "lon": location_info["lon"]}],
            zoom=12
        )

    st.divider()

    # Step 3: Prepare Message
    location_message = (
        f"Emergency detected.\n"
        f"Location: {location_info['city']}, {location_info['region']}, {location_info['country']}.\n"
        f"Coordinates: {location_info['lat']:.5f}, {location_info['lon']:.5f}.\n"
        f"Time: {location_info['timestamp']}"
    )

    # Step 4: Send SMS & Trigger Call
    with st.spinner("Sending emergency SMS and triggering call..."):
        speak_text(
            "Emergency workflow activated. Capturing screenshot, getting your location and alerting emergency contact."
        )
        send_emergency_sms(location_info, screenshot_path)
        vapi_phone_number = "+16478668110"
        trigger_vapi_call(vapi_phone_number, message=location_message)
        time.sleep(1)
    st.success("Emergency SMS sent to your most used contacts")

    st.divider()

    st.info("Your emergency contacts have been called 🚑")
    with st.expander("Emergency Details", expanded=True):
        st.markdown("### Emergency Summary")
        st.markdown(f"**Location:** {location_info['city']}, {location_info['region']}, {location_info['country']}")
        st.markdown(f"**Coordinates:** {location_info['lat']:.5f}, {location_info['lon']:.5f}")
        st.markdown(f"**Timestamp:** {location_info['timestamp']}")
        st.markdown(f"**Contacted Phone:** {vapi_phone_number}")
        st.markdown("**Message Sent:**")
        st.code(location_message, language="text")
