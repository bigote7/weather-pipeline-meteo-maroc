# Pipeline météo Maroc — 4IASDG2

**Module :** Architecture des données — **EMSI** — 2025/2026  
**Architecture :** Medallion (Bronze → Silver → Gold) + Airflow + Power BI  
**Villes :** Casablanca, Rabat, Marrakech, Fès, Tanger, Agadir, Meknès, Oujda

---

## Structure du projet

```
weather_project/
│
├── config/                 # Configuration (MinIO, villes, API)
│   ├── settings.py
│   └── minio_client.py
│
├── scripts/                # Pipeline Python
│   ├── bronze_ingestion.py # Partie 1 — Ingestion API
│   ├── silver_transform.py # Partie 2 — Nettoyage
│   ├── gold_enrich.py      # Partie 3 — KPI + classement
│   ├── data_quality.py     # Partie 4 — Tests qualité
│   └── run_pipeline.py     # Exécution complète
│
├── dags/                   # Partie 5 — Airflow
│   └── weather_morocco_pipeline.py
│
├── powerbi/                # Partie 6 — Reporting
│   └── weather_analytics.json
│
├── docs/                   # Documentation
│   ├── AIRBYTE_SETUP.md
│   ├── POWER_BI.md
│   ├── QUALITE_DONNEES.md
│   └── LIENS.md
│
├── captures/               # Captures d'écran (rapport)
│   ├── minio/
│   ├── airflow/
│   └── powerbi/
│
├── rapport/                # Rapport LaTeX / PDF
│
├── infra/                  # Docker
│   └── docker-compose.yml  # Airflow
│
├── .env.example            # Modèle de configuration
├── requirements.txt
└── start.ps1               # Démarrage rapide
```

---

## Démarrage rapide

### 1. Configuration

```powershell
cd "C:\Users\HP\Desktop\4IIR7\Decisionel POWER BI\weather_project"
copy .env.example .env
# Éditer .env : OPENWEATHER_API_KEY=...
```

### 2. Python

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. MinIO (déjà installé chez vous)

```powershell
docker start minio
```

→ http://localhost:9001 — bucket `data-pipeline`

### 4. Pipeline complet

```powershell
python scripts/run_pipeline.py
```

### 5. Airflow

```powershell
docker compose -f infra/docker-compose.yml up -d
```

→ http://localhost:8080 — DAG `weather_morocco_pipeline` — **Trigger DAG**

### 6. Power BI

Fichier : `powerbi/weather_analytics.json`  
Voir `docs/POWER_BI.md`

---

## Chemins MinIO (bucket `data-pipeline`)

| Couche | Chemin |
|--------|--------|
| Bronze | `bronze/weather_raw/YYYY-MM-DD/<ville>.json` |
| Silver | `silver/weather_clean/YYYY-MM-DD/weather_clean.json` |
| Gold | `gold/weather_analytics/YYYY-MM-DD/weather_analytics.json` |

---

## Documentation

| Fichier | Contenu |
|---------|---------|
| [docs/AIRBYTE_SETUP.md](docs/AIRBYTE_SETUP.md) | Configuration Airbyte |
| [docs/POWER_BI.md](docs/POWER_BI.md) | Dashboard Power BI |
| [docs/QUALITE_DONNEES.md](docs/QUALITE_DONNEES.md) | Tests qualité (soutenance) |
| [docs/LIENS.md](docs/LIENS.md) | URLs et logins |

---



  Labib Layachi — **4IASDG1** — EMSI
