from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from google.oauth2 import service_account
import google.auth.transport.requests
from google.cloud import bigquery

SERVICE_ACCOUNT_FILE = '/opt/airflow/gcp-sa.json'

cryptos = [
    "bitcoin", "ethereum", "tether", "xrp", 
    "binance-coin", "solana", "usd-coin", "tron", 
    "dogecoin", "steth"
]

def execute_bigquery_procedure(procedure_query):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/bigquery']
    )
    
    client = bigquery.Client(credentials=credentials, project='cadastra-teste')
    
    print(f"Executando: {procedure_query}")
    query_job = client.query(procedure_query)
    
    query_job.result()
    
    print(f"Procedure executada com sucesso: {procedure_query}")

def execute_services():
    target_audience = "https://coincap-api-753104042367.us-central1.run.app"
    
    credentials = service_account.IDTokenCredentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        target_audience=target_audience
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    token = credentials.token
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "cryptos": cryptos
    }
    
    response = requests.post(target_audience, headers=headers, json=data)
    
    print("Status:", response.status_code)
    print("Response:", response.text)
    response.raise_for_status()

default_args = {
    'start_date': datetime(2025, 7, 5),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

procedures = [
    "CALL `cadastra-teste.APIcripto.latest_rates`()",
    "CALL `cadastra-teste.APIcripto.crypto_analysis_by_hour`()",
    "CALL `cadastra-teste.APIcripto.best_performers_last_24h`()"
]

with DAG(
    'execute_all_services',
    schedule_interval='@hourly',
    default_args=default_args,
    catchup=False
) as dag:
    task_execute_services = PythonOperator(
        task_id='execute_services',
        python_callable=execute_services
    )
    
    bq_tasks = []
    for i, procedure in enumerate(procedures, start=1):
        bq_task = PythonOperator(
            task_id=f'call_procedure_{i}',
            python_callable=execute_bigquery_procedure,
            op_args=[procedure]
        )
        bq_tasks.append(bq_task)
    
    task_execute_services >> bq_tasks
