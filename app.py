from dotenv import load_dotenv
load_dotenv()
import emergency
import stress_relief
import snapshot

input = "SNAPSHOT"  # Change this value to "EMERGENCY", "STRESS_RELIEF", or "SNAPSHOT" to test different functionalities

if input == "EMERGENCY":
    emergency.main()
elif input == "STRESS_RELIEF":
    stress_relief.main()
elif input == "SNAPSHOT":
    snapshot.main("./poem.png")

    
    
