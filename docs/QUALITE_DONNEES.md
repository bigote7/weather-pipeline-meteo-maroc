# Partie 4 — Qualité des données

## Objectif

Garantir la fiabilité des données à chaque couche du pipeline Medallion.

## Tests (`scripts/data_quality.py`)

| Couche | Test | Critères |
|--------|------|----------|
| Bronze | `test_bronze` | 8 fichiers JSON dans `bronze/weather_raw/` |
| Silver | `test_silver` | 8 enregistrements, colonnes obligatoires, types, humidité 0–100 |
| Gold | `test_gold` | 8 villes, score 0–100, classement présent |

## Intégration Airflow

```
ingestion_bronze → test_bronze → transform_silver → test_silver → enrich_gold → test_gold
```

## Commandes

```powershell
python scripts/data_quality.py --layer all
```
