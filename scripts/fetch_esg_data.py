import requests
import pandas as pd

API_KEY = "giJEifZAxHjCm8CSFa0iRmrKZwy9wNSW"
symbols = ["AAPL", "MSFT", "TSLA", "GOOGL", "INFY"]

url = f"https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings?symbol={','.join(symbols)}&apikey={API_KEY}"
response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)
df.to_csv("esg_data.csv", index=False)

print("ESG data saved as esg_data.csv")