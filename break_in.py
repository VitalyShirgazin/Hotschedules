#!/usr/bin/env python3
import sys
import time
import random
import os
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- Load credentials from environment variables for security ---
USERNAME = os.getenv("HS_USERNAME", "YOUR_USERNAME")
PASSWORD = os.getenv("HS_PASSWORD", "YOUR_PASSWORD")
POS_ID   = os.getenv("HS_POS_ID", "YOUR_POS_ID")


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUCCESS_LOG_FILE = os.path.join(SCRIPT_DIR, "success.log")
ERROR_LOG_FILE   = os.path.join(SCRIPT_DIR, "errors.log")
BLOCK_SEPARATOR  = "\n\n"

def log_msg(message):
    timestamp = datetime.now().isoformat()
    print(f"{timestamp} {message}")
    with open(SUCCESS_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")

def log_error(message):
    timestamp = datetime.now().isoformat()
    print(f"{timestamp} {message}")
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")

def wait_clickable(wait, selector, by=By.XPATH, timeout_msg=None):
    try:
        return wait.until(EC.element_to_be_clickable((by, selector)))
    except TimeoutException:
        log_error(timeout_msg or f"❌ Element not clickable: {selector}")
        raise

def main():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver:
            wait = WebDriverWait(driver, 20)

            # 1. Login
            driver.get("https://app.hotschedules.com/hs/webclock/")
            wait.until(EC.presence_of_element_located((By.ID, "web-clock-username"))).send_keys(USERNAME)
            wait.until(EC.presence_of_element_located((By.XPATH, "(//input[@type='password'])[1]"))).send_keys(PASSWORD)
            wait_clickable(wait, "button.web-clock--button-full-width", By.CSS_SELECTOR).click()
            log_msg("✅ Login succeeded")
            time.sleep(1)

            # 2. Enter POS_ID via keypad
            for digit in POS_ID:
                wait_clickable(wait, f"//div[contains(@class, 'keypad-cell') and normalize-space(text())='{digit}']").click()
                time.sleep(random.uniform(0.12, 0.25))
            log_msg("✅ POS entry simulated")
            time.sleep(1)

            # Go button
            wait_clickable(wait, "button.go-button", By.CSS_SELECTOR).click()
            log_msg("✅ POS entry submitted")

            # 3. Wait for START BREAK button and click it
            start_break_xpath = '//*[@id="root"]/div/div[2]/div/div[2]/div/button[2]'
            start_break_btn = wait.until(EC.element_to_be_clickable((By.XPATH, start_break_xpath)))
            start_break_btn.click()
            log_msg("✅ Clicked the START BREAK button")

            # Final page message
            time.sleep(2)
            page_text = driver.find_element(By.TAG_NAME, "body").text
            log_msg(f"🟢 Final page message:\n{page_text}")

            # Append separator to success log
            with open(SUCCESS_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(BLOCK_SEPARATOR)

    except TimeoutException as e:
        log_error(f"⏰ Timeout: {str(e)}")
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            traceback.print_exc(file=f)
            f.write(BLOCK_SEPARATOR)
        sys.exit(2)

    except Exception as e:
        log_error(f"❌ Error during automation: {e}")
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            traceback.print_exc(file=f)
            f.write(BLOCK_SEPARATOR)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

