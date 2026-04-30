import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Dashboard CF Sant Julià", layout="wide")

# Sustituye 'TU_API_KEY_AQUÍ' por la clave que guardaste
genai.configure(api_key='AIzaSyCIdKeOwc0mEPR38_2BIDNbXekk413GxE4')

# URL de tu Google Sheet (formato export para que Python lo lea directo)
# Reemplaza el ID largo por el de tu documento
SHEET_ID = '1CB3J-6sIzuWxUzCqFARUIoYySyj-dlyuSNkuDu5DMbo'
URL = f'https://docs.google.com/spreadsheets/d/1CB3J-6sIzuWxUzCqFARUIoYySyj-dlyuSNkuDu5DMbo/export?format=csv'

@st.cache_data
def load_data():
    df = pd.read_csv(URL)
    return df

df = load_data()

st.title("⚽ Panel de Análisis CF Sant Julià")
st.write("Datos sincronizados en tiempo real desde Google Sheets.")

# Mostrar métricas generales del equipo
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Partidos Jugados", "412") # Dato de tu tabla I1:N2
with col2:
    st.metric("Goles Totales", "872")    # Dato de tu tabla I1:N2
with col3:
    st.metric("Victorias", "189")       # Dato de tu tabla I1:N2[cite: 1]

st.dataframe(df)
