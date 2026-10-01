import pandas as pd
import os
from datetime import datetime
from google.cloud import bigquery

# Credenciais
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais_gcp.json"
client = bigquery.Client(project='portifolio-martech')

hoje = datetime.now()
data_alvo = hoje.date()
particao_hoje = hoje.strftime('%Y%m%d')

print(f"Extraindo dados da Bronze para a data alvo: {data_alvo}...")
# Lemos apenas os dados inseridos hoje (Carga Incremental)
query = f"""
    SELECT *
    FROM `portifolio-martech.bronze.eventos_ga4`
    WHERE _ingestion_date = '{data_alvo}'
"""
df_silver = client.query(query).to_dataframe()

print("Aplicando limpeza e regras de qualidade (Camada Silver)...")
# Converte a data do evento para o formato correto datetime
df_silver['event_date'] = pd.to_datetime(
    df_silver['event_date'], format='%Y%m%d')

#  A linha que preenchia user_pseudo_id com 'ID_AUSENTE' foi removida!
# Deixamos o ID como nulo para a camada Gold contar os eventos anônimos corretamente.

# Tratamento de nulos em outras colunas e padronização
df_silver['country'] = df_silver['country'].fillna('NÃO INFORMADO').str.upper()
df_silver['event_name'] = df_silver['event_name'].str.upper()

print("Carregando tabela no BigQuery (Silver - Modo Sandbox)...")
# Usamos o decorador de partição para sobrescrever apenas a "gaveta" de hoje
tabela_destino = f'portifolio-martech.silver.eventos_ga4${particao_hoje}'

config_carga = bigquery.LoadJobConfig(
    write_disposition='WRITE_TRUNCATE',
    time_partitioning=bigquery.TimePartitioning(field='_ingestion_date'),
)

client.load_table_from_dataframe(
    df_silver, tabela_destino, job_config=config_carga
).result()

print("✅ Limpeza e Carga Incremental da Camada Silver concluídas com sucesso!")
