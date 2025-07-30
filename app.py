import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import numpy as np
import os

# ------------------------
# APP CONFIG
# ------------------------
st.set_page_config(page_title="ESG Dashboard", page_icon="🌍", layout="wide")

st.title("🌍 Beginner-Friendly ESG & Financial Dashboard")
st.markdown(
    """
    This dashboard uses **Kaggle ESG data** and **Yahoo Finance stock data**  
    to show sustainability metrics and price trends.
    """
)

# ------------------------
# COMPANY NAME TO TICKER MAP
# ------------------------
company_name_map = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Meta": "META",
    "Netflix": "NFLX",
    "Nvidia": "NVDA",
    "IBM": "IBM",
    "Oracle": "ORCL",
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
}

company_sector_map = {
    "AAPL": "Technology",
    "MSFT": "Technology",
    "TSLA": "Automotive",
    "GOOGL": "Technology",
    "AMZN": "E-commerce",
    "META": "Technology",
    "NFLX": "Entertainment",
    "NVDA": "Technology",
    "IBM": "Technology",
    "ORCL": "Technology",
    "RELIANCE.NS": "Energy & Telecom",
    "TCS.NS": "Technology",
    "INFY.NS": "Technology",
    "HDFCBANK.NS": "Banking",
    "ICICIBANK.NS": "Banking",
}

popular_companies = list(company_name_map.values())
reverse_map = {v: k for k, v in company_name_map.items()}

# ------------------------
# LOAD ESG DATA FROM KAGGLE
# ------------------------
def load_esg_history():
    if os.path.exists("data/sp500_esg_data.csv"):
        df_esg_hist = pd.read_csv("data/sp500_esg_data.csv")
        df_esg_hist.columns = [col.strip() for col in df_esg_hist.columns]
        return df_esg_hist
    else:
        st.error("Missing data file: data/sp500_esg_data.csv")
        return pd.DataFrame()

esg_history = load_esg_history()

def get_latest_esg_data(symbol):
    """Fetch the latest ESG metrics for a given company from the CSV."""
    if esg_history.empty:
        return pd.DataFrame()
    company_esg = esg_history[esg_history["Symbol"] == symbol]
    if company_esg.empty:
        return pd.DataFrame()
    latest = company_esg.sort_values(by=["ratingYear", "ratingMonth"], ascending=False).head(1)
    data = {
        "Metric": ["environmentScore", "socialScore", "governanceScore", "totalEsg"],
        "Value": [
            latest["environmentScore"].values[0],
            latest["socialScore"].values[0],
            latest["governanceScore"].values[0],
            latest["totalEsg"].values[0]
        ],
        "Company": symbol
    }
    return pd.DataFrame(data)

# Create combined ESG dataframe
df = pd.concat([get_latest_esg_data(symbol) for symbol in popular_companies])

# ------------------------
# SIDEBAR SEARCH
# ------------------------
st.sidebar.header("Search or Select a Company")

company_names = list(company_name_map.keys())
search_name = st.sidebar.selectbox(
    "Type or select a company name:",
    options=[""] + company_names,
    index=0
)

company_to_display = company_name_map.get(search_name) if search_name else popular_companies[0]

# ------------------------
# TABS
# ------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "ℹ️ Overview", "📊 Company Data", "🏆 Compare & Rank", "🌐 Global ESG Snapshot"
])

# ------------------------
# TAB 1: OVERVIEW
# ------------------------
with tab1:
    st.header("What is ESG?")
    st.write(
        """
        **ESG** = **Environmental + Social + Governance**,  
        metrics that measure sustainability & ethical performance:
        - **Environmental (E):** Carbon emissions, renewable energy usage.
        - **Social (S):** Employee welfare, diversity, and community relations.
        - **Governance (G):** Leadership ethics, board independence.
        """
    )
    st.info("ESG scores come directly from Kaggle’s `sp500_esg_history.csv`.")

