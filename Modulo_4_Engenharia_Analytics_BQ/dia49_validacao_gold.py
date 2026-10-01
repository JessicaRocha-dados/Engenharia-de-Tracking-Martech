import os
import logging
from google.cloud import bigquery

# Credenciais e conexão
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais_gcp.json"
client = bigquery.Client(project='portifolio-martech')

# Configura o log
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
T = 'portifolio-martech.gold.fato_eventos_marketing'

print("Iniciando bateria de testes de qualidade na Camada Gold...")

# Dicionário de testes: 'Nome do teste': ('Query SQL', regra de aprovação)
checks = {
    'tabela vazia': (f'SELECT COUNT(*) AS n FROM `{T}`', lambda n: n > 0),
    'chaves nulas': (f'SELECT COUNT(*) AS n FROM `{T}` WHERE data_evento IS NULL OR pais IS NULL', lambda n: n == 0),
    'frescor (dias)': (f'SELECT DATE_DIFF(CURRENT_DATE(), MAX(data_evento), DAY) AS n FROM `{T}`', lambda n: n <= 15),
    'duplicidade': (f'SELECT COUNT(*) AS n FROM (SELECT 1 FROM `{T}` GROUP BY data_evento, pais HAVING COUNT(*) > 1)', lambda n: n == 0),
}

falhas = []
for nome, (sql, ok) in checks.items():
    # Executa cada query de validação
    valor = list(client.query(sql))[0]['n']

    # Valida a regra
    if ok(valor):
        logging.info('OK: %s (valor=%s)', nome, valor)
    else:
        logging.error('FALHOU: %s (valor=%s)', nome, valor)
        falhas.append(nome)

# Se houver falhas, levanta um erro com a lista de todos os problemas
if falhas:
    raise RuntimeError(f'Testes falharam: {falhas}')
else:
    print("✅ Todos os testes de qualidade passaram com sucesso!")
