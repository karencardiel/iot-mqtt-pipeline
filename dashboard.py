import streamlit as st
import pandas as pd
import psycopg2
from streamlit_autorefresh import st_autorefresh


# Page Configuration
st.set_page_config(page_title="IoT Real-Time Pipeline", layout="wide")

st.markdown("""
    <style>
    /* Importamos ambas fuentes */
    @import url('https://fonts.googleapis.com/css2?family=Albert+Sans:wght@700;900&family=Poppins:wght@300;400;600&display=swap');
    /* FUENTE GLOBAL: Forzamos Poppins en todos los elementos de Streamlit */
    html, body, [class*="css"], .stMarkdown, .stText, .stMetric, .stWidget, label, p {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* TÍTULO CON PLAYFAIR (Serif) Y AZUL */
    .main-title {
        font-family: 'Albert Sans', serif !important;
        color: #00d4ff; 
        font-weight: 900;
        font-size: 60px;
        margin-top: 10px;
        text-align: center; 
    }

    /* NÚMEROS DE LAS MÉTRICAS: Forzamos Poppins y color azul */
    [data-testid="stMetricValue"] div {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 10 !important;
        color: #00d4ff !important;
    }

    /* ETIQUETAS DE LAS MÉTRICAS */
    [data-testid="stMetricLabel"] p {
        font-family: 'Poppins', sans-serif !important;
        font-size: 10 !important;
        font-weight: 10 !important;
        color: #8b949e !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* TÍTULOS DE LAS GRÁFICAS (###) */
    h3 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 20px !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    /* CAMBIAR LABELS DE LOS EJES (DENTRO DE LA GRÁFICA) */
    .stVegaLiteChart text, .vega-bind label {
        font-family: 'Poppins', sans-serif !important;
        fill: #8b949e !important; /* Color de la letra en la gráfica */
        font-size: 12px !important;
    }

    /* Etiquetas de los inputs (Records to show) */
    label[data-testid="stWidgetLabel"] {
        font-family: 'Poppins', sans-serif !important;
        color: #00d4ff !important; /* Un toque azul para que resalte */
        font-weight: 600 !important;
    }

    /* Estilo para el contenedor de la métrica */
    [data-testid="stMetric"] {
        background-color: #161b22; /* Color de fondo oscuro */
        border: 1px solid #30363d;   /* Borde gris sutil */
        padding: 15px 20px;          /* Espacio interno */
        border-radius: 10px;         /* Orillas redondeadas */
        box-shadow: 0 4px 6px rgba(0,0,0,0.2); /* Sombra para dar profundidad */
    }

    /* Color del título de la métrica */
    [data-testid="stMetricLabel"] p {
        color: #8b949e !important;
        font-weight: 600;
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

st.markdown('<h1 class="main-title">IoT MONITORING SYSTEM</h1>', unsafe_allow_html=True)

# --- CONTROL SCTION 
header_col1, header_col2 = st.columns([3, 1])

with header_col2:

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
    val_i = df_int['value'].iloc[-1] if not df_int.empty else 0
    st.metric(label="LATEST INTEGER", value=f"{val_i} units")

with m2:
    val_f = df_float['value'].iloc[-1] if not df_float.empty else 0
    st.metric(label="LATEST FLOAT", value=f"{val_f:.2f} units")

# --- CHARTS SECTION ---
g1, g2 = st.columns(2)
with g1:
    st.write("### INTEGER STREAM")
    if not df_int.empty:
        st.area_chart(
            df_int.set_index("ts")["value"], 
            use_container_width=True,
            x_label="Time",
            y_label="Sensor value"
        )

with g2:
    st.write("### FLOATING-POINT STREAM")
    if not df_float.empty:      
        st.line_chart(
            df_float.set_index("ts")["value"], 
            use_container_width=True, 
            color="#00d4ff",
            x_label="Timestamp",
            y_label="Precision units"
        )
# --- DATA TABLE ---
with st.expander("Raw data"):
    st.dataframe(df_float, use_container_width=True)