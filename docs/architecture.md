# Arquitetura — FarmTech Solutions Fase 7

## Diagrama de alto nível

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      USUÁRIO (gestor / funcionário da fazenda)              │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │ HTTP (browser)
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                  DASHBOARD STREAMLIT — app.py (porta 8501)                  │
│  ┌────────────┐ ┌──────────┐ ┌──────────┐ ┌──────┐ ┌────────┐ ┌──────────┐  │
│  │  Visão     │ │  Fase 1  │ │  Fase 2  │ │ F3  │ │  F4    │ │   F6     │  │
│  │  geral     │ │  Área    │ │  Clima   │ │ DB  │ │  ML    │ │  Visão   │  │
│  └────────────┘ └──────────┘ └──────────┘ └──────┘ └────────┘ └──────────┘  │
│                       ┌────────────────┐  ┌─────────────────┐               │
│                       │  F5 — AWS SNS  │  │ Ir Além — Rek.  │               │
│                       └────────────────┘  └─────────────────┘               │
└──────┬──────────┬──────────┬───────────┬──────────┬──────────┬──────────────┘
       │          │          │           │          │          │
       ▼          ▼          ▼           ▼          ▼          ▼
┌──────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ ┌────────┐ ┌──────────────┐
│ phases/  │ │ phases/ │ │ phases/ │ │phases/ │ │phases/ │ │ rekognition/ │
│ fase1    │ │ fase2   │ │ fase3   │ │fase4_ml│ │fase6   │ │ aws_         │
│ _area    │ │ _weather│ │ _database│ │ .py    │ │_vision │ │ rekognition  │
└──────────┘ └─────────┘ └─────────┘ └────────┘ └────────┘ └──────────────┘
     │           │            │           │           │           │
     ▼           ▼            ▼           ▼           ▼           ▼
┌──────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐
│ SQLite   │ │ OpenWthr│ │ SQLite  │ │  .pkl  │ │ YOLOv5  │ │   AWS    │
│ (cultura)│ │   API   │ │(sensors)│ │ (sklrn)│ │ +Pillow │ │Rekognition│
└──────────┘ └─────────┘ └─────────┘ └────────┘ └─────────┘ └────┬─────┘
                                                                  │
                                                                  ▼
                                                          ┌──────────────┐
                                                          │   AWS SNS    │
                                                          │  (Email/SMS) │
                                                          └──────┬───────┘
                                                                 │
                                                                 ▼
                                                       Funcionários da fazenda
```

## Fluxo de dados crítico (alerta de irrigação)

```
1. Sensor IoT (ESP32 simulado / dados sintéticos)
        │
        ▼
2. Insert em data/farmtech.db (tabela sensores_soja)
        │
        ▼
3. Modelo ML carregado (modelo_irrigacao.pkl)
        │
        ▼
4. Predição → score >= 0.5?
        │
   ┌────┴────┐
   │         │
 sim         não
   │         │
   ▼         ▼
SNS publish  log somente
   │
   ▼
Email + SMS aos funcionários
   │
   ▼
Funcionário recebe ação recomendada:
"Ativar bomba de irrigação no setor X"
```

## Decisões técnicas

### Por que SQLite em vez do Oracle FIAP?

A Fase 3 original usava `oracle.fiap.com.br:1521`. Este servidor é instável e fora do controle do aluno. Replicamos o **mesmo schema** em SQLite, garantindo:

- Funcionamento 100% offline
- Sem dependências externas para o avaliador rodar o projeto
- Mesmas queries SQL funcionam (sintaxe ANSI)

### Por que fallback simulado na API OpenWeather?

A chave da API expira e nem todos os avaliadores terão uma. O módulo `fase2_weather.py` detecta automaticamente a ausência de chave e gera **dados realistas** (temperaturas seguindo ciclo diário, umidade correlacionada com chuva). Isso permite demonstrar a integração sem dependência externa.

### Por que YOLOv5 com fallback?

`torch` é pesado (>1 GB). Se o avaliador não quiser instalar PyTorch, o módulo `fase6_vision.py` simula detecções **baseadas no nome do arquivo** (`car_*.jpg` → detecta carro). Isso mantém o fluxo completo da UI funcionando.

### Por que Random Forest para irrigação?

A decisão de irrigar é fortemente regrada (boolean determinístico):

```python
irrigar = umidade < 60 AND chuva < 1 AND 6.0 <= pH <= 6.8 AND NPK >= 2
```

Random Forest captura essas interações não-lineares melhor que regressão linear. Esperamos R² > 0.95 após treino com 300 amostras.

## Stack tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Frontend (dashboard) | Streamlit + Plotly |
| Backend / lógica | Python 3.10+ |
| ML | scikit-learn + joblib |
| Visão computacional | YOLOv5 (PyTorch) com fallback |
| Banco de dados | SQLite (file-based) |
| Mensageria | AWS SNS via boto3 |
| Reconhecimento em nuvem | AWS Rekognition (Ir Além) |
| Dados sintéticos | random.seed(42) para reprodutibilidade |

## Próximos passos sugeridos

- Substituir SQLite por PostgreSQL gerenciado (RDS) quando em produção
- Adicionar autenticação (Streamlit Auth ou Cognito)
- Treinar modelo YOLOv5 customizado para detecção de pragas (não só veículos)
- Implementar o algoritmo genético do "Ir Além Opção 2" para otimização de insumos
