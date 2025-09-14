import streamlit as st
from api.snapshot.snapshot_workflow import capture_screenshot, analyze_image_enhanced, snapshot_workflow
from api.text_to_speech import speak_text
st.title("Snapshort Workflow")

st.divider()

image_path = capture_screenshot()

analysis = analyze_image_enhanced(image_path)
speak_text(analysis)
