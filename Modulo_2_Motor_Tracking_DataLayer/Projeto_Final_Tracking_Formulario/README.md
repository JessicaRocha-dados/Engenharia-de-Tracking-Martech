#  Case Study: Refatoração de Tracking de Formulário

## 📌 Visão Geral do Projeto
Este projeto documenta a evolução da arquitetura de rastreamento de um formulário de captação de leads. O objetivo foi migrar de um acionador genérico (`Form Submission`), altamente propenso a disparos falsos, para uma estrutura robusta baseada em **Data Layer Push**.

Como o site utiliza formulários **AJAX** (sem recarregamento de página), a injeção do evento via Camada de Dados garante que o GTM e as plataformas de mídia (GA4 e Meta Ads) só registrem a conversão após a validação real do envio, eliminando a sujeira de dados na origem e garantindo a integridade dos relatórios de performance.

---

##  Etapas de Execução

- [x] **Etapa 1:** Planejamento Arquitetural (Dia 24)
- [ ] **Etapa 2:** Configuração do Gatilho Avançado (Dia 25)
- [ ] **Etapa 3:** Enriquecimento de Dados com Variáveis (Dia 26)
- [ ] **Etapa 4:** Configuração das Tags de Conversão (Dia 27)
- [ ] **Etapa 5:** QA, Validação de Disparo e Conclusão (Dia 28)

---

##  Etapa 1: Planejamento Arquitetural e Dicionário de Dados

A primeira decisão técnica foi abandonar abordagens passivas (como Visibilidade do Elemento) e atuar diretamente no código-fonte do site. Foi injetado um script na função de sucesso do formulário para empurrar um pacote de dados limpo para o GTM.

**Payload Definido (Dicionário de Dados):**
Para enriquecer a coleta e permitir segmentações futuras, definimos o seguinte padrão de envio no momento exato da conversão:

```javascript
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
    'event': 'lead_gerado',           // Gatilho principal e exclusivo da conversão
    'form_name': 'newsletter_home',   // Identificador de contexto do lead
    'lead_status': 'qualificado'      // Regra de negócio aplicada via código
});
```

### 📸 Evidência Visual: Disparo do Data Layer Push

![Tag Assistant capturando o evento lead_gerado na Camada de Dados](./Dia24_01-datalayer-push-lead.png)

Acima, o painel de Debug do GTM comprova a injeção do evento `lead_gerado` e do payload de contexto (`form_name` e `lead_status`) perfeitamente estruturados na Camada de Dados, atestando o sucesso da nova arquitetura no código-fonte.
