#!/usr/bin/env python3
import time
import subprocess

def run_script(script_name):
    print(f"▶️ Running: {script_name}")
    subprocess.run(["python3", script_name])

# 1. Run delete_create_successlog.py
run_script("delete_create_successlog.py")

# 2. Wait 10 sec
time.sleep(10)

# 3. Run break_in.py
run_script("break_in.py")

# 4. Run send_log_email.py (after break_in.py)
run_script("send_log_email.py")

# 5. Wait 10 sec
time.sleep(10)

# 6. Run break_out.py
run_script("break_out.py")

# 7. Run send_log_email.py again at the end
run_script("send_log_email.py")

