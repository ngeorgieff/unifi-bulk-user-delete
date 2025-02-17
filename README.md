# Unifi User Management Script

## Overview
This script automates the **bulk deactivation and deletion of users** from a **UniFi Access system** using the **UniFi API** and session authentication.

### Why This Script?
I was looking for a way to **bulk delete users from UniFi Access**, but there was **no way to do it through the UI or any documented API**. After analyzing network requests, I identified the necessary API calls to achieve this functionality.

### Features
- ✅ Fetches users from UniFi UDM Pro using an API key.
- ✅ Deactivates users **not in the allowed list**.
- ✅ Authenticates with **local admin credentials** for deletion.
- ✅ **Deletes deactivated users** securely using session tokens.
- ✅ Includes **error handling** and **logging** for debugging.

---

## Prerequisites
- **Python 3.x**
- **pip installed**
- **Access to your UniFi UDM Pro**
- **Environment variables set for authentication**

---

## Installation
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/ngeorgieff/unifi-bulk-user-delete.git
cd unifi-bulk-user-delete
```

Install required dependencies:
```bash
pip install requests python-dotenv
```

---

## Configuration
Set environment variables before running the scripts:

```bash
export UNIFI_API_KEY="your-api-key"
export UNIFI_ADMIN_USER="your-admin-username"
export UNIFI_ADMIN_PASS="your-admin-password"
```

Add these to your `~/.bashrc`, `~/.bash_profile`, or `.env` file for persistence.

---

## Usage

### Step 1: Fetch Users and Get Their UIDs
Before deleting users, first **fetch all users** and get their **UIDs**:

```bash
python3 fetch_users.py
```

This will print a list of users in the format:

```bash
Fetched Users:
ID: d3950ced-0b7c-41fe-88f4-1251b076921a, Name: Homebridge API, Status: ACTIVE
ID: 07331101-623c-4f51-8958-a190ad77669d, Name: homeassistant-api , Status: ACTIVE
...
```

### Step 2: Update `delete_users.py` with Allowed UIDs
Modify the `ALLOWED_USERS` list in `delete_users.py` with **UIDs of users you want to keep**:

```python
ALLOWED_USERS = {
    "d3950ced-0b7c-41fe-88f4-1251b076921a",  # Homebridge API
    "07331101-623c-4f51-8958-a190ad77669d",  # homeassistant-api
}
```

### Step 3: Run the Deletion Script
Once you have updated the **allowed users**, run:

```bash
python3 delete_users.py
```

Expected output:
```bash
🔍 Processing users...
🚨 Deactivating user: John Doe (22eb5f2a-ed6c-4d32-a22f-401a4688a4f3)
✅ Successfully deactivated: John Doe (22eb5f2a-ed6c-4d32-a22f-401a4688a4f3)
✅ Successfully authenticated. Session token retrieved.
🗑️ Removing user: John Doe (22eb5f2a-ed6c-4d32-a22f-401a4688a4f3)
🗑️ Successfully deleted: John Doe (22eb5f2a-ed6c-4d32-a22f-401a4688a4f3)
✅ User deactivation & removal process completed.
```

---

## Troubleshooting

### **401 Unauthorized?**
- Ensure the API key has the correct permissions.
- Verify the local admin credentials are correct.
- Ensure the session token is correctly extracted and passed.

### **Users not deleting?**
- Make sure the user is **deactivated** before deletion.
- Ensure the script is using the correct **DELETE endpoint**.

---

## License
This project is licensed under the **MIT License**. Feel free to modify and distribute.

---

## Contributing
Feel free to submit **pull requests** and contribute to improvements! 🚀

---

## Author
👤 Nikolay Georgiev
📧 n@data-protect.net
📌 **GitHub:** [ngeorgieff](https://github.com/ngeorgieff)
# unifi-bulk-user-delete
# unifi-bulk-user-delete
