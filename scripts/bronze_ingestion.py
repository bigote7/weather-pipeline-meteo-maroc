"""Bronze Layer — ingestion OpenWeatherMap vers MinIO."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config.minio_client import ensure_bucket, get_s3_client, put_json
from config.settings import CITIES, OPENWEATHER_API_KEY, OPENWEATHER_URL


def ingest_bronze(run_date: str | None = None) -> int:
    if not OPENWEATHER_API_KEY:
        raise ValueError(
            "OPENWEATHER_API_KEY manquante. Copiez .env.example vers .env et ajoutez votre clé."
        )

    run_date = run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    client = get_s3_client()
    ensure_bucket(client)
    now_iso = datetime.now(timezone.utc).isoformat()
    count = 0

    for city in CITIES:
        ville = city["ville"]
        params = {"q": city["api_name"], "appid": OPENWEATHER_API_KEY, "units": "metric"}
        resp = requests.get(OPENWEATHER_URL, params=params, timeout=30)
        resp.raise_for_status()
        raw = resp.json()

        payload = {
            "ville": ville,
            "pays": raw.get("sys", {}).get("country", "MA"),
            "temperature": raw["main"]["temp"],
            "temp_min": raw["main"]["temp_min"],
            "temp_max": raw["main"]["temp_max"],
            "humidite": raw["main"]["humidity"],
            "pression": raw["main"]["pressure"],
            "vent_vitesse": raw["wind"]["speed"],
            "vent_direction": raw["wind"].get("deg"),
            "description": raw["weather"][0]["description"] if raw.get("weather") else "",
            "event_timestamp": datetime.fromtimestamp(
                raw["dt"], tz=timezone.utc
            ).isoformat(),
            "ingestion_timestamp": now_iso,
            "raw_api": raw,
        }

        key = f"bronze/weather_raw/{run_date}/{ville.lower()}.json"
        put_json(key, payload, client)
        print(f"[Bronze] OK — {ville} -> {key}")
        count += 1

    print(f"[Bronze] {count} villes ingérées pour {run_date}")
    return count


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=None, help="YYYY-MM-DD")
    args = parser.parse_args()
    ingest_bronze(args.date)
