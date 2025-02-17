import requests

# UniFi UDM Pro IP Address
UNIFI_CONSOLE_IP = "192.168.1.1"
API_KEY = os.getenv("UNIFI_API_KEY")

# API Endpoint
URL = f"https://{UNIFI_CONSOLE_IP}:12445/api/v1/developer/users"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Fetch all users
def fetch_all_users():
    try:
        response = requests.get(URL, headers=HEADERS, verify=False)  # Disable SSL verification
        response.raise_for_status()
        
        data = response.json()
        if data.get("code") == "SUCCESS":
            return data.get("data", [])
        else:
            print("Error:", data.get("msg"))
            return []
    
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return []

if __name__ == "__main__":
    users = fetch_all_users()
    
    if users:
        print("Fetched Users:")
        for user in users:
            print(f"ID: {user.get('id')}, Name: {user.get('first_name')} {user.get('last_name')}, Status: {user.get('status')}")
    else:
        print("No users found.")