from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)

    token = json_result["access_token"]
    return token

def get_calm_music(token):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": "calm",
        "type": "playlist",
        "limit": 3
    }
    response = get(url, headers=headers, params=params)
    
    # Check if request was successful
    if response.status_code != 200:
        print(f"Error: API request failed with status code {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    
    # Debug: print the full response to understand its structure
    print("Full API response:")
    print(json.dumps(data, indent=2))
    
    # Safely access the playlists data
    playlists = data.get("playlists", {})
    items = playlists.get("items", [])
    
    print(f"\nFound {len(items)} playlists:")
    
    for index, item in enumerate(items):
        print(f"\nPlaylist {index + 1}:")
        if item is None:
            print("  - Empty item")
            continue
            
        # Safely access name
        name = item.get('name')
        if name:
            print(f"  - Name: {name}")
        else:
            print("  - Name: Not available")
            
        # Safely access URL
        external_urls = item.get('external_urls', {})
        spotify_url = external_urls.get('spotify')
        if spotify_url:
            print(f"  - URL: {spotify_url}")
        else:
            print("  - URL: Not available")
            
        # Print other useful info
        print(f"  - ID: {item.get('id', 'Not available')}")
        print(f"  - Description: {item.get('description', 'Not available')[:100]}...")

# Main execution
if __name__ == "__main__":
    try:
        token = get_token()
        print("Access Token retrieved successfully")
        get_calm_music(token)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure your CLIENT_ID and CLIENT_SECRET are set correctly in the .env file")
