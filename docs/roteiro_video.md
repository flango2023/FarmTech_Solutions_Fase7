# Roteiros dos vídeos — FarmTech Solutions Fase 7

Dois vídeos precisam ser gravados:

1. **Vídeo principal** — até **10 minutos** — apresenta funcionalidades das Fases 1 a 6 integradas (entrega obrigatória).
2. **Vídeo "Ir Além"** — até **5 minutos** — foca exclusivamente na integração AWS Rekognition.

Ambos devem ser postados no **YouTube como "não listado"** e os links inseridos no README.

---

## 🎬 VÍDEO 1 — Principal (até 10 minutos)

### Preparação antes de gravar

- [ ] Rodar `python scripts/gerar_dados.py` para gerar dataset fresco
- [ ] Subir o app: `streamlit run app.py`
- [ ] Treinar modelos via dashboard (Fase 4 → "Treinar")
- [ ] Ter pelo menos um e-mail inscrito no SNS confirmado
- [ ] Abrir o VS Code lateralmente para mostrar a estrutura de pastas
- [ ] Resolução: 1920x1080, zoom de fonte para ficar legível
- [ ] Ferramenta de gravação: OBS / QuickTime / Loom

### Estrutura (com tempos)

| Bloco | Tempo | Conteúdo |
|-------|-------|----------|
| 0. Abertura | 0:00 — 0:30 | Identifique-se, contextualize a fase |
| 1. Estrutura do projeto | 0:30 — 1:15 | Mostre o VS Code com a árvore de pastas |
| 2. Fase 1 — Área & Insumos | 1:15 — 2:15 | Cadastre, liste, edite, exclua |
| 3. Fase 2 — Clima | 2:15 — 3:15 | Consulte clima, mostre recomendação |
| 4. Fase 3 — Banco de Dados | 3:15 — 4:15 | Visualize, insira leitura, condições críticas |
| 5. Fase 4 — Machine Learning | 4:15 — 5:30 | Treine, mostre métricas, faça predição |
| 6. Fase 6 — Visão Computacional | 5:30 — 6:45 | Analise imagem de carro e drone |
| 7. Fase 5 — AWS SNS | 6:45 — 8:30 | Console AWS + dashboard → inscreva → dispare alerta → mostre e-mail chegando |
| 8. Documentação no GitHub | 8:30 — 9:30 | README + arquitetura |
| 9. Encerramento | 9:30 — 10:00 | Resumo + GitHub link |

### Falas sugeridas (português, tom direto)

**Abertura (0:00 — 0:30)**

> "Olá, sou Richard Schmitz, RM 567951, aluno do curso de Inteligência Artificial da FIAP.
> Este é o vídeo da Fase 7 do meu projeto FarmTech Solutions. Nesta fase, consolidei todas as fases anteriores — da Fase 1 à Fase 6 — em uma única dashboard Streamlit, integrada a serviços de mensageria na AWS."

**Estrutura do projeto (0:30 — 1:15)**

> "Antes de mostrar a dashboard, abro o VS Code. Veja a organização: cada fase está em um módulo Python dentro da pasta `phases`. A pasta `alerts` contém a mensageria AWS SNS, e a `rekognition` é o módulo do meu 'Ir Além'. O `app.py` na raiz é o ponto de entrada da dashboard."

**Fase 1 (1:15 — 2:15)**

> "Começando pela Fase 1. O sistema permite cadastrar áreas de plantio. Vou cadastrar um café com 100 metros de comprimento, 50 de largura, dose de 0.5 kg por metro. Repare que o sistema calcula a área total e a quantidade de fertilizante automaticamente — e persiste no banco SQLite local. Posso listar, editar, e excluir registros. Isso atende exatamente ao que a Fase 1 do enunciado pede: cálculo de área e gestão de insumos."

**Fase 2 (2:15 — 3:15)**

> "Na Fase 2, integramos com a API OpenWeather. Vou consultar o clima atual de São Paulo. O sistema retorna temperatura, umidade do ar, pressão, e — o mais importante — uma recomendação automática de irrigação baseada no clima atual e na previsão das próximas horas. Se há chuva prevista, o sistema recomenda NÃO irrigar, evitando desperdício de água."

**Fase 3 (3:15 — 4:15)**

