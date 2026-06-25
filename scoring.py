import pandas as pd
from utils import log

def score(row):
    s = 0

    if row["website"]:
        s += 2
    if row["emails"]:
        s += 3
    if row["job_signal"] == 1:
        s += 4

    return s


def run_score():
    df = pd.read_excel("data/enriched.xlsx")

    df["score"] = df.apply(score, axis=1)

    df["tier"] = df["score"].apply(
        lambda x: "HIGH" if x >= 8 else "MEDIUM" if x >= 5 else "LOW"
    )

    df = df.sort_values("score", ascending=False)

    df.to_excel("data/final.xlsx", index=False)

    log("SCORING DONE")


if __name__ == "__main__":
    run_score()