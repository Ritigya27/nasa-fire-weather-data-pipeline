import os
from pathlib import Path
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv


# Load .env from project root explicitly
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

MAP_KEY = os.getenv("NASA_FIRMS_MAP_KEY")
START_DATE = os.getenv("START_DATE", "2026-05-01")

print("Loaded MAP_KEY:", MAP_KEY)

RAW_DIR = BASE_DIR / "data" / "raw" / "firms"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_firms_data():
    if not MAP_KEY:
        raise ValueError("NASA_FIRMS_MAP_KEY missing inside .env file.")

    # India bounding box
    area = "68.1,6.5,97.4,35.7"

    sensor = "VIIRS_SNPP_NRT"
    day_range = 1

    url = (
        f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{MAP_KEY}/{sensor}/{area}/{day_range}/{START_DATE}"
    )

    print("Fetching NASA FIRMS data...")

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    run_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = RAW_DIR / f"firms_india_{run_date}.csv"

    output_file.write_text(response.text, encoding="utf-8")

    df = pd.read_csv(output_file)

    print(f"Saved raw data to: {output_file}")
    print(f"Rows ingested: {len(df)}")
    print(df.head())


if __name__ == "__main__":
    fetch_firms_data()