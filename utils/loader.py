import pandas as pd

def load_contacts(filepath):
    df = pd.read_csv(filepath)
    print(f" Loaded {len(df)} contacts from {filepath}")
    return df