"""Exécute le pipeline complet Bronze -> Gold + tests qualité."""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from bronze_ingestion import ingest_bronze
from data_quality import test_bronze, test_gold, test_silver
from gold_enrich import enrich_gold
from silver_transform import transform_silver


def run_full_pipeline(run_date: str | None = None) -> None:
    run_date = run_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"=== Pipeline météo Maroc — {run_date} ===\n")

    ingest_bronze(run_date)
    test_bronze(run_date)

    transform_silver(run_date)
    test_silver(run_date)

    enrich_gold(run_date)
    test_gold(run_date)

    print("\n=== Pipeline terminé avec succès ===")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=None)
    args = parser.parse_args()
    run_full_pipeline(args.date)
