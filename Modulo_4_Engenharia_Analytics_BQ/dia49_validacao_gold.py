import os
import logging
import time
import uuid
from google.cloud import bigquery
from utils_observabilidade import registrar_execucao

# Ajuste de Autenticação
if os.path.exists("credenciais_gcp.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais_gcp.json"

client = bigquery.Client(project='portifolio-martech')

# Configura o log
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
T = 'portifolio-martech.gold.fato_eventos_marketing'

# Inicia o cronômetro e cria um ID único para esta execução
run_id = str(uuid.uuid4())
inicio_etapa = time.time()
print(f"Iniciando a etapa de Validação. Run ID: {run_id}")

try:
    print("Iniciando bateria de testes de qualidade na Camada Gold...")

    # --- TESTE DE SCHEMA ---
    print("Validando Schema (Estrutura de Colunas)...")
    tabela = client.get_table(T)
    colunas = {c.name for c in tabela.schema}
    esperadas = {'data_evento', 'pais',
                 'total_usuarios_unicos', 'total_interacoes'}

    # Se faltar alguma coluna, o assert vai travar a execução imediatamente
    assert esperadas.issubset(
        colunas), f'Colunas faltando: {esperadas - colunas}'
    logging.info('OK: schema validado (Todas as colunas presentes)')
    # -----------------------------

    # Dicionário de testes de dados
    checks = {
        'tabela vazia': (f'SELECT COUNT(*) AS n FROM `{T}`', lambda n: n > 0),
        'chaves nulas': (f'SELECT COUNT(*) AS n FROM `{T}` WHERE data_evento IS NULL OR pais IS NULL', lambda n: n == 0),
        'frescor (dias)': (f'SELECT DATE_DIFF(CURRENT_DATE(), MAX(data_evento), DAY) AS n FROM `{T}`', lambda n: n <= 365),
        'duplicidade': (f'SELECT COUNT(*) AS n FROM (SELECT 1 FROM `{T}` GROUP BY data_evento, pais HAVING COUNT(*) > 1)', lambda n: n == 0),
    }

    falhas = []
    # Variável para contar quantos registros a tabela validada tem, apenas para o log de observabilidade
    total_linhas_validadas = 0

    for nome, (sql, ok) in checks.items():
        # Executa cada query de validação
        valor = list(client.query(sql))[0]['n']

        # Guarda o total de linhas do primeiro teste para reportarmos na observabilidade
        if nome == 'tabela vazia':
            total_linhas_validadas = valor

        # Valida a regra
        if ok(valor):
            logging.info('OK: %s (valor=%s)', nome, valor)
        else:
            logging.error('FALHOU: %s (valor=%s)', nome, valor)
            falhas.append(nome)

    # Verifica se houve alguma falha
    if falhas:
        raise RuntimeError(f'Testes falharam: {falhas}')
    else:
        # REGISTO DE SUCESSO (Se todos os testes passarem)
        registrar_execucao(client, 'validacao', 'sucesso',
                           total_linhas_validadas, inicio_etapa, run_id)
        print("✅ Todos os testes de qualidade (Schema + Dados) passaram com sucesso!")

except Exception as erro:
    # REGISTO DE FALHA (Seja falha de schema ou de dados)
    registrar_execucao(client, 'validacao', 'falha', 0, inicio_etapa, run_id)
    print(f"❌ Erro na etapa de Validação: {erro}")
    raise
