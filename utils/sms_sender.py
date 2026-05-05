import csv
import os
import random
import time
import requests
from datetime import datetime

from config import (
    SIMULATE,
    SPARROW_TOKEN,
    SPARROW_SENDER_ID,
    SPARROW_API_URL,
    SMS_LOG_FILE,
    MAX_RETRIES,
    RETRY_DELAY_SECONDS
)


def send_sms(name, phone, message, log_filepath=SMS_LOG_FILE):
    """Send SMS with retry logic - simulation or real"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "failed"
    api_response = "Not attempted"

    for attempt in range(1, MAX_RETRIES + 1):
        status, api_response = _attempt_send(name, phone, message, attempt)

        if status == "sent":
            break

        if attempt < MAX_RETRIES:
            print(f"  Retrying in {RETRY_DELAY_SECONDS}s... (attempt {attempt + 1} of {MAX_RETRIES})")
            time.sleep(RETRY_DELAY_SECONDS)

    if status == "failed":
        print(f"  Failed after {MAX_RETRIES} attempts: {phone} ({name})")

    _log_to_csv(log_filepath, name, phone, message, status, timestamp, api_response)
    return status


def _attempt_send(name, phone, message, attempt):
    """Single send attempt - returns (status, api_response)"""

    if SIMULATE:
        # Randomly fail 20% of first attempts to demonstrate retry
        if attempt == 1 and random.random() < 0.2:
            print(f"  Attempt {attempt}: Simulated failure for {phone} ({name})")
            return "failed", "Simulated failure"

        print(f"  Attempt {attempt}: SMS sent to {phone} ({name}) - [SIMULATION MODE]")
        return "sent", "Simulation mode"

    else:
        if not SPARROW_TOKEN:
            print("  Warning: SPARROW_TOKEN not found!")
            return "failed", "Missing token"

        try:
            data = {
                'token': SPARROW_TOKEN,
                'from': SPARROW_SENDER_ID,
                'to': phone,
                'text': message
            }
            response = requests.post(SPARROW_API_URL, data=data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if result.get("response_code") == 200:
                    return "sent", "Success"
                else:
                    return "failed", f"API Error: {result}"
            else:
                return "failed", f"HTTP {response.status_code}: {response.text}"

        except requests.exceptions.RequestException as e:
            return "failed", f"Request failed: {str(e)}"


def _log_to_csv(filepath, name, phone, message, status, timestamp, api_response):
    """Save sending record to CSV"""
    file_exists = os.path.isfile(filepath)

    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "phone", "message", "status", "timestamp", "api_response"])

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "name": name,
            "phone": phone,
            "message": message,
            "status": status,
            "timestamp": timestamp,
            "api_response": api_response
        })