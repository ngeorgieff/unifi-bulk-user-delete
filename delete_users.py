import requests
import urllib3
import os

# Suppress SSL warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# UniFi UDM Pro API Details
UNIFI_CONSOLE_IP = "192.168.1.1"

# API Tokens
FETCH_DEACTIVATE_API_KEY = os.getenv("UNIFI_API_KEY")  # Used for fetching and deactivating users

# API Endpoints
LOGIN_URL = f"https://{UNIFI_CONSOLE_IP}/api/auth/login"
FETCH_USERS_URL = f"https://{UNIFI_CONSOLE_IP}:12445/api/v1/developer/users"
UPDATE_USER_URL = f"https://{UNIFI_CONSOLE_IP}:12445/api/v1/developer/users"
DELETE_USER_URL = f"https://{UNIFI_CONSOLE_IP}/proxy/users/api/v2/user"

# Local Admin Credentials
LOCAL_ADMIN_USERNAME = os.getenv("UNIFI_ADMIN_USER")
LOCAL_ADMIN_PASSWORD = os.getenv("UNIFI_ADMIN_PASS")

# Headers for fetching & deactivating users (using API key)
FETCH_DEACTIVATE_HEADERS = {
    "Authorization": f"Bearer {FETCH_DEACTIVATE_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Allowed active users (these users will NOT be deleted)
ALLOWED_USERS = {
    "d3950ced-0b7c-41fe-88f4-1251b076921a"  # List UIDs to skip
}

# Global variables for session token and CSRF token (for delete action)
SESSION_TOKEN = None
CSRF_TOKEN = None

# Authenticate and retrieve session token for deletion
def authenticate():
    global SESSION_TOKEN, CSRF_TOKEN
    try:
        login_payload = {
            "username": LOCAL_ADMIN_USERNAME,
            "password": LOCAL_ADMIN_PASSWORD
        }
        response = requests.post(LOGIN_URL, json=login_payload, headers={"Content-Type": "application/json"}, verify=False)
        response.raise_for_status()
        
        # Extract session token from cookies
        SESSION_TOKEN = response.cookies.get("TOKEN")
        
        # Extract CSRF token from headers
        CSRF_TOKEN = response.headers.get("x-updated-csrf-token")

        if SESSION_TOKEN:
            print("✅ Successfully authenticated. Session token retrieved.")
        else:
            print("❌ Authentication failed: No session token received.")
            return False

        return True
    except requests.exceptions.RequestException as e:
        print("❌ Authentication request failed:", e)
        return False

# Fetch all users (using API key)
def fetch_all_users():
    try:
        response = requests.get(FETCH_USERS_URL, headers=FETCH_DEACTIVATE_HEADERS, verify=False)
        response.raise_for_status()
        data = response.json()
        if data.get("code") == "SUCCESS":
            return data.get("data", [])
        else:
            print("❌ Error fetching users:", data.get("msg"))
            return []
    except requests.exceptions.RequestException as e:
        print("❌ Request failed:", e)
        return []

# Deactivate a user (using API key)
def deactivate_user(user_id, user_name):
    try:
        update_payload = {"status": "DEACTIVATED"}  # API requires this to deactivate a user
        response = requests.put(f"{UPDATE_USER_URL}/{user_id}", headers=FETCH_DEACTIVATE_HEADERS, json=update_payload, verify=False)
        response.raise_for_status()
        data = response.json()
        if data.get("code") == "SUCCESS":
            print(f"✅ Successfully deactivated: {user_name} ({user_id})")
            return True
        else:
            print(f"❌ Failed to deactivate {user_name}: {data.get('msg')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed for {user_name}:", e)
        return False

# Delete a user using the session token and CSRF token
def delete_user(user_id, user_name):
    try:
        delete_url = f"{DELETE_USER_URL}/{user_id}"  # Construct correct delete URL
        headers = {
            "Cookie": f"TOKEN={SESSION_TOKEN}",
            "x-csrf-token": CSRF_TOKEN,  # Include CSRF token if needed
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.delete(delete_url, headers=headers, verify=False)

        if response.status_code == 200:
            print(f"🗑️ Successfully deleted: {user_name} ({user_id})")
        else:
            print(f"❌ Failed to delete {user_name}: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed for {user_name}: {e}")

# Main execution
if __name__ == "__main__":
    users = fetch_all_users()
    
    if users:
        print("🔍 Processing users...")
        for user in users:
            user_id = user.get("id")
            user_name = user.get("first_name", "Unknown") + " " + user.get("last_name", "Unknown")
            user_status = user.get("status")

            if user_id not in ALLOWED_USERS:
                if user_status == "ACTIVE":
                    print(f"🚨 Deactivating user: {user_name} ({user_id})")
                    if deactivate_user(user_id, user_name):
                        if not SESSION_TOKEN:  # Authenticate only once before deletion
                            if not authenticate():
                                print("❌ Authentication failed. Skipping deletion.")
                                break
                        print(f"🗑️ Removing user: {user_name} ({user_id})")
                        delete_user(user_id, user_name)
                elif user_status == "DEACTIVATED":
                    if not SESSION_TOKEN:  # Authenticate only once before deletion
                        if not authenticate():
                            print("❌ Authentication failed. Skipping deletion.")
                            break
                    print(f"🗑️ Removing user: {user_name} ({user_id})")
                    delete_user(user_id, user_name)
    
    print("✅ User deactivation & removal process completed.")