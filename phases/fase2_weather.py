"""
FarmTech Solutions - Fase 2: Weather API Integration
Author: Richard Schmitz - RM567951
"""

import random
import requests
from datetime import datetime, timedelta


class WeatherService:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.cidade = "Sao Paulo,BR"

    def get_current(self) -> dict:
        if self.api_key and self.api_key not in ("", "SUA_CHAVE_API_AQUI"):
            try:
                r = requests.get(
                    f"{self.base_url}/weather",
                    params={"q": self.cidade, "appid": self.api_key,
                            "units": "metric", "lang": "pt_br"},
                    timeout=8,
                )
                if r.status_code == 200:
                    d = r.json()
                    return {
                        "temperatura": d["main"]["temp"],
                        "umidade": d["main"]["humidity"],
                        "pressao": d["main"]["pressure"],
                        "descricao": d["weather"][0]["description"],
                        "chuva": d.get("rain", {}).get("1h", 0),
                        "vento": d["wind"]["speed"],
                        "timestamp": datetime.now().isoformat(),
                        "fonte": "OpenWeather API",
                    }
            except Exception:
                pass
        return self._simulated()

    def get_forecast(self) -> list:
        if self.api_key and self.api_key not in ("", "SUA_CHAVE_API_AQUI"):
            try:
                r = requests.get(
                    f"{self.base_url}/forecast",
                    params={"q": self.cidade, "appid": self.api_key,
                            "units": "metric", "lang": "pt_br"},
                    timeout=8,
                )
                if r.status_code == 200:
                    return [
                        {
                            "datetime": i["dt_txt"],
                            "temperatura": i["main"]["temp"],
                            "umidade": i["main"]["humidity"],
                            "chuva": i.get("rain", {}).get("3h", 0),
                            "descricao": i["weather"][0]["description"],
                        }
                        for i in r.json()["list"][:8]
                    ]
            except Exception:
                pass
        return self._simulated_forecast()

    def irrigation_recommendation(self, current: dict, forecast: list) -> dict:
        chuva_atual = current.get("chuva", 0)
        chuva_prevista = sum(f.get("chuva", 0) for f in forecast[:2])
        if chuva_atual > 1:
            return {"irrigar": False, "motivo": "Chovendo atualmente",
                    "chuva_atual": chuva_atual, "chuva_prevista": chuva_prevista}
        if chuva_prevista > 3:
            return {"irrigar": False, "motivo": "Chuva prevista nas próximas horas",
                    "chuva_atual": chuva_atual, "chuva_prevista": chuva_prevista}
        if current.get("umidade", 0) > 85:
            return {"irrigar": False, "motivo": "Umidade do ar muito alta",
                    "chuva_atual": chuva_atual, "chuva_prevista": chuva_prevista}
        return {"irrigar": True, "motivo": "Condições normais — irrigação recomendada",
                "chuva_atual": chuva_atual, "chuva_prevista": chuva_prevista}

    def _simulated(self) -> dict:
        return {
            "temperatura": round(random.uniform(18, 32), 1),
            "umidade": round(random.uniform(40, 90), 1),
            "pressao": round(random.uniform(1010, 1025), 1),
            "descricao": random.choice(["céu limpo", "nublado", "chuva leve"]),
            "chuva": round(random.uniform(0, 5), 1),
            "vento": round(random.uniform(2, 15), 1),
            "timestamp": datetime.now().isoformat(),
            "fonte": "Dados Simulados",
        }

    def _simulated_forecast(self) -> list:
        return [
            {
                "datetime": (datetime.now() + timedelta(hours=i * 3)).strftime("%Y-%m-%d %H:%M:%S"),
                "temperatura": round(random.uniform(18, 32), 1),
                "umidade": round(random.uniform(40, 90), 1),
                "chuva": round(random.uniform(0, 8), 1),
                "descricao": random.choice(["céu limpo", "nublado", "chuva leve"]),
            }
            for i in range(8)
        ]
