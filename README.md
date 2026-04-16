# 🚀 Engenharia de Tracking & Martech: 60 Dias de Imersão

> "Um modelo de dados perfeito não salva uma coleta de dados ruim. Garbage in, garbage out."

Bem-vindo(a) ao meu repositório de **Engenharia de Rastreamento e Analytics**. 

Após concluir uma imersão intensiva de 90 dias em Análise de Dados (SQL, Excel e Power BI), percebi que a verdadeira dor do mercado de marketing não é a falta de dashboards bonitos, mas sim a **fragmentação e a falta de confiabilidade dos dados na origem**. 

Este repositório documenta a minha jornada de 60 dias construindo soluções de infraestrutura do zero absoluto ao nível de engenharia, garantindo que a coleta de dados seja fiel à realidade antes de chegar a qualquer modelo de Machine Learning ou painel de BI.

---

## 🛠️ Stack Tecnológico
* **Coleta e Lógica:** Google Tag Manager (GTM Client-Side & Server-Side), JavaScript (Custom JS), HTML/CSS (DOM Scraping).
* **Analytics e Negócios:** Google Analytics 4 (GA4), Estrutura de E-commerce, Consent Mode V2.
* **Engenharia e Banco de Dados:** Google BigQuery, SQL (foco em `UNNEST` e recálculo de métricas brutas).
* **Visualização:** Looker Studio.

---

## 📅 Estrutura do Desafio (Roadmap)

Aqui você encontrará todos os scripts, arquiteturas (Data Layers) e queries SQL desenvolvidos durante o desafio, divididos por módulos:

### 📁 [Módulo 1: Os Fundamentos da Coleta (GA4 + GTM Web)](./Modulo_1_Fundamentos_GTM)
* **Dias 1 a 14:** A base da internet. Variáveis, Acionadores, Tags, Auto-Event Tracking e garantia de qualidade (QA) via DebugView.

### 📁 [Módulo 2: O Motor do Tracking e Lógica Avançada](./Modulo_2_Motor_Tracking_DataLayer)
* **Dias 15 a 28:** Abandono de regras baseadas em CSS (frágeis) e adoção do `dataLayer`. Construção de eventos personalizados, tabelas de Regex e injeção de Custom JS.

### 📁 [Módulo 3: E-commerce, Consentimento e Visualização](./Modulo_3_Ecommerce_ConsentMode)
* **Dias 29 a 42:** O esquema oficial de *Items Array* do Google, funis transacionais (`view_item` até `purchase`), adequação à LGPD (Consent Mode V2) e dashboards executivos.

### 📁 [Módulo 4: Nuvem, Server-Side e Engenharia Analytics](./Modulo_4_Engenharia_Analytics_BQ)
* **Dias 43 a 60:** A intersecção com a Ciência de Dados. Provisionamento de servidor (sGTM), contorno de ITPs, exportação de dados brutos para o BigQuery e queries SQL complexas para recálculo de LTV e ROI.

---

## 👩‍💻 Sobre a Autora
**Jéssica Rocha**
*Estudante de Ciência de Dados e profissional focada em Engenharia Analytics para Marketing (Martech).*

Acredito no poder de *aprender em público*. Todo o código aqui é voltado para resolver problemas do mundo real. 

📫 **Acompanhe as atualizações diárias:** [https://www.linkedin.com/in/jessica-rocha-dados/]
