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
print(f"Iniciando a etapa Gold. Run ID: {run_id}")

try:
    print("Executando modelagem da Camada Gold (Modo Full Refresh)...")

    # Lendo da pasta sql dinamicamente
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_sql = os.path.join(
        diretorio_atual, 'sql', 'gold_fato_eventos_marketing.sql')

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

    # Executa a query diretamente no BigQuery e aguarda a conclusão
    query_job = client.query(sql, job_config=config_carga)
    query_job.result()

    # O query_job.num_dml_affected_rows mostra as linhas afetadas,
    # mas em operações de DDL/overwrite às vezes vem vazio. Usamos 0 como fallback.
    linhas_afetadas = query_job.num_dml_affected_rows or 0

    # REGISTO DE SUCESSO
    registrar_execucao(client, 'gold', 'sucesso',
                       linhas_afetadas, inicio_etapa, run_id)
    print("✅ Camada Gold (Full Refresh) concluída com sucesso!")

except Exception as erro:
    # REGISTO DE FALHA
    registrar_execucao(client, 'gold', 'falha', 0, inicio_etapa, run_id)
    print(f"❌ Erro na etapa Gold: {erro}")
    raise
