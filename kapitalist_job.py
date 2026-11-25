import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY not set in environment")

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}

URLS = ["http://localhost:30003/api/cron/btc-data",
	"http://localhost:30003/api/cron/price-change-alert",
	"http://localhost:30003/api/cron/portfolio-sync"]

def send_requests():
    for url in URLS:
        response = requests.post(url, headers=HEADERS, timeout=30)
        print(f"{url} -> {response.status_code}")

if __name__ == "__main__":
    send_requests()

