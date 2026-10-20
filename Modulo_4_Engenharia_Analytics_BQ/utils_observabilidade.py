import time
import uuid
import pandas as pd


def registrar_execucao(client, etapa, status, linhas, inicio, run_id):
    """Regista o tempo e o status de cada etapa da pipeline através de um DataFrame."""
    try:
        duracao = time.time() - inicio

        # Cria um pequeno DataFrame (tabela) com apenas a nossa linha de log
        df_log = pd.DataFrame([{
            'run_id': run_id,
            'etapa': etapa,
            'status': status,
            'linhas': int(linhas),
            'duracao_segundos': duracao,
            # Usamos o Timestamp nativo do Pandas, que o BigQuery entende perfeitamente!
            'executado_em': pd.Timestamp.utcnow(),
        }])

        tabela_destino = 'portifolio-martech.gold.pipeline_execucoes'

        # Envia o DataFrame como um lote (Load Job) - Método gratuito do BigQuery!
        job = client.load_table_from_dataframe(df_log, tabela_destino)
        job.result()  # Aguarda a conclusão

        print(
            f"[{status.upper()}] Etapa '{etapa}' registada. Duração: {duracao:.2f}s.")

    except Exception as e:
        print(
            f"Falha ao registar observabilidade (não interrompe a pipeline): {e}")