> "Aqui está o banco de dados estruturado dos sensores IoT — esta é a Fase 3. Reproduzi em SQLite o mesmo schema da tabela Oracle que usei na fase original. Veja as 300 leituras carregadas. O gráfico mostra a evolução da umidade e do pH ao longo do tempo. Posso inserir uma nova leitura, e o sistema decide automaticamente se a irrigação deve ser ligada."

**Fase 4 (4:15 — 5:30)**

> "A Fase 4 é o coração analítico do sistema: Machine Learning. Vou treinar quatro modelos: umidade, pH, irrigação e rendimento esperado. Olha as métricas: o modelo de irrigação tem R² de 0.93, o de rendimento 0.98. Agora vou usar a predição interativa: simulo umidade de 45%, pH 6.2, temperatura 28°C — o sistema prevê que SIM, deve irrigar. E ainda gera alertas baseados em regras de negócio."

**Fase 6 (5:30 — 6:45)**

> "A Fase 6 é o módulo de visão computacional baseado em YOLOv5. Escolho uma imagem de teste — um carro — e clico em 'Analisar'. O sistema detecta com 95% de confiança. Repare que essa confiança alta passa do limiar e o sistema oferece disparar um alerta SNS automaticamente. Agora faço o mesmo com um drone — mesma coisa. Isso é seguração patrimonial: detectar veículos não autorizados no perímetro da fazenda."

**Fase 5 — AWS SNS (6:45 — 8:30)** ⭐ _Parte mais crítica do vídeo_

> "Agora a Fase 5: a integração com a AWS. Aqui mostro o console do AWS SNS — vejam meu tópico 'farmtech-alerts' criado. Tenho meu e-mail confirmado como inscrito. Voltando à dashboard, posso disparar alertas direto daqui. Vou simular uma condição crítica: umidade 35%, pH 5.7, temperatura 33°C. Clique em 'Disparar alerta SNS'. Pronto, a mensagem foi publicada — e agora abro meu e-mail. Olha aí: o alerta chegou, com as ações recomendadas: 'Ativar bomba de irrigação imediatamente', 'Aplicar calcário', 'Monitorar estresse térmico'. Mensageria funcionando ponta a ponta."

**Documentação GitHub (8:30 — 9:30)**

> "Abro o GitHub. O repositório tem a mesma estrutura do projeto local. O README é detalhado: explica como rodar, como configurar a AWS, mostra o diagrama de arquitetura, e tem prints do console AWS. A pasta `docs` tem o diagrama de fluxo de dados. Todo o código está comentado em inglês, com docstrings."

**Encerramento (9:30 — 10:00)**

> "Para fechar: a Fase 7 entrega uma dashboard unificada, alertas reais via AWS SNS, e meu Ir Além usa AWS Rekognition — mostro isso no segundo vídeo. O link do GitHub está no portal da FIAP. Obrigado!"

---

## 🎬 VÍDEO 2 — Ir Além AWS Rekognition (até 5 minutos)

### Preparação antes de gravar

- [ ] Ter conta AWS ativa com Rekognition habilitado (us-east-1)
- [ ] Ter um usuário IAM com `AmazonRekognitionReadOnlyAccess`
- [ ] `aws configure` rodado com sucesso
- [ ] Imagens variadas em `dataset/images/test/` (carro, drone, plantação)
- [ ] App rodando

### Estrutura (com tempos)

| Bloco | Tempo | Conteúdo |
|-------|-------|----------|
| 0. Abertura | 0:00 — 0:20 | Identifique-se + escopo do "Ir Além" |
| 1. Por que Rekognition | 0:20 — 1:00 | Justificativa técnica |
| 2. Console AWS — IAM | 1:00 — 1:45 | Mostre usuário, policy, screenshots de configuração |
| 3. Console AWS — Rekognition | 1:45 — 2:30 | Painel do serviço, demonstração da API DetectLabels no console |
| 4. Integração na dashboard | 2:30 — 3:45 | Selecione imagem → analise → veja resposta + ações |
| 5. Integração com SNS | 3:45 — 4:30 | Demonstre o trigger automático quando há detecção crítica |
| 6. Encerramento | 4:30 — 5:00 | Arquitetura + GitHub |

### Falas sugeridas

**Abertura (0:00 — 0:20)**

> "Richard Schmitz, RM 567951, FIAP. Este é o vídeo do meu 'Ir Além' da Fase 7: a integração com o AWS Rekognition, complementando a visão computacional local da Fase 6."

**Por que Rekognition (0:20 — 1:00)**

