#!/usr/bin/env python3
import os
import pytz
from datetime import datetime
import subprocess

# --- Config ---
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
SUCCESS_FILE = os.path.join(SCRIPT_DIR, "success.log")
TO_EMAIL     = "my_email@email.com"

# --- Step 1: Check if success.log exists ---
if not os.path.exists(SUCCESS_FILE):
    print("❌ success.log does not exist.")
    exit(1)

# --- Step 2: Extract last block ---
with open(SUCCESS_FILE, "r") as f:
    content = f.read().strip()

blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
last_block = blocks[-1] if blocks else "⚠️ No content found in success.log."

# --- Step 3: NYC timestamp in subject ---
nyc_time = datetime.now(pytz.timezone("America/New_York"))
subject = f"Log Update from success.log @ {nyc_time.strftime('%Y-%m-%d %I:%M %p %Z')}"

# --- Step 4: Send email using mailx ---
send_command = f'echo "{last_block}" | mailx -s "{subject}" {TO_EMAIL}'
exit_code = subprocess.call(send_command, shell=True)

if exit_code == 0:
    print("✅ Email sent.")
else:
    print("❌ Failed to send email.")

