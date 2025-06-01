
import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

# Title
st.title("InsightIQ - SME Sales Dashboard")

# Connect to the database
conn = sqlite3.connect("insightiq_sales.db")
df = pd.read_sql_query("SELECT * FROM sales", conn)

# KPI Section
st.header("Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df['total'].sum():,.2f}")
col2.metric("Total Orders", f"{df['order_id'].nunique()}")
col3.metric("Unique Customers", f"{df['customer_id'].nunique()}")

# Time Series Chart
st.header("Revenue Over Time")
df['order_date'] = pd.to_datetime(df['order_date'])
monthly_sales = df.groupby(df['order_date'].dt.to_period('M')).sum().reset_index()
monthly_sales['order_date'] = monthly_sales['order_date'].astype(str)
line_chart = alt.Chart(monthly_sales).mark_line(point=True).encode(
    x='order_date:T',
    y='total:Q',
    tooltip=['order_date', 'total']
).properties(width=700, height=400)
st.altair_chart(line_chart)

# Top Products
st.header("Top 5 Products by Revenue")
top_products = df.groupby('product')['total'].sum().sort_values(ascending=False).head(5)
st.bar_chart(top_products)

# Category Breakdown
st.header("Sales by Category")
category_sales = df.groupby('category')['total'].sum()
st.bar_chart(category_sales)

conn.close()
