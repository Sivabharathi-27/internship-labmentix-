import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="📊 PhonePe Pulse Dashboard", layout="wide")
st.title("📱 PhonePe Pulse Data Visualization")

# --- LOAD DATA ---
@st.cache_data
def load_data(path):
    dfs = {}
    for file in os.listdir(path):
        if file.endswith(".csv"):
            name = file.replace(".csv", "")
            dfs[name] = pd.read_csv(os.path.join(path, file))
    return dfs

# 🔹 Change this path to your folder with the 18 preprocessed CSVs
path = os.path.join("preprocessed_data_frames", "other_df")
dfs = load_data(path)

# --- FILTER SELECTION ---
col1, col2, col3 = st.columns(3)
with col1:
    data_type = st.selectbox("📁 Select Data Type", ["Aggregated", "Map", "Top"])
with col2:
    category = st.selectbox("📈 Select Category", ["Transaction", "Insurance", "User"])
with col3:
    level = st.selectbox("🗺️ Select Level", ["State", "Years"])

df_key = f"df_{data_type.lower()}_{category.lower()}_{level.lower()}_new"

# --- CHECK DATA ---
if df_key not in dfs:
    st.warning("⚠️ Data not found for this combination!")
    st.stop()

df = dfs[df_key]

# --- KPI CARDS ---
st.markdown("### 🔍 Quick Insights")
col1, col2, col3 = st.columns(3)

numeric_cols = df.select_dtypes(include="number").columns
if "count" in numeric_cols or "amount" in numeric_cols:
    total_count = df["count"].sum() if "count" in df.columns else 0
    total_amount = df["amount"].sum() if "amount" in df.columns else 0
    avg_amount = df["amount"].mean() if "amount" in df.columns else 0

    col1.metric("Total Count", f"{total_count:,.0f}")
    col2.metric("Total Amount", f"₹{total_amount:,.0f}")
    col3.metric("Average Amount", f"₹{avg_amount:,.2f}")
else:
    st.info("ℹ️ No numeric columns available for KPI display.")

# --- DATA PREVIEW ---
with st.expander("📄 View DataFrame"):
    st.dataframe(df, use_container_width=True)

with st.expander("📊 Summary Statistics"):
    st.write(df.describe())

# --- VISUALIZATION CONTROLS ---
st.markdown("---")
compare_mode = st.toggle("🔀 Enable Compare Mode")

chart_types = ["Bar Chart", "Line Chart", "Scatter Plot", "Area Chart", "Box Plot", "Histogram"]

def make_chart(df, chart_type, x_col, y_col=None):
    """Helper function for charts"""
    if chart_type == "Bar Chart":
        return px.bar(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    elif chart_type == "Line Chart":
        return px.line(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    elif chart_type == "Scatter Plot":
        return px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    elif chart_type == "Area Chart":
        return px.area(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    elif chart_type == "Box Plot":
        return px.box(df, x=x_col, y=y_col, title=f"Distribution of {y_col} by {x_col}")
    elif chart_type == "Histogram":
        return px.histogram(df, x=x_col, title=f"Distribution of {x_col}")
    return None

# --- NORMAL MODE ---
if not compare_mode:
    st.markdown("### 🖼️ Single Visualization")
    c1, c2, c3 = st.columns(3)
    with c1:
        chart_type = st.selectbox("Chart Type", chart_types)
    with c2:
        x_col = st.selectbox("X-axis Column", df.columns)
    with c3:
        y_col = None if chart_type == "Histogram" else st.selectbox("Y-axis Column", [None] + list(df.columns))

    fig = make_chart(df, chart_type, x_col, y_col)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

# --- COMPARE MODE ---
else:
    st.markdown("### 🧩 Compare Visualizations Side-by-Side")
    colA, colB = st.columns(2)

    with colA:
        st.subheader("Chart A")
        chart_type_A = st.selectbox("Chart Type (A)", chart_types, key="chartA_type")
        x_col_A = st.selectbox("X-axis (A)", df.columns, key="xA")
        y_col_A = None if chart_type_A == "Histogram" else st.selectbox("Y-axis (A)", [None] + list(df.columns), key="yA")
        figA = make_chart(df, chart_type_A, x_col_A, y_col_A)
        if figA:
            st.plotly_chart(figA, use_container_width=True)

    with colB:
        st.subheader("Chart B")
        chart_type_B = st.selectbox("Chart Type (B)", chart_types, key="chartB_type")
        x_col_B = st.selectbox("X-axis (B)", df.columns, key="xB")
        y_col_B = None if chart_type_B == "Histogram" else st.selectbox("Y-axis (B)", [None] + list(df.columns), key="yB")
        figB = make_chart(df, chart_type_B, x_col_B, y_col_B)
        if figB:
            st.plotly_chart(figB, use_container_width=True)

st.markdown("---")
st.caption("✨ Built with ❤️ using Streamlit & Plotly | PhonePe Pulse Project")
