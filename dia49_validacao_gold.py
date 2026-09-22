from google.cloud import bigquery
from google.oauth2 import service_account

print("--- Iniciando Testes de Qualidade de Dados (Data Quality) ---")

# 1. Autenticação
credenciais = service_account.Credentials.from_service_account_file(
    'credenciais_gcp.json')
client = bigquery.Client(credentials=credenciais, project='portifolio-martech')

# 2. Definição da tabela
tabela_gold = "portifolio-martech.gold.fato_eventos_marketing"
print(f" Validando a tabela: {tabela_gold}...\n")

# ===========================================================
# TESTE 1: Integridade Técnica (Granularidade Duplicada)
# ==========================================================

# Chave primária composta é (data_evento, pais)
# OBS: Não podem existir duas linhas com o mesmo país no mesmo dia.
query_duplicatas = f"""
    SELECT COUNT(*) as qtd_duplicatas
    FROM (
        SELECT data_evento, pais, COUNT(*) as qtd
        FROM `{tabela_gold}`
        GROUP BY data_evento, pais
        HAVING qtd > 1
    )
"""
job_duplicatas = client.query(query_duplicatas)
resultado_duplicatas = list(job_duplicatas)[0].qtd_duplicatas

# O 'assert' atua como Circuit Breaker
assert resultado_duplicatas == 0, f"🚨 ALERTA DE INTEGRIDADE: Encontradas {resultado_duplicatas} combinações de data e país duplicadas!"
print("✅ Teste 1 (Integridade Técnica): Aprovado. Granularidade correta, sem duplicatas.")

# ==============================================
# TESTE 2: Regra de Negócio (Métricas Negativas)
# ==============================================
# OBS: O total de interações e de usuários únicos jamais pode ser menor que zero.

query_negativo = f"""
    SELECT COUNT(*) as qtd_erros
    FROM `{tabela_gold}`
    WHERE total_interacoes < 0 OR total_usuarios_unicos < 0
"""
job_negativo = client.query(query_negativo)
resultado_negativo = list(job_negativo)[0].qtd_erros

assert resultado_negativo == 0, f"🚨 ALERTA DE NEGÓCIO: Existem {resultado_negativo} registros com métricas negativas!"
print("✅ Teste 2 (Regra de Negócio): Aprovado. Nenhuma métrica negativa encontrada.")

# ==========================================
#                SUCESSO
# ==========================================
print("\n🚀 DATA QUALITY APROVADO! O pipeline está íntegro e a Camada Gold está liberada para o BI.")
