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
print(f"Iniciando a etapa Gold (Fato + Semantic View). Run ID: {run_id}")

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

try:
    # =========================================================================
    # 1. Atualização da Tabela Fato (gold.fato_eventos_marketing)
    # =========================================================================
    print("1/2 - Executando carga da Tabela Fato (gold.fato_eventos_marketing)...")
    caminho_sql_fato = os.path.join(
        diretorio_atual, 'sql', 'gold_fato_eventos_marketing.sql'
    )
    with open(caminho_sql_fato, 'r', encoding='utf-8') as file:
        sql_fato = file.read()

    tabela_fato_id = "portifolio-martech.gold.fato_eventos_marketing"
    config_fato = bigquery.QueryJobConfig(
        destination=tabela_fato_id,
        write_disposition="WRITE_TRUNCATE",
        maximum_bytes_billed=50 * 1024 * 1024  # Trava FinOps: 50 MB
    )

    job_fato = client.query(sql_fato, job_config=config_fato)
    job_fato.result()

    linhas_fato = client.get_table(tabela_fato_id).num_rows
    registrar_execucao(client, 'gold_fato_eventos_marketing', 'sucesso',
                       linhas_fato, inicio_etapa, run_id)
    print(
        f"✅ Tabela Fato atualizada com sucesso! Total de linhas: {linhas_fato}")

    # =========================================================================
    # 2. Atualização da View Semântica (gold.vw_martech_customer_360)
    # =========================================================================
    print("2/2 - Executando atualização da View Semântica (Customer 360)...")
    caminho_sql_view = os.path.join(
        diretorio_atual, 'sql', 'gold_vw_martech_customer_360.sql'
    )
    with open(caminho_sql_view, 'r', encoding='utf-8') as file:
        sql_view = file.read()

    config_view = bigquery.QueryJobConfig(
        maximum_bytes_billed=50 * 1024 * 1024  # Trava FinOps: 50 MB
    )

    job_view = client.query(sql_view, job_config=config_view)
    job_view.result()

    linhas_afetadas = job_view.num_dml_affected_rows or 0
    registrar_execucao(client, 'gold_customer_360', 'sucesso',
                       linhas_afetadas, inicio_etapa, run_id)
    print("✅ Camada Gold (Fato + Customer 360 View) atualizada e blindada com sucesso!")

except Exception as erro:
    registrar_execucao(client, 'gold_customer_360',
                       'falha', 0, inicio_etapa, run_id)
    print(f"❌ Erro na etapa Gold: {erro}")
    raise
