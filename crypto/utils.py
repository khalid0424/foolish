import requests

def standardize_symbol(symbol, exchange_name):
    
    if exchange_name == "kucoin":
        return symbol.replace("-", "")
    elif exchange_name == "bybit":
        return symbol.replace("/", "")
    return symbol

def fetch_binance_prices():
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {item['symbol']: float(item['price']) for item in data}
    except requests.RequestException as e:
        print("Error fetching Binance prices:", e)
        return {}

def fetch_kucoin_prices():
    url = "https://api.kucoin.com/api/v1/market/allTickers"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get('data', {}).get('ticker', [])
        return {
            standardize_symbol(item['symbol'], "kucoin"): float(item['last']) if item['last'] is not None else 0.0
            for item in data
        }
    except requests.RequestException as e:
        print("Error fetching KuCoin prices:", e)
        return {}

def fetch_bybit_prices():
    url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get('data', [])
        return {item['instId']: float(item['last']) for item in data}
    except requests.RequestException as e:
        print("Error fetching OKX prices:", e)
        return {}
def fetch_all_prices():
    
    binance_prices = fetch_binance_prices()
    kucoin_prices = fetch_kucoin_prices()
    bybit_prices = fetch_bybit_prices()

    return binance_prices, kucoin_prices, bybit_prices




def query_ollama(prompt, conversation_history):
    url = "http://127.0.0.1:11434"
    payload = {
        "model": "llama2", 
        "prompt": f"{conversation_history}\nUser: {prompt}\nAI:",
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    try:
        data = response.json()
        return data.get("response", "No response")
    except requests.JSONDecodeError:
        return "Error: Could not parse response from Ollama."
