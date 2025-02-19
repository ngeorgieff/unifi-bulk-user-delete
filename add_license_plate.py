import os
import csv
import requests
import urllib3

# Suppress SSL warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# UniFi Protect API details (from environment variables)
UNIFI_CONSOLE_IP = os.getenv("UNIFI_CONSOLE_IP")
API_KEY = os.getenv("UNIFI_API_KEY")

# Local admin credentials (needed for adding license plates)
ADMIN_USERNAME = os.getenv("UNIFI_ADMIN_USER")
ADMIN_PASSWORD = os.getenv("UNIFI_ADMIN_PASS")

# API Endpoints
FETCH_USERS_URL = f"https://{UNIFI_CONSOLE_IP}:12445/api/v1/developer/users"
ADD_LICENSE_PLATE_URL = f"https://{UNIFI_CONSOLE_IP}/proxy/users/access/api/v2/credential"
LOGIN_URL = f"https://{UNIFI_CONSOLE_IP}/api/auth/login"

# CSV File Path (Change this if necessary)
CSV_FILE = "license_plates.csv"  # Format: email,license_plate

# Global authentication variables
SESSION_TOKEN = None
CSRF_TOKEN = None

def authenticate():
    """Authenticate using local admin credentials and retrieve session & CSRF tokens."""
    global SESSION_TOKEN, CSRF_TOKEN
    payload = {"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
    headers = {"Content-Type": "application/json"}

    response = requests.post(LOGIN_URL, json=payload, headers=headers, verify=False)
    
    if response.status_code == 200:
        SESSION_TOKEN = response.cookies.get("TOKEN")
        CSRF_TOKEN = response.headers.get("x-updated-csrf-token")

        if SESSION_TOKEN:
            print("✅ Successfully authenticated. Session token retrieved.")
        else:
            print("❌ Authentication failed: No session token received.")
            return False
    else:
        print(f"❌ Authentication failed: {response.text}")
        return False

    return True

def fetch_users():
    """Fetch all users using the API key (same as fetch_users.py)."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(FETCH_USERS_URL, headers=headers, verify=False)
        response.raise_for_status()

        data = response.json()
        if data.get("code") == "SUCCESS":
            return {user.get("email"): user.get("id") for user in data.get("data", []) if "email" in user}
        else:
            print("❌ Error fetching users:", data.get("msg"))
            return {}

    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
        return {}

def add_license_plate(user_id, license_plate):
    """Adds a license plate to the user's credentials using session authentication."""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Cookie": f"TOKEN={SESSION_TOKEN}",
        "x-csrf-token": CSRF_TOKEN
    }

    payload = {
        "user_id": user_id,
        "user_type": "user",  # Required field as seen in HAR file
        "credential": license_plate,  # License plate number
        "credential_type": "license"
    }

    print(f"📡 Sending request to {ADD_LICENSE_PLATE_URL} with payload: {payload}")

    response = requests.post(ADD_LICENSE_PLATE_URL, json=payload, headers=headers, verify=False)

    try:
        response_json = response.json()  # Parse the response JSON
        print(f"🔍 API Response: {response_json}")  # Print the full API response
    except requests.exceptions.JSONDecodeError:
        print(f"⚠️ Non-JSON response received: {response.text}")

    if response.status_code == 200:
        print(f"✅ Successfully added license plate {license_plate} to user {user_id}")
    else:
        print(f"❌ Failed to add license plate {license_plate} to {user_id}: {response.text}")

def process_csv():
    """Read CSV file and process each row."""
    try:
        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            # Authenticate first (to get session token for adding license plates)
            if not authenticate():
                print("❌ Authentication failed. Exiting.")
                return

            user_dict = fetch_users()  # Fetch users using API key

            for row in reader:
                email = row["email"].strip()
                license_plate = row["license_plate"].strip()

                print(f"🔍 Processing: {email} -> {license_plate}")

                user_id = user_dict.get(email)
                if user_id:
                    add_license_plate(user_id, license_plate)
                else:
                    print(f"❌ No user found for email: {email}")

    except FileNotFoundError:
        print(f"❌ CSV file '{CSV_FILE}' not found. Please ensure the file exists.")

if __name__ == "__main__":
    process_csv()