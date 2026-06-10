# Roteiros de Vídeo — FarmTech Solutions Fase 7

---

## Vídeo 1 — Demonstração Completa (até 10 min)

**Pré-requisitos antes de gravar:**
- `streamlit run app.py` rodando em `http://localhost:8501`
- Banco populado: `python scripts/gerar_dados.py` já executado
- Modelos treinados: `models/modelo_irrigacao.pkl` presente
- AWS configurada via `aws configure` para SNS funcionar ao vivo
- Resolução 1920×1080, fonte do browser aumentada para boa legibilidade

---

### [00:00 – 00:30] Apresentação

> "Olá. Meu nome é Richard Schmitz, RM 567951, curso de Inteligência Artificial da FIAP.
> Este vídeo demonstra o projeto FarmTech Solutions Fase 7 — a consolidação de todos os
> serviços das fases anteriores em uma única plataforma de gestão de fazenda inteligente.
> Vou percorrer cada fase pelo menu da dashboard Streamlit, nessa ordem."

---

### [00:30 – 01:30] Visão Geral

Abrir o browser em `http://localhost:8501`, página "Visão Geral".

> "A tela inicial mostra quatro KPIs calculados em tempo real pelo banco SQLite:
> 300 leituras de sensores carregadas, 33 irrigações acionadas,
> umidade média de 66,3% e pH médio de 6,43."

Rolar para baixo.

> "A tabela de arquitetura confirma os sete serviços ativos — Fases 1 a 6 mais o Ir Além.
> Abaixo, o fluxo de dados do sistema: sensores → banco → modelos ML →
> visão computacional → alertas SNS. É esse pipeline que vou demonstrar agora."

---

### [01:30 – 03:00] Fase 1 — Cálculo de Área e Insumos

Clicar em "Fase 1 - Area & Insumos" no menu lateral.

> "Fase 1 é o CRUD de culturas. Vou cadastrar uma lavoura de café."

Na aba "Novo cadastro":
- Selecionar "Cafe (retangular)"
- Comprimento: 100 m — Largura: 50 m — Dose: 0,50 kg/m
- Clicar "Calcular e salvar Cafe"

> "O sistema calcula: 5.000 m² de área e 2.500 kg de fertilizante,
> e salva na tabela `culturas` do SQLite."

Clicar na aba "Listar".

> "Aqui vejo todos os registros com o gráfico de área por cultura.
> A aba Editar permite alterar área e insumo, e excluir registros — CRUD completo."

---

### [03:00 – 04:00] Fase 2 — Clima e Irrigação

Clicar em "Fase 2 - Clima".

> "Fase 2 integra a API OpenWeather. Sem chave configurada, o sistema usa dados simulados
> com ciclo diário de temperatura — o que garante a demonstração sem dependência externa."

Clicar "Consultar clima atual".

> "Retorna temperatura, umidade, pressão e precipitação para São Paulo.
> A lógica de recomendação: se há chuva atual ou prevista — não irrigar.
> Se umidade do ar acima de 85% — não irrigar. Caso contrário — irrigar.
> O gráfico de previsão cobre as próximas 24 horas em janelas de 3 horas."

---

### [04:00 – 05:30] Fase 3 — Banco de Dados IoT

Clicar em "Fase 3 - Banco de Dados".

> "Fase 3 é o banco de sensores IoT. O schema SQLite é idêntico ao Oracle
> usado nas fases anteriores — tabela `sensores_soja` com campos de umidade do solo,
> pH, nitrogênio, fósforo, potássio, temperatura, chuva e status de irrigação."

Na aba "Visualizar":

> "300 leituras do `dados_sensores.csv`, gerado com seed=42 para reprodutibilidade.
> O gráfico de linha mostra evolução de umidade e pH ao longo dos 12 dias de dados.
> O scatter plot relaciona umidade com temperatura, destacando pontos com irrigação ativa."

Na aba "Inserir leitura": Umidade 45%, pH 5,7, Temperatura 32°C, sem N sem P sem K. Clicar "Inserir".

> "Com umidade abaixo de 60% e sem chuva, o sistema decide automaticamente ligar a irrigação.
> Esse registro entra no banco e alimenta os modelos na próxima fase."

---

### [05:30 – 07:00] Fase 4 — Machine Learning

Clicar em "Fase 4 - Machine Learning".

> "Fase 4 tem quatro modelos treinados com scikit-learn e persistidos em arquivos .pkl."

Mostrar a tabela de métricas.

> "Random Forest para irrigação: R² de 0,930. Gradient Boosting para rendimento: R² de 0,977.
> Linear Regression para umidade: R² de 0,573.
> O modelo de pH tem R² negativo — o pH foi gerado com ruído uniforme sem correlação
> direta com as features disponíveis. Esse comportamento é esperado e está documentado."

Nos sliders: Umidade 55%, pH 6,5, Temperatura 25°C, N e P ligados, K desligado, Chuva 0. Clicar "Prever".

> "Score de irrigação 0,99 — o modelo recomenda ligar a irrigação.
> Os alertas baseados em regras confirmam que as condições estão dentro do esperado."

---

### [07:00 – 08:00] Fase 6 — Visão Computacional YOLOv5

Clicar em "Fase 6 - Visao Computacional".

> "Fase 6 usa YOLOv5 para detecção de objetos — foco em carros e drones,
> que representam ameaças ao perímetro da fazenda."

Selecionar `car_040.jpg`. Clicar "Analisar imagem".

> "O modelo retorna bounding boxes, classe detectada e score de confiança.
> Com confiança acima de 70%, o sistema exibe o alerta e habilita o botão
> de envio para o SNS. O fallback por nome de arquivo mantém o sistema funcional
> mesmo sem PyTorch instalado."

