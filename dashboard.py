import streamlit as st
import pandas as pd
import psycopg2
from streamlit_autorefresh import st_autorefresh


# Page Configuration
st.set_page_config(page_title="IoT Real-Time Pipeline", layout="wide")

# CSS Style for the "Dark/Pro" look (Blue accents)
st.markdown("""
    <style>
    /* Import Poppins font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* Apply Poppins to everything */
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Forces dark background for the main container */
    .stApp { background-color: #0e1117; }
    
    /* Global text color */
    h1, h2, h3, p, span, label { color: #ffffff !important; }
    
    /* Metric styling */
    div[data-testid="stMetricValue"] { 
        font-size: 40px !important; 
        color: #00d4ff !important; 
    }
    
    /* Input box styling */
    div[data-baseweb="input"] { 
        background-color: #1a1c24; 
        border: 1px solid #00d4ff; 
    }
    </style>
""", unsafe_allow_html=True)


# Connection Parameters
DB_PARAMS = {
    "host": "localhost",
    "database": "postgres",
    "user": "karen",
    "password": ""
}

# Auto-refresh every 2 seconds
st_autorefresh(interval=2000, key="datarefresh")

st.title("IoT MONITORING SYSTEM")

# --- CONTROL SCTION (Side-by-side Top Header) ---
header_col1, header_col2 = st.columns([3, 1])

with header_col2:
    # Record selector located at the top right (no sidebar)
    limit = st.number_input("Records to show:", min_value=5, max_value=100, value=20)

st.divider()

def get_data(table_name, row_limit):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        query = f"SELECT ts, value FROM {table_name} ORDER BY ts DESC LIMIT {row_limit}"
        df = pd.read_sql(query, conn)
        conn.close()
        return df.iloc[::-1] # Reverse for chronological flow
    except Exception as e:
        return pd.DataFrame()

# Data acquisition with dynamic limit
df_int = get_data("lake_raw_data_int", limit)
df_float = get_data("lake_raw_data_float", limit)

# --- METRICS SECTION ---
m1, m2 = st.columns(2)
with m1:
    val = df_int['value'].iloc[-1] if not df_int.empty else 0
    st.metric("Latest Integer Value", f"{val} units")
with m2:
    val = df_float['value'].iloc[-1] if not df_float.empty else 0
    st.metric("Latest Float Value", f"{val:.2f} units")

# --- CHARTS SECTION ---
g1, g2 = st.columns(2)
with g1:
    st.write("### INTEGER STREAM")
    if not df_int.empty:
        st.area_chart(df_int.set_index("ts")["value"], use_container_width=True)

with g2:
    st.write("### FLOATING-POINT STREAM")
    if not df_float.empty:
        st.line_chart(df_float.set_index("ts")["value"], use_container_width=True, color="#00d4ff")

# --- DATA TABLE ---
with st.expander("Raw data"):
    st.dataframe(df_float, use_container_width=True)