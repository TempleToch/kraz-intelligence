import pandas as pd
import os

INPUT = "data/foreigners_ranked_leads_v2.xlsx"
OUTPUT = "data/outreach_ready_leads.xlsx"

os.makedirs("data", exist_ok=True)

df = pd.read_excel(INPUT)

# -----------------------------
# CLEAN EMAILS
# -----------------------------
df["email"] = df["email"].fillna("").astype(str).str.strip().str.lower()

df = df[df["email"].str.contains("@", na=False)]

# remove generic or useless emails
bad_keywords = ["example", "test", "info@", "office@", "admin@"]

df = df[~df["email"].str.contains("|".join(bad_keywords))]

# -----------------------------
# REMOVE DUPLICATES
# -----------------------------
df = df.drop_duplicates(subset=["email"])

# -----------------------------
# EXTRACT EMAIL DOMAIN
# -----------------------------
df["email_domain"] = df["email"].str.split("@").str[-1]

# -----------------------------
# FINAL SORT (best leads first)
# -----------------------------
df = df.sort_values(by="lead_score", ascending=False)

# -----------------------------
# FINAL COLUMNS FOR OUTREACH
# -----------------------------
columns = [
    "nazwaAgencji",
    "nrWRejestrze",
    "email",
    "email_domain",
    "telefon",
    "miejscowosc",
    "wojewodztwo",
    "lead_score"
]

df[columns].to_excel(OUTPUT, index=False)

print(f"Outreach dataset ready -> {len(df)} leads")