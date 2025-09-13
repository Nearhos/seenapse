"""
Mental Health Glasses AI - Main Orchestrator
Ready for Crown (Neurosity) EEG Integration

This is the main dispatcher that routes EEG signals to specific workflows:
1. EMERGENCY - SOS function (location, alerts, logging)
2. SNAPSHOT - Screenshot analysis (math, translation, description)
3. MESSAGE - Send message to specific contact
4. STRESS_RELIEF - Calming music, breathing exercises, affirmations
"""

import sys
from datetime import datetime

# Direct imports from root level
from emergency_workflow import emergency_workflow
from snapshot_workflow import snapshot_workflow
from messaging_workflow import send_message_workflow
from stress_relief_workflow import stress_relief_workflow
from text_to_speech import speak_text

# Workflow mappings for EEG signal integration
WORKFLOWS = {
    "EMERGENCY": emergency_workflow,
    "SNAPSHOT": snapshot_workflow, 
    "MESSAGE": send_message_workflow,
    "STRESS_RELIEF": stress_relief_workflow
}

def main_orchestrator(workflow_name="SNAPSHOT"):
    """
    Main orchestrator function - routes to appropriate workflow
    
    Args:
        workflow_name (str): One of "EMERGENCY", "SNAPSHOT", "MESSAGE", "STRESS_RELIEF"
        
    This function will be called by the Crown EEG integration when specific
    brain signals are detected.
    """
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*60}")
    print(f"🧠 MENTAL HEALTH AI ACTIVATED - {timestamp}")
    print(f"🎯 Workflow: {workflow_name}")
    print(f"{'='*60}")
    
    # Validate workflow
    if workflow_name not in WORKFLOWS:
        error_msg = f"❌ Unknown workflow: {workflow_name}. Available: {list(WORKFLOWS.keys())}"
        print(error_msg)
        speak_text("Unknown workflow requested")
        return None
    
    # Execute the requested workflow
    try:
        result = WORKFLOWS[workflow_name]()
        
        # Log workflow execution
        log_entry = f"{timestamp}: Executed {workflow_name} workflow\n"
        with open("workflow_log.txt", "a") as f:
            f.write(log_entry)
        
        print(f"\n✅ {workflow_name} workflow completed successfully!")
        return result
        
    except Exception as e:
        error_msg = f"❌ Error in {workflow_name} workflow: {e}"
        print(error_msg)
        speak_text(f"Error occurred in {workflow_name} workflow")
        return None

def test_all_workflows():
    """Test all workflows to ensure they work correctly"""
    
    print("🧪 TESTING ALL WORKFLOWS")
    print("="*50)
    
    for workflow_name in WORKFLOWS.keys():
        print(f"\n🔄 Testing {workflow_name}...")
        result = main_orchestrator(workflow_name)
        
        if result is not None:
            print(f"✅ {workflow_name} test passed")
        else:
            print(f"❌ {workflow_name} test failed")
        
        print("-" * 30)
    
    print("\n🧪 All workflow tests completed!")

# Crown EEG Integration Point
def crown_signal_handler(eeg_signal_type):
    """
    This function will be called by the Crown EEG integration
    when specific brain signals are detected.
    
    Args:
        eeg_signal_type (str): The type of EEG signal detected
                              Maps to our workflow names
    """
    
    print(f"🧠 Crown EEG Signal Detected: {eeg_signal_type}")
    return main_orchestrator(eeg_signal_type)

if __name__ == "__main__":
    # For testing: change this value or pass as command line argument
    if len(sys.argv) > 1:
        workflow = sys.argv[1].upper()
    else:
        # Default workflow for testing
        workflow = "SNAPSHOT"  # Change this to test different workflows
    
    # Special command to test all workflows
    if workflow == "TEST_ALL":
        test_all_workflows()
    else:
        main_orchestrator(workflow)
