import pandas as pd
import os
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais_gcp.json"

print("--- DIA 47: Iniciando Pipeline ELT - Camada Silver ---")
print("Objetivo: Limpeza, tipagem e padronização (Data Quality).\n")

# 1. EXTRAÇÃO: Lendo da Camada Bronze direto do BigQuery
print("Lendo dados da camada Bronze no BigQuery...")
client = bigquery.Client(project='portifolio-martech')
df_silver = client.query(
    "SELECT * FROM `portifolio-martech.bronze.eventos_ga4`").to_dataframe()

print("1. Visão do Dado Bruto (Bronze) antes da limpeza:")
print(df_silver[['event_date', 'country', 'user_pseudo_id']].head(3))
print("\nIniciando transformações...\n")

# 2. TRANSFORMAÇÃO: Camada Silver

# A. Conversão de Tipagem (Data)
df_silver['event_date'] = pd.to_datetime(
    df_silver['event_date'].astype(str), format='%Y%m%d')

# B. Tratamento de Nulos (NaN)
df_silver['country'] = df_silver['country'].fillna('NÃO INFORMADO')
df_silver['user_pseudo_id'] = df_silver['user_pseudo_id'].fillna('ID_AUSENTE')

# C. Padronização de Strings
df_silver['country'] = df_silver['country'].str.upper()

print("---------------------------------------------------")
print("2. Visão do Dado Limpo (Silver) após a limpeza:")
print(df_silver[['event_date', 'country', 'user_pseudo_id']].head(3))
print("\nTipagem atual da coluna event_date:", df_silver['event_date'].dtype)

# Adicionando as colunas de governança de dados
print(df_silver[['event_date', 'country', 'user_pseudo_id',
      '_ingestion_timestamp', '_source_file']].head(3))
print("\nTipagem atual da coluna event_date:", df_silver['event_date'].dtype)

# 3. CARGA: Salvando o resultado direto no BigQuery
print("\nEnviando dados tratados para a Camada Silver no BigQuery...")
df_silver.to_gbq(
    destination_table='silver.eventos_ga4',
    project_id='portifolio-martech',
    if_exists='replace'
)
print("Carga Silver concluída com sucesso!")
