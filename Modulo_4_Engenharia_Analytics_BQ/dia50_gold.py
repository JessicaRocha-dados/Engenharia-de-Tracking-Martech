import os
import time
import uuid
from google.cloud import bigquery
from utils_observabilidade import registrar_execucao

# Ajuste de Autenticação
if os.path.exists("credenciais_gcp.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais_gcp.json"

client = bigquery.Client(project='portifolio-martech')

# Inicia o cronômetro e cria um ID único para esta execução
run_id = str(uuid.uuid4())
inicio_etapa = time.time()
print(f"Iniciando a etapa Gold (Semantic View). Run ID: {run_id}")

try:
    print("Executando modelagem da Camada Gold (Customer 360)...")

    # 1. Lendo dinamicamente o arquivo SQL da View Semântica (GitOps)
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_sql = os.path.join(
        diretorio_atual, 'sql', 'gold_vw_martech_customer_360.sql')

    with open(caminho_sql, 'r') as file:
        sql = file.read()

    print("Enviando comando para o BigQuery criar/atualizar a View...")

    # 2. Configuração com Trava FinOps (Blindagem de Custos limitando a 50 MB)
    config_carga = bigquery.QueryJobConfig(
        maximum_bytes_billed=50 * 1024 * 1024  # 50 MB
    )

    # 3. Executa a query DDL diretamente no BigQuery e aguarda a conclusão
    query_job = client.query(sql, job_config=config_carga)
    query_job.result()

    # Como é criação de View, DML affected rows será vazio/nulo. Usamos 0.
    linhas_afetadas = query_job.num_dml_affected_rows or 0

    # REGISTO DE SUCESSO
    registrar_execucao(client, 'gold_customer_360', 'sucesso',
                       linhas_afetadas, inicio_etapa, run_id)
    print("✅ Camada Gold (Customer 360 View) atualizada e blindada com sucesso!")

except Exception as erro:
    # REGISTO DE FALHA
    registrar_execucao(client, 'gold_customer_360',
                       'falha', 0, inicio_etapa, run_id)
    print(f"❌ Erro na etapa Gold: {erro}")
    raise
