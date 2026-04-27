from utils.loader import load_contacts
from utils.message_generator import generate_message

df = load_contacts("data/contacts.csv")

for _, row in df.iterrows():
    message = generate_message(row["name"], row["business_name"], row["business_type"])
    print(f"\nTo: {row['phone']}")
    print(f"Message: {message}")