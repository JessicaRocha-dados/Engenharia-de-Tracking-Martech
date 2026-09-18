import pandas as pd
from datetime import datetime

print("--- DIA 46: Iniciando Pipeline ELT (Batch) ---")
print("Conceito FinOps: Ingestão de dados reais extraídos do BigQuery sem transformação prévia (Camada Bronze).\n")

# Lendo o arquivo real extraído do GCP
bq_df = pd.read_csv('dia46_bronze_eventos_ga4.csv')

# --- GOVERNANÇA DE DADOS  ---
# Adicionando metadados de controle da engenharia
bq_df['_ingestion_timestamp'] = datetime.now()
bq_df['_source_file'] = 'dia46_bronze_eventos_ga4.csv'

print("Visão da Camada Lógica Bronze (Eventos Brutos - GA4):")
# Selecionando colunas de negócio + metadados de engenharia
print(bq_df[['event_date', 'event_name', 'user_pseudo_id',
      'country', '_ingestion_timestamp', '_source_file']].head())

print("\n--- Ponto de Atenção Arquitetural ---")
print("Observe que o 'event_date' veio nativamente como número inteiro (ex: 20260914) da API do Google.")
print("Na Arquitetura Medalhão, a Camada Bronze DEVE manter o dado no seu estado original.")
print("A limpeza e conversão para formato de data (YYYY-MM-DD) ocorrerá apenas na Camada Silver, usando poder computacional sob demanda.")
