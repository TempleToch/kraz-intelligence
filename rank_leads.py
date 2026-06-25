import pandas as pd

df = pd.read_excel("data/foreigners_email_leads.xlsx")

# basic scoring rules
df["score"] = 0

# priority: recent agencies
df["score"] += pd.to_datetime(df["dataWpisu"], errors="coerce").apply(
    lambda x: 2 if x and x.year >= 2024 else 0
)

# temporary work agencies (higher foreign demand)
df["score"] += df["rodzajAgencji"].astype(str).str.lower().apply(
    lambda x: 2 if "tymczas" in x or "temporary" in x else 0
)

# email present already assumed, but boost business domains slightly
df["score"] += df["email"].astype(str).apply(
    lambda x: 1 if not any(p in x.lower() for p in ["gmail", "outlook", "wp.pl", "onet"]) else 0
)

df = df.sort_values("score", ascending=False)

df.to_excel("data/foreigners_ranked_leads.xlsx", index=False)

print("Ranked leads saved:", len(df))