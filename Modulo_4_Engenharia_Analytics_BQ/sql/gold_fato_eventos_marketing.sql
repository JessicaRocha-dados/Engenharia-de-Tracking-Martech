CREATE OR REPLACE TABLE `portifolio-martech.gold.fato_eventos_marketing` AS
SELECT
    DATE(event_date) AS data_evento,
    country AS pais,
    COUNT(event_name) AS total_interacoes,
    COUNT(DISTINCT user_pseudo_id) AS total_usuarios_unicos
FROM `portifolio-martech.silver.eventos_ga4`
GROUP BY data_evento, pais;