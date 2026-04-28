from utils.loader import load_contacts
from utils.validator import validate_phone
from utils.message_generator import generate_message
from utils.sms_sender import send_sms

df = load_contacts("data/contacts.csv")

sent_count = 0
failed_count = 0
skipped_count = 0

print("\nStarting Bulk SMS Pipeline...\n")

for _, row in df.iterrows():
    name  = row["name"]
    phone = str(row["phone"]).strip()
    biz   = row["business_name"]

    if not validate_phone(phone):
        print(f"Skipping invalid number: {phone} ({name})")
        skipped_count += 1
        continue

    message = generate_message(name, biz)
    print(f"\nTo: {phone}")
    print(f"Message: {message}")

    status = send_sms(name, phone, message)

    if status == "sent":
        sent_count += 1
    else:
        failed_count += 1

print("\n--- Pipeline Complete ---")
print(f"Sent:    {sent_count}")
print(f"Failed:  {failed_count}")
print(f"Skipped: {skipped_count}")
print(f"\nLog saved to: data/sms_log.csv")