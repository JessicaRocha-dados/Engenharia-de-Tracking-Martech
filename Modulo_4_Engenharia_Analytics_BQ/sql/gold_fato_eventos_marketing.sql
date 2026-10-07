SELECT 
    event_date AS data_evento, 
    IFNULL(country, 'Desconhecido') AS pais,
    COUNT(DISTINCT user_pseudo_id) AS total_usuarios_unicos, 
    COUNT(event_name) AS total_interacoes,
    COUNTIF(user_pseudo_id IS NULL) AS eventos_sem_id,
    MAX(DATE(_ingestion_date)) AS data_ingestao
FROM `portifolio-martech.silver.eventos_ga4`
GROUP BY event_date, country