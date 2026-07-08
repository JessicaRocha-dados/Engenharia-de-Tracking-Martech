 # 🛒 Módulo 3: E-commerce, Consentimento e Visualização (Dias 29 a 42)

**Objetivo:** Estruturar dados transacionais de alto valor (Padrão GA4 E-commerce) e conectar com painéis de visualização estratégica.

## 📦 Etapa 1: Injeção do Payload Standard E-commerce (Dia 29)

A transição de métricas de engajamento (leads) para métricas transacionais (receita) exige a adoção rigorosa do **Esquema Padrão de E-commerce do Google Analytics 4**. 

Nesta primeira etapa, realizei a injeção manual de um payload completo para simular o evento `view_item` (visualização de produto).

**A Arquitetura do Dado Transacional:**
* **Objeto Raiz:** `ecommerce` (mandatório para relatórios de monetização).
* **Estrutura de Itens:** O array `items` mapeando as propriedades do produto (SKU, Nome, Categoria, Preço, Quantidade e Marca).

A auditoria no ambiente de depuração comprovou que o Google Tag Manager é capaz de interceptar e estruturar variáveis complexas de carrinho e catálogo.

**📸 Evidência Visual: Injeção e Estruturação do Payload de E-commerce**

Para garantir a rastreabilidade de ponta a ponta, a documentação abaixo comprova o envio do comando simulando o front-end do site e a recepção perfeitamente estruturada no ambiente do GTM.

![Injeção do Payload no Console](./Dia29_01-injecao-console-ecommerce.png)
*Imagem 1: Simulação do front-end injetando o payload transacional de E-commerce via console.*

![Data Layer do Evento view_item](./Dia29_02-view-item-datalayer.png)
*Imagem 2: Inspeção do Tag Assistant confirmando a captura e formatação do objeto ecommerce e do array items.*

---