# ------------------------
# TAB 2: COMPANY DATA
# ------------------------
with tab2:
    company_data = get_latest_esg_data(company_to_display)

    st.subheader(f"ESG Metrics for {reverse_map.get(company_to_display, company_to_display)}")

    if company_data.empty:
        st.warning("No ESG data available for this company.")
    else:
        # --- ESG Badge ---
        total_esg_val = company_data.loc[company_data["Metric"] == "totalEsg", "Value"].values[0]
        if total_esg_val <= 20:
            badge = "🏆 **ESG Leader**"
            badge_color = "green"
        elif total_esg_val <= 40:
            badge = "⚖️ **Average Performer**"
            badge_color = "orange"
        else:
            badge = "⚠️ **Needs Improvement**"
            badge_color = "red"
        st.markdown(f"<h3 style='color:{badge_color};'>{badge}</h3>", unsafe_allow_html=True)

        # --- ESG KPI Scorecards ---
        st.write("### ESG Scorecards")
        col1, col2, col3 = st.columns(3)
        for col, metric_name in zip([col1, col2, col3], ["environmentScore", "socialScore", "governanceScore"]):
            value = company_data.loc[company_data["Metric"] == metric_name, "Value"].values[0]
            color = "green" if value <= 20 else "orange" if value <= 40 else "red"
            col.metric(label=metric_name.replace("Score", ""), value=round(value, 2))
            col.markdown(f"<div style='background-color:{color}; height:4px;'></div>", unsafe_allow_html=True)

        # --- ESG Table ---
        st.write("### Detailed ESG Table")
        st.dataframe(company_data, use_container_width=True)

        st.download_button(
            label="📥 Download ESG Data as CSV",
            data=company_data.to_csv(index=False),
            file_name=f"{company_to_display}_esg_data.csv",
            mime="text/csv"
        )

        # --- ESG & Stock Price Trend ---
        st.write("### 📉 ESG & Stock Price Trend (Last 1 Year + ESG History)")
        esg_company_hist = esg_history[esg_history["Symbol"] == company_to_display]

        try:
            stock = yf.Ticker(company_to_display)
            hist = stock.history(period="1y").reset_index()
            if not hist.empty:
                fig_trend = px.line(
                    hist, x="Date", y="Close",
                    title=f"{company_to_display} Stock Price vs ESG Trend",
                    labels={"Close": "Stock Price (USD)"}
                )

                if not esg_company_hist.empty:
                    # Fix ratingYear and ratingMonth
                    esg_company_hist["ratingYear"] = esg_company_hist["ratingYear"].astype(int)
                    esg_company_hist["ratingMonth"] = esg_company_hist["ratingMonth"].astype(int)
                    esg_company_hist["Date"] = pd.to_datetime(
                        esg_company_hist["ratingYear"].astype(str) + "-" +
                        esg_company_hist["ratingMonth"].astype(str).str.zfill(2) + "-01"
                    )

                    for col, label in [("totalEsg", "Total ESG"),
                                       ("environmentScore", "Environment"),
                                       ("socialScore", "Social"),
                                       ("governanceScore", "Governance")]:
                        fig_trend.add_scatter(
                            x=esg_company_hist["Date"],
                            y=esg_company_hist[col],
                            mode="lines+markers",
                            name=label,
                            yaxis="y2"
                        )
                    fig_trend.update_layout(
                        yaxis=dict(title="Stock Price (USD)"),
                        yaxis2=dict(title="ESG Score", overlaying="y", side="right")
                    )

                st.plotly_chart(fig_trend, use_container_width=True)

                if not esg_company_hist.empty:
                    st.write("### ESG Trends Table (Last 12 Months)")
                    st.dataframe(
                        esg_company_hist[["Date", "environmentScore", "socialScore", "governanceScore", "totalEsg"]].tail(12)
                    )
                else:
                    st.info("No ESG history available for this company.")
            else:
                st.info("Stock price history unavailable.")
        except Exception as e:
            st.warning(f"Could not fetch trend data: {e}")

# ------------------------
# TAB 3: COMPARE & RANK
# ------------------------
with tab3:
    st.subheader("Top ESG Performers (Lower = Better)")
    esg_scores = df[df["Metric"] == "totalEsg"].sort_values(by="Value", ascending=True)
    st.dataframe(esg_scores, use_container_width=True)

    fig_top = px.bar(
        esg_scores,
        x="Company",
        y="Value",
        title="Top ESG Performers (Lower Score = Better)",
        color="Company",
        text="Value"
    )
    fig_top.update_traces(textposition="outside")
    st.plotly_chart(fig_top, use_container_width=True)

    # ESG Heatmap
    st.subheader("ESG Heatmap (Environment / Social / Governance)")
    heatmap_data = df[df["Metric"].isin(["environmentScore", "socialScore", "governanceScore"])].copy()
    heatmap_data["Sector"] = heatmap_data["Company"].map(company_sector_map)

    selected_sector = st.selectbox("Filter by Sector:", options=["All"] + sorted(set(company_sector_map.values())))
    if selected_sector != "All":
        heatmap_data = heatmap_data[heatmap_data["Sector"] == selected_sector]

    if not heatmap_data.empty:
        pivot_df = heatmap_data.pivot(index="Company", columns="Metric", values="Value").fillna(0)
        fig_heatmap = px.imshow(
            pivot_df,
            labels=dict(x="ESG Metric", y="Company", color="Score"),
            x=["environmentScore", "socialScore", "governanceScore"],
            y=[reverse_map.get(c, c) for c in pivot_df.index],
            color_continuous_scale="RdYlGn_r",
            aspect="auto",
            title="ESG Heatmap (Lower Score = Better)"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.info("No ESG data available for heatmap.")

# ------------------------
# TAB 4: GLOBAL ESG SNAPSHOT
# ------------------------
with tab4:
    st.subheader("Global ESG Snapshot by Sector")
    sector_df = df[df["Metric"] == "totalEsg"].copy()
    sector_df["Sector"] = sector_df["Company"].map(company_sector_map)
    sector_avg = sector_df.groupby("Sector")["Value"].mean().reset_index().sort_values(by="Value")

    if not sector_avg.empty:
        st.write("### Average ESG Score by Sector")
        st.dataframe(sector_avg, use_container_width=True)
        fig_sector = px.bar(
            sector_avg,
            x="Sector",
            y="Value",
            title="Average ESG Score by Sector (Lower = Better)",
            color="Sector",
            text="Value"
        )
        fig_sector.update_traces(textposition="outside")
        st.plotly_chart(fig_sector, use_container_width=True)
    else:
        st.info("No ESG sector data available.")
