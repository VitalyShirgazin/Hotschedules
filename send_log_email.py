#!/usr/bin/env python3
import os
import pytz
from datetime import datetime
import subprocess

# --- Config ---
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
SUCCESS_FILE = os.path.join(SCRIPT_DIR, "success.log")
TO_EMAIL     = "my-email@gmail.com"

# --- Step 1: Check if success.log exists ---
if not os.path.exists(SUCCESS_FILE):
    print("❌ success.log does not exist.")
    exit(1)

# --- Step 2: Extract last block ---
with open(SUCCESS_FILE, "r") as f:
    content = f.read().strip()

blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
last_block = blocks[-1] if blocks else ""

# --- Step 2.5: Shutdown trigger check in last block ---
if "Clock in with your POS ID" in last_block:
    print("🕒 Shutdown triggered by last log block.")
    subprocess.run(['sudo', 'shutdown', '-h', '+1', '--no-wall'])
    exit(0)

# --- Step 2.6: Extract lines from "Final page message:", excluding lines with "EXIT" ---
lines = last_block.splitlines()
selected_lines = []

start_collecting = False
for line in lines:
    if "Final page message:" in line:
        start_collecting = True
    if start_collecting and "EXIT" not in line:
        selected_lines.append(line)

selected_text = "\n".join(selected_lines) if selected_lines else "⚠️ No matching lines found."

# --- Step 3: NYC timestamp in subject ---
nyc_time = datetime.now(pytz.timezone("America/New_York"))
subject = f"Hotschedule @ {nyc_time.strftime('%Y-%m-%d %I:%M %p %Z')}"

# --- Step 4: Send email using mailx ---
send_command = f'echo "{selected_text}" | mailx -s "{subject}" {TO_EMAIL}'
exit_code = subprocess.call(send_command, shell=True)

if exit_code == 0:
    print("✅ Email sent.")
else:
    print("❌ Failed to send email.")

