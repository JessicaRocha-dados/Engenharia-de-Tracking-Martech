import pandas as pd
import os
from datetime import datetime
from google.cloud import bigquery
import uuid
import time
from utils_observabilidade import registrar_execucao

print("Conectando ao BigQuery via Workload Identity...")
# Inicializa o cliente de forma limpa, herdando automaticamente o token seguro do GitHub Actions
client = bigquery.Client(project='portfolio-martech')

# Inicia o cronômetro e cria um ID único para esta execução
run_id = str(uuid.uuid4())
inicio_etapa = time.time()
print(f"Iniciando a etapa Bronze. Run ID: {run_id}")

try:
    # Query de extração dos dados brutos do GA4
    query = """
        SELECT event_date, event_timestamp, event_name,
               user_pseudo_id, geo.country AS country
        FROM `portfolio-martech.analytics_538183128.events_*`
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
    particao_hoje = hoje.strftime('%Y%m%d')
    tabela_destino = f'portfolio-martech.bronze.eventos_ga4${particao_hoje}'

    config_carga = bigquery.LoadJobConfig(
        write_disposition='WRITE_TRUNCATE',
        time_partitioning=bigquery.TimePartitioning(field='_ingestion_date'),
    )

    client.load_table_from_dataframe(
        bq_df, tabela_destino, job_config=config_carga
    ).result()

    # REGISTO DE SUCESSO
    registrar_execucao(client, 'bronze', 'sucesso',
                       len(bq_df), inicio_etapa, run_id)
    print("✅ Ingestão Incremental da Camada Bronze concluída com sucesso!")

except Exception as erro:
    # REGISTO DE FALHA
    registrar_execucao(client, 'bronze', 'falha', 0, inicio_etapa, run_id)
    print(f"❌ Erro catastrófico na etapa Bronze: {erro}")
    raise
