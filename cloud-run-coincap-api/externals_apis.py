import requests
from constants import Config
from utils import build_headers, format_http_error

apiURL = Config.API_URL

def get_assets_data(token, ids=None):
    ids_str = ",".join(ids) if isinstance(ids, list) else (ids or "bitcoin,ethereum")
    url = f"{apiURL}/assets"
    headers = build_headers(token)
    params = {"ids": ids_str}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as e:
        return None, format_http_error(e)
    except Exception as e:
        return None, {"error": f"Erro inesperado: {str(e)}", "status": 502}

def get_rates_data(token, ids=None):
    ids_str = ",".join(ids) if isinstance(ids, list) else (ids or "bitcoin,ethereum")
    url = f"{apiURL}/rates"
    headers = build_headers(token)
    params = {"ids": ids_str}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 404:
            try:
                error_data = e.response.json()
                if "not found" in error_data.get("error", "").lower():
                    return None, {"error": f"Conversion rate não encontrado para: {ids_str}", "status": 404}
            except:
                pass
        return None, format_http_error(e, "para rates")
    except Exception as e:
        return None, {"error": f"Erro inesperado para rates: {str(e)}", "status": 502}

def get_assets_history_data(token, crypto_id, start_timestamp, end_timestamp):
    url = f"{apiURL}/assets/{crypto_id}/history"
    headers = build_headers(token)
    params = {
        "interval": "h1",
        "start": start_timestamp,
        "end": end_timestamp
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 404:
            try:
                error_data = e.response.json()
                if "not found" in error_data.get("error", "").lower():
                    return None, {"error": f"Crypto '{crypto_id}' não encontrada", "status": 404}
            except:
                pass
        return None, format_http_error(e, f"para {crypto_id}")
    except Exception as e:
        return None, {"error": f"Erro inesperado para {crypto_id}: {str(e)}", "status": 502}
