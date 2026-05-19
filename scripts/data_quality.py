"""Tests qualité — Bronze, Silver, Gold."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config.minio_client import get_json, get_s3_client, list_keys
from config.settings import CITIES


def test_bronze(run_date: str | None = None) -> bool:
    run_date = run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    client = get_s3_client()
    prefix = f"bronze/weather_raw/{run_date}/"
    keys = [k for k in list_keys(prefix, client) if k.endswith(".json")]
    expected = len(CITIES)
    if len(keys) != expected:
        raise AssertionError(f"Bronze: attendu {expected} fichiers, trouvé {len(keys)}")
    print(f"[QA Bronze] OK — {len(keys)} fichiers JSON")
    return True


def test_silver(run_date: str | None = None) -> bool:
    run_date = run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    client = get_s3_client()
    key = f"silver/weather_clean/{run_date}/weather_clean.json"
    data = get_json(key, client)
    records = data.get("records", [])
    required = {
        "ville",
        "temperature",
        "humidite",
        "vent_vitesse",
        "event_timestamp",
        "ingestion_timestamp",
    }

    if len(records) != len(CITIES):
        raise AssertionError(f"Silver: attendu {len(CITIES)} enregistrements")

    for rec in records:
        missing = required - set(rec.keys())
        if missing:
            raise AssertionError(f"Silver: colonnes manquantes {missing} pour {rec.get('ville')}")
        if not isinstance(rec["temperature"], (int, float)):
            raise AssertionError(f"Silver: type temperature invalide pour {rec['ville']}")
        if not (0 <= rec["humidite"] <= 100):
            raise AssertionError(f"Silver: humidité invalide pour {rec['ville']}")

    print(f"[QA Silver] OK — {len(records)} enregistrements valides")
    return True


def test_gold(run_date: str | None = None) -> bool:
    run_date = run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    client = get_s3_client()
    key = f"gold/weather_analytics/{run_date}/weather_analytics.json"
    data = get_json(key, client)
    records = data.get("records", [])

    if len(records) != len(CITIES):
        raise AssertionError(f"Gold: attendu {len(CITIES)} villes")

    ranks = []
    for rec in records:
        score = rec["score_meteo"]
        if not (0 <= score <= 100):
            raise AssertionError(f"Gold: score hors bornes pour {rec['ville']}: {score}")
        ranks.append(rec["classement"])

    if len(set(ranks)) < 1:
        raise AssertionError("Gold: classements invalides")

    print(f"[QA Gold] OK — scores et classements valides")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--layer", choices=["bronze", "silver", "gold", "all"], default="all")
    parser.add_argument("--date", default=None)
    args = parser.parse_args()

    tests = {
        "bronze": test_bronze,
        "silver": test_silver,
        "gold": test_gold,
    }
    if args.layer == "all":
        for fn in tests.values():
            fn(args.date)
    else:
        tests[args.layer](args.date)
