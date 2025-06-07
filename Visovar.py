import streamlit as st
import pandas as pd
import os

# Ruta al directorio
carpeta = r"C:\Users\Ariel\Desktop\Inacap\Práctica Profesional\DATA REGISTER _MC316\Datos_csv"

# Buscar archivo CSV más reciente
def obtener_csv_mas_reciente(carpeta):
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.lower().endswith('.csv')]
    if not archivos:
        return None
    return max(archivos, key=os.path.getmtime)

# Cargar y mostrar el CSV más reciente
st.title("Visualizador de CSV - Streamlit")

archivo = obtener_csv_mas_reciente(carpeta)
if archivo:
    st.success(f"Archivo más reciente: {os.path.basename(archivo)}")
    try:
        df = pd.read_csv(archivo, encoding='utf-8', sep=None, engine='python')
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
else:
    st.warning("No se encontró ningún archivo CSV.")
