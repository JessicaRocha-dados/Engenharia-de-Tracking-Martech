import os
from google.cloud import bigquery

# Credenciais
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais_gcp.json"
client = bigquery.Client(project='portifolio-martech')

print("Executando modelagem da Camada Gold (Modo Full Refresh)...")

# Lendo da pasta sql dinamicamente
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_sql = os.path.join(diretorio_atual, 'sql', 'gold_fato_eventos_marketing.sql')

with open(caminho_sql, 'r') as file:
    sql = file.read()

print("Enviando comando para o BigQuery processar...")

# Tabela de destino SEM o sufixo de partição sobrescrevendo tudo
tabela_destino = 'portifolio-martech.gold.fato_eventos_marketing'

# Configuração para sobrescrever a tabela inteira, mas mantendo a organização da partição
config_carga = bigquery.QueryJobConfig(
    destination=tabela_destino,
    write_disposition='WRITE_TRUNCATE',
    time_partitioning=bigquery.TimePartitioning(field='data_ingestao') 
)

# Executa a query diretamente no BigQuery 
client.query(sql, job_config=config_carga).result()

print("✅ Camada Gold (Full Refresh) concluída com sucesso! ")
