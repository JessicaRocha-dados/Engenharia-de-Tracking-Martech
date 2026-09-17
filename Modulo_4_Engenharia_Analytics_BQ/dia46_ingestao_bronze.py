import pandas as pd

print("--- DIA 46: Iniciando Pipeline ELT (Batch) ---")
print("Conceito FinOps: Ingestão de dados reais extraídos do BigQuery sem transformação prévia (Camada Bronze).\n")

# Lendo o arquivo real extraído do GCP
bq_df = pd.read_csv('dia46_bronze_eventos_ga4.csv')

print("Visão da Camada Lógica Bronze (Eventos Brutos - GA4):")
# Selecionando colunas específicas para o terminal não ficar ilegível
print(bq_df[['event_date', 'event_name', 'user_pseudo_id', 'country']].head())

print("\n--- Ponto de Atenção Arquitetural ---")
print("Observe que o 'event_date' veio nativamente como número inteiro (ex: 20260914) da API do Google.")
print("Na Arquitetura Medalhão, a Camada Bronze DEVE manter o dado no seu estado original.")
print("A limpeza e conversão para formato de data (YYYY-MM-DD) ocorrerá apenas na Camada Silver, usando poder computacional sob demanda.")
