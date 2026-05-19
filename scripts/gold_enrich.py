"""Gold Layer — KPI météo et classement des villes."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config.minio_client import ensure_bucket, get_json, get_s3_client, put_json


def score_temperature(temp: float) -> float:
    """40 pts si température entre 20 et 28 °C."""
    if 20 <= temp <= 28:
        return 40.0
    if 15 <= temp < 20 or 28 < temp <= 32:
        return 25.0
    if 10 <= temp < 15 or 32 < temp <= 35:
        return 15.0
    return 5.0


def score_humidity(humidity: int) -> float:
    """30 pts si humidité faible (< 50 %)."""
    if humidity < 50:
        return 30.0
    if humidity < 65:
        return 20.0
    if humidity < 80:
        return 10.0
    return 5.0


def score_wind(speed: float) -> float:
    """30 pts si vent faible (< 5 m/s)."""
    if speed < 5:
        return 30.0
    if speed < 8:
        return 20.0
    if speed < 12:
        return 10.0
    return 5.0


def compute_score(record: dict) -> float:
    total = (
        score_temperature(record["temperature"])
        + score_humidity(record["humidite"])
        + score_wind(record["vent_vitesse"])
    )
    return round(min(100.0, total), 0)


def assign_rankings(records: list[dict]) -> list[dict]:
    sorted_recs = sorted(records, key=lambda r: (-r["score_meteo"], r["ville"]))
    rank = 0
    prev_score = None
    for i, rec in enumerate(sorted_recs, start=1):
        if rec["score_meteo"] != prev_score:
            rank = i
            prev_score = rec["score_meteo"]
        rec["classement"] = rank
    return sorted_recs


def enrich_gold(run_date: str | None = None) -> dict:
    run_date = run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    client = get_s3_client()
    ensure_bucket(client)

    silver_key = f"silver/weather_clean/{run_date}/weather_clean.json"
    silver = get_json(silver_key, client)
    records = silver["records"]

    enriched = []
    for r in records:
        score = compute_score(r)
        enriched.append(
            {
                "ville": r["ville"],
                "pays": r["pays"],
                "temperature": r["temperature"],
                "humidite": r["humidite"],
                "vent_vitesse": r["vent_vitesse"],
                "description": r["description"],
                "score_meteo": score,
                "date": run_date,
            }
        )

    enriched = assign_rankings(enriched)
    best = min(enriched, key=lambda x: (x["classement"], x["ville"]))

    result = {
        "date": run_date,
        "meilleure_ville": best["ville"],
        "records": enriched,
    }

    gold_key = f"gold/weather_analytics/{run_date}/weather_analytics.json"
    put_json(gold_key, result, client)

    # Export local pour Power BI
    pbi_dir = ROOT / "powerbi"
    pbi_dir.mkdir(exist_ok=True)
    pbi_file = pbi_dir / "weather_analytics.json"
    pbi_file.write_text(json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[Gold] Analytics -> {gold_key}")
    print(f"[Gold] Export Power BI -> {pbi_file}")
    print(f"[Gold] Meilleure ville: {best['ville']} (score {best['score_meteo']})")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=None)
    args = parser.parse_args()
    enrich_gold(args.date)
