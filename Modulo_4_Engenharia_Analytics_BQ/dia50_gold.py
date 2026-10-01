import os
import pandas as pd
from datetime import datetime
from google.cloud import bigquery

# Credenciais
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais_gcp.json"
client = bigquery.Client(project='portifolio-martech')

hoje = datetime.now()
data_alvo = hoje.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD para o SQL
particao_hoje = hoje.strftime('%Y%m%d')  # Formato YYYYMMDD para o Decorador

print(f"Executando modelagem da Camada Gold para a data: {data_alvo}...")

# Lendo da pasta sql
with open('sql/gold_fato_eventos_marketing.sql', 'r') as file:
    sql_template = file.read()

sql = sql_template.replace('@data_alvo', f"'{data_alvo}'")

df_gold = client.query(sql).to_dataframe()

# Converte as colunas de datas para o formato datetime do Pandas
df_gold['data_evento'] = pd.to_datetime(df_gold['data_evento'])
df_gold['data_ingestao'] = pd.to_datetime(df_gold['data_ingestao'])

print("Carregando tabela no BigQuery (Gold - Modo Sandbox)...")
tabela_destino = f'portifolio-martech.gold.fato_eventos_marketing${particao_hoje}'

config_carga = bigquery.LoadJobConfig(
    write_disposition='WRITE_TRUNCATE',
    time_partitioning=bigquery.TimePartitioning(
        field='data_ingestao'),  # Alterado para a ingestão!
)

client.load_table_from_dataframe(
    df_gold, tabela_destino, job_config=config_carga
).result()

print("✅ Camada Gold Incremental concluída com sucesso!")
