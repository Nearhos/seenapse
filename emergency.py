import os, requests
from twilio.rest import Client

def send_sms(location_message):
    # Find Account SID and Auth Token at twilio.com/console
    account_sid = "ACdc98fda075d039d46598b4c54462b5f3"  # Twilio Account SID
    auth_token = "ca0ab5df258db91e2ea2b1b8ab7ba6a5"  # Twilio Auth Token
    client = Client(account_sid, auth_token)


    num = "+14159807815"  # your number
    emergency_contacts = ["+16478668110"]   # Emergency contact numbers - Police(911), Family, Friends, Neighbors, Workplace, School, Doctor, Therapist, Crisis Hotline, etc.

    for to in emergency_contacts:
        message = client.messages.create(
        body="SOS\n"+location_message,
        from_=num,
        to=to,
    )

def get_location():
    # IP-based geolocation (city-level, approximate).
    # If you have an ipinfo token, export IPINFO_TOKEN for better accuracy/rate limits.
    token = os.getenv("IPINFO_TOKEN")
    url = "https://ipinfo.io/json" + (f"?token={token}" if token else "")
    j = requests.get(url, timeout=4).json()
    lat, lon = map(float, j.get("loc", "0,0").split(","))
    return {
        "lat": lat,
        "lon": lon,
        "ip": j.get("ip"),
        "city": j.get("city"),
        "region": j.get("region"),
        "country": j.get("country"),
        "source": "ipinfo"
    }

def main():
    loc = get_location()
    location_message = (
        f"Location: {loc['lat']:.5f},{loc['lon']:.5f} "
        f"({loc.get('city')}, {loc.get('region')}, {loc.get('country')}) "
        f"[ip={loc.get('ip')}]"
    )
    print("SOS\n"+location_message) 
    # send_sms(location_message)