---

### [08:00 – 09:30] Fase 5 — AWS SNS

Clicar em "Fase 5 - AWS SNS (Alertas)".

> "Fase 5 é o serviço de mensageria. O tópico SNS foi criado na AWS Console
> e o ARN foi configurado em `alerts/sns_alerts.py` com credenciais via `aws configure`."

Aba "Disparar alerta de sensor". Ajustar: Umidade 45%, pH 5,7, Temperatura 32°C, Nutrientes 1. Clicar "Disparar alerta SNS".

> "O alerta é publicado no tópico e a AWS retorna o ID da mensagem.
> O e-mail chega com subject 'FarmTech Alert — Sensor Threshold Exceeded',
> listando as quatro condições detectadas e as quatro ações recomendadas:
> ativar irrigação, aplicar calcário, monitorar temperatura, aplicar fertilizante."

Aba "Inscrições ativas" → "Listar inscrições".

> "Aqui vejo as inscrições ativas — e-mail confirmado e pronto para receber alertas."

---

### [09:30 – 10:00] Encerramento

> "Com isso demonstrei as seis fases integradas: gestão de culturas, dados meteorológicos,
> banco IoT, machine learning preditivo, visão computacional e alertas em nuvem.
> O repositório está no GitHub — link na descrição e no README do projeto. Obrigado."

---

---

## Vídeo 2 — "Ir Além": AWS Rekognition (até 5 min)

**Pré-requisitos:**
- Dashboard rodando
- Se Rekognition ainda estiver acessível: `aws configure` com usuário IAM configurado
- Se conta Learner Lab bloqueou o serviço: usar os screenshots documentados no README, explicando o bloqueio e mostrando o código

---

### [00:00 – 00:20] Abertura

> "Richard Schmitz, RM 567951, FIAP. Este vídeo demonstra o 'Ir Além' da Fase 7:
> integração com Amazon Rekognition, o serviço de reconhecimento de imagens da AWS,
> complementar ao YOLOv5 local da Fase 6."

---

### [00:20 – 01:00] Diferença em relação ao YOLOv5

Clicar em "Ir Alem - AWS Rekognition" no menu lateral.

> "A página mostra a comparação entre as duas abordagens.
> O YOLOv5 roda offline, foi treinado para classes específicas — carros e drones —
> e exige PyTorch localmente.
> O Rekognition é um serviço gerenciado na nuvem: sem instalação, sem GPU,
> pré-treinado em milhares de labels. A desvantagem é o custo — gratuito até 5.000 imagens
> por mês — e o risco de bloqueio em contas Learner Lab, o que de fato aconteceu.
> Os prints que vou mostrar foram capturados antes do bloqueio, conforme orientação da FIAP."

---

### [01:00 – 02:30] Análise de imagem

Se Rekognition estiver acessível ao vivo:

- Selecionar imagem no dropdown
- Clicar "Analisar com AWS Rekognition"
- Mostrar a tabela de rótulos retornados

Se bloqueado:

> "Vou mostrar os resultados documentados no README."

Abrir o README no browser e rolar até a seção "Ir Além".

Em ambos os casos:

> "O Rekognition retorna rótulos com score de confiança. Para um drone:
> Aircraft com 99,74%, Vehicle com 99,74%, Person com 99,48%, Flying com 90,23%.
> A função `interpret_farm_labels()` mapeia esses rótulos para ações agrícolas:
> Aircraft → monitorar espaço aéreo.
> Vehicle → verificar acesso não autorizado.
> Person → verificar identidade do visitante.
> Quando o sistema detecta uma ameaça, recomenda disparar alerta SNS —
> o mesmo tópico usado na Fase 5."

---

### [02:30 – 03:30] Código

Abrir `rekognition/aws_rekognition.py` no VS Code.

> "O módulo tem três funções principais.
> `detect_labels_from_file()` lê a imagem em bytes e chama DetectLabels com
> confiança mínima de 70% — o mesmo limiar do YOLOv5.
> `interpret_farm_labels()` percorre os rótulos e mapeia para ações de fazenda.
> `get_architecture_description()` retorna o texto exibido na dashboard,
> descrevendo o fluxo: imagem → boto3 → Rekognition → labels → interpret → SNS."

---

### [03:30 – 04:30] Configuração IAM

> "A configuração exige dois passos.
> Primeiro: usuário IAM com a policy `AmazonRekognitionReadOnlyAccess`
> mais permissão `sns:Publish` — o mesmo usuário já utilizado no projeto.
> Segundo: `aws configure` com as credenciais.
> O código não armazena credenciais em texto — usa o cliente boto3
> que lê do arquivo de configuração local da AWS.
> Isso está alinhado com o princípio de menor privilégio e boas práticas de segurança
> abordadas na Fase 5."

---

### [04:30 – 05:00] Encerramento

> "Em resumo: o 'Ir Além' escala a visão computacional para a nuvem
> sem dependências locais pesadas, usando o mesmo pipeline de alertas SNS da Fase 5.
> O código está em `rekognition/aws_rekognition.py` e a documentação completa no README.
> Obrigado."

---

## Checklist pós-gravação

- [ ] Subir Vídeo 1 no YouTube como "não listado"
- [ ] Subir Vídeo 2 no YouTube como "não listado"
- [ ] Substituir o placeholder do Vídeo 1 no README (linha 32)
- [ ] Substituir o placeholder do Vídeo 2 no README (linha 35)
- [ ] Commit e push do README com os links reais
- [ ] Enviar link do repositório via portal FIAP (PDF)
