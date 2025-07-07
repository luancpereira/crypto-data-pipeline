from flask import jsonify, request
from service import process_assets_data, process_assets_history_data, process_rates_data
from utils import check_token

def main(request):
    response_data = {
        "assets": {},
        "rates": {},
        "history": {}
    }

    request_json = request.get_json() or {}
    cryptos = request_json.get('cryptos', ["bitcoin", "ethereum", "tether", "xrp", "binance-coin", "solana", "usd-coin", "tron", "dogecoin", "steth"])
    
    token, error = check_token()
    if error:
        return None, error

    try:
        result, error = process_assets_data(token, cryptos)
        if error:
            response_data["assets"] = {"error": error["error"], "status": error["status"]}
        else:
            response_data["assets"] = {"success": True, "data": result}
    except Exception as e:
        response_data["assets"] = {"error": f"Erro inesperado no processamento de assets: {str(e)}", "status": 500}
    
    try:
        result, error = process_rates_data(token, cryptos)
        if error:
            response_data["rates"] = {"error": error["error"], "status": error["status"]}
        else:
            response_data["rates"] = {"success": True, "data": result}
    except Exception as e:
        response_data["rates"] = {"error": f"Erro inesperado no processamento de rates: {str(e)}", "status": 500}
    
    try:
        results, errors, skipped = process_assets_history_data(token, cryptos)
        response_data["history"] = {
            "success": True,
            "results": results,
            "errors": errors if errors else None,
            "skipped": skipped if skipped else None,
            "total_processed": len(results),
            "total_errors": len(errors),
            "total_skipped": len(skipped)
        }
    except Exception as e:
        response_data["history"] = {"error": f"Erro inesperado no processamento de histórico: {str(e)}", "status": 500}
    
    has_errors = (
        response_data["assets"].get("error") or 
        response_data["rates"].get("error") or
        response_data["history"].get("errors") or
        response_data["history"].get("error")
    )
    
    status_code = 207 if has_errors else 200
    
    return jsonify(response_data), status_code