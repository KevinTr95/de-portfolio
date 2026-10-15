"""Scarica i dati meteo orari di una città da Open-Meteo e li salva in un CSV."""

import argparse
import csv
import os

import requests

API_URL = "https://api.open-meteo.com/v1/forecast"

# Città disponibili, con latitudine e longitudine
CITIES = {
    "Milano": (45.46, 9.19),
    "Lugano": (46.00, 8.95),
    "Zurigo": (47.37, 8.54),
}

# Cartella di destinazione: si può cambiare con una variabile d'ambiente
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "data")


def fetch_weather(city: str) -> list[dict]:
    """Chiede all'API le temperature e le precipitazioni orarie di ieri e oggi."""
    latitude, longitude = CITIES[city]
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation",
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "Europe/Rome",
    }
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()  # se l'API risponde con un errore, lo script si ferma
    hourly = response.json()["hourly"]

    return [
        {
            "city": city,
            "observed_at": time,
            "temperature_c": temperature,
            "precipitation_mm": precipitation,
        }
        for time, temperature, precipitation in zip(
            hourly["time"], hourly["temperature_2m"], hourly["precipitation"]
        )
    ]


def write_csv(rows: list[dict], city: str) -> str:
    """Scrive le righe in un CSV e restituisce il percorso del file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"weather_{city.lower()}.csv")
    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingestion dei dati meteo")
    parser.add_argument("--city", default="Milano", choices=list(CITIES))
    args = parser.parse_args()

    rows = fetch_weather(args.city)
    path = write_csv(rows, args.city)
    print(f"Salvate {len(rows)} righe in {path}")


if __name__ == "__main__":
    main()