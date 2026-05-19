# Scripts du pipeline

| Script | Partie | Rôle |
|--------|--------|------|
| `bronze_ingestion.py` | 1 | API OpenWeather → MinIO (Bronze) |
| `silver_transform.py` | 2 | Nettoyage JSON → Silver |
| `gold_enrich.py` | 3 | Score météo + classement → Gold |
| `data_quality.py` | 4 | Tests Bronze / Silver / Gold |
| `run_pipeline.py` | — | Enchaîne tout le pipeline |

```powershell
python scripts/run_pipeline.py
python scripts/data_quality.py --layer all
```
