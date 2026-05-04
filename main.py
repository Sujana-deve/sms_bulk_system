from utils.loader import load_contacts, preprocess_contacts
from utils.validator import validate_phone, validate_name, validate_business_name, validate_message_length
from utils.message_generator import generate_message
from utils.sms_sender import send_sms
from utils.reporter import generate_report
from utils.loader import load_contacts,preprocess_contacts,validate_csv_structure

# ── Load ──────────────────────────────────────────────
df = load_contacts("data/contacts.csv")
validate_csv_structure(df)
df = load_contacts("data/contacts.csv")

# ── Preprocess ────────────────────────────────────────
df = preprocess_contacts(df)

# ── Pipeline ──────────────────────────────────────────
sent_count    = 0
failed_count  = 0
skipped_count = 0

print("Starting Bulk SMS Pipeline...\n")

for _, row in df.iterrows():
    name  = row["name"]
    phone = str(row["phone"]).strip()
    biz   = row["business_name"]

    # validate name
    if not validate_name(name):
        print(f"  [SKIP] Invalid name: '{name}'")
        skipped_count += 1
        continue

    # validate business name
    if not validate_business_name(biz):
        print(f"  [SKIP] Invalid business name for {name}: '{biz}'")
        skipped_count += 1
        continue

    # validate phone
    if not validate_phone(phone):
        print(f"  [SKIP] Invalid phone: {phone} ({name})")
        skipped_count += 1
        continue

    # generate message
    message = generate_message(name, biz)

    # warn if message too long but still send
    if not validate_message_length(message):
        print(f"  [WARN] Message too long for {name}: {len(message)} chars")

    print(f"  [OK]   {name} | {phone} | {biz}")

    status = send_sms(name, phone, message)

    if status == "sent":
        sent_count += 1
    else:
        failed_count += 1

# ── Summary ───────────────────────────────────────────
print("\n--- Pipeline Complete ---")
print(f"  Sent:    {sent_count}")
print(f"  Failed:  {failed_count}")
print(f"  Skipped: {skipped_count}")
print(f"\nLog saved to: data/sms_log.csv")

generate_report()