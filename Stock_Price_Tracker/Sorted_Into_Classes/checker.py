import requests

API_key = "156DW7OTQGTLJESV"
url = "https://www.alphavantage.co/query"
params = {
    "function": "SYMBOL_SEARCH",
    "keywords": "Apple",
    "apikey": API_key,
}
response = requests.get(url, params=params)
print(response.json())  # Check if response contains "bestMatches"
