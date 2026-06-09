"""
FarmTech Solutions - Fase 3: IoT Database (SQLite — Oracle-compatible schema)
Author: Richard Schmitz - RM567951
"""

import sqlite3
import os
import pandas as pd
from datetime import datetime
import random

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(_BASE, "data", "farmtech.db")
_CSV_PATH = os.path.join(_BASE, "data", "dados_sensores.csv")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sensores_soja (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            umidade_solo REAL,
            ph_solo REAL,
            nitrogenio INTEGER,
            fosforo INTEGER,
            potassio INTEGER,
            temperatura REAL,
            chuva_mm REAL,
            irrigacao_ativa INTEGER
        )
    """)
    conn.commit()

    # Seed with CSV data if table is empty
    cur = conn.execute("SELECT COUNT(*) FROM sensores_soja")
    if cur.fetchone()[0] == 0:
        try:
            df = pd.read_csv(_CSV_PATH)
            df.to_sql("sensores_soja", conn, if_exists="append", index=False)
        except Exception:
            _seed_demo_data(conn)
    conn.close()


def _seed_demo_data(conn):
    base = datetime(2025, 10, 1, 8, 0)
    for i in range(15):
        ts = base.replace(hour=8 + i)
        umidade = round(random.uniform(40, 85), 2)
        ph = round(random.uniform(5.8, 7.0), 1)
        n, p, k = random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)
        temp = round(random.uniform(18, 35), 1)
        chuva = round(random.uniform(0, 5), 1)
        irrig = 1 if umidade < 60 and chuva < 1 else 0
        conn.execute(
            "INSERT INTO sensores_soja (timestamp,umidade_solo,ph_solo,nitrogenio,fosforo,"
            "potassio,temperatura,chuva_mm,irrigacao_ativa) VALUES (?,?,?,?,?,?,?,?,?)",
            (ts.isoformat(), umidade, ph, n, p, k, temp, chuva, irrig),
        )
    conn.commit()


def insert_reading(umidade: float, ph: float, nitrogenio: int, fosforo: int,
                   potassio: int, temperatura: float, chuva_mm: float, irrigacao: int):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO sensores_soja (timestamp,umidade_solo,ph_solo,nitrogenio,fosforo,"
        "potassio,temperatura,chuva_mm,irrigacao_ativa) VALUES (?,?,?,?,?,?,?,?,?)",
        (datetime.now().isoformat(), umidade, ph, nitrogenio, fosforo,
         potassio, temperatura, chuva_mm, irrigacao),
    )
    conn.commit()
    conn.close()


def get_all_readings() -> pd.DataFrame:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sensores_soja ORDER BY timestamp DESC", conn)
    conn.close()
    return df


def get_summary() -> dict:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("""
        SELECT COUNT(*) total, SUM(irrigacao_ativa) irrigacoes,
               ROUND(AVG(umidade_solo),2) umid_media,
               ROUND(AVG(ph_solo),2) ph_medio,
               ROUND(AVG(temperatura),2) temp_media
        FROM sensores_soja
    """).fetchone()
    conn.close()
    return {"total": row[0], "irrigacoes": row[1], "umidade_media": row[2],
            "ph_medio": row[3], "temperatura_media": row[4]}


def delete_reading(id_: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM sensores_soja WHERE id=?", (id_,))
    conn.commit()
    conn.close()


def get_critical_conditions() -> pd.DataFrame:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM sensores_soja WHERE umidade_solo < 50 AND irrigacao_ativa=1 ORDER BY timestamp",
        conn,
    )
    conn.close()
    return df
