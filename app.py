"""
FarmTech Solutions - Fase 7: Dashboard Unificado
Author: Richard Schmitz - RM567951

Ponto de entrada do sistema consolidado. Integra os servicos das Fases
1, 2, 3, 4 e 6 em uma unica interface Streamlit, com botoes que disparam
cada modulo. A Fase 5 (Cloud + Seguranca) e materializada nos servicos
AWS SNS (alertas) e AWS Rekognition (Ir Alem).

Executar:
    streamlit run app.py
"""

import os
import sys
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Garante que o diretorio do projeto esteja no sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from phases import fase1_area_calc as fase1
from phases import fase2_weather as fase2
from phases import fase3_database as fase3
from phases import fase4_ml as fase4
from phases import fase6_vision as fase6
from alerts import sns_alerts
from rekognition import aws_rekognition


# ----------------------------- CONFIG -----------------------------
st.set_page_config(
    page_title="FarmTech Solutions - Fase 7",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY_COLOR = "#2E7D32"
ACCENT_COLOR = "#FF6F00"

st.markdown(
    f"""
    <style>
        .main-header {{
            color: {PRIMARY_COLOR};
            text-align: center;
            padding: 1rem 0;
            border-bottom: 2px solid {PRIMARY_COLOR};
            margin-bottom: 1rem;
        }}
        .metric-card {{
            background-color: #F1F8E9;
            border-left: 5px solid {PRIMARY_COLOR};
            padding: 1rem;
            border-radius: 6px;
            margin: 0.5rem 0;
        }}
        .stButton button {{
            background-color: {PRIMARY_COLOR};
            color: white;
            font-weight: bold;
            border-radius: 4px;
        }}
        .stButton button:hover {{
            background-color: {ACCENT_COLOR};
            color: white;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------- SIDEBAR -----------------------------
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Tractor_psf.svg/240px-Tractor_psf.svg.png",
    width=120,
)
st.sidebar.title("🌾 FarmTech Solutions")
st.sidebar.caption("Fase 7 - Sistema Consolidado")
st.sidebar.markdown("**Autor:** Richard Schmitz - RM567951")
st.sidebar.markdown("**Curso:** Inteligencia Artificial - FIAP")
st.sidebar.divider()

pagina = st.sidebar.radio(
    "Navegacao",
    [
        "🏠 Visao Geral",
        "🌱 Fase 1 - Area & Insumos",
        "🌦️ Fase 2 - Clima",
        "🗄️ Fase 3 - Banco de Dados",
        "🤖 Fase 4 - Machine Learning",
        "📷 Fase 6 - Visao Computacional",
        "☁️ Fase 5 - AWS SNS (Alertas)",
        "🚀 Ir Alem - AWS Rekognition",
    ],
)

st.sidebar.divider()
st.sidebar.markdown("### Status do sistema")
db_ok = os.path.exists("data/farmtech.db") or os.path.exists("data/dados_sensores.csv")
models_ok = os.path.exists("models/modelo_irrigacao.pkl")
st.sidebar.markdown(f"- Banco: {'✅' if db_ok else '⚠️'}")
st.sidebar.markdown(f"- Modelos ML: {'✅' if models_ok else '⚠️'}")
st.sidebar.markdown(f"- SNS configurado: {'✅' if sns_alerts.TOPIC_ARN else '⚠️ definir TOPIC_ARN'}")


# ----------------------------- PAGINA: VISAO GERAL -----------------------------
def pagina_visao_geral():
    st.markdown("<h1 class='main-header'>🌾 FarmTech Solutions - Sistema Consolidado</h1>", unsafe_allow_html=True)
    st.write(
        "Plataforma unificada que integra os servicos desenvolvidos da Fase 1 a Fase 6, "
        "permitindo gestao completa de uma fazenda inteligente a partir de uma unica interface."
    )

    col1, col2, col3, col4 = st.columns(4)
    try:
        resumo = fase3.get_summary()
        col1.metric("Leituras de sensores", resumo.get("total", 0))
        col2.metric("Irrigacoes acionadas", resumo.get("irrigacoes", 0))
        col3.metric("Umidade media (%)", resumo.get("umidade_media", 0))
        col4.metric("pH medio do solo", resumo.get("ph_medio", 0))
    except Exception as e:
        st.warning(f"Banco de dados nao inicializado ainda: {e}")

    st.subheader("Arquitetura do sistema")
    st.markdown("""
    | Fase | Servico | Status |
    |------|---------|--------|
    | 1 | Calculo de area e insumos (CRUD em SQLite) | ✅ |
    | 2 | API meteorologica OpenWeather (com fallback simulado) | ✅ |
    | 3 | Banco de dados estruturado dos sensores | ✅ |
    | 4 | Pipeline de Machine Learning + dashboard | ✅ |
    | 5 | Mensageria AWS SNS (email + SMS) | ✅ |
    | 6 | Visao computacional YOLOv5 (carros / drones) | ✅ |
    | 7 | Integracao via Streamlit (este dashboard) | ✅ |
    | Ir Alem | AWS Rekognition | ✅ |
    """)

    st.subheader("Como o sistema flui")
    st.markdown("""
    1. **Sensores** (Fase 3) → coletam umidade, pH, NPK, temperatura e chuva.
    2. **API meteorologica** (Fase 2) → enriquece com previsao de chuva.
    3. **Banco SQLite** (Fase 3) → persiste tudo com o mesmo schema do Oracle.
    4. **Modelos ML** (Fase 4) → preveem condicoes futuras e necessidade de irrigacao.
    5. **Visao computacional** (Fase 6) → analisa imagens da fazenda para seguranca.
    6. **AWS SNS** (Fase 5) → dispara alertas por email / SMS aos funcionarios.
    7. **AWS Rekognition** (Ir Alem) → analise extra de imagens na nuvem.
    """)


# ----------------------------- FASE 1 -----------------------------
def pagina_fase1():
    st.header("🌱 Fase 1 - Calculo de area e gestao de insumos")
    st.caption("CRUD completo das culturas, armazenado em SQLite local.")

    tab_add, tab_list, tab_edit = st.tabs(["➕ Novo cadastro", "📋 Listar", "✏️ Editar / Excluir"])

    with tab_add:
        st.subheader("Cadastrar nova cultura")
        cultura = st.selectbox("Cultura", ["Cafe (retangular)", "Milho (circular)"])
        if cultura.startswith("Cafe"):
            c1, c2, c3 = st.columns(3)
            comp = c1.number_input("Comprimento (m)", min_value=1.0, value=100.0, step=1.0)
            larg = c2.number_input("Largura (m)", min_value=1.0, value=50.0, step=1.0)
            dose = c3.number_input("Dose de fertilizante (kg/m)", min_value=0.01, value=0.5, step=0.1)
            if st.button("Calcular e salvar Cafe"):
                dados = fase1.calcular_area_cafe(comp, larg, dose)
                fase1.salvar_cultura(dados)
                st.success(f"✅ Cadastrado: area = {dados['area_m2']} m², fertilizante = {dados['insumo_total']} kg")
        else:
            c1, c2 = st.columns(2)
            raio = c1.number_input("Raio (m)", min_value=1.0, value=20.0, step=1.0)
            litros = c2.number_input("Defensivo (l/hectare)", min_value=0.01, value=10.0, step=0.5)
            if st.button("Calcular e salvar Milho"):
                dados = fase1.calcular_area_milho(raio, litros)
                fase1.salvar_cultura(dados)
                st.success(f"✅ Cadastrado: area = {dados['area_m2']} m², defensivo = {dados['insumo_total']} l")

    with tab_list:
        st.subheader("Culturas cadastradas")
        df = fase1.listar_culturas()
        if df.empty:
            st.info("Nenhuma cultura cadastrada ainda.")
        else:
            st.dataframe(df, use_container_width=True)
            fig = px.bar(df, x="tipo", y="area_m2", color="tipo",
                         title="Area cadastrada por cultura (m²)")
            st.plotly_chart(fig, use_container_width=True)

    with tab_edit:
        df = fase1.listar_culturas()
        if df.empty:
            st.info("Cadastre uma cultura primeiro.")
        else:
            id_ = st.selectbox("Selecione o registro", df["id"].tolist())
            row = df[df["id"] == id_].iloc[0]
            c1, c2 = st.columns(2)
            new_area = c1.number_input("Nova area (m²)", value=float(row["area_m2"]))
            new_insumo = c2.number_input("Novo insumo total", value=float(row["insumo_total"]))
            colA, colB = st.columns(2)
            if colA.button("💾 Atualizar"):
                fase1.atualizar_cultura(id_, new_area, new_insumo)
                st.success("Registro atualizado.")
                st.rerun()
            if colB.button("🗑️ Excluir", type="secondary"):
                fase1.excluir_cultura(id_)
                st.success("Registro excluido.")
                st.rerun()


# ----------------------------- FASE 2 -----------------------------
def pagina_fase2():
    st.header("🌦️ Fase 2 - Integracao com API meteorologica")
    st.caption("Consulta OpenWeather (ou usa fallback simulado quando nao ha chave configurada).")

    api_key = st.text_input("Chave OpenWeather (opcional)", type="password",
                            help="Sem chave, o sistema retorna dados simulados realistas.")
    cidade = st.text_input("Cidade", value="Sao Paulo,BR")

    svc = fase2.WeatherService(api_key=api_key)
    svc.cidade = cidade

    if st.button("🔄 Consultar clima atual"):
        with st.spinner("Consultando..."):
            atual = svc.get_current()
            previsao = svc.get_forecast()
            recomendacao = svc.irrigation_recommendation(atual, previsao)

        st.subheader("Condicoes atuais")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Temperatura", f"{atual['temperatura']}°C")
        col2.metric("Umidade do ar", f"{atual['umidade']}%")
        col3.metric("Pressao", f"{atual['pressao']} hPa")
        col4.metric("Chuva (1h)", f"{atual['chuva']} mm")
        st.caption(f"Fonte: {atual['fonte']} | {atual['descricao'].title()}")

        st.subheader("Recomendacao de irrigacao")
        if recomendacao["irrigar"]:
            st.success(f"💧 {recomendacao['motivo']}")
        else:
            st.warning(f"⏸️ {recomendacao['motivo']}")

        st.subheader("Previsao para as proximas 24h")
        df_prev = pd.DataFrame(previsao)
        st.dataframe(df_prev, use_container_width=True)
        if not df_prev.empty:
            fig = px.line(df_prev, x="datetime", y=["temperatura", "umidade"],
                          title="Temperatura e umidade previstas")
            st.plotly_chart(fig, use_container_width=True)


# ----------------------------- FASE 3 -----------------------------
def pagina_fase3():
    st.header("🗄️ Fase 3 - Banco de dados estruturado dos sensores IoT")
    st.caption("Banco SQLite com o mesmo schema da tabela Oracle SENSORES_SOJA_RM567951.")

    tab_view, tab_insert, tab_critical = st.tabs(["📊 Visualizar", "➕ Inserir leitura", "⚠️ Condicoes criticas"])

    with tab_view:
        df = fase3.get_all_readings()
        st.metric("Total de leituras", len(df))
        if not df.empty:
            st.dataframe(df.head(50), use_container_width=True)
            fig = px.line(df.sort_values("timestamp"), x="timestamp",
                          y=["umidade_solo", "ph_solo"],
                          title="Evolucao temporal de umidade e pH")
            st.plotly_chart(fig, use_container_width=True)
            fig2 = px.scatter(df, x="umidade_solo", y="temperatura",
                              color="irrigacao_ativa",
                              title="Umidade x Temperatura (irrigacao em destaque)")
            st.plotly_chart(fig2, use_container_width=True)

    with tab_insert:
        st.subheader("Nova leitura de sensor")
        c1, c2, c3 = st.columns(3)
        umid = c1.number_input("Umidade do solo (%)", 0.0, 100.0, 55.0)
        ph = c2.number_input("pH do solo", 4.0, 9.0, 6.5, step=0.1)
        temp = c3.number_input("Temperatura (°C)", 0.0, 50.0, 25.0)
        c4, c5, c6 = st.columns(3)
        n = c4.checkbox("Nitrogenio (N)", value=True)
        p = c5.checkbox("Fosforo (P)", value=True)
        k = c6.checkbox("Potassio (K)", value=False)
        chuva = st.number_input("Chuva acumulada (mm)", 0.0, 100.0, 0.0)
        if st.button("💾 Inserir no banco"):
            irrig = 1 if umid < 60 and chuva < 1 else 0
            fase3.insert_reading(umid, ph, int(n), int(p), int(k), temp, chuva, irrig)
            st.success(f"Leitura inserida. Irrigacao decidida: {'LIGAR' if irrig else 'DESLIGAR'}")

    with tab_critical:
        st.subheader("Condicoes que demandam atencao")
        df = fase3.get_critical_conditions()
        if df.empty:
            st.info("Nenhuma condicao critica detectada (umidade<50 com irrigacao ligada).")
        else:
            st.dataframe(df, use_container_width=True)


# ----------------------------- FASE 4 -----------------------------
def pagina_fase4():
    st.header("🤖 Fase 4 - Machine Learning preditivo")
    st.caption("Modelos treinados para prever umidade, pH, necessidade de irrigacao e rendimento esperado.")

    col_acao, col_metric = st.columns([1, 2])

    with col_acao:
        if st.button("🔁 Treinar / re-treinar modelos"):
            with st.spinner("Treinando modelos..."):
                results = fase4.train_all()
            st.success("Modelos treinados.")
            st.json(results)

    with col_metric:
        metricas = fase4.get_metrics()
        if metricas:
            st.subheader("Metricas atuais")
            df_m = pd.DataFrame(metricas).T
            st.dataframe(df_m.round(3), use_container_width=True)

    st.divider()
    st.subheader("Predicao interativa")
    models = fase4.load_models()
    if not models:
        st.warning("Modelos nao encontrados. Clique em 'Treinar' acima.")
        return

    c1, c2, c3 = st.columns(3)
    umid = c1.slider("Umidade do solo (%)", 0, 100, 55)
    ph = c2.slider("pH do solo", 4.0, 9.0, 6.5, step=0.1)
    temp = c3.slider("Temperatura (°C)", 10, 45, 25)
    c4, c5, c6 = st.columns(3)
    n = c4.checkbox("N", value=True, key="ml_n")
    p = c5.checkbox("P", value=True, key="ml_p")
    k = c6.checkbox("K", value=False, key="ml_k")
    chuva = st.slider("Chuva (mm)", 0.0, 30.0, 0.0)
    nutrientes = int(n) + int(p) + int(k)

    if st.button("🔮 Prever"):
        if "irrigacao" in models:
            score_irr = fase4.predict(models, "irrigacao",
                                      [umid, ph, temp, chuva, nutrientes])
            st.metric("Score de irrigacao (0-1)", f"{score_irr:.2f}")
            if score_irr >= 0.5:
                st.success("✅ Sistema recomenda LIGAR a irrigacao.")
            else:
                st.info("⏸️ Sistema recomenda manter irrigacao DESLIGADA.")

        analise = fase4.analyze_conditions(umid, ph, int(n), int(p), int(k), temp)
        st.subheader("Alertas baseados em regras")
        if analise["alertas"]:
            for a in analise["alertas"]:
                st.warning(a)
        else:
            st.success("Todas as condicoes estao dentro do esperado.")


# ----------------------------- FASE 6 -----------------------------
def pagina_fase6():
    st.header("📷 Fase 6 - Visao computacional (YOLOv5)")
    st.caption("Deteccao de carros e drones em imagens para seguranca patrimonial da fazenda.")

    imagens = fase6.get_test_images()
    opcoes = ["(Selecione uma imagem)"] + imagens
    escolha = st.selectbox("Imagens de teste do dataset", opcoes)

    upload = st.file_uploader("Ou envie sua propria imagem", type=["jpg", "jpeg", "png"])

    img_path = None
    if upload is not None:
        os.makedirs("dataset/images/uploaded", exist_ok=True)
        img_path = f"dataset/images/uploaded/{upload.name}"
        with open(img_path, "wb") as f:
            f.write(upload.getbuffer())
    elif escolha != "(Selecione uma imagem)":
        img_path = escolha

    if img_path:
        col1, col2 = st.columns([1, 1])
        col1.image(img_path, caption=os.path.basename(img_path), use_container_width=True)

        with col2:
            if st.button("🔍 Analisar imagem"):
                with st.spinner("Processando..."):
                    resultado = fase6.run_inference(img_path)
                st.json(resultado)

                if fase6.alert_needed(resultado):
                    st.error("🚨 Deteccao acima do limiar — alerta sera disparado.")
                    if st.button("📤 Enviar alerta SNS"):
                        topic = sns_alerts.TOPIC_ARN
                        if not topic:
                            st.error("Defina o TOPIC_ARN em alerts/sns_alerts.py antes de enviar.")
                        else:
                            r = sns_alerts.send_vision_alert(resultado)
                            st.write(r)
                else:
                    st.success("Confianca abaixo do limiar de alerta.")


# ----------------------------- FASE 5 / SNS -----------------------------
def pagina_sns():
    st.header("☁️ Fase 5 - Servico de mensageria AWS SNS")
    st.caption("Mensageria configurada para disparar alertas a partir das Fases 1, 3 e 6.")

    st.markdown("""
    **Setup necessario antes de usar:**
    1. Crie um topico no AWS SNS Console.
    2. Cole o ARN do topico no arquivo `alerts/sns_alerts.py` (variavel `TOPIC_ARN`)
       ou cole abaixo.
    3. Configure credenciais via `aws configure`.
    """)

    topic_in = st.text_input("ARN do topico SNS", value=sns_alerts.TOPIC_ARN)

    tab1, tab2, tab3 = st.tabs(["📧 Inscrever email/SMS", "🚨 Disparar alerta de sensor", "📋 Inscricoes ativas"])

    with tab1:
        email = st.text_input("Email para receber alertas", placeholder="seu@email.com")
        if st.button("➕ Inscrever email"):
            r = sns_alerts.subscribe_email(email, topic_in)
            st.write(r)
            if r.get("success"):
                st.info("📬 Verifique sua caixa de entrada e confirme a inscricao.")
        sms = st.text_input("Telefone (formato E.164: +5511999999999)")
        if st.button("➕ Inscrever SMS"):
            r = sns_alerts.subscribe_sms(sms, topic_in)
            st.write(r)

    with tab2:
        st.write("Use leituras de sensores para simular um alerta:")
        c1, c2 = st.columns(2)
        umid = c1.slider("Umidade (%)", 0.0, 100.0, 45.0)
        ph = c2.slider("pH", 4.0, 9.0, 5.7, step=0.1)
        c3, c4 = st.columns(2)
        temp = c3.slider("Temperatura (°C)", 10, 45, 32)
        nutrientes = c4.slider("Nutrientes N+P+K", 0, 3, 1)
        if st.button("🚨 Disparar alerta SNS"):
            r = sns_alerts.send_sensor_alert(umid, ph, temp, nutrientes, topic_in)
            if r.get("success"):
                st.success(f"Mensagem publicada: id {r.get('message_id')}")
            else:
                st.error(f"Falha: {r.get('error')}")

    with tab3:
        if st.button("Listar inscricoes"):
            subs = sns_alerts.list_subscriptions(topic_in)
            if subs:
                st.dataframe(pd.DataFrame(subs))
            else:
                st.info("Nenhuma inscricao encontrada (ou credenciais nao configuradas).")


# ----------------------------- IR ALEM / REKOGNITION -----------------------------
def pagina_rekognition():
    st.header("🚀 Ir Alem - AWS Rekognition")
    st.caption("Reconhecimento de imagens na nuvem via Amazon Rekognition (servico DetectLabels).")

    st.markdown(aws_rekognition.get_architecture_description())

    st.divider()
    st.subheader("Testar Rekognition com uma imagem")

    imagens = fase6.get_test_images()
    opcoes = ["(Selecione)"] + imagens
    escolha = st.selectbox("Imagens disponiveis", opcoes, key="rek_select")
    upload = st.file_uploader("Ou faca upload", type=["jpg", "jpeg", "png"], key="rek_upload")

    img_path = None
    if upload is not None:
        os.makedirs("dataset/images/uploaded", exist_ok=True)
        img_path = f"dataset/images/uploaded/{upload.name}"
        with open(img_path, "wb") as f:
            f.write(upload.getbuffer())
    elif escolha != "(Selecione)":
        img_path = escolha

    if img_path:
        st.image(img_path, caption=os.path.basename(img_path), use_container_width=True)
        if st.button("🔎 Analisar com AWS Rekognition"):
            with st.spinner("Enviando para AWS..."):
                resultado = aws_rekognition.detect_labels_from_file(img_path)
            if resultado.get("success"):
                st.success(f"Recebidos {resultado['label_count']} rotulos.")
                st.dataframe(pd.DataFrame(resultado["labels"]), use_container_width=True)

                interp = aws_rekognition.interpret_farm_labels(resultado["labels"])
                if interp["actions"]:
                    st.subheader("Acoes sugeridas")
                    for a in interp["actions"]:
                        st.warning(f"**{a['label']}** ({a['confidence']}%) — {a['action']}")
                if interp["requires_alert"]:
                    st.error("⚠️ Recomendacao: disparar alerta SNS automatico.")
            else:
                st.error(f"Falha: {resultado.get('error')}")
                st.info("Verifique credenciais AWS e permissoes IAM (rekognition:DetectLabels).")


# ----------------------------- ROTEAMENTO -----------------------------
PAGINAS = {
    "🏠 Visao Geral": pagina_visao_geral,
    "🌱 Fase 1 - Area & Insumos": pagina_fase1,
    "🌦️ Fase 2 - Clima": pagina_fase2,
    "🗄️ Fase 3 - Banco de Dados": pagina_fase3,
    "🤖 Fase 4 - Machine Learning": pagina_fase4,
    "📷 Fase 6 - Visao Computacional": pagina_fase6,
    "☁️ Fase 5 - AWS SNS (Alertas)": pagina_sns,
    "🚀 Ir Alem - AWS Rekognition": pagina_rekognition,
}

PAGINAS[pagina]()

st.sidebar.divider()
st.sidebar.caption("FarmTech Solutions © 2026 - FIAP")
