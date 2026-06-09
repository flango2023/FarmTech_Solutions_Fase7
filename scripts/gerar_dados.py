"""
FarmTech Solutions - Gerador de dataset sintetico expandido
Author: Richard Schmitz - RM567951

Cria 300 linhas de leituras de sensores correlacionadas, salva em
data/dados_treinamento.csv e em data/dados_sensores.csv (mesma estrutura).
Reproducao garantida via random.seed.
"""

import os
import csv
import random
import math
from datetime import datetime, timedelta

ROWS = 300
START = datetime(2025, 10, 1, 0, 0)
SEED = 42

OUT_TREINO = "data/dados_treinamento.csv"
OUT_SENSOR = "data/dados_sensores.csv"


def gerar_linha(i: int) -> dict:
    ts = START + timedelta(hours=i)
    hora = ts.hour

    # Ciclo diario de temperatura
    temp = 22 + 8 * math.sin((hora - 6) / 24 * 2 * math.pi) + random.uniform(-2, 2)
    temp = round(max(15, min(38, temp)), 1)

    # Chuva ocasional (10% das horas)
    chuva = round(random.uniform(2, 15), 1) if random.random() < 0.10 else 0.0

    # Umidade do solo correlacionada com chuva e temperatura
    base_umidade = 65 + (chuva * 1.5) - (temp - 22) * 0.8
    umidade = round(max(20, min(95, base_umidade + random.uniform(-8, 8))), 1)

    # pH com leve variacao em torno de 6.4 (ideal soja)
    ph = round(max(5.0, min(7.5, 6.4 + random.uniform(-0.6, 0.6))), 1)

    # Nutrientes NPK (probabilidade independente)
    n = 1 if random.random() < 0.75 else 0
    p = 1 if random.random() < 0.65 else 0
    k = 1 if random.random() < 0.70 else 0

    # Logica determinstica de irrigacao (target previsivel para o RF)
    nutrientes = n + p + k
    irrigar = int(umidade < 60 and chuva < 1 and 6.0 <= ph <= 6.8 and nutrientes >= 2)

    return {
        "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "umidade_solo": umidade,
        "ph_solo": ph,
        "nitrogenio": n,
        "fosforo": p,
        "potassio": k,
        "temperatura": temp,
        "chuva_mm": chuva,
        "irrigacao_ativa": irrigar,
    }


def salvar(path: str, linhas: list):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        writer.writeheader()
        writer.writerows(linhas)


def main():
    random.seed(SEED)
    linhas = [gerar_linha(i) for i in range(ROWS)]
    salvar(OUT_TREINO, linhas)
    salvar(OUT_SENSOR, linhas)
    irrigacoes = sum(l["irrigacao_ativa"] for l in linhas)
    print(f"Gerado: {ROWS} linhas em {OUT_TREINO} e {OUT_SENSOR}")
    print(f"  Irrigacoes ativadas: {irrigacoes}/{ROWS} ({irrigacoes/ROWS*100:.1f}%)")
    print(f"  Umidade media: {sum(l['umidade_solo'] for l in linhas)/ROWS:.1f}%")
    print(f"  pH medio: {sum(l['ph_solo'] for l in linhas)/ROWS:.2f}")


if __name__ == "__main__":
    main()
