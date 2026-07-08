#  Módulo 3: E-commerce, Consentimento e Visualização

**Objetivo:** Estruturar dados transacionais de alto valor (Padrão GA4 E-commerce) e conectar com painéis de visualização estratégica.

---

##  Dia 29: Injeção do Payload Standard E-commerce (`view_item`)

A transição de métricas de engajamento (leads) para métricas de receita (vendas) exige a adoção rigorosa do **Esquema Padrão de E-commerce do Google Analytics 4**. 

###  O que foi feito nesta etapa?
Para iniciar a arquitetura de tracking de e-commerce, atuei simulando o comportamento do código fonte do site (Front-end). 
Realizei a **injeção manual de um payload via console do navegador** para disparar o evento `view_item` (visualização de produto). O objetivo técnico foi auditar se o contêiner do GTM estava apto a interceptar e estruturar cargas complexas de dados transacionais antes de configurarmos o roteamento para o Analytics.

###  A Arquitetura do Dado Transacional
O código injetado seguiu estritamente as regras de taxonomia do Google:
* **Objeto Raiz:** A chave `ecommerce` encapsulando toda a transação (indispensável para relatórios de monetização).
* **Métricas Financeiras:** Parâmetros de `currency` (moeda) e `value` (valor total).
* **Estrutura de Itens (Array):** A lista `items` mapeando as propriedades comerciais exatas do produto (ID/SKU, Nome, Categoria, Marca, Preço e Quantidade).

A auditoria no ambiente de depuração (Debug Mode) comprovou o sucesso da operação, com o GTM formatando perfeitamente as variáveis no Data Layer.


### 📸 Evidências Visuais: Rastreabilidade de Ponta a Ponta

A documentação abaixo atesta o ciclo completo do dado: do disparo na interface (origem) à captura na Camada de Dados (destino).

![Injeção do Payload no Console](./Dia29_01-injecao-console-ecommerce.png)
*Imagem 1: Ação (Front-end) - Injeção do payload transacional simulando o comportamento do site.*

![Data Layer do Evento view_item](./Dia29_02-view-item-datalayer.png)
*Imagem 2: Reação (GTM) - Tag Assistant confirmando a captura e estruturação exata do objeto ecommerce e do array de produtos.*

---
