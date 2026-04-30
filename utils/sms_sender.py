import csv
import os
import requests
from datetime import datetime

# For now we are using simulation mode (safe)
# Later we can use real SMS by changing SIMULATE to False
SIMULATE = True

# This will get the token from environment if we set it
SPARROW_TOKEN = os.getenv("SPARROW_TOKEN")
SPARROW_SENDER_ID = "Demo"


def send_sms(name, phone, message, log_filepath="data/sms_log.csv"):
    """Send SMS - simulation or real"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if SIMULATE:
        print(f"SMS sent to {phone} ({name}) - [SIMULATION MODE]")
        status = "sent"
        api_response = "Simulation mode"
    else:
        # Real SMS sending using Sparrow SMS
        if not SPARROW_TOKEN:
            print("Warning: SPARROW_TOKEN not found!")
            status = "failed"
            api_response = "Missing token"
        else:
            try:
                url = "http://api.sparrowsms.com/v2/sms/"
                data = {
                    'token': SPARROW_TOKEN,
                    'from': SPARROW_SENDER_ID,
                    'to': phone,
                    'text': message
                }
                response = requests.post(url, data=data, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("response_code") == 200:
                        status = "sent"
                        api_response = "Success"
                    else:
                        status = "failed"
                        api_response = "API Error"
                else:
                    status = "failed"
                    api_response = "HTTP Error"
                    
            except:
                status = "failed"
                api_response = "Request failed"

    # Save to log file
    _log_to_csv(log_filepath, name, phone, message, status, timestamp, api_response)
    
    return status


def _log_to_csv(filepath, name, phone, message, status, timestamp, api_response):
    """Save sending record to csv"""
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