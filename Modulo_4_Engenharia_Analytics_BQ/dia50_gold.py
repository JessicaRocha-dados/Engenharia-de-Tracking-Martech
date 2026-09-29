import os
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais_gcp.json"
client = bigquery.Client(project='portifolio-martech')

print("Processando a Camada Gold...")
sql = open(
    'Modulo_4_Engenharia_Analytics_BQ/sql/gold_fato_eventos_marketing.sql').read()
client.query(sql).result()

print('✅ Camada Gold atualizada com sucesso.')
