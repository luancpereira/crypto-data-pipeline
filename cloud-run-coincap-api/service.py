from datetime import datetime
from externals_apis import get_assets_data, get_assets_history_data, get_rates_data
from etl import transform_assets_data, transform_assets_history_data, transform_rates_data
from bigquery_functions import insert_into_bigquery, check_execution_date, insert_log_entry
from utils import get_previous_day_timestamps, get_current_timestamp_hour
from constants import TableNames

def process_assets_data(token, cryptos):
    current_timestamp = get_current_timestamp_hour()
    json_data, error = get_assets_data(token, cryptos)
    if error:
        for crypto_id in cryptos:
            insert_log_entry(crypto_id, "ERROR", str(error), current_timestamp)
        return None, error
    try:
        rows = transform_assets_data(json_data)
        errors = insert_into_bigquery(rows, TableNames.ASSETS, 500)
        if errors:
            for crypto_id in cryptos:
                insert_log_entry(crypto_id, "ERROR", str(errors), current_timestamp)
            return None, {"error": f"Erro ao inserir no BigQuery para tabela Assets: {errors}", "status": 500}
        return {"message": f"{len(rows)} registros inseridos com sucesso na tabela Assets."}, None
    except Exception as e:
        for crypto_id in cryptos:
            insert_log_entry(crypto_id, "ERROR", str(e), current_timestamp)
        return None, {"error": f"Erro ao transformar os dados para tabela Assets: {str(e)}", "status": 500}

def process_rates_data(token, cryptos):
    current_timestamp = get_current_timestamp_hour()
    json_data, error = get_rates_data(token, cryptos)
    if error:
        for crypto_id in cryptos:
            insert_log_entry(crypto_id, "ERROR", str(error), current_timestamp)
        return None, error
    try:
        rows = transform_rates_data(json_data)
        errors = insert_into_bigquery(rows, TableNames.RATES, 500)
        if errors:
            for crypto_id in cryptos:
                insert_log_entry(crypto_id, "ERROR", str(errors), current_timestamp)
            return None, {"error": f"Erro ao inserir no BigQuery para tabela Rates: {errors}", "status": 500}
        return {"message": f"{len(rows)} registros inseridos com sucesso na tabela Rates."}, None
    except Exception as e:
        for crypto_id in cryptos:
            insert_log_entry(crypto_id, "ERROR", str(e), current_timestamp)
        return None, {"error": f"Erro ao transformar os dados para tabela Rates: {str(e)}", "status": 500}

def process_assets_history_data(token, cryptos):
    current_date = datetime.now().date()
    start_timestamp, end_timestamp = get_previous_day_timestamps()
    current_timestamp = get_current_timestamp_hour()
    results = []
    errors = []
    skipped = []
    for crypto_id in cryptos:
        try:
            if check_execution_date(crypto_id, current_date):
                skipped.append(f"Dados para {crypto_id} já foram processados hoje")
                continue
            json_data, error = get_assets_history_data(token, crypto_id, start_timestamp, end_timestamp)
            if error:
                error_msg = f"Erro para {crypto_id}: {error['error']}"
                errors.append(error_msg)
                insert_log_entry(crypto_id, "ERROR", str(error), current_timestamp)
                continue
            if json_data.get("error"):
                error_msg = f"Erro na API para {crypto_id}: {json_data['error']}"
                errors.append(error_msg)
                insert_log_entry(crypto_id, "ERROR", str(json_data['error']), current_timestamp)
                continue
            rows = transform_assets_history_data(json_data, crypto_id, current_date.isoformat())
            if not rows:
                result_msg = f"Nenhum dado histórico encontrado para {crypto_id}"
                results.append(result_msg)
                continue
            bq_errors = insert_into_bigquery(rows, TableNames.ASSETS_HISTORY, 500)
            if bq_errors:
                error_msg = f"Erro ao inserir {crypto_id} no BigQuery: {bq_errors}"
                errors.append(error_msg)
                insert_log_entry(crypto_id, "ERROR", str(bq_errors), current_timestamp)
            else:
                result_msg = f"{len(rows)} registros históricos inseridos para {crypto_id}"
                results.append(result_msg)
        except Exception as e:
            error_msg = f"Erro inesperado para {crypto_id}: {str(e)}"
            errors.append(error_msg)
            insert_log_entry(crypto_id, "ERROR", str(e), current_timestamp)
    return results, errors, skipped
