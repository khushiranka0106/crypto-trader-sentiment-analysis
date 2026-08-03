import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import gdown
import os

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Crypto Trader Behavior Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
}

h1,h2,h3{
    color:white;
}

div[data-testid="metric-container"]{
    background:#1E1E1E;
    border:1px solid #30363d;
    padding:18px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.2);
}

</style>
""", unsafe_allow_html=True)

st.sidebar.title("📈 Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Dataset",
        "Insights",
        "About"
    ]
)

file_id = "14fmNDvAFFoTUjzgjHfwHkwORtmkq9ACW"

if not os.path.exists("historical_data.csv"):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "historical_data.csv", quiet=False)

history = pd.read_csv("historical_data.csv")
fear = pd.read_csv("fear_greed_index.csv")

st.title("📈 Crypto Trader Behavior Analysis Dashboard")

st.caption(
    "Historical Trading Data + Fear & Greed Index"
)
import pandas as pd
file_id = "14fmNDvAFFoTUjzgjHfwHkwORtmkq9ACW"

if not os.path.exists("historical_data.csv"):
    gdown.download(
        f"https://drive.google.com/uc?id={file_id}",
        "historical_data.csv",
        quiet=False
    )

history = pd.read_csv("historical_data.csv")
fear = pd.read_csv("fear_greed_index.csv")



history["Timestamp IST"] = pd.to_datetime(
    history["Timestamp IST"],
    dayfirst=True,
    format="mixed"
)
fear["date"] = pd.to_datetime(fear["date"])

history["date"] = history["Timestamp IST"].dt.date

fear["date"] = pd.to_datetime(fear["date"]).dt.date

merged = pd.merge(
    history,
    fear,
    on="date",
    how="inner"
)

st.write("Merged Shape:", merged.shape)
st.write(merged.head())


avg_pnl = merged["Closed PnL"].mean()

win_rate = (merged["Closed PnL"] > 0).mean()*100

total_trades = len(merged)

avg_position = merged["Size USD"].mean()

c1,c2,c3,c4 = st.columns(4)

c1.metric("💰 Average PnL",f"{avg_pnl:.2f}")

c2.metric("🎯 Win Rate",f"{win_rate:.2f}%")

c3.metric("📊 Total Trades",f"{total_trades:,}")

c4.metric("💵 Avg Position",f"${avg_position:.2f}")

st.subheader("📊 Average PnL by Market Sentiment")

avg_pnl = merged.groupby("classification")["Closed PnL"].mean()

fig, ax = plt.subplots(figsize=(8,4))
avg_pnl.plot(kind="bar", ax=ax)
ax.set_ylabel("Average Closed PnL")

st.pyplot(fig)



st.subheader("🏆 Win Rate by Market Sentiment")

merged["Win"] = merged["Closed PnL"] > 0

win_rate = merged.groupby("classification")["Win"].mean()*100

fig, ax = plt.subplots(figsize=(8,4))
win_rate.plot(kind="bar", ax=ax)

ax.set_ylabel("Win Rate (%)")

st.pyplot(fig)


st.subheader("📈 Trade Frequency")

trade = merged["classification"].value_counts()

fig, ax = plt.subplots(figsize=(8,4))
trade.plot(kind="bar", ax=ax)

ax.set_ylabel("Trades")

st.pyplot(fig)

st.subheader("💰 Average Position Size")

position = merged.groupby("classification")["Size USD"].mean()

fig, ax = plt.subplots(figsize=(8,4))
position.plot(kind="bar", ax=ax)

ax.set_ylabel("USD")

st.pyplot(fig)


st.header("📌 Insights")

st.success("""
• Traders earned higher average profits during Greed and Extreme Greed periods.

• Win rate increased when market sentiment was positive.

• Fear periods produced lower profitability.

• Larger position sizes were associated with higher average returns but also higher risk.

• Market sentiment significantly influenced trader behavior.
""")