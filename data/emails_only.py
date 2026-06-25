import pandas as pd

df = pd.read_excel("data/foreigners_agencies.xlsx")

# Remove rows without email
df = df[df["email"].notna()]
df = df[df["email"].astype(str).str.strip() != ""]

# Remove duplicate emails
df = df.drop_duplicates(subset=["email"])

# Keep useful columns
cols = [
    "nazwaAgencji",
    "email",
    "telefon",
    "nrWRejestrze",
    "wojewodztwo",
    "adres",
    "rodzajAgencji",
    "dataWpisu"
]

cols = [c for c in cols if c in df.columns]

df = df[cols]

df.to_excel(
    "data/foreigners_email_leads.xlsx",
    index=False
)

print(f"Unique email leads: {len(df)}")