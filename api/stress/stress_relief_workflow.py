import os
import random
from datetime import datetime
import sys
from pathlib import Path

# Direct import from root level
from text_to_speech import speak_text

def play_calming_music():
    """Play calming music/sounds (placeholder for music integration)"""
    
    # List of calming activities/sounds that could be integrated
    calming_options = [
        "Playing your favorite calm playlist",
        "Starting guided breathing exercise", 
        "Playing nature sounds",
        "Starting meditation session",
        "Playing lo-fi music"
    ]
    
    selected = random.choice(calming_options)
    print(f"🎵 {selected}...")
    
    # Placeholder for actual music integration
    # You could integrate with:
    # - Spotify API
    # - Apple Music API  
    # - Local music files
    # - YouTube API
    # - Calm/Headspace APIs
    
    return selected

def breathing_exercise():
    """Guide user through breathing exercise"""
    
    breathing_text = (
        "Let's do a quick breathing exercise. "
        "Breathe in slowly for 4 counts. "
        "Hold for 4 counts. "
        "Breathe out slowly for 6 counts. "
        "Repeat this cycle 3 times."
    )
    
    print("🫁 Starting breathing exercise...")
    speak_text(breathing_text)
    
    return "breathing_exercise"

def stress_relief_workflow():
    """Complete stress relief workflow: music + breathing + positive affirmations"""
    
    print("🧘‍♀️ STRESS RELIEF WORKFLOW ACTIVATED 🧘‍♀️")
    
    # Step 1: Acknowledge stress detection
    acknowledge_text = "I've detected that you might be feeling stressed. Let me help you relax."
    print("💙 Acknowledging stress...")
    speak_text(acknowledge_text)
    
    # Step 2: Start calming music
    music_action = play_calming_music()
    speak_text(music_action)
    
    # Step 3: Guide breathing exercise
    breathing_exercise()
    
    # Step 4: Positive affirmation
    affirmations = [
        "You are strong and capable of handling whatever comes your way.",
        "This feeling is temporary. You have overcome challenges before and you will again.",
        "Take it one breath at a time. You've got this.",
        "You are exactly where you need to be right now.",
        "Your mental health matters. It's okay to take a moment for yourself."
    ]
    
    affirmation = random.choice(affirmations)
    print(f"💙 Positive affirmation: {affirmation}")
    speak_text(affirmation)
    
    # Step 5: Log stress relief session in organized folder
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = "stress_relief_log.txt"
    
    with open(log_file, 'a') as f:
        f.write(f"{timestamp}: Stress relief session - {music_action}, breathing exercise, affirmation\n")
    
    print("📝 Stress relief session logged")
    print("✅ Stress relief workflow complete!")
    
    return {
        "music": music_action,
        "breathing": "completed",
        "affirmation": affirmation,
        "timestamp": timestamp
    }

if __name__ == "__main__":
    stress_relief_workflow()
