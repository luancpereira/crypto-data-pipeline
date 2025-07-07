from datetime import datetime, timedelta
import os

def check_token():
    token = os.environ.get("API_TOKEN")
    if not token:
        return None, {"error": "API_TOKEN não configurado", "status": 401}
    return token, None

def parse_timestamp(timestamp):
    dt = datetime.utcfromtimestamp(timestamp / 1000)
    date = dt.date().isoformat()
    hour = dt.strftime("%H:%M:%S")
    return date, hour

def get_previous_day_timestamps():
    today = datetime.now()
         
    yesterday = today - timedelta(days=1)
         
    start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
         
    end_of_yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
         
    start_timestamp = int(start_of_yesterday.timestamp() * 1000)
    end_timestamp = int(end_of_yesterday.timestamp() * 1000)
         
    return start_timestamp, end_timestamp

def get_current_timestamp_hour():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def build_headers(token):
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

def format_http_error(e, context=""):
    status = e.response.status_code if e.response else 502
    try:
        message = e.response.json().get("error", e.response.text)
    except:
        message = e.response.text if e.response else str(e)
    
    prefix = f"Erro na API externa{f' {context}' if context else ''}"
    return {"error": f"{prefix}: {status} - {message}", "status": status}