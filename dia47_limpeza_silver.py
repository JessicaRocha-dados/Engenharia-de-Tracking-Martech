import pandas as pd
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credenciais_gcp.json"

print("--- DIA 47: Iniciando Pipeline ELT - Camada Silver ---")
print("Objetivo: Limpeza, tipagem e padronização (Data Quality).\n")

# 1. EXTRAÇÃO: Lendo o arquivo bruto e imutável da Camada Bronze
df_silver = pd.read_csv('dia46_bronze_eventos_ga4.csv')
print("1. Visão do Dado Bruto (Bronze) antes da limpeza:")
print(df_silver[['event_date', 'country', 'user_pseudo_id']].head(3))
print("\nIniciando transformações...\n")

# 2. TRANSFORMAÇÃO: Camada Silver

# A. Conversão de Tipagem (Data)
# Transforma o inteiro 20260914 em texto '20260914' e depois converte para data '2026-09-14'
df_silver['event_date'] = pd.to_datetime(
    df_silver['event_date'].astype(str), format='%Y%m%d')

# B. Tratamento de Nulos (NaN)
# Se o GA4 falhou em capturar o país ou o ID, substituímos o vazio por um valor padrão
df_silver['country'] = df_silver['country'].fillna('NÃO INFORMADO')
df_silver['user_pseudo_id'] = df_silver['user_pseudo_id'].fillna('ID_AUSENTE')

# C. Padronização de Strings
# Padroniza todos os países para letras maiúsculas, garantindo uniformidade
df_silver['country'] = df_silver['country'].str.upper()

print("---------------------------------------------------")
print("2. Visão do Dado Limpo (Silver) após a limpeza:")
print(df_silver[['event_date', 'country', 'user_pseudo_id']].head(3))
print("\nTipagem atual da coluna event_date:", df_silver['event_date'].dtype)

# Adicionando as colunas de governança de dados
print(df_silver[['event_date', 'country', 'user_pseudo_id',
      '_ingestion_timestamp', '_source_file']].head(3))
print("\nTipagem atual da coluna event_date:", df_silver['event_date'].dtype)

# 3. CARGA: Salvando o resultado
df_silver.to_csv('dia47_silver_eventos_ga4.csv', index=False)
print("\nLog: Sucesso! Arquivo 'dia47_silver_eventos_ga4.csv' gerado e pronto para a Camada Gold.")

print("\nEnviando dados tratados para a Camada Silver no BigQuery...")
df_silver.to_gbq(
    destination_table='portifolio-martech.silver.eventos_ga4',
    project_id='portifolio-martech',
    if_exists='replace'
)
print("Carga Silver concluída com sucesso!")
