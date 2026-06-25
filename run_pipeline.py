import os
import subprocess

print("STARTING KRAZ FULL PIPELINE...")

steps = [
    "python extractor.py",
    "python normalize.py",
    "python check_foreigners.py",
    "python rank_leads_v2.py",
    "python prepare_outreach.py"
]

for step in steps:
    print(f"\nRUNNING: {step}")
    result = subprocess.run(step, shell=True)
    
    if result.returncode != 0:
        print(f"FAILED AT: {step}")
        break

print("\nPIPELINE COMPLETE")