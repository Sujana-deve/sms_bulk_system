import csv
import os
from datetime import datetime

# set to False to use real SMS API instead of simulation
SIMULATE = True


def send_sms(name, phone, message, log_filepath="data/sms_log.csv"):
    # get current time for the log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if SIMULATE:
        print(f"SMS sent to {phone} ({name})")
        status = "sent"
    else:
        # real API call would go here
        status = "failed"

    _log_to_csv(log_filepath, name, phone, message, status, timestamp)
    return status


def _log_to_csv(filepath, name, phone, message, status, timestamp):
    # check if file exists to decide whether to write header
    file_exists = os.path.isfile(filepath)

    # open in append mode so previous records are not overwritten
    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "phone", "message", "status", "timestamp"]
        )
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "name": name,
            "phone": phone,
            "message": message,
            "status": status,
            "timestamp": timestamp,
        })