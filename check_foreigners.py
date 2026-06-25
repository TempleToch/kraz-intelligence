import pandas as pd
import os

INPUT = "data/raw_kraz_clean.xlsx"
OUTPUT = "data/foreigners_agencies.xlsx"

os.makedirs("data", exist_ok=True)

df = pd.read_excel(INPUT)

print("VALUE CHECK:")
print(df["uslugiDlaCudzoziemcow"].value_counts(dropna=False))

# normalize
df["uslugiDlaCudzoziemcow"] = (
    df["uslugiDlaCudzoziemcow"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# keep only valid YES
filtered = df[df["uslugiDlaCudzoziemcow"].isin(["tak", "yes"])]

filtered = filtered.drop_duplicates(subset=["nrWRejestrze"])

filtered.to_excel(OUTPUT, index=False)

print(f"Saved {len(filtered)} agencies -> {OUTPUT}")