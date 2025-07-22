The app is a Product Demand Forecasting Tool. It takes historical sales data (CSV format), lets you pick a product line, and uses Facebook Prophet to predict sales for upcoming months. It also displays forecast statistics and visualizations.
🔧 What the App Does:
This app helps forecast product demand using uploaded sales data and Facebook Prophet.

🚀 Key Features:
Upload CSV
Upload a sales data file with columns like Date, Order_Demand, Product_ID.

Data Cleaning

Parses date column

Filters invalid or negative demand

Dashboard Metrics

Total products

Total sales

Date range

Average daily demand

Top 5 products (bar chart)

Product Forecasting

Select a product

Predict future demand (1–12 months)

Show line plot and table

Group forecasts by month & 10-day periods

Download Forecast

Download predictions as CSV

📦 Libraries Used:
Streamlit for UI

Pandas for data handling

Prophet for forecasting

Matplotlib for plotting

Column	Meaning
yhat	The predicted (forecasted) value for that date
yhat_lower	The lower bound of the prediction interval (e.g., 80% confidence)
yhat_upper	The upper bound of the prediction interval
📊 Example:
Let’s say Prophet gives this forecast:

Date	yhat	yhat_lower	yhat_upper
2025-04-15	320	290	350
This means:

The model predicts 320 units will be demanded.

But it's 80% confident that the actual demand will be between 290 and 350.

output:
Absolutely! Here's a **short and clear explanation** of the **output** from your app:

---

### ✅ **App Output Summary**

Once you upload your CSV file and select a product, the app gives you:

---

### 1. 🧾 **Dashboard Stats**
Displays key metrics like:
- **Total Products** → Count of unique products
- **Total Sales Volume** → Sum of all order demands
- **Date Range** → Time span of your dataset
- **Average Daily Demand** → Avg. orders per day
- **Top 5 Products** → A bar chart showing top-selling products

---

### 2. 🔮 **Forecast Output**
After choosing a product to forecast:
- **Forecast Table**:
  - Shows predicted demand for the selected product  
  - Aggregated by:
    - **Month**
    - **10-day Period**
  - Columns:
    - `yhat`: Predicted quantity
    - `yhat_lower`: Lower estimate
    - `yhat_upper`: Upper estimate

- **Forecast Plot**:
  - A line chart showing:
    - Past demand (historical)
    - Predicted future demand with uncertainty intervals
  - Title: “Demand Forecast for [Your Product]”

- **Download Button**:
  - Lets you export the forecast table as a CSV file

---

### 📊 Example Output Table:

| Month   | 10-day Period | Product | yhat | yhat_lower | yhat_upper |
|---------|----------------|---------|------|-------------|-------------|
| 2025-05 | 1              | A123    | 420  | 390         | 460         |
| 2025-05 | 2              | A123    | 460  | 430         | 490         |

This means:
- In the **first 10 days of May 2025**, demand is predicted to be **420** units for product `A123`.
- Lower and upper bounds give a **range** of prediction.

---
