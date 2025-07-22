import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

# ─── App Title ─────────────────────────────────────────────────────────────────
st.title("Retail Product Demand Forecasting & Sales Analytics")

# ─── File Upload ────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("Upload your sales data (CSV format)", type=["csv"])
if uploaded_file is None:
    st.info("Please upload a CSV file to get started.")
    st.stop()

# ─── Read & Clean ───────────────────────────────────────────────────────────────
df = pd.read_csv(uploaded_file)
try:
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
except:
    st.error("❌ Failed to parse your 'Date' column.")
    st.stop()

df.dropna(subset=['Date', 'Order_Demand'], inplace=True)
df['Order_Demand'] = pd.to_numeric(df['Order_Demand'], errors='coerce')
df = df[df['Order_Demand'] >= 0]

# ─── Identify Product Column ───────────────────────────────────────────────────
product_column = next((c for c in ['Product_ID','Product_Code','Product_Category'] if c in df.columns), None)
if not product_column:
    st.error("❌ No product column found (need Product_ID/Product_Code/Product_Category).")
    st.stop()

# ─── Sales Statistics ─────────────────────────────────────────────────────────
st.header("Dataset Sales Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Products", df[product_column].nunique())
with col2:
    st.metric("Total Sales Volume", int(df["Order_Demand"].sum()))
with col3:
    st.metric("Date Range", f"{df['Date'].min().date()} to {df['Date'].max().date()}")
if 'Customer_ID' in df.columns:
    st.metric("Unique Customers", df['Customer_ID'].nunique())

daily_demand = df.groupby("Date")["Order_Demand"].sum()
st.metric("Average Daily Demand", round(daily_demand.mean(), 2))

st.subheader("Top 5 Products by Total Demand")
top5 = (
    df.groupby(product_column)["Order_Demand"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
)
st.bar_chart(top5)

# ─── Forecasting UI ─────────────────────────────────────────────────────────────
st.header("Forecasting Of Quantity")
products = sorted(df[product_column].dropna().unique().tolist())
selected_products = st.multiselect("Select products to forecast", products, default=products[:2])

months = st.slider("Forecast months into future:", 1, 12, 3)
forecast_days = months * 30

if not selected_products:
    st.info("Please select at least one product.")
    st.stop()

# ─── Run Forecasts & Plot ───────────────────────────────────────────────────────
st.subheader("Demand Forecast Plot")
fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.get_cmap('tab10', len(selected_products))

combined = []
for idx, pid in enumerate(selected_products):
    df_p = df[df[product_column] == pid]
    df_daily = (
        df_p.groupby("Date")["Order_Demand"]
            .sum()
            .reset_index()
            .rename(columns={"Date": "ds", "Order_Demand": "y"})
    )

    with st.spinner(f"Training model for {pid}..."):
        model = Prophet()
        model.fit(df_daily)

    future = model.make_future_dataframe(periods=forecast_days)
    fc = model.predict(future)

    ax.plot(fc["ds"], fc["yhat"], label=pid, color=colors(idx))

    tmp = fc[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
    tmp["Product"] = pid
    combined.append(tmp)

ax.set_title("Forecasted Demand for Selected Products")
ax.set_xlabel("Date")
ax.set_ylabel("Forecast (yhat)")
ax.legend()
st.pyplot(fig)

# ─── Aggregate & Display Table ─────────────────────────────────────────────────
df_all = pd.concat(combined, ignore_index=True)
df_all["10-day Period"] = (df_all["ds"].dt.day - 1) // 10 + 1
df_all["Month"] = df_all["ds"].dt.strftime("%Y-%m")
for col in ["yhat", "yhat_lower", "yhat_upper"]:
    df_all[col] = df_all[col].round().astype(int).clip(lower=0)

forecast_agg = (
    df_all
    .groupby(["Month", "10-day Period", "Product"])[["yhat", "yhat_lower", "yhat_upper"]]
    .sum()
    .reset_index()
)

st.subheader("Forecast (Aggregated by 10-Day Periods)")
st.dataframe(forecast_agg)

# ─── CSV Download ─────────────────────────────────────────────────────────────
csv = forecast_agg.to_csv(index=False).encode('utf-8')
st.download_button("Download Forecast CSV", csv, "forecast_data.csv", "text/csv")
