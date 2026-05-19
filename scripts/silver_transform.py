"""Silver Layer — nettoyage et structuration des données Bronze."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config.minio_client import ensure_bucket, get_json, get_s3_client, list_keys, put_json
from config.settings import CITIES


def _clean_record(raw: dict) -> dict | None:
    try:
        temp = float(raw["temperature"])
        humidite = int(raw["humidite"])
        vent = float(raw["vent_vitesse"])
    except (KeyError, TypeError, ValueError):
        return None

    if temp < -20 or temp > 55 or humidite < 0 or humidite > 100 or vent < 0:
        return None

    return {
        "ville": str(raw["ville"]),
        "pays": str(raw.get("pays", "MA")),
        "temperature": round(temp, 2),
        "temp_min": round(float(raw.get("temp_min", temp)), 2),
        "temp_max": round(float(raw.get("temp_max", temp)), 2),
        "humidite": humidite,
        "pression": int(raw.get("pression", 0)),
        "vent_vitesse": round(vent, 2),
        "vent_direction": raw.get("vent_direction"),
        "description": str(raw.get("description", "")),
        "event_timestamp": raw.get("event_timestamp"),
        "ingestion_timestamp": raw.get("ingestion_timestamp"),
    }


def transform_silver(run_date: str | None = None) -> int:
    run_date = run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    client = get_s3_client()
    ensure_bucket(client)
    prefix = f"bronze/weather_raw/{run_date}/"
    keys = [k for k in list_keys(prefix, client) if k.endswith(".json")]

    if not keys:
        raise FileNotFoundError(f"Aucun fichier Bronze sous {prefix}")

    cleaned: list[dict] = []
    for key in keys:
        record = _clean_record(get_json(key, client))
        if record:
            cleaned.append(record)

    expected = {c["ville"] for c in CITIES}
    found = {r["ville"] for r in cleaned}
    if found != expected:
        missing = expected - found
        raise ValueError(f"Villes manquantes après nettoyage Silver: {missing}")

    out_key = f"silver/weather_clean/{run_date}/weather_clean.json"
    put_json(out_key, {"date": run_date, "records": cleaned}, client)
    print(f"[Silver] {len(cleaned)} villes -> {out_key}")
    return len(cleaned)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=None)
    args = parser.parse_args()
    transform_silver(args.date)
