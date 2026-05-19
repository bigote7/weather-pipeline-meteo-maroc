import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "data-pipeline")

# 8 villes marocaines (nom API OpenWeatherMap)
CITIES = [
    {"ville": "Casablanca", "api_name": "Casablanca,MA"},
    {"ville": "Rabat", "api_name": "Rabat,MA"},
    {"ville": "Marrakech", "api_name": "Marrakech,MA"},
    {"ville": "Fes", "api_name": "Fes,MA"},
    {"ville": "Tanger", "api_name": "Tangier,MA"},
    {"ville": "Agadir", "api_name": "Agadir,MA"},
    {"ville": "Meknes", "api_name": "Meknes,MA"},
    {"ville": "Oujda", "api_name": "Oujda,MA"},
]

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
