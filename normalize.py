import pandas as pd
import os

INPUT = "data/raw_kraz.xlsx"
OUTPUT = "data/raw_kraz_clean.xlsx"

os.makedirs("data", exist_ok=True)

df = pd.read_excel(INPUT)

# normalize column
df["uslugiDlaCudzoziemcow"] = (
    df["uslugiDlaCudzoziemcow"]
    .astype(str)
    .str.strip()
    .str.lower()
    .replace({
        "tak": "yes",
        "nie": "no",
        "-": "unknown",
        "none": "unknown"
    })
)

df.to_excel(OUTPUT, index=False)

print(f"normalized -> {len(df)} rows saved to {OUTPUT}")