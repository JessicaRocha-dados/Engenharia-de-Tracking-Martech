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
2. **Cookies (1st e 3rd Party):** Arquivos de texto que dão "memória" ao navegador. Sem eles, o protocolo HTTP sofre de amnésia a cada clique. Eles são a base da identificação de usuários.
3. **Payloads (Disparos):** É o pacote de dados empacotado pelo Script e enviado de volta ao servidor quando um evento acontece.

## 💻 Prática: Inspecionando o Tráfego (O caso Amazon)

Para sair da teoria, acessei o e-commerce da Amazon e utilizei o **DevTools (F12)**, focando na aba **Network (Rede)** — a verdadeira mesa de cirurgia de quem trabalha com dados na web.

**Laboratório executado:**
1. Filtrei o tráfego por **JS** (JavaScript) e observei a "cachoeira" de scripts de terceiros sendo carregados apenas para montar a página (identificando bibliotecas de rastreamento).
2. Limpei o console e alterei o filtro para **Fetch/XHR** (o canal por onde os dados trafegam silenciosamente).
3. **A captura:** Ao clicar em um produto específico (um chinelo Havaianas), interceptei em tempo real as requisições disparando na aba Network (arquivos `EventTracking`). 

Essas requisições `fetch/xhr` são o coração do Martech: pacotes de dados saindo do meu navegador avisando os servidores da Amazon sobre a minha interação exata.

## 💡 Insight Principal
> *Garbage in, garbage out.* Se um bloqueador de anúncios (AdBlock) ou uma restrição de navegador (ITP da Apple) barrar essa requisição `fetch` na aba Network, o dado morre ali. Ele nunca chegará ao Google Analytics, Looker Studio ou BigQuery. A **Engenharia de Dados aplicada ao Marketing** começa na trincheira do navegador, garantindo que a requisição web aconteça com sucesso antes mesmo de pensarmos em modelagem ou dashboards.

---
➡️ *Próximo passo: Dia 02 - A Mentalidade GA4 e a Arquitetura de Eventos.*
