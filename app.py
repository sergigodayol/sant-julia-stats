import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. CONFIGURACIÓN DE PÁGINA E IA
st.set_page_config(page_title="IA Analista CF Sant Julià", layout="wide", page_icon="⚽")

# TU API KEY INTEGRADA
genai.configure(api_key='AIzaSyCIdKeOwc0mEPR38_2BIDNbXekk413GxE4')
model = genai.GenerativeModel('gemini-1.5-flash')

# ID de tu documento de Google Sheets
SHEET_ID = '1CB3J-6sIzuWxUzCqFARUIoYySyj-dlyuSNkuDu5DMbo'

# 2. GENERACIÓN DE LISTA DE TEMPORADAS (T 11-12 hasta T 25-26 + Global)
temporadas_lista = [f"T {i}-{i+1}" for i in range(11, 25)]
temporadas_lista.append("T 25-26")
opciones_pestañas = ["JUGADORS (GLOBALS)"] + temporadas_lista

# Menú lateral
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/53/53283.png", width=100)
st.sidebar.title("CF Sant Julià")
pestaña_seleccionada = st.sidebar.selectbox("📅 Selecciona Temporada:", opciones_pestañas)

# 3. FUNCIÓN PARA CARGAR Y LIMPIAR DATOS
@st.cache_data
def load_data(sheet_name):
    sheet_name_csv = sheet_name.replace(" ", "%20")
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name_csv}'
    try:
        data = pd.read_csv(url)
        
        # Filtramos solo las columnas de interés para evitar los "None" de la derecha
        cols_interes = ['JUGADOR', 'PARTITS JUGATS', 'GOLS', 'TG', 'TV', 'G/P']
        existentes = [c for c in cols_interes if c in data.columns]
        
        # Limpiamos: Solo filas donde haya nombre de jugador y solo columnas principales
        df_limpio = data[existentes].dropna(subset=['JUGADOR'])
        
        # Extraer métricas generales del equipo si existen en la hoja (PJ, PG, PE, PP, GF, GC)
        metrics_cols = ['PJ', 'PG', 'PE', 'PP', 'GF', 'GC']
        df_metrics = data[[c for c in metrics_cols if c in data.columns]].dropna().iloc[:1] if any(c in data.columns for c in metrics_cols) else None
        
        return df_limpio, df_metrics
    except Exception as e:
        return None, None

df, df_metrics = load_data(pestaña_seleccionada)

# 4. INTERFAZ PRINCIPAL
st.title(f"📊 Analista IA: {pestaña_seleccionada}")

if df is not None and not df.empty:
    # Mostrar Resumen del Equipo en tarjetas si hay datos disponibles
    if df_metrics is not None and not df_metrics.empty:
        st.subheader("📈 Rendimiento Colectivo")
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("PJ", int(df_metrics.iloc[0].get('PJ', 0)))
        m2.metric("PG", int(df_metrics.iloc[0].get('PG', 0)))
        m3.metric("PE", int(df_metrics.iloc[0].get('PE', 0)))
        m4.metric("PP", int(df_metrics.iloc[0].get('PP', 0)))
        m5.metric("GF", int(df_metrics.iloc[0].get('GF', 0)))
        m6.metric("GC", int(df_metrics.iloc[0].get('GC', 0)))
    
    st.divider()

    # Buscador de Jugador Individual
    st.subheader("🔍 Consulta de Jugador")
    lista_jugadores = sorted(df['JUGADOR'].unique())
    jugador_sel = st.selectbox("Busca un jugador para ver su histórico en este periodo:", lista_jugadores)
    
    # Datos del jugador seleccionado
    datos_j = df[df['JUGADOR'] == jugador_sel].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Partidos", datos_j.get('PARTITS JUGATS', 0))
    c2.metric("Goles", datos_j.get('GOLS', 0))
    c3.metric("Tarjetas Amarillas", datos_j.get('TG', 0))
    c4.metric("Promedio G/P", datos_j.get('G/P', 0))

    st.divider()

    # 5. EL AGENTE DE IA (EL CEREBRO)
    st.subheader("🤖 Agente Analista Inteligente")
    st.write("Pregunta cualquier cosa sobre los datos de esta temporada (Ej: ¿Quién es el máximo goleador? o ¿Quién tiene más tarjetas?)")
    
    pregunta = st.text_input("Introduce tu pregunta aquí:")
    
    if pregunta:
        # Convertimos la tabla a texto para que la IA la "lea"
        contexto_ia = df.to_string(index=False)
        prompt = f"""
        Actúa como el analista jefe del club de fútbol CF Sant Julià. 
        Utiliza exclusivamente estos datos de la temporada {pestaña_seleccionada} para responder:
        
        {contexto_ia}
        
        Pregunta: {pregunta}
        Respuesta (sé profesional y directo):
        """
        
        with st.spinner('Analizando estadísticas con IA...'):
            try:
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                st.error("La IA está ocupada. Inténtalo de nuevo en un momento.")

    st.divider()
    # Tabla de datos limpia
    with st.expander("📂 Ver base de datos completa"):
        st.dataframe(df, use_container_width=True)

else:
    st.error("No se han podido cargar los datos. Verifica que el nombre de la pestaña en Google Sheets sea correcto.")

st.sidebar.markdown("---")
st.sidebar.caption("Ingeniería de Datos aplicada al CF Sant Julià")
