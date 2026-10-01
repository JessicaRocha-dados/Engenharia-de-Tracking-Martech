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

# Configuração das datas para filtrar apenas o mês desejado
config_extracao = bigquery.QueryJobConfig(query_parameters=[
    bigquery.ScalarQueryParameter('inicio', 'STRING', '20260901'),
    bigquery.ScalarQueryParameter('fim', 'STRING', '20260930'),
])

print("Extraindo dados do GA4...")
# Executa a query e transforma em DataFrame
bq_df = client.query(query, job_config=config_extracao).to_dataframe()

print("Adicionando metadados da Camada Bronze...")
hoje = datetime.now()
bq_df['_ingestion_timestamp'] = pd.to_datetime(hoje)
bq_df['_source_file'] = 'API_GA4_BigQuery'
bq_df['_ingestion_date'] = hoje.date()

print("Carregando tabela no BigQuery (Idempotência via Decorador de Partição)...")
# Formata a data de hoje para o formato YYYYMMDD (ex: 20261001)
particao_hoje = hoje.strftime('%Y%m%d')

# No modo Sandbox, anexamos o decorador de partição ($YYYYMMDD) ao nome da tabela.
tabela_destino = f'portifolio-martech.bronze.eventos_ga4${particao_hoje}'

# Usamos WRITE_TRUNCATE. Como especificamos a partição alvo acima,
# ele recria APENAS os dados de hoje, sem apagar o resto do histórico e sem precisar de DELETE!
config_carga = bigquery.LoadJobConfig(
    write_disposition='WRITE_TRUNCATE',
    time_partitioning=bigquery.TimePartitioning(field='_ingestion_date'),
)

client.load_table_from_dataframe(
    bq_df, tabela_destino, job_config=config_carga
).result()

print("✅ Ingestão Incremental da Camada Bronze concluída com sucesso!")
