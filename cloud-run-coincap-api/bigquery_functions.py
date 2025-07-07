from google.cloud import bigquery
from datetime import datetime
from constants import TableNames, Config

def insert_into_bigquery(rows, table, chunksize):
    client = bigquery.Client()
    errors = []
             
    for i in range(0, len(rows), chunksize):
        chunk = rows[i:i + chunksize]
        chunk_errors = client.insert_rows_json(table, chunk)
        if chunk_errors:
            errors.extend(chunk_errors)
             
    return errors

def check_execution_date(crypto_id, current_date):
    client = bigquery.Client()
         
    query = f"""
    SELECT max(execution_date) as max_execution_date
    FROM `{TableNames.ASSETS_HISTORY}`
    WHERE id = '{crypto_id}'
    """
         
    try:
        results = client.query(query)
        for row in results:
            max_execution_date = row.max_execution_date
            if max_execution_date:
                if max_execution_date == current_date:
                    return True
         
        return False
    except Exception as e:
        print(f"Erro ao verificar execution_date para {crypto_id}: {str(e)}")
        return False

def insert_log_entry(crypto_id, status, json_error, timestamp_hour):
    client = bigquery.Client()
    
    row = {
        "id": crypto_id,
        "status": status,
        "json_error": json_error,
        "timestamp_hour": timestamp_hour
    }
    
    try:
        errors = client.insert_rows_json(TableNames.LOG_EXECUTION, [row])
        if errors:
            print(f"Erro ao inserir log para {crypto_id}: {errors}")
        return errors
    except Exception as e:
        print(f"Erro inesperado ao inserir log para {crypto_id}: {str(e)}")
        return [str(e)]
