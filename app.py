import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. CONFIGURACIÓN DE PÁGINA E IA
st.set_page_config(page_title="IA Analista CF Sant Julià", layout="wide", page_icon="⚽")

# SUSTITUYE AQUÍ TU API KEY
genai.configure(api_key='AIzaSyCIdKeOwc0mEPR38_2BIDNbXekk413GxE4')
model = genai.GenerativeModel('gemini-1.5-flash')

# ID de tu documento
SHEET_ID = '1CB3J-6sIzuWxUzCqFARUIoYySyj-dlyuSNkuDu5DMbo'

# 2. GENERACIÓN DE LISTA DE TEMPORADAS
# Creamos la lista: T 11-12, T 12-13... hasta T 25-26 + la Global
temporadas_lista = [f"T {i}-{i+1}" for i in range(11, 25)]
temporadas_lista.append("T 25-26")
opciones_pestañas = ["JUGADORS (GLOBALS)"] + temporadas_lista

# 3. LÓGICA DE CARGA DE DATOS
st.sidebar.title("Configuración")
pestaña_seleccionada = st.sidebar.selectbox("Selecciona Temporada o Global:", opciones_pestañas)

@st.cache_data
def load_data(sheet_name):
    # Formateamos el nombre para la URL (espacios por %20)
    sheet_name_csv = sheet_name.replace(" ", "%20")
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name_csv}'
    try:
        data = pd.read_csv(url)
        # Limpieza rápida: quitar columnas vacías si las hay
        data = data.dropna(axis=1, how='all')
        return data
    except:
        return None

df = load_data(pestaña_seleccionada)

# 4. INTERFAZ PRINCIPAL
st.title(f"⚽ Analista IA: {pestaña_seleccionada}")

if df is not None:
    # Métricas destacadas del equipo según la pestaña
    if pestaña_seleccionada == "JUGADORS (GLOBALS)":
        col1, col2, col3 = st.columns(3)
        col1.metric("Partidos Totales", "412")
        col2.metric("Goles Históricos", "872")
        col3.metric("Victorias", "189")
    
    st.divider()

    # Buscador de Jugador
    st.subheader("🔍 Ficha Individual de Jugador")
    lista_jugadores = sorted(df['JUGADOR'].dropna().unique())
    jugador_sel = st.selectbox("Busca un jugador:", lista_jugadores)
    
    datos_jugador = df[df['JUGADOR'] == jugador_sel].iloc[0]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Partidos", datos_jugador.get('PARTITS JUGATS', 0))
    c2.metric("Goles", datos_jugador.get('GOLS', 0))
    c3.metric("Amarillas", datos_jugador.get('TG', 0))
    c4.metric("Promedio G/P", datos_jugador.get('G/P', 0))

    st.divider()

    # EL AGENTE DE IA
    st.subheader(f"🤖 Pregunta a la IA sobre {pestaña_seleccionada}")
    st.info("La IA analizará los datos de la temporada seleccionada para responderte.")
    
    pregunta = st.text_input("Ejemplo: ¿Quién es el más eficiente goleador de este periodo?")
    
    if pregunta:
        # Enviamos los datos actuales a la IA como contexto
        contexto = df.to_string()
        prompt = f"""
        Eres el Director Deportivo del CF Sant Julià. 
        Analiza estos datos de la temporada {pestaña_seleccionada}:
        {contexto}
        
        Pregunta del usuario: {pregunta}
        """
        
        with st.spinner('Pensando como analista...'):
            response = model.generate_content(prompt)
            st.write("---")
            st.markdown(response.text)

    st.divider()
    # Tabla completa
    with st.expander("Ver tabla completa de datos"):
        st.dataframe(df, use_container_width=True)

else:
    st.error(f"No se pudo cargar la pestaña '{pestaña_seleccionada}'. Revisa que el nombre sea exacto en Google Sheets.")

st.sidebar.markdown("---")
st.sidebar.write("Desarrollado con Streamlit + Google Gemini")





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
