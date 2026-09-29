import pandas as pd
import os
from datetime import datetime
from google.cloud import bigquery

# Garante que o script encontre as credenciais quando rodar no GitHub Actions
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais_gcp.json"

print("Conectando ao BigQuery...")
# Inicializa o cliente apontando para o seu projeto
client = bigquery.Client(project='portifolio-martech')

# Query de extração dos dados brutos do GA4
query = """
    SELECT event_date, event_timestamp, event_name,
           user_pseudo_id, geo.country AS country
    FROM `portifolio-martech.analytics_538183128.events_*`
    WHERE _TABLE_SUFFIX BETWEEN @inicio AND @fim
"""

# Configuração das datas para filtrar apenas o mês desejado e evitar tabelas intraday
config = bigquery.QueryJobConfig(query_parameters=[
    bigquery.ScalarQueryParameter('inicio', 'STRING', '20260901'),
    bigquery.ScalarQueryParameter('fim', 'STRING', '20260930'),
])

print("Extraindo dados do GA4...")
# Executa a query e transforma em DataFrame
bq_df = client.query(query, job_config=config).to_dataframe()

print("Adicionando metadados da Camada Bronze...")
# Adiciona as colunas de metadados obrigatórias
bq_df['_ingestion_timestamp'] = pd.to_datetime(datetime.now())
bq_df['_source_file'] = 'API_GA4_BigQuery'

print("Carregando tabela no BigQuery...")
# Salva o DataFrame na camada Bronze (usando replace conforme a nossa limitação documentada)
bq_df.to_gbq(
    destination_table='bronze.eventos_ga4',
    project_id='portifolio-martech',
    if_exists='replace'
)

print("✅ Ingestão da Camada Bronze concluída com sucesso!")
