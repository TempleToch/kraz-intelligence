import pandas as pd
import os

INPUT = "data/foreigners_agencies.xlsx"
OUTPUT = "data/foreigners_ranked_leads_v2.xlsx"

os.makedirs("data", exist_ok=True)

df = pd.read_excel(INPUT)

# -----------------------------
# CLEAN BASIC FIELDS
# -----------------------------
df["email"] = df["email"].fillna("").astype(str).str.strip()
df["dataWpisu"] = pd.to_datetime(df["dataWpisu"], errors="coerce")

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------

# 1. Email quality
df["has_email"] = df["email"].apply(lambda x: 1 if "@" in x else 0)
df = df[df["email"].str.contains("@", na=False)]

# 2. Recency score (newer agencies = higher intent)
latest_year = df["dataWpisu"].dt.year.max()
df["recency_score"] = latest_year - df["dataWpisu"].dt.year
df["recency_score"] = df["recency_score"].fillna(5)

# 3. Agency type strength
df["type_score"] = df["rodzajAgencji"].astype(str).apply(
    lambda x: 2 if "Temporary work" in x else 1
)

# 4. Multi-service bonus
df["service_score"] = df["rodzajAgencji"].astype(str).apply(
    lambda x: len(x.split(",")) if x != "nan" else 1
)

# -----------------------------
# FINAL SCORE (weighted)
# -----------------------------

df["lead_score"] = (
    df["has_email"] * 5 +
    df["type_score"] * 3 +
    df["service_score"] * 2 -
    df["recency_score"] * 0.5
)

# -----------------------------
# SORT + CLEAN OUTPUT
# -----------------------------

df = df.sort_values(by="lead_score", ascending=False)

columns = [
    "nazwaAgencji",
    "nrWRejestrze",
    "email",
    "telefon",
    "miejscowosc",
    "wojewodztwo",
    "dataWpisu",
    "lead_score"
]

df[columns].to_excel(OUTPUT, index=False)

print(f"Ranked leads saved -> {len(df)} records")