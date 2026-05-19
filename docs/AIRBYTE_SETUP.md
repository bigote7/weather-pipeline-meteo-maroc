# Configuration Airbyte — OpenWeather → MinIO (5 min)

## Liens directs

| Service | URL |
|---------|-----|
| **Airbyte** | http://localhost:8000 |
| **MinIO** | http://localhost:9001 |
| **Airflow** | http://localhost:8080 |

---

## Étape 1 — Source OpenWeather

1. http://localhost:8000 → **Sources** → **+ New source**
2. Chercher **OpenWeather** → **Set up source**
3. Remplir :

| Champ | Valeur |
|-------|--------|
| Source name | `OpenWeather_Marrakech` |
| API Key (appid) | *(votre clé dans .env)* |
| Latitude | `31.6295` |
| Longitude | `-7.9811` |
| Units | `metric` |

4. **Test connection** → **Set up source**

> Répéter pour chaque ville (nouvelle source) ou utiliser le script Python Bronze pour les 8 villes d'un coup.

---

## Étape 2 — Destination S3 / MinIO

1. **Destinations** → **+ New destination** → **S3**
2. Remplir :

| Champ | Valeur |
|-------|--------|
| Destination name | `MinIO_Bronze` |
| S3 Key ID | `minioadmin` |
| S3 Access Key | `minioadmin` |
| S3 Bucket Name | `data-pipeline` |
| S3 Bucket Path | `bronze/weather_raw` |
| S3 Bucket Region | `us-east-1` |
| S3 Endpoint | `http://host.docker.internal:9000` |

3. **Test connection** → **Set up destination**

---

## Étape 3 — Connection

1. **Connections** → **Create your first connection**
2. Source : `OpenWeather_Marrakech`
3. Destination : `MinIO_Bronze`
4. **Set up connection** → **Sync now**

---

## Vérification

MinIO → bucket `data-pipeline` → `bronze` → `weather_raw` → fichiers JSON
