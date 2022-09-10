"""
este script mantiene el CSV trabajos_epec.csv con la info nueva que encuentre en el sitio de EPEC
"""

import csv
from pathlib import Path

import requests


def strip(row):
    """strip the values of a dict"""
    return {k: v.strip() for k,v in row.items()}


target = Path("trabajos_epec.csv")
try:
    with target.open() as file:
        rows = [row for row in csv.DictReader(file)]
    ids = [r["id"] for r in rows]
except FileNotFoundError:
    rows = []
    ids = []

data = requests.post(
    "https://www.epec.com.ar/api/mantenimiento/trabajos-mejora",
    headers={"apiKey": "web-prod"},
    json={"trabajoId": None},
).json()["trabajos"]

rows += [strip(r) for r in data if r["id"] not in ids]

with target.open("w") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=['id', 'fecha', 'horaDesde', 'horaHasta', 'zona', 'zonaResumida', 'localidad', 'motivo', 'motivoExplicacion', 'motivoResumido']
    )
    writer.writeheader()
    writer.writerows(rows)
