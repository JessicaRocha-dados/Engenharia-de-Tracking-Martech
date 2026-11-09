-- Criação da Feature Table (View Semântica) de Visão do Cliente 360
CREATE OR REPLACE VIEW `portifolio-martech.gold.vw_martech_customer_360` AS

WITH extracao_base AS (
    SELECT
        user_pseudo_id,
        event_timestamp,
        event_name,
        -- Conversão de Data para Cálculo de Recência
        DATE(TIMESTAMP_MICROS(event_timestamp)) AS event_date,

        -- Extração Limpa de Parâmetros e Sessão
        (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_location') AS pagina_atual,
        (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS session_id,
        
        -- Valor Financeiro
        COALESCE(
            (SELECT value.double_value FROM UNNEST(event_params) WHERE key = 'value'),
            CAST((SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'value') AS FLOAT64),
            0.0
        ) AS event_value,
        
        geo.country AS pais,

        -- Motor de Lead Scoring
        CASE
            WHEN event_name = 'purchase' THEN 50
            WHEN event_name = 'generate_lead' THEN 20
            WHEN event_name = 'view_footer' THEN 5
            WHEN event_name = 'scroll' THEN 2
            WHEN event_name = 'page_view' THEN 1
            ELSE 0
        END AS pontos_evento
    FROM
        `portifolio-martech.analytics_538183128.events_*`
    WHERE
        -- Trava FinOps (Processamento Histórico Controlado)
        _TABLE_SUFFIX BETWEEN '20260901' AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
),

jornada_first_touch AS (
    SELECT
        *,
        -- Window Functions: Fixando a Origem
        FIRST_VALUE(pagina_atual) OVER(PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS primeira_pagina,
        FIRST_VALUE(pais) OVER(PARTITION BY user_pseudo_id ORDER BY event_timestamp ASC) AS pais_origem
    FROM
        extracao_base
),

consolidado_rfm AS (
    SELECT
        user_pseudo_id,
        ANY_VALUE(primeira_pagina) AS primeira_pagina,
        ANY_VALUE(pais_origem) AS pais_origem,

        -- Métrica [R] Recency
        DATE_DIFF(CURRENT_DATE(), MAX(event_date), DAY) AS recencia_dias,

        -- Métrica [F] Frequency
        COUNT(DISTINCT session_id) AS frequencia_sessoes,
        COUNT(event_name) AS total_eventos,

        -- Métrica [M] Monetary
        SUM(event_value) AS ltv_monetario,

        -- Métrica de Engajamento
        SUM(pontos_evento) AS martech_engagement_score
    FROM
        jornada_first_touch
    GROUP BY
        user_pseudo_id
)

-- Tabela de Atributos Final (Feature Table)
SELECT
    user_pseudo_id,
    primeira_pagina,
    pais_origem,
    recencia_dias,
    frequencia_sessoes,
    total_eventos,
    ltv_monetario,
    martech_engagement_score,
    -- Label de Classificação para MQLs
    CASE
        WHEN martech_engagement_score >= 50 THEN '4 - Cliente VIP'
        WHEN martech_engagement_score >= 20 THEN '3 - Quente (MQL)'
        WHEN martech_engagement_score BETWEEN 5 AND 19 THEN '2 - Morno'
        ELSE '1 - Frio'
    END AS segmentacao_lead
FROM
    consolidado_rfm;