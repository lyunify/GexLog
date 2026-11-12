import csv
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_URL = "https://lab.flashalpha.com"
SYMBOL = "spy"

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "flashalpha_spy.csv"

load_dotenv(ROOT / ".env")
API_KEY = os.environ["FLASHALPHA_API_KEY"]

FIELDS = [
    "fetched_at", "as_of", "spy_price", "spx_price",
    "gamma_flip", "call_wall", "put_wall", "net_gex",
    "regime", "atm_iv", "vix",
]


def fetch_summary(symbol):
    response = requests.get(
        f"{BASE_URL}/v1/stock/{symbol}/summary",
        headers={"X-Api-Key": API_KEY},
        timeout=10,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"Request failed ({response.status_code}): {response.text}"
        )
    return response.json()


def parse_summary(data):
    exposure = data["exposure"]
    macro = data["macro"]
    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "as_of": data["as_of"],
        "spy_price": round(data["price"]["last"], 2),
        "spx_price": macro["spx"]["value"],
        "gamma_flip": round(exposure["gamma_flip"], 2),
        "call_wall": exposure["call_wall"],
        "put_wall": exposure["put_wall"],
        "net_gex": exposure["net_gex"],
        "regime": exposure["regime"],
        "atm_iv": data["volatility"]["atm_iv"],
        "vix": macro["vix"]["value"],
    }


def append_row(row, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new_file = not path.exists()
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if is_new_file:
            writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    data = fetch_summary(SYMBOL)
    row = parse_summary(data)
    append_row(row, CSV_PATH)
    print("Saved:", row)