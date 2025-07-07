import os

class Config:
    API_URL = os.environ.get("API_URL")
    BIGQUERY_DATASET = "cadastra-teste.APIcripto"
    BATCH_SIZE = 500
    
class TableNames:
    ASSETS = f"{Config.BIGQUERY_DATASET}.assets"
    RATES = f"{Config.BIGQUERY_DATASET}.rates"
    ASSETS_HISTORY = f"{Config.BIGQUERY_DATASET}.assets_history"
    LOG_EXECUTION = f"{Config.BIGQUERY_DATASET}.log_execution"