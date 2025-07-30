import yfinance as yf
import pandas as pd

# List of company tickers
symbols = [
    "AAPL", "MSFT", "TSLA", "GOOGL", "AMZN",
    "META", "NFLX", "NVDA", "IBM", "ORCL",
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"
]

all_data = []

for symbol in symbols:
    stock = yf.Ticker(symbol)
    esg_data = stock.sustainability

    if esg_data is not None:
        esg_df = esg_data.reset_index()
        esg_df.columns = ["Metric", "Value"]
        esg_df["Company"] = symbol
        all_data.append(esg_df)

# Combine all ESG data into one DataFrame
if all_data:
    final_df = pd.concat(all_data)
    final_df.to_csv("esg_data.csv", index=False)
    print("✅ ESG data saved to esg_data.csv")
else:
    print("❌ No ESG data found for given tickers.")
