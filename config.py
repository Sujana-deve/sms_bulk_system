import os
from dotenv import load_dotenv

load_dotenv()

# --- SMS Settings ---
SIMULATE = True  # Set to False when ready for real sending

SPARROW_TOKEN = os.getenv("SPARROW_TOKEN", "")
SPARROW_SENDER_ID = os.getenv("SPARROW_SENDER_ID", "Demo")
SPARROW_API_URL = "http://api.sparrowsms.com/v2/sms/"

# --- Retry Settings ---
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

# --- File Paths ---
CONTACTS_FILE = "data/contacts.csv"
SMS_LOG_FILE = "data/sms_log.csv"
REPORT_FILE = "data/report.html"