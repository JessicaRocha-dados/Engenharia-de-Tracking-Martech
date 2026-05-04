# 🌐 Dia 01: O Ecossistema Web e a "Matrix" do Navegador

**Módulo:** 1 (Os Fundamentos da Coleta)  
**Status:** Concluído ✔️

## 🎯 Objetivo do Dia
Entender a base da internet (a comunicação Client-Server) e aprender a utilizar a aba **Network (Rede)** do navegador para inspecionar os disparos reais de rastreamento, antes de abrir ferramentas como GTM ou GA4.

## 🧠 Teoria Absorvida

Para atuar com engenharia de rastreamento, é preciso entender que a web funciona através de um fluxo contínuo de **Requisições e Respostas**.
* **O Navegador (Client):** Solicita as informações e interage com o usuário.
* **O Servidor (Server):** Devolve os arquivos que constroem a experiência (HTML, CSS, JS) e recebe os dados de volta.

**Os agentes do Tracking Client-Side:**
1. **Scripts (JavaScript):** São os "trabalhadores" dinâmicos. Eles rodam na página do navegador, "escutando" as interações do usuário (cliques, rolagens, adições ao carrinho).
2. **Cookies (1st e 3rd Party):** Arquivos de texto que dão "memória" ao navegador. Sem eles, o protocolo HTTP sofre de amnésia a cada clique.
3. **Payloads (Disparos):** É o pacote de dados empacotado pelo Script e enviado de volta ao servidor quando um evento acontece.

---

## 💻 Prática: Inspecionando o Tráfego (O caso Amazon)

Utilizei o **DevTools (F12)** no e-commerce da Amazon, focando na aba **Network (Rede)** — a verdadeira mesa de cirurgia de quem trabalha com dados na web.

### Laboratório executado:

1. Filtrei o tráfego por **JS** (JavaScript) e observei a "cachoeira" de scripts de terceiros sendo carregados apenas para montar a página inicial.

![Inspecionando os arquivos JavaScript](Dia01_tracking_martech.png)

2. Limpei o console e alterei o filtro para **Fetch/XHR** para monitorar a comunicação silenciosa de dados.
3. **A captura:** Ao interagir com o site e clicar em um produto (Havaianas), interceptei em tempo real as requisições disparando na aba Rede.

![Capturando os eventos XHR/Fetch em tempo real](Dia01_tracking_martech02.png)

Essas requisições `fetch/xhr` são o coração do Martech: pacotes de dados saindo do meu navegador avisando os servidores da Amazon sobre a minha interação exata.

---

## 💡 Insight Principal
> *Garbage in, garbage out.* Se um bloqueador de anúncios (AdBlock) ou uma restrição de navegador (ITP da Apple) barrar essa requisição `fetch` na aba Network, o dado morre ali. Ele nunca chegará ao Google Analytics ou ao BigQuery. A **Engenharia de Dados aplicada ao Marketing** começa na trincheira do navegador, garantindo que a requisição web aconteça com sucesso.

---
**Autora:** Jéssica Rocha  
*Estudante de Ciência de Dados & Engenharia de Analytics*

# 📊 Dia 02: Arquitetura de Dados e Mensuração de E-commerce (GA4)

Neste segundo dia de documentação, o foco foi sair da execução operacional e entrar na mentalidade de **Engenharia de Analytics**. Antes de configurar o Google Tag Manager, desenvolvemos o planejamento arquitetural estruturando o fluxo de dados de um e-commerce para garantir a precisão da coleta.

---

## 🎯 1. O Problema de Negócio (Discovery)

Para criar uma arquitetura de dados eficiente, partimos de perguntas reais que precisam ser respondidas para otimizar o ROI e a conversão:

*   **Validação de Intenção:** "Muitas pessoas clicam no botão de comprar, mas o item realmente entra no carrinho com sucesso?"
*   **Análise de Atrito:** "O usuário desiste da compra na reta final por causa do preço do produto ou pelo valor do frete?"
*   **Métricas de Performance:** "Como garantir que a receita e o ROI das campanhas no banco de dados reflitam o faturamento real, sem vendas duplicadas?"

---

## 🧠 2. O Framework de Solução

Aplicamos o framework de **Solution Design Reference (SDR)**, focado em Marketing Performance:

1.  **Discovery:** Entendimento das métricas de sucesso e perguntas de negócio.
2.  **Jornada do Usuário:** Mapeamento do caminho no site (Vitrine ➔ Carrinho ➔ Checkout ➔ Compra Confirmada).
3.  **O Verbo (Eventos GA4):** Tradução dos gatilhos para a nomenclatura padrão do Google Analytics 4.
4.  **O Payload (Contexto):** Definição dos parâmetros globais e da matriz de itens (`array`) necessários para dar contexto à ação.
5.  **O Entregável:** A consolidação do Dicionário de Dados e do Fluxograma visual.

---

## 📑 3. Dicionário de Dados (SDR)

Abaixo está o mapeamento técnico dos eventos que serão implementados na camada de dados (DataLayer). O parâmetro `items` deve acompanhar o usuário em toda a jornada para manter a integridade do funil.

| Etapa do Funil | Evento (Verbo) | Parâmetros Globais | Parâmetros do Array (`items`) | Objetivo de Negócio |
| :--- | :--- | :--- | :--- | :--- |
| **Vitrine** | `view_item` | `currency`, `value` | `item_id`, `item_name`, `price` | Medir o interesse inicial em produtos específicos. |
| **Carrinho** | `add_to_cart` | `currency`, `value` | *Mesmos do passo anterior* + `quantity` | Identificar taxa de adição ao carrinho e volume. |
| **Checkout** | `begin_checkout` | `currency`, `value` | *Mesmos do passo anterior* | Medir abandono na tela de pagamento. |
| **Fechamento** | `purchase` | `transaction_id`, `currency`, `value` | *Mesmos do passo anterior* | Validar faturamento real e calcular ROI das campanhas. |

> **Nota Técnica:** O disparo do evento `add_to_cart` foi definido para ocorrer **apenas na confirmação de sucesso** do sistema, garantindo a integridade dos dados e evitando o registro de falsos positivos no fluxo de conversão.

---

## 🗺️ 4. Fluxograma Arquitetural

Abaixo está a representação visual da esteira de dados, detalhando como os parâmetros de nível superior e os arrays de produtos interagem em cada disparo para o GA4.

![Fluxograma de Arquitetura do E-commerce](./arquitetura_ecommerce_ga4.png)
