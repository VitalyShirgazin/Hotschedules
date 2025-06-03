#!/usr/bin/env python3
import os
import time

file_path = "success.log"

# Step 1: Delete if exists
if os.path.exists(file_path):
    os.remove(file_path)
    print("✅ success.log deleted.")

# Step 2: Wait 3 seconds
time.sleep(3)

# Step 3: Create the file
with open(file_path, "w") as f:
    f.write("")
print("✅ success.log created.")

