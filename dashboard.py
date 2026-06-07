import streamlit as st
import duckdb
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="E-Commerce Analytics", page_icon="🛒", layout="wide")
st.title("🛒 E-Commerce Analytics Dashboard")

# --- DATABASE CONNECTION ---
# Connect to the DuckDB warehouse built by our dbt pipeline
@st.cache_resource
def get_connection():
    return duckdb.connect('data/ecommerce.duckdb', read_only=True)

con = get_connection()

# --- DATA FETCHING ---
# Cache data to keep dashboard fast and snappy
@st.cache_data(ttl=600)
def load_data():
    # Query 1: Revenue over time
    df_revenue_time = con.execute("""
        SELECT 
            DATE_TRUNC('month', order_date) AS order_month,
            SUM(item_revenue) AS monthly_revenue
        FROM main.fct_order_items
        WHERE order_status NOT IN ('CANCELLED')
        GROUP BY 1
        ORDER BY 1
    """).fetchdf()

    # Query 2: Revenue by category
    df_category = con.execute("""
        SELECT 
            p.category,
            SUM(f.item_revenue) AS category_revenue
        FROM main.fct_order_items f
        JOIN main.dim_products p ON f.product_id = p.product_id
        WHERE f.order_status NOT IN ('CANCELLED')
        GROUP BY 1
        ORDER BY 2 DESC
    """).fetchdf()

    # Query 3: Core KPIs
    df_kpis = con.execute("""
        SELECT 
            COUNT(DISTINCT order_id) AS total_orders,
            SUM(item_revenue) AS total_revenue,
            SUM(item_revenue) / COUNT(DISTINCT order_id) AS average_order_value
        FROM main.fct_order_items
        WHERE order_status NOT IN ('CANCELLED')
    """).fetchdf()

    return df_revenue_time, df_category, df_kpis

df_revenue_time, df_category, df_kpis = load_data()

# --- DASHBOARD LAYOUT ---
# KPI Section
st.markdown("### Core Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_revenue = df_kpis['total_revenue'].iloc[0]
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")

with col2:
    total_orders = int(df_kpis['total_orders'].iloc[0])
    st.metric(label="Total Orders", value=f"{total_orders:,}")

with col3:
    aov = df_kpis['average_order_value'].iloc[0]
    st.metric(label="Average Order Value", value=f"${aov:,.2f}")

st.divider()

# Charts Section
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### Monthly Revenue Trend")
    st.line_chart(df_revenue_time, x='order_month', y='monthly_revenue')

with col_right:
    st.markdown("#### Revenue by Product Category")
    st.bar_chart(df_category, x='category', y='category_revenue')

# Close connection on app shutdown
con.close()