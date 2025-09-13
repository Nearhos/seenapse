# Real-Time AI Assistant with Meta Ray-Ban Glasses and YOLOv8 Nano

This project enables real-time object detection on a livestream from Meta Ray-Ban AI Glasses using YOLOv8 Nano on a Mac M1. The glasses stream video to Instagram, which is then captured and processed on the Mac to identify objects in the user's field of view. Originally intended to assist with Arduino projects by identifying components, the current focus is on the vision system, with potential for future expansion.

## Clone the Repository

```bash
# Clone with HTTPS
git clone https://github.com/ghsaboias/glasses-ai.git

# Or clone with SSH
git clone git@github.com:ghsaboias/glasses-ai.git

cd glasses-ai
```

## Table of Contents

- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

## Project Overview

The goal of this project is to create a real-time AI assistant that processes the livestream from Meta Ray-Ban AI Glasses to help identify objects or components (e.g., Arduino parts) in the user's environment. The glasses livestream to Instagram, and the video feed is captured and analyzed on a Mac M1 using YOLOv8 Nano for object detection. This setup leverages the glasses' camera and the Mac's processing power to provide real-time visual feedback.

## Requirements

### Hardware

- Meta Ray-Ban AI Glasses
- Mac M1 with 8GB RAM (or similar)
- Dual monitors (optional, but instructions include dual-monitor configuration)

### Software

- Python 3.8+
- uv (Python package manager)
dependencies = [
    "mss>=10.0.0",
    "numpy>=2.1.1",
    "opencv-python>=4.11.0.86",
    "ultralytics>=8.3.78",
    "google-generativeai>=0.8.5",
    "pillow>=11.1.0",
]

## Setup Instructions

### 1. Set Up the Environment

Make sure you have Python 3.8+ and uv installed, then:

```bash
# Clone and enter the repository
git clone https://github.com/ghsaboias/glasses-ai.git
cd glasses-ai

# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### 2. Configure the Livestream

1. Pair your Meta Ray-Ban AI Glasses with the Meta View app on your phone
2. Set up a private Instagram account for streaming
3. Start the livestream from the glasses using the voice command: "Hey Meta, start livestream"

### 3. Access the Livestream on Your Mac

1. Open a browser (e.g., Chrome, Safari) and log into the private Instagram account
2. Ensure the livestream video is visible. If using Brave, you may need to disable Shields or switch browsers if video fails to display

### 4. Configure Screen Capture

Use mss to capture the livestream window on your screen.

For dual-monitor setups, identify the correct monitor and coordinates:

- Primary monitor: 1440x900 (left)
- Extended monitor: 2560x1080 (right)
- Livestream was on the right half of the extended monitor

Use a test script to verify the capture area:

```python
import cv2
from mss import mss
import numpy as np

sct = mss()
monitor = {"top": 0, "left": 2780, "width": 320, "height": 320} # Adjust based on your setup
while True:
    screenshot = sct.grab(monitor)
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
    cv2.imshow("Test Capture", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()
```

Adjust the monitor coordinates until the livestream is fully captured in the test window.

### 5. Run Object Detection

You now have multiple options:

**Option 1: Real-time YOLO Detection (Original)**
```bash
uv run python detect_live.py
```

**Option 2: Screenshot + Gemini Analysis + Text-to-Speech (New)**
```bash
uv run python workflow_with_speech.py
```

**Option 3: Test Screen Capture Area**
```bash
uv run python test_capture.py
```

### 6. Optimize Performance

- Enable MPS (Metal Performance Shaders) for faster inference on the M1 GPU by adding `device='mps'` to the model inference
- Implement frame skipping to process detection only every nth frame, improving FPS
- Persist the last annotated frame to avoid visual glitching during skipped frames

## Usage

### Real-time YOLO Detection (Original)
1. Start the livestream from the Meta Ray-Ban AI Glasses
2. Run the detection script:

```bash
uv run python detect_live.py
```

3. A window will display the livestream with real-time object detection annotations
4. Press 'q' to quit the detection window

### AI Analysis with Text-to-Speech (New)
1. Make sure the livestream is visible on your screen
2. Run the complete workflow:

```bash
uv run python workflow_with_speech.py
```

3. The system will:
   - Capture a screenshot of the livestream area
   - Analyze it with Gemini AI using a comprehensive prompt
   - Speak the analysis results aloud using macOS Alex voice

### Test Screen Capture
To verify your screen capture coordinates:

```bash
uv run python test_capture.py
```

## Technical Details

- **Livestreaming**: The glasses livestream to Instagram, which is accessed via a browser on the Mac
- **Screen Capture**: mss captures a specific region of the screen where the livestream is displayed
- **Object Detection**: YOLOv8 Nano processes the captured frames for real-time detection
- **Performance Optimizations**:
  - MPS: Leverages the M1's GPU for faster inference
  - Frame Skipping: Processes detection every nth frame to improve FPS
  - Persistent Annotations: Displays the last detected frame during skipped frames to avoid visual glitching

## Troubleshooting

- **Livestream Video Not Displaying**: If the video doesn't appear in the browser, try disabling ad-blockers (e.g., Brave Shields) or switching to another browser
- **Incorrect Screen Capture Coordinates**: For dual-monitor setups, ensure the monitor coordinates in the script match the livestream's location. Use the test capture script to verify
- **Low FPS**: If performance is sluggish, increase the `frame_skip` value or reduce the capture resolution (e.g., from 320x320 to 224x224)
- **Package Import Issues**: If imports freeze or fail, reinstall packages with uv or check for M1 compatibility

## Future Improvements

- **Custom Model Training**: Fine-tune YOLOv8 Nano on a dataset of Arduino components for specialized object detection
- **Voice Commands**: Integrate speech recognition to enable hands-free interaction with the AI assistant
- **Arduino Integration**: Connect the system to an Arduino board to provide real-time feedback based on detected components and board states
- **Enhanced Voice Quality**: Explore other TTS options like ElevenLabs or Azure Speech for different voice options
- **Real-time Analysis**: Combine YOLO detection with Gemini analysis for continuous AI assistance
