import pandas as pd


def load_contacts(filepath):
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} contacts from {filepath}")
    return df


def preprocess_contacts(df):
    print("\n--- Preprocessing Contacts ---")

    original_count = len(df)

    # strip whitespace from all column names first
    df.columns = df.columns.str.strip()

    # strip leading/trailing spaces from all string cells
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # replace truly empty strings and whitespace-only values with NaN
    df = df.replace(r'^\s*$', pd.NA, regex=True)

    # title case the name column — "sujana sharma" -> "Sujana Sharma"
    df["name"] = df["name"].apply(
        lambda x: x.title() if isinstance(x, str) else x
    )

    # title case the business_name column
    df["business_name"] = df["business_name"].apply(
        lambda x: x.title() if isinstance(x, str) else x
    )

    # clean phone — remove +977 country code prefix if present
    df["phone"] = df["phone"].apply(_clean_phone)

    # drop duplicate phone numbers — keep first occurrence
    before_dedup = len(df)
    df = df.drop_duplicates(subset=["phone"], keep="first")
    dupes_removed = before_dedup - len(df)
    if dupes_removed > 0:
        print(f"Removed {dupes_removed} duplicate phone number(s)")

    print(f"Preprocessing complete: {original_count} rows → {len(df)} rows remaining")
    print("-------------------------------\n")

    return df


def _clean_phone(phone):
    # convert to string first
    phone_str = str(phone).strip()

    # remove +977 or 977 country code prefix
    if phone_str.startswith("+977"):
        phone_str = phone_str[4:]
    elif phone_str.startswith("977") and len(phone_str) > 10:
        phone_str = phone_str[3:]

    # remove all non-digit characters (dashes, spaces, dots)
    phone_str = ''.join(c for c in phone_str if c.isdigit())

    return phone_str

def validate_csv_structure(df):
    # these are the exact columns our pipeline depends on
    required_columns = {"name", "phone", "business_name"}

    # get the actual columns from the dataframe as a set
    actual_columns = set(df.columns.str.strip().str.lower())

    # find which required columns are missing
    missing = required_columns - actual_columns

    if missing:
        raise ValueError(
            f"CSV is missing required column(s): {', '.join(missing)}\n"
            f"Expected: {', '.join(required_columns)}\n"
            f"Found:    {', '.join(actual_columns)}"
        )

    print("CSV structure check passed ✓")