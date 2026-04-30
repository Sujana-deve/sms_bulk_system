# Bulk SMS System

A simple bulk SMS system built in Python for sending promotional messages to business contacts.


## What it does

- Loads contacts from a CSV file
- Validates Nepal mobile numbers
- Generates a personalized message for each contact
- Simulates SMS sending and logs the result
- Generates an HTML report after each run


## How to run

Install dependencies:
pip install -r requirements.txt

Run:
python main.py


## Note

Runs in simulate mode by default — no real SMS is sent. Mock contact data is used for this project. Invalid phone numbers are skipped automatically.