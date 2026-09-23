from google.cloud import bigquery
from google.oauth2 import service_account

print("--- Inicializando Setup da Arquitetura (GCP) ---")

# 1. Forçar a leitura direta do ficheiro JSON (ignora a cache do computador)
credenciais = service_account.Credentials.from_service_account_file(
    'credenciais_gcp.json')

# 2. Conectando ao GCP
client = bigquery.Client(credentials=credenciais, project='portifolio-martech')

# 3. Configurar e criar o Dataset Bronze
print("A criar Dataset da Camada Bronze...")
dataset_bronze = bigquery.Dataset('portifolio-martech.bronze')
dataset_bronze.location = "US"
client.create_dataset(dataset_bronze, exists_ok=True)

# 4. Configurar e criar o Dataset Silver
print("A criar Dataset da Camada Silver...")
dataset_silver = bigquery.Dataset('portifolio-martech.silver')
dataset_silver.location = "US"
client.create_dataset(dataset_silver, exists_ok=True)

print("\nSucesso! Conjuntos de dados 'bronze' e 'silver' criados.")
