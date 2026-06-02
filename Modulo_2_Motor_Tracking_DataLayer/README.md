##  Módulo 2: Tracking e Lógica Avançada
**Objetivo:** Parar de depender de CSS (raspagem de tela), utilizar o Data Layer como fonte da verdade e aplicar lógica de programação no Google Tag Manager.


###  Dia 15: O Conceito de Data Layer (Camada de Dados)

####  Visão Geral da Teoria
O Data Layer (Camada de Dados) é um objeto JavaScript do tipo *Array* (uma lista) que armazena informações estruturadas. Ele funciona como uma ponte de comunicação blindada entre o back-end/front-end do site e o Google Tag Manager. 

Ao invés do GTM tentar "adivinhar" dados lendo textos na tela (o que quebra se o layout mudar), a equipe de engenharia do site injeta os dados reais diretamente nesta camada invisível.

**A Regra de Ouro da Injeção de Dados:**
* **Declaração (`=`):** Sobrescreve e apaga o histórico do GTM. Deve ser evitado após o carregamento inicial da página.
* **O Método `.push()`:** O padrão ouro. Adiciona novas informações ao final da lista (array) sem destruir os dados anteriores, acionando o GTM em tempo real a cada novo evento.



#### Laboratório Prático: Explorando a "Matrix"
A missão consistiu em acessar um e-commerce de grande porte (Nike) e inspecionar a arquitetura de dados deles diretamente pelo Console do navegador (DevTools).

**Passo 1: Destravando a Segurança do Navegador (Self-XSS)**
Ao tentar interagir com o console pela primeira vez, o Chrome ativa uma proteção contra *Self-XSS*. Foi necessário executar o comando `permitir colagem` para habilitar a execução de scripts no ambiente, um procedimento de segurança padrão para desenvolvedores e analistas.

![Destravando a Segurança do Console](dia15-datalayer-console-security.png)

**Passo 2: Inspeção do Array `dataLayer`**
Após liberar o console, executamos a chamada `dataLayer` para revelar os pacotes de dados injetados pela engenharia da Nike no carregamento da página. 

Ao expandir o Objeto `0`, pudemos ler chaves riquíssimas em detalhes, sem nenhuma dependência visual da página:
* `event: "pageView"` (aviso claro da ação).
* `platform: "web_mobile"` (identificação exata do ambiente).
* `user: {id: null, email: undefined...}` (comprovação do estado de navegação anônima/deslogada do usuário).

![Inspeção do Data Layer da Nike](dia15-datalayer-inspecao-array.png)

