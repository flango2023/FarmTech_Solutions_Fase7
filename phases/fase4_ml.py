"""
FarmTech Solutions - Fase 4: ML Pipeline (self-contained)
Author: Richard Schmitz - RM567951
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(_BASE, "data", "dados_treinamento.csv")
MODELS_DIR = os.path.join(_BASE, "models")


def _load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hora"] = df["timestamp"].dt.hour
    df["nutrientes_total"] = df["nitrogenio"] + df["fosforo"] + df["potassio"]
    df["deficit_umidade"] = np.maximum(0, 60 - df["umidade_solo"])
    df["ph_ideal"] = ((df["ph_solo"] >= 6.0) & (df["ph_solo"] <= 6.8)).astype(int)
    df["temp_stress"] = (df["temperatura"] > 30).astype(int)
    return df


def train_all() -> dict:
    os.makedirs(MODELS_DIR, exist_ok=True)
    df = _load_data()
    results = {}

    # --- Umidade (Linear) ---
    X, y = df[["temperatura", "chuva_mm", "hora", "nutrientes_total"]], df["umidade_solo"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)
    sc = StandardScaler(); Xtr_s = sc.fit_transform(Xtr); Xte_s = sc.transform(Xte)
    m = LinearRegression().fit(Xtr_s, ytr)
    yp = m.predict(Xte_s)
    results["umidade"] = {"mae": mean_absolute_error(yte, yp), "r2": r2_score(yte, yp),
                          "rmse": float(np.sqrt(mean_squared_error(yte, yp)))}
    joblib.dump(m, f"{MODELS_DIR}/modelo_umidade.pkl")
    joblib.dump(sc, f"{MODELS_DIR}/scaler_umidade.pkl")

    # --- pH (Linear) ---
    X, y = df[["nitrogenio", "fosforo", "potassio", "temperatura"]], df["ph_solo"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)
    sc = StandardScaler(); Xtr_s = sc.fit_transform(Xtr); Xte_s = sc.transform(Xte)
    m = LinearRegression().fit(Xtr_s, ytr)
    yp = m.predict(Xte_s)
    results["ph"] = {"mae": mean_absolute_error(yte, yp), "r2": r2_score(yte, yp),
                     "rmse": float(np.sqrt(mean_squared_error(yte, yp)))}
    joblib.dump(m, f"{MODELS_DIR}/modelo_ph.pkl")
    joblib.dump(sc, f"{MODELS_DIR}/scaler_ph.pkl")

    # --- Irrigação (Random Forest) ---
    X = df[["umidade_solo", "ph_solo", "temperatura", "chuva_mm", "nutrientes_total"]]
    y = df["irrigacao_ativa"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)
    sc = StandardScaler(); Xtr_s = sc.fit_transform(Xtr); Xte_s = sc.transform(Xte)
    m = RandomForestRegressor(n_estimators=100, random_state=42).fit(Xtr_s, ytr)
    yp = m.predict(Xte_s)
    results["irrigacao"] = {"mae": mean_absolute_error(yte, yp), "r2": r2_score(yte, yp),
                            "rmse": float(np.sqrt(mean_squared_error(yte, yp)))}
    joblib.dump(m, f"{MODELS_DIR}/modelo_irrigacao.pkl")
    joblib.dump(sc, f"{MODELS_DIR}/scaler_irrigacao.pkl")

    # --- Rendimento (Gradient Boosting) ---
    df["rendimento"] = (df["umidade_solo"] / 100 * 0.3 + df["ph_ideal"] * 0.2
                        + df["nutrientes_total"] / 3 * 0.3 + (1 - df["temp_stress"]) * 0.2) * 100
    X = df[["umidade_solo", "ph_solo", "temperatura", "nutrientes_total", "chuva_mm"]]
    y = df["rendimento"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)
    m = GradientBoostingRegressor(n_estimators=100, random_state=42).fit(Xtr, ytr)
    yp = m.predict(Xte)
    results["rendimento"] = {"mae": mean_absolute_error(yte, yp), "r2": r2_score(yte, yp),
                             "rmse": float(np.sqrt(mean_squared_error(yte, yp)))}
    joblib.dump(m, f"{MODELS_DIR}/modelo_rendimento.pkl")

    with open(f"{MODELS_DIR}/metricas.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


def load_models() -> dict:
    models = {}
    for name in ["umidade", "ph", "irrigacao"]:
        mp = f"{MODELS_DIR}/modelo_{name}.pkl"
        sp = f"{MODELS_DIR}/scaler_{name}.pkl"
        if os.path.exists(mp) and os.path.exists(sp):
            models[name] = {"model": joblib.load(mp), "scaler": joblib.load(sp)}
    rp = f"{MODELS_DIR}/modelo_rendimento.pkl"
    if os.path.exists(rp):
        models["rendimento"] = {"model": joblib.load(rp), "scaler": None}
    return models


def predict(models: dict, name: str, features: list) -> float:
    if name not in models:
        return 0.0
    entry = models[name]
    x = np.array(features).reshape(1, -1)
    if entry["scaler"]:
        x = entry["scaler"].transform(x)
    return float(entry["model"].predict(x)[0])


def get_metrics() -> dict:
    mp = f"{MODELS_DIR}/metricas.json"
    if os.path.exists(mp):
        with open(mp) as f:
            return json.load(f)
    return {}


def analyze_conditions(umidade: float, ph: float, n: int, p: int, k: int, temp: float) -> dict:
    alertas = []
    if umidade < 60:
        alertas.append(f"⚠️ Umidade baixa ({umidade}%) — Irrigação necessária")
    elif umidade > 80:
        alertas.append(f"⚠️ Umidade alta ({umidade}%) — Risco de encharcamento")
    if not (6.0 <= ph <= 6.8):
        alertas.append(f"⚠️ pH inadequado ({ph}) — Faixa ideal: 6.0–6.8")
    if n + p + k < 2:
        alertas.append(f"⚠️ Nutrientes insuficientes ({n+p+k}/3 disponíveis)")
    if temp > 30:
        alertas.append(f"⚠️ Temperatura elevada ({temp}°C) — Stress térmico")
    return {"alertas": alertas, "status": "atencao" if alertas else "normal"}