> "O Rekognition é um serviço gerenciado de visão computacional da AWS. Diferente do meu YOLOv5 local, que detecta só carros e drones, o Rekognition já vem pré-treinado em milhões de imagens e reconhece centenas de classes: pessoas, animais, fogo, fumaça, plantas, veículos. Para uma fazenda, isso significa segurança em camadas: o YOLOv5 cuida do perímetro, o Rekognition cuida do inesperado."

**IAM (1:00 — 1:45)**

> "Aqui está meu console AWS. Crei um usuário IAM chamado 'farmtech-rekognition' com a policy gerenciada `AmazonRekognitionReadOnlyAccess`. Veja a permissão `rekognition:DetectLabels` — é a única que preciso. Apliquei o princípio do menor privilégio, alinhado com as boas práticas ISO 27001 que estudamos na Fase 5."
>
> _[Mostre prints já tirados: usuário criado, policy attached, access key gerada]_

**Console Rekognition (1:45 — 2:30)**

> "Agora vou ao serviço Rekognition. Faço upload de uma imagem aqui no console — uma foto de drone — e clico em 'Detect labels'. Veja: detecta 'Aircraft' com 99% de confiança, 'Vehicle' com 97%, 'Drone' com 95%. Tudo já pré-treinado, sem custos de treinamento."

**Integração na dashboard (2:30 — 3:45)**

> "Agora a integração real, programática, dentro do meu sistema. Abro a dashboard, vou para 'Ir Além — AWS Rekognition'. Seleciono uma imagem do meu dataset. Clico 'Analisar com AWS Rekognition'. O sistema envia a imagem via boto3 para a AWS, recebe os rótulos, e — esta é a parte interessante — eu mapeio os rótulos para ações da fazenda. Se detectar 'drone', a ação é 'verificar autorização'. Se detectar 'fire', a ação é 'alertar bombeiros imediatamente'."

**Integração com SNS (3:45 — 4:30)**

> "E veja a integração com a Fase 5: quando o Rekognition retorna uma classe sensível, o sistema marca 'requires_alert' como verdadeiro, e oferece disparar um alerta SNS. Isso faz com que toda a infraestrutura — Rekognition + SNS — trabalhe junta: a IA detecta, o SNS notifica os funcionários por e-mail e SMS. É o sistema funcionando ponta a ponta na AWS."

**Encerramento (4:30 — 5:00)**

> "Resumo da arquitetura: imagem → boto3 → Rekognition → interpretação → SNS → funcionário. Tudo está no meu GitHub, na seção 'Ir Além' do README, incluindo prints do console e código comentado. Obrigado!"

---

## 📝 Checklist final antes de publicar

### Para o vídeo principal (10 min)
- [ ] Vídeo dentro de 10 minutos
- [ ] Cobre todas as Fases 1, 2, 3, 4, 5 e 6
- [ ] Mostra o e-mail recebido via SNS
- [ ] Postado no YouTube como "não listado"
- [ ] Link colado no README na seção "Vídeo demonstrativo"

### Para o vídeo Ir Além (5 min)
- [ ] Vídeo dentro de 5 minutos
- [ ] Mostra console AWS com prints (mesmo que serviço esteja bloqueado)
- [ ] Demonstra integração programática (mesmo se for só código + simulação)
- [ ] Postado como "não listado"
- [ ] Link colado no README na seção "Ir Além"

### Repositório GitHub
- [ ] Criado com nome do grupo (você é solo — pode usar `FarmTech-Solutions-Fase7` ou similar)
- [ ] Estrutura espelha 100% a pasta local
- [ ] **Nenhum commit após o prazo de 10/06/2026**
- [ ] Compartilhe acesso (se quiser privado) com `SabrinaOtoni` e `anacrissantos` no GitHub
- [ ] Link enviado pelo portal FIAP (em PDF se preferir)

### Prints AWS necessários no README
- [ ] `docs/aws/sns_topic_criado.png` — tópico SNS criado
- [ ] `docs/aws/sns_subscriptions.png` — inscrições e-mail/SMS confirmadas
- [ ] `docs/aws/sns_alerta_recebido.png` — e-mail / SMS chegando
- [ ] `docs/aws/rekognition_console.png` — console Rekognition
- [ ] `docs/aws/rekognition_resultado.png` — resultado DetectLabels
- [ ] `docs/aws/iam_rekognition_policy.png` — política IAM aplicada
