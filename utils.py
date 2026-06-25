import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/run.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    force=True
)

def log(msg):
    print(msg)
    logging.info(msg)