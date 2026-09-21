#  Engenharia de Tracking & Martech: Infraestrutura e Qualidade de Dados

> "Um modelo de dados perfeito não salva uma coleta de dados ruim. Garbage in, garbage out."

Bem-vindo(a) ao repositório dos meus estudos e aplicações práticas em Engenharia de Rastreamento e Analytics.

Após concluir meu roteiro de 90 dias focado em Análise de Dados (SQL, Excel e Power BI), percebi na prática que um dos maiores gargalos do mercado não é a falta de dashboards, mas sim a fragmentação e a falta de confiabilidade dos dados na sua origem. 

Este repositório documenta a minha jornada contínua de aprendizado para construir bases sólidas de coleta de dados. O objetivo aqui é investigar problemas reais e garantir que a coleta seja estruturada e fiel à realidade antes de chegar a qualquer modelo de Machine Learning ou painel de BI.

## 🛠️ Stack Tecnológica

* **Coleta e Lógica:** Google Tag Manager (GTM Client-Side & Server-Side), JavaScript (Custom JS), HTML/CSS (DOM Scraping).
* **Analytics e Negócios:** Google Analytics 4 (GA4), Estrutura de E-commerce, Consent Mode V2.
* **Engenharia e Banco de Dados:** Google BigQuery, SQL (foco em UNNEST e recálculo de métricas brutas).
* **Visualização:** Looker Studio.

## 📅 Estrutura do Projeto (Roadmap de Estudos)

Aqui você encontrará os scripts, arquiteturas (Data Layers) e queries SQL que venho desenvolvendo e documentando, divididos por fases de aprendizado:

### 📁 Fase 1: Os Fundamentos da Coleta (GA4 + GTM Web)
A base do rastreamento web. Estruturação de Variáveis, Acionadores, Tags, Auto-Event Tracking e garantia de qualidade (QA) via fluxo de DebugView.

### 📁 Fase 2: O Motor do Tracking e Lógica Avançada
Evolução na confiabilidade dos dados: abandono de regras baseadas em CSS (que são frágeis) e adoção do padrão dataLayer. Construção de eventos personalizados, tabelas de Regex e injeção de Custom JS.

### 📁 Fase 3: E-commerce, Consentimento e Visualização
Aplicação do esquema oficial de Items Array do Google para funis transacionais (do `view_item` até `purchase`), adequação à LGPD (Consent Mode V2) e montagem de dashboards executivos.

### 📁 Fase 4: Nuvem, Server-Side e Engenharia Analytics
A intersecção com a Engenharia de Dados. Estudos práticos sobre provisionamento de servidor na nuvem para Server-Side GTM, contorno de bloqueadores (ITPs), exportação de dados brutos para o BigQuery e queries SQL para recálculo de métricas como LTV e ROI.

---

## 👩‍💻 Sobre a Autora

**Jéssica Rocha**  
Recém-formada no CST em Ciência de Dados e profissional atuando de forma autônoma estruturando soluções de métricas para clientes de tráfego pago. 

Acredito no poder de aprender em público e de colocar a mão na massa. Todo o código e documentação presentes aqui refletem meu momento atual: uma profissional em início de jornada, focada em investigar problemas, documentar acertos e erros, e construir uma base técnica sólida aplicável ao mundo real.

📫 **Acompanhe minhas atualizações e conexões:** [https://www.linkedin.com/in/jessica-rocha-dados/]
