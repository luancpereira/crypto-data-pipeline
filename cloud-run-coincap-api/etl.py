from utils import parse_timestamp

def transform_assets_data(json_data):
    data = json_data.get("data", [])
    timestamp = json_data.get("timestamp")
    date, hour = parse_timestamp(timestamp)
    
    rows = []
    for item in data:
        rows.append({
            "id": item.get("id"),
            "rank": int(item.get("rank")),
            "symbol": item.get("symbol"),
            "name": item.get("name"),
            "supply": float(item.get("supply")) if item.get("supply") else None,
            "maxSupply": float(item.get("maxSupply")) if item.get("maxSupply") else None,
            "marketCapUsd": float(item.get("marketCapUsd")) if item.get("marketCapUsd") else None,
            "volumeUsd24Hr": float(item.get("volumeUsd24Hr")) if item.get("volumeUsd24Hr") else None,
            "priceUsd": float(item.get("priceUsd")) if item.get("priceUsd") else None,
            "changePercent24Hr": float(item.get("changePercent24Hr")) if item.get("changePercent24Hr") else None,
            "vwap24Hr": float(item.get("vwap24Hr")) if item.get("vwap24Hr") else None,
            "explorer": item.get("explorer"),
            "date": date,
            "hour": hour
        })
    return rows

def transform_rates_data(json_data):
    data = json_data.get("data", [])
    timestamp = json_data.get("timestamp")
    date, hour = parse_timestamp(timestamp)
    
    rows = []
    for item in data:
        rows.append({
            "id": item.get("id"),
            "symbol": item.get("symbol"),
            "currencySymbol": item.get("currencySymbol"),
            "type": item.get("type"),
            "rateUsd": float(item.get("rateUsd")) if item.get("rateUsd") else None,
            "date": date,
            "hour": hour
        })
    return rows

def transform_assets_history_data(json_data, crypto_id, execution_date):
    data = json_data.get("data", [])
    
    rows = []
    for item in data:
        date, hour = parse_timestamp(item.get("time"))
        
        rows.append({
            "id": crypto_id,
            "priceUsd": float(item.get("priceUsd")) if item.get("priceUsd") else None,
            "date": date,
            "hour": hour,
            "execution_date": execution_date
        })
    
    return rows