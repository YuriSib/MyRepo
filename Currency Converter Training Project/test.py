import json
import requests


url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=10"

payload = {}
headers= {
  "apikey": "Rv702xecWbI1rtNt85HUvM4zVfkldYK0"
}
response = requests.request("GET", url, headers=headers, data = payload)

result = json.loads(response.content)
print(result.get('result'))