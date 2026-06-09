"""
FarmTech Solutions - Fase 1: Area Calculation & Input Management
Author: Richard Schmitz - RM567951
"""

import math
import os
import sqlite3
import pandas as pd
from datetime import datetime

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(_BASE, "data", "farmtech.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS culturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            area_m2 REAL,
            insumo_total REAL,
            unidade_insumo TEXT,
            criado_em TEXT
        )
    """)
    conn.commit()
    conn.close()


def calcular_area_cafe(comprimento: float, largura: float, doses_por_metro: float) -> dict:
    area = comprimento * largura
    fertilizante = doses_por_metro * largura * comprimento
    return {"tipo": "Café", "area_m2": round(area, 2),
            "insumo_total": round(fertilizante, 2), "unidade_insumo": "kg"}


def calcular_area_milho(raio: float, litros_por_hectare: float) -> dict:
    area = math.pi * (raio ** 2)
    defensivo = litros_por_hectare * (area / 10000)
    return {"tipo": "Milho", "area_m2": round(area, 2),
            "insumo_total": round(defensivo, 2), "unidade_insumo": "litros"}


def salvar_cultura(dados: dict):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO culturas (tipo, area_m2, insumo_total, unidade_insumo, criado_em) VALUES (?,?,?,?,?)",
        (dados["tipo"], dados["area_m2"], dados["insumo_total"],
         dados["unidade_insumo"], datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def listar_culturas() -> pd.DataFrame:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM culturas ORDER BY id DESC", conn)
    conn.close()
    return df


def atualizar_cultura(id_: int, area_m2: float, insumo_total: float):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE culturas SET area_m2=?, insumo_total=? WHERE id=?",
        (area_m2, insumo_total, id_)
    )
    conn.commit()
    conn.close()


def excluir_cultura(id_: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM culturas WHERE id=?", (id_,))
    conn.commit()
    conn.close()
