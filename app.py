import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_KEY = "YOUR_API_KEY"
symbols = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "INFY"]

@st.cache_data
def fetch_esg_data():
    url = f"https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings?symbol={','.join(symbols)}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data)

# Fetch data
df = fetch_esg_data()

st.title("🌍 ESG Dashboard")
st.markdown("**Real-time ESG insights using Financial Modeling Prep API**")

# Company filter
company = st.selectbox("Select a company:", df['symbol'].unique())
company_data = df[df['symbol'] == company].iloc[0]

st.subheader(f"ESG Ratings for {company}")
st.write(f"**Environmental:** {company_data['environmentalRating']}")
st.write(f"**Social:** {company_data['socialRating']}")
st.write(f"**Governance:** {company_data['governanceRating']}")
st.write(f"**Total ESG Score:** {company_data['ESGScore']}")

# Chart - Compare ESG across all companies
fig = px.bar(df, x='symbol', y='ESGScore', title='ESG Score Comparison')
st.plotly_chart(fig)
