from utils.loader import load_contacts, preprocess_contacts, validate_csv_structure
from utils.validator import validate_phone, validate_name, validate_business_name, validate_message_length
from utils.message_generator import generate_message
from utils.sms_sender import send_sms
from utils.reporter import generate_report

# ── Load ──────────────────────────────────────────────
df = load_contacts("data/contacts.csv")
validate_csv_structure(df)
df = preprocess_contacts(df)

# ── Pipeline ──────────────────────────────────────────
sent_count   = 0
failed_count = 0

skip_reasons = {
    "invalid_name":     0,
    "invalid_business": 0,
    "invalid_phone":    0
}

print("Starting Bulk SMS Pipeline...\n")

for _, row in df.iterrows():
    name  = row["name"]
    phone = str(row["phone"]).strip()
    biz   = row["business_name"]

    if not validate_name(name):
        print(f"  [SKIP] Invalid name: '{name}'")
        skip_reasons["invalid_name"] += 1
        continue

    if not validate_business_name(biz):
        print(f"  [SKIP] Invalid business name for {name}: '{biz}'")
        skip_reasons["invalid_business"] += 1
        continue

    if not validate_phone(phone):
        print(f"  [SKIP] Invalid phone: {phone} ({name})")
        skip_reasons["invalid_phone"] += 1
        continue

    message = generate_message(name, biz)

    if not validate_message_length(message):
        print(f"  [WARN] Message too long for {name}: {len(message)} chars")

    print(f"  [OK]   {name} | {phone} | {biz}")

    status = send_sms(name, phone, message)

    if status == "sent":
        sent_count += 1
    else:
        failed_count += 1

# ── Summary ───────────────────────────────────────────
total_skipped = sum(skip_reasons.values())

print("\n--- Pipeline Complete ---")
print(f"  Sent:    {sent_count}")
print(f"  Failed:  {failed_count}")
print(f"  Skipped: {total_skipped}")

if total_skipped > 0:
    print("  Skip breakdown:")
    for reason, count in skip_reasons.items():
        if count > 0:
            print(f"    - {reason}: {count}")

print(f"\nLog saved to: data/sms_log.csv")

generate_report(skip_reasons=skip_reasons)