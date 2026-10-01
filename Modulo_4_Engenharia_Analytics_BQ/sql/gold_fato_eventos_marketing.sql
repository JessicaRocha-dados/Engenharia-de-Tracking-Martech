SELECT 
    event_date AS data_evento, 
    country AS pais,
    COUNT(DISTINCT user_pseudo_id) AS total_usuarios_unicos, 
    COUNT(event_name) AS total_interacoes,
    COUNTIF(user_pseudo_id IS NULL) AS eventos_sem_id,
    DATE(@data_alvo) AS data_ingestao
FROM `portifolio-martech.silver.eventos_ga4`
WHERE _ingestion_date = DATE(@data_alvo)
GROUP BY event_date, country, data_ingestao;