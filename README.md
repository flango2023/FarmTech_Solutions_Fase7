# FIAP — Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="https://raw.githubusercontent.com/flango2023/TEMPLATE-TIAO-2026/main/assets/logo-fiap.png"
         alt="FIAP" border="0" width="40%" height="40%">
  </a>
</p>

<br>

<h2 align="center">🌾 FarmTech Solutions — Fase 7: A Consolidação de um Sistema</h2>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=flat&logo=scikit-learn&logoColor=white">
  <img src="https://img.shields.io/badge/AWS_SNS-Configurado-FF9900?style=flat&logo=amazonaws&logoColor=white">
  <img src="https://img.shields.io/badge/YOLOv5-v7.0-00FFFF?style=flat">
  <img src="https://img.shields.io/badge/SQLite-3.x-003B57?style=flat&logo=sqlite&logoColor=white">
</p>

<p align="center">
  <strong>Autor:</strong> Richard Schmitz &nbsp;|&nbsp; <strong>RM:</strong> 567951<br>
  <strong>Disciplina:</strong> Inteligência Artificial — FIAP &nbsp;|&nbsp; <strong>Fase:</strong> 7 — A Consolidação de um Sistema
</p>

---

## 🎥 Vídeo demonstrativo

> 🎬 **[Demonstração completa — Fase 7 (até 10 min)](https://youtu.be/COLE_AQUI_O_LINK)**
> _Postado no YouTube como "não listado". Demonstra todas as fases integradas na dashboard._
>
> 🎬 **["Ir Além" — AWS Rekognition (até 5 min)](https://youtu.be/COLE_AQUI_O_LINK_IR_ALEM)**
> _Demonstração do reconhecimento de imagens em nuvem via Amazon Rekognition._

---

## 📋 Sobre o projeto

A **Fase 7** consolida em um **único projeto Python** todos os serviços desenvolvidos ao longo das Fases 1 a 6, integrando-os em uma **dashboard Streamlit unificada** acessível por qualquer gestor agrícola via `http://localhost:8501`.

Cada fase aparece como uma página no menu lateral. Além da consolidação, esta entrega inclui:

- 🔔 **Serviço de mensageria AWS SNS** — dispara alertas por e-mail e SMS aos funcionários quando sensores detectam condições críticas (umidade, pH, temperatura, NPK) ou quando a visão computacional identifica objetos não autorizados.
- 🚀 **"Ir Além" — AWS Rekognition** — reconhecimento de imagens em nuvem complementar ao YOLOv5 local, com ações sugeridas e disparo automático de alertas via SNS.

---

## 🛠️ Stack Tecnológica

### 🌐 Linguagem & Frameworks
| Tecnologia | Versão | Uso no Projeto |
|-----------|--------|----------------|
| **Python** | `3.10+` | Linguagem principal — todos os módulos do sistema |
| **Streamlit** | `1.32+` | Dashboard interativa multi-página (8 páginas) |
| **boto3** | `1.34+` | SDK AWS — integração com SNS e Rekognition |

### 🖥️ Visualização & Frontend
| Tecnologia | Versão | Uso no Projeto |
|-----------|--------|----------------|
| **Plotly** | `5.18+` | Gráficos interativos de séries temporais e métricas |
| **Pandas** | `2.0+` | Manipulação de dados tabulares e exibição de tabelas |
| **NumPy** | `1.24+` | Operações numéricas e geração de dados sintéticos |

### 🤖 Machine Learning
| Tecnologia | Versão | Uso no Projeto |
|-----------|--------|----------------|
| **scikit-learn** | `1.3+` | Linear Regression, Random Forest, Gradient Boosting, StandardScaler |
| **joblib** | `1.3+` | Serialização e carregamento dos modelos `.pkl` |

### 👁️ Visão Computacional
| Tecnologia | Detalhe | Uso no Projeto |
|-----------|---------|----------------|
| **YOLOv5** | `v7.0` | Detecção de objetos (carros e drones) em imagens |
| **PyTorch** | `hub.load` | Carregamento do modelo YOLOv5 pré-treinado |
| **Pillow** | `10.0+` | Processamento e exibição de imagens na dashboard |

### ☁️ Cloud AWS
| Serviço | Uso no Projeto |
|---------|----------------|
| **Amazon SNS** | Mensageria — publica alertas para e-mail e SMS dos funcionários |
| **Amazon Rekognition** | DetectLabels API — análise de imagens em nuvem ("Ir Além") |
| **IAM** | Usuário `richard-adm` com políticas `sns:Publish` e `rekognition:DetectLabels` |

### 🗄️ Dados & Banco de Dados
| Tecnologia | Detalhe | Uso no Projeto |
|-----------|---------|----------------|
| **SQLite** | `3.x` | Banco local com schema idêntico ao Oracle das fases anteriores |
| **CSV** | `dados_sensores.csv` | 300 leituras históricas de sensores IoT (seed=42) |
| **JSON** | `metricas.json` | Armazenamento das métricas de avaliação dos modelos ML |

### 🔧 Ferramentas de Desenvolvimento
| Ferramenta | Uso |
|-----------|-----|
| **VS Code** | Editor de código principal |
| **Claude Code (Anthropic)** | Assistente de desenvolvimento com IA |
| **Git + GitHub** | Controle de versão e repositório remoto |
| **Python 3.10** | Linguagem principal do projeto |
| **macOS Terminal** | Execução e testes locais |

### 📐 Padrões e Boas Práticas
| Prática | Implementação |
|---------|--------------|
| **Reprodutibilidade** | `random.seed(42)` — dataset e modelos idênticos em qualquer ambiente |
| **Fallback gracioso** | YOLOv5 → simulação por nome; OpenWeather → dados sintéticos realistas |
| **Arquitetura modular** | Módulos independentes por fase: `phases/`, `alerts/`, `rekognition/` |
| **Schema Oracle-compatível** | SQLite com mesmas colunas do Oracle — migração futura sem reescrita de SQL |
| **Gitignore** | `.venv/`, `farmtech.db`, `uploaded/`, `.env` excluídos do repositório |

### 🖼️ Créditos das Imagens de Teste
| Arquivo | Fonte | Uso no Projeto |
|---------|-------|----------------|
| `car_037–040.jpg` | Dataset público de veículos | Demo de detecção de carro (Fase 6 — YOLOv5) |
| `drone_037–040.jpg` | Dataset público de drones | Demo de detecção de drone (Fase 6 — YOLOv5) |
| `pexels-photo-724921.jpg` | [Pexels](https://www.pexels.com) — licença gratuita | Imagem de teste para AWS Rekognition ("Ir Além") |

---

## 🗂️ Estrutura do repositório

```
FarmTech-Solutions-Fase7/
├── app.py                          ← Dashboard Streamlit unificada (entry point)
├── requirements.txt                ← Dependências Python
├── README.md
├── .gitignore
│
├── phases/                         ← Um módulo por fase
│   ├── __init__.py
│   ├── fase1_area_calc.py         ← Cálculo de área + CRUD em SQLite
│   ├── fase2_weather.py           ← API meteorológica OpenWeather (com fallback)
│   ├── fase3_database.py          ← Banco IoT — schema Oracle em SQLite
│   ├── fase4_ml.py                ← Pipeline de Machine Learning (4 modelos)
│   └── fase6_vision.py            ← Visão computacional YOLOv5
│
├── alerts/                         ← Fase 5 — Mensageria AWS
│   ├── __init__.py
│   └── sns_alerts.py              ← Integração AWS SNS (e-mail + SMS)
│
├── rekognition/                    ← "Ir Além" — AWS Rekognition
│   ├── __init__.py
│   └── aws_rekognition.py
│
├── scripts/
│   └── gerar_dados.py             ← Gerador reprodutível de dataset (seed=42)
│
├── data/
│   ├── dados_sensores.csv         ← 300 leituras de sensores IoT
│   ├── dados_treinamento.csv      ← Dataset para treinamento ML
│   └── farmtech.db                ← SQLite criado em runtime
│
├── dataset/images/test/           ← Imagens de teste para Fase 6 (car, drone)
│
├── models/                         ← Modelos ML treinados + scalers (.pkl)
│   ├── modelo_irrigacao.pkl       ← Random Forest  — R² 0.930
│   ├── modelo_rendimento.pkl      ← Gradient Boosting — R² 0.977
│   ├── modelo_umidade.pkl         ← Linear Regression — R² 0.573
│   ├── modelo_ph.pkl              ← Linear Regression — R² -0.069
│   ├── scaler_*.pkl
│   └── metricas.json
│
├── screenshots/                    ← Capturas do sistema em funcionamento
└── docs/
    └── architecture.md             ← Diagrama de arquitetura + decisões técnicas
```

---

## 🚀 Como executar

### Pré-requisitos

- Python 3.10 ou superior
- (Opcional) Credenciais AWS configuradas via `aws configure` — necessário para SNS e Rekognition
- (Opcional) Chave de API [OpenWeather](https://openweathermap.org/api) — sem ela, o sistema usa dados simulados realistas

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/flango2023/FarmTech_Solutions_Fase7.git
cd FarmTech_Solutions_Fase7

# 2. Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Gere o dataset sintético (apenas na primeira execução)
python scripts/gerar_dados.py

# 5. Inicie a dashboard
streamlit run app.py
```

Acesse `http://localhost:8501` no navegador.

---

## 🧭 Dashboard — Visão Geral

A tela inicial exibe **KPIs em tempo real** calculados a partir do banco de dados SQLite, a tabela de arquitetura do sistema e o fluxo completo de dados entre as fases.

![Dashboard — Visão Geral](screenshots/01_dashboard.png)
> **KPIs ativos:** 300 leituras de sensores armazenadas · 33 irrigações acionadas pelos modelos ML · 66,3% de umidade média do solo · pH médio de 6,43 (dentro da faixa ideal 6,0–6,8). A tabela de arquitetura confirma todos os 7 serviços como `✅ ativos`.

O menu lateral lista todas as páginas na ordem de navegação da dashboard:

| # | Página | Fase | Função principal |
|---|--------|------|-----------------|
| 1 | 🏠 Visão Geral | — | KPIs, arquitetura, fluxo de dados |
| 2 | 🌱 Fase 1 — Área & Insumos | 1 | CRUD de culturas, cálculo de área e dosagem |
| 3 | 🌦️ Fase 2 — Clima | 2 | API meteorológica e recomendação de irrigação |
| 4 | 🗄️ Fase 3 — Banco de Dados | 3 | Visualização e inserção de leituras de sensores |
| 5 | 🤖 Fase 4 — Machine Learning | 4 | Treinamento, métricas e predições interativas |
| 6 | 📷 Fase 6 — Visão Computacional | 6 | Inferência YOLOv5 em imagens (carros / drones) |
| 7 | ☁️ Fase 5 — AWS SNS | 5 | Inscrição de e-mail/SMS e disparo de alertas |
| 8 | 🚀 Ir Além — Rekognition | Extra | Análise de imagens via Amazon Rekognition |

---

## 🌱 Fase 1 — Cálculo de Área e Gestão de Insumos

CRUD completo para cadastro de culturas agrícolas com cálculo automático de área e dosagem de insumos, persistido em SQLite local.

- **Café (retangular):** `área = comprimento × largura`
- **Milho (circular):** `área = π × raio²`
- Dosagem automática de fertilizante e defensivo a partir da área calculada
- Operações suportadas: **Novo cadastro · Listar · Editar · Excluir**

![Fase 1 — Cálculo de Área e Gestão de Insumos](screenshots/02_fase1_area_insumos.png)
> **Exemplo real:** Cultura Café (retangular) com 100 m × 50 m e dose de 0,50 kg/m de fertilizante → resultado calculado: **5.000 m² de área** e **2.500 kg de fertilizante**. O registro é salvo automaticamente na tabela `culturas` do SQLite.

---

## 🌦️ Fase 2 — Integração com API Meteorológica

Consulta à **API OpenWeather** para obter condições climáticas em tempo real e gerar recomendação automática de irrigação. Quando a chave não está configurada, o sistema usa um **fallback simulado realista** (ciclo diário de temperatura + probabilidade de chuva) para manter o sistema funcional.

![Fase 2 — Integração com API Meteorológica](screenshots/03_fase2_clima.png)
> **Dados simulados para São Paulo:** 22,0°C · 47,3% umidade do ar · 1.019,4 hPa de pressão · 3,2 mm de chuva. O módulo detecta precipitação ativa e exibe **"Chovendo atualmente — não irrigar"**. A tabela de previsão 24h (8 períodos de 3 horas) orienta o planejamento de irrigação do dia seguinte.

**Lógica de recomendação:**
| Condição | Recomendação |
|----------|-------------|
| Chuva atual ou prevista | ❌ Não irrigar |
| Umidade do ar > 85% | ❌ Não irrigar |
| Demais condições | ✅ Irrigar |

---

## 🗄️ Fase 3 — Banco de Dados de Sensores IoT

Banco de dados SQLite com schema idêntico ao Oracle utilizado nas fases anteriores (`SENSORES_SOJA_RM567951`). Armazena leituras simuladas de sensores ESP32 com suporte a visualização, inserção e análise histórica.

**Campos da tabela `sensores_soja`:** `id · timestamp · umidade_solo · ph_solo · nitrogenio · fosforo · potassio · temperatura · chuva_mm · irrigacao_ativa`

![Fase 3 — Banco de Dados de Sensores IoT](screenshots/04_fase3_banco_dados.png)
> **300 leituras históricas** carregadas do CSV (`dados_sensores.csv`, gerado com `seed=42`). A tabela exibe todas as colunas do schema Oracle. O gráfico de linha sobreposto mostra a evolução temporal de **umidade do solo** e **pH** ao longo dos 12 dias de dados simulados (01–12/10/2025), evidenciando a correlação entre chuva e umidade.

---

## 🤖 Fase 4 — Machine Learning Preditivo

Pipeline de 4 modelos treinados com scikit-learn sobre o dataset sintético (300 amostras, `seed=42`). Os modelos são persistidos em `.pkl` e carregados pela dashboard para predições interativas em tempo real.

![Fase 4 — Machine Learning Preditivo](screenshots/05_fase4_ml.png)
> **Predição ao vivo:** com Umidade 55%, pH 6,50, Temperatura 25°C, Chuva 0 mm e nutrientes N+P ativos, o modelo Random Forest retorna **score de irrigação 0,99** → *"Sistema recomenda LIGAR a irrigação."*

### Modelos treinados

| Modelo | Algoritmo | MAE | RMSE | R² |
|--------|-----------|-----|------|----|
| Umidade do solo | Linear Regression | 3,96% | 4,64% | 0,573 |
| pH do solo | Linear Regression | 0,286 | 0,340 | -0,069 |
| Irrigação (ligar/desligar) | **Random Forest** (100 árvores) | 0,026 | 0,083 | **0,930** |
| Rendimento esperado | **Gradient Boosting** (100 estimadores) | 0,962 | 1,813 | **0,977** |

> **Nota sobre o modelo de pH:** O pH foi gerado com ruído uniforme em torno de 6,4, sem correlação forte com as features — por isso R² negativo. Os modelos de irrigação e rendimento, cujos targets têm lógica determinística, alcançam performance excelente.

---

## 📷 Fase 6 — Visão Computacional (YOLOv5)

Sistema de detecção de objetos com **YOLOv5 pré-treinado** para identificar carros e drones na fazenda. Quando um objeto é detectado com confiança ≥ 70%, o sistema sugere envio de alerta via AWS SNS. Se PyTorch não estiver instalado, um **fallback baseado no nome do arquivo** mantém a UI funcional.

**Detecção de veículo (carro):**

![Fase 6 — Detecção de Carro com YOLOv5](screenshots/06_fase6_visao.png)
> Imagem de teste `car_040.jpg` processada pelo YOLOv5. O modelo retorna o JSON de detecção com bounding boxes, classe (`car`) e score de confiança. O sistema exibe **"Alerta de atividade incomum!"** e habilita o botão **"Enviar alerta SNS"** para notificar os funcionários da fazenda.

**Detecção de drone:**

![Fase 6 — Detecção de Drone com YOLOv5](screenshots/09_rekognition_2.png)
> Imagem de teste `drone_037.jpg`: drone amarelo em voo detectado. A detecção acima do limiar de 70% de confiança aciona automaticamente a recomendação de inspeção do perímetro.

---

## ☁️ Fase 5 — Cloud Computing & Mensageria AWS SNS

Serviço de mensageria em nuvem utilizando **Amazon SNS (Simple Notification Service)** para envio de alertas por **e-mail e SMS** aos funcionários da fazenda. A integração é acionada tanto manualmente pela dashboard quanto automaticamente pelas Fases 3 e 6.

**Condições que disparam alertas:**

| Condição detectada | Ação recomendada ao funcionário |
|--------------------|--------------------------------|
| Umidade do solo < 60% | Ativar bomba de irrigação imediatamente |
| Umidade do solo > 80% | Verificar sistema de drenagem |
| pH < 6,0 | Aplicar calcário (corretivo de acidez) |
| pH > 6,8 | Aplicar acidificante ao solo |
| Temperatura > 30°C | Monitorar estresse térmico das plantas |
| Nutrientes NPK < 2 de 3 | Aplicar fertilizante específico |
| Detecção de carro/drone | Inspecionar perímetro imediatamente |

### Passo a passo — implementado e testado ✅

**1. Criação do tópico SNS no console da AWS**

Acesse **AWS Console → Simple Notification Service → Topics → Create topic**. Selecione o tipo **Standard** e defina o nome `Farmtech_alertas`.

![SNS — Criação do tópico (formulário)](screenshots/12_sns_topic_created.png)
> Print do formulário "Create topic" com o tipo **Standard** selecionado e o campo Name preenchido com `alertas` — capturado antes de clicar no botão de criação, conforme exigido pela FIAP.

![SNS — Tópico criado com sucesso](screenshots/13_sns_topic_created_2.png)
> Banner verde **"Topic alertas created successfully"** confirmando a criação. Os dados do tópico: **ARN:** `arn:aws:sns:us-east-1:311141542302:Farmtech_alertas` · **Tipo:** Standard · **Conta:** 311141542302 · **Região:** us-east-1.

**2. Configuração do ARN no código**

O ARN gerado foi inserido diretamente em `alerts/sns_alerts.py`:

```python
TOPIC_ARN = "arn:aws:sns:us-east-1:311141542302:Farmtech_alertas"
AWS_REGION = "us-east-1"
```

As credenciais AWS foram configuradas via `aws configure` com o usuário IAM `richard-adm` (conta `311141542302`).

**3. Inscrição de e-mail e confirmação**

Ao inscrever um e-mail pela dashboard, a AWS envia automaticamente um e-mail de confirmação.

![SNS — E-mail de confirmação de inscrição](screenshots/14_sns_subscription_confirmed.png)
> E-mail da **AWS Notifications** recebido com o link "Confirm subscription" para o tópico `arn:aws:sns:us-east-1:311141542302:Farmtech_alertas`. Ao clicar, a inscrição é ativada.

![SNS — Inscrição confirmada pela AWS](screenshots/15_sns_active_subscriptions.png)
> Página de confirmação da AWS: **"Subscription confirmed!"** com o ID da inscrição: `arn:aws:sns:us-east-1:311141542302:Farmtech_alertas:5c29fffc-0f2c-4251-a39f-19d4d5f27cab`.

**4. Alerta disparado e recebido**

Usando a dashboard → aba **"Disparar alerta de sensor"** com valores críticos simulados:

![Fase 5 — Dashboard SNS com alerta disparado](screenshots/07_fase5_sns.png)
> Alerta disparado com: Umidade **45%** · pH **5,70** · Temperatura **32°C** · Nutrientes **1/3**. O campo verde exibe **"Mensagem publicada: id 743e6197-3b87-55bb-8e34-03351f554510"** — confirmação da AWS de que a mensagem foi publicada no tópico SNS com sucesso.

![SNS — E-mail de alerta recebido](screenshots/11_sns_email_recebido.png)
> E-mail recebido em segundos com subject **"FarmTech Alert — Sensor Threshold Exceeded"** contendo as 4 issues detectadas e as 4 ações recomendadas:
> 1. Activate the irrigation pump immediately
> 2. Apply lime or acidifier to correct pH
> 3. Monitor crop for heat stress
> 4. Apply fertilizer — check N, P, K levels

---

## 🚀 "Ir Além" — Opção 1: AWS Rekognition

Integração com **Amazon Rekognition (DetectLabels API)** para análise de imagens da fazenda diretamente na nuvem, complementando o modelo YOLOv5 local da Fase 6.

### Por que Rekognition?

| | YOLOv5 local (Fase 6) | AWS Rekognition (Ir Além) |
|-|----------------------|--------------------------|
| Treinamento necessário | Sim (customizável) | Não (pré-treinado) |
| Hardware GPU | Recomendado | Sem necessidade |
| Classes detectáveis | Limitadas ao dataset | Milhares de labels |
| Custo | Gratuito | Pago após 5.000 imagens/mês |
| Integração com SNS | Manual | Automática via `interpret_farm_labels()` |

### Arquitetura e funcionamento

![Ir Além — Arquitetura AWS Rekognition](screenshots/08_rekognition_1.png)
> Página do sistema exibindo a arquitetura completa: `Farm Images → [Streamlit Dashboard] → [boto3 SDK Python] → AWS Rekognition (DetectLabels) → Labels + Confidence → interpret_farm_labels() → Normal / Alerta → AWS SNS (Email + SMS)`. Serviços utilizados: **Amazon Rekognition** (DetectLabels API) · **Amazon SNS** (alert delivery) · **IAM** (policy `rekognition:DetectLabels` + `sns:Publish`).

### Análise de imagem em tempo real

![Ir Além — Resultado DetectLabels com drone](screenshots/10_rekognition_3.png)
> Análise da imagem `drone_enthusiasts_mobile.jpeg` pelo Rekognition: **10 rótulos detectados** — Aircraft (99,74%), Takeoff (99,74%), Vehicle (99,74%), Adult (99,48%), Male (99,48%), Man (99,48%), Person (99,48%), Flying (90,23%), Airplane (86,91%), Outdoors (77,86%). O módulo `interpret_farm_labels()` mapeia os labels para ações agrícolas: **Aircraft → monitor airspace · Vehicle → check unauthorized access · Person → verify identity**. O sistema exibe automaticamente **"Recomendação: disparar alerta SNS automaticamente."**

### Passo a passo de configuração

1. Acesse o **AWS Console → Amazon Rekognition** (região `us-east-1` recomendada).
2. Crie um usuário IAM com a policy `AmazonRekognitionReadOnlyAccess`.
3. Configure as credenciais via `aws configure`.
4. Na dashboard → **"Ir Além — AWS Rekognition"**, selecione uma imagem e clique em **"Analisar com AWS Rekognition"**.
5. O sistema exibe os rótulos com confiança, categorias agrupadas, ações sugeridas e botão para disparo automático de alerta SNS.

> ⚠️ **Atenção:** Em conta de estudante (Learner Lab), o Rekognition pode ser bloqueado. Os prints acima foram tirados antes do bloqueio, conforme orientação da FIAP.

---

## 🧠 Decisões técnicas relevantes

| Tema | Decisão | Justificativa |
|------|---------|---------------|
| Banco de dados | SQLite com schema idêntico ao Oracle | Funciona offline, dispensa o servidor `oracle.fiap.com.br` (instável fora da rede FIAP), mantém compatibilidade total de SQL |
| API meteorológica sem chave | Fallback simulado com ciclo diário realista | Permite avaliação sem depender de chave expirada; o fallback gera dados com sazonalidade e chuva ocasional (10%) |
| YOLOv5 sem PyTorch instalado | Fallback baseado no nome do arquivo (`car_*.jpg → "car"`) | Evita instalação de ~1 GB de dependências; a UI permanece totalmente funcional para demonstração |
| Geração de dados | Script reprodutível com `random.seed(42)` | Garante que métricas e modelos sejam idênticos em qualquer ambiente |
| Random Forest para irrigação | Em vez de Logistic Regression | Captura bem a lógica booleana complexa (`umidade < 60 AND pH 6,0–6,8 AND NPK ≥ 2`); R² = 0,930 |
| Gradient Boosting para rendimento | Em vez de regressão linear | Modela interações não-lineares entre NPK, temperatura e umidade; R² = 0,977 |
| Estrutura em pacotes Python | `phases/`, `alerts/`, `rekognition/` | Imports limpos no `app.py`, separação de responsabilidades por fase, escalabilidade |

---

## 📚 Histórico das fases anteriores

| Fase | Repositório | Foco |
|------|-------------|------|
| 1 — Startup | `Startup_FarmTech_Solutions` | Cálculo de área de café/milho em Python + análise estatística em R |
| 2 | `FarmTech-Solutions-Fase2` | IoT ESP32 + Wokwi + integração OpenWeather |
| 3 | `FarmTech-Solutions-Fase3` | Banco relacional Oracle (`SENSORES_SOJA_RM567951`) — MER e DER |
| 4 | `FarmTech-Solutions-Fase4` | Dashboard ML inicial com Streamlit + display LCD no ESP32 |
| 5 | `FarmTech-Solutions-Fase5` | Cloud AWS — estudo de custo, região e segurança (ISO 27001/27002) |
| 6 | `FarmTech-Solutions-Fase6` | YOLOv5 — detecção car/drone (mAP 94,3%) |
| **7** | _este repositório_ | **Consolidação de tudo em uma dashboard unificada** |

---

## 📄 Licença

Projeto acadêmico desenvolvido por **Richard Schmitz** (RM 567951) para o curso de Inteligência Artificial da FIAP — 2026.

---

<p align="center">
  <em>FarmTech Solutions — agronegócio guiado por inteligência artificial 🌾</em>
</p>
