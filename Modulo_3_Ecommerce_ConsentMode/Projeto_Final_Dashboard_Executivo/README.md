# 🚀 Projeto Final (Módulo 3): Dashboard Executivo no Looker Studio (Dias 35 a 37)

## 📖 Visão Geral
Este projeto final consolida a nossa jornada de engenharia de dados do Módulo 3. O objetivo é transformar os dados brutos de navegação e as conversões mapeadas via Data Layer em inteligência de negócios através de um painel executivo e visual no Looker Studio.

---

## 📅 Dia 35: Conexão e Infraestrutura de Dados
O foco inicial foi garantir a integridade da fundação técnica estabelecendo a conexão nativa entre a propriedade do GA4 e o Looker Studio. 

**Teoria Aplicada:**
Estudamos o impacto das **Cotas de API (API Quotas)** do GA4. Em painéis com alto volume de acessos simultâneos, o limite de requisições pode ser excedido, quebrando os gráficos. Para contornar isso em ambientes corporativos, documentamos a importância de utilizar a extração de dados estática (Extract Data) ou a exportação nativa para o BigQuery (via SQL) para sustentar a operação.

**Evidência Visual:**
![Conexão Nativa GA4](Dia35_01-conexao-ga4.png)

---

## 📅 Dia 36: Estruturação e Cruzamento Analítico
Com a base de dados conectada e segura, iniciamos a construção do esqueleto do dashboard aplicando a "Regra dos 5 Segundos" de design hierárquico (leitura em Z). O foco foi responder à pergunta central de negócios: *"Quais canais de aquisição trazem o tráfego mais qualificado?"*

**Prática Executada:**
* **Scorecards (Visão Geral):** Inserção de cartões no topo da tela para leitura rápida e absoluta do `Total de usuários` e dos `Eventos principais` (nomenclatura atualizada do GA4 para conversões).
* **Tabela Principal:** Cruzamento estratégico da dimensão de `Origem / mídia da sessão` com as métricas de volume e conversão para auditar o tráfego.
* **Proporção Visual:** Inserção de um gráfico de rosca para ilustrar rapidamente o peso e a dominância de cada canal de tráfego.

**Evidências Visuais:**
![Tabela de Conversões](Dia36_01-tabela-conversao.png)
![Dashboard com Scorecards e Gráfico](Dia36_02-dashboard-inicial.png)

---

## 📅 Dia 37: Refinamento e Filtros Dinâmicos
*(Em andamento - O painel receberá controles de período e refinamento de interface )*
