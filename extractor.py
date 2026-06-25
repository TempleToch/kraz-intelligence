import os
import time
import random
import requests
import pandas as pd

os.makedirs("data", exist_ok=True)

URL = "https://stor.praca.gov.pl/api/kraz/lista"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}


def extract_records(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in ["lista", "content", "data", "items", "result"]:
            if k in data and isinstance(data[k], list):
                return data[k]
    return []


def safe_request(payload, retries=3):
    for i in range(retries):
        try:
            return requests.post(URL, json=payload, headers=HEADERS, timeout=40)
        except requests.exceptions.RequestException:
            print(f"Retry {i+1}/{retries}")
            time.sleep(3)
    return None


def run_extract():
    print("STARTING KRAZ STABLE SCRAPER...")

    all_rows = []
    page = 1

    while True:

        payload = {
            "stronicowanie": {
                "strona": page,
                "rozmiarStrony": 100,
                "ilosc": 0
            },
            "sortowanie": {
                "kierunek": "ASC",
                "kolumna": "NAZWA"
            },
            "kryteria": []
        }

        r = safe_request(payload)

        if not r:
            print("STOP: request failed")
            break

        try:
            data = r.json()
        except:
            print("INVALID JSON")
            break

        records = extract_records(data)

        if not records:
            print(f"No more data at page {page}")
            break

        all_rows.extend(records)

        print(f"Page {page} -> {len(records)} records")

        page += 1

        time.sleep(random.uniform(1.0, 2.5))

    df = pd.DataFrame(all_rows)
    df.to_excel("data/raw_kraz.xlsx", index=False)

    print(f"DONE -> {len(df)} rows saved")


if __name__ == "__main__":
    run_extract()