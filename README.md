# UniFi Access - Bulk User Management & License Plate Assignment

## Overview
This repository provides Python scripts for managing users and credentials in UniFi Access. It allows you to:

✅ **Fetch all users** from UniFi Access.
✅ **Bulk deactivate & delete users** (except for whitelisted ones).
✅ **Assign license plates** to users based on a CSV file.

## Features
- Uses **API Key authentication** for fetching users.
- Uses **local admin login** for modifying users (deactivation, deletion, adding license plates).
- Supports **dry-run mode** for safe execution before deletion.

## Prerequisites
1. **UniFi UDM Pro / UniFi Access Setup**
2. **Python 3.6+ Installed**
3. Required Python packages:
   ```bash
   pip install requests urllib3
   ```
4. Set up the following **environment variables**:
   ```bash
   export UNIFI_CONSOLE_IP="192.168.1.231"
   export UNIFI_API_KEY="your-api-key"
   export UNIFI_ADMIN_USER="your-admin-username"
   export UNIFI_ADMIN_PASS="your-admin-password"
   ```

## Usage

### 1️⃣ Fetch Users
Run `fetch_users.py` to get a list of all users:
```bash
python3 fetch_users.py
```

✅ **Output Example:**
```
Fetched Users:
ID: d3950ced-0b7c-41fe-88f4-1251b076921a, Name: Homebridge API, Status: ACTIVE
...
```

### 2️⃣ Deactivate & Delete Users
1. **Fetch users first** (`fetch_users.py`).
2. **Edit `delete_users.py`** to add user IDs you want to keep.
3. **Run the script:**
```bash
python3 delete_users.py
```
✅ **Supports dry-run mode** before actual deletion.

### 3️⃣ Assign License Plates
1. **Prepare a CSV file (`license_plates.csv`)**:
   ```csv
   email,license_plate
   user1@example.com,ABC123
   user2@example.com,XYZ987
   ```
2. **Run the script**:
   ```bash
   python3 add_license_plate.py
   ```
✅ **Script will match users by email and add the license plate.**

## Notes
- **No bulk delete option exists in the UniFi UI**—this script automates the process.
- **License plate assignment requires local admin login**, not just an API key.
- The `fetch_users.py` script is required to retrieve user IDs before running `delete_users.py` or `add_license_plate.py`.

## Support
If you encounter any issues, feel free to open an issue or contribute!

