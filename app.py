import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
from shapely.geometry import Point, shape
import os


print("reproducir amargo amor - chacaolon")
# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Estrategia Territorial San Miguel", layout="wide", page_icon="🛡️")

# --- 2. MAPEO ESTRATÉGICO (Según tu imagen en tinta) ---
MAPEO_SECTORES = {
    0: "Sector 01", 1: "Sector 02", 2: "Sector 03", 4: "Sector 04",
    3: "Sector 05", 5: "Sector 09", 8: "Sector 07", 7: "Sector 08",
    9: "Sector 06", 6: "Sector 10"
}

@st.cache_data
def cargar_geometria():
    # USANDO EL NOMBRE CORRECTO: sectores.geojson
    nombre_archivo = 'data/sectores.geojson'
    if not os.path.exists(nombre_archivo):
        st.error(f"❌ Error: No se encuentra el archivo '{nombre_archivo}' en la carpeta raíz.")
        return None
        
    try:
        with open(nombre_archivo, 'r') as f:
            data = json.load(f)
        for feature in data['features']:
            id_geo = int(feature['id'])
            feature['properties']['sector_label'] = MAPEO_SECTORES.get(id_geo, f"ID {id_geo}")
        return data
    except Exception as e:
        st.error(f"Error al procesar el GeoJSON: {e}")
        return None

# --- 3. LÓGICA DE ASIGNACIÓN AUTOMÁTICA DE SECTOR ---
def encontrar_sector(lat, lon, geojson_data):
    if not geojson_data: return "N/A"
    try:
        # IMPORTANTE: Shapely usa (Longitud, Latitud)
        punto = Point(float(lon), float(lat)) 
        for feature in geojson_data['features']:
            poligono = shape(feature['geometry'])
            if poligono.contains(punto):
                return feature['properties']['sector_label']
    except Exception:
        return "Error Coordenadas"
    return "Fuera de Jurisdicción"

# --- 4. CARGA DE BASE DE DATOS (EXCEL REAL) ---
@st.cache_data
def cargar_base_datos(_geojson_data):
    ruta_excel = 'data/data.xlsx'
    if not os.path.exists(ruta_excel):
        st.error(f"❌ Error: No se encuentra el archivo '{ruta_excel}'.")
        return pd.DataFrame()
        
    try:
        df = pd.read_excel(ruta_excel)
        print(df)
        df.columns = df.columns.str.strip() # Limpiamos espacios en nombres de columnas
        
        # Aseguramos que lat y lon sean numéricos (para que no falle la comparación)
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        df = df.dropna(subset=['lat', 'lon']) # Quitamos filas sin coordenadas
        
        # ASIGNACIÓN AUTOMÁTICA
        df['Sector'] = df.apply(lambda x: encontrar_sector(x['lat'], x['lon'], _geojson_data), axis=1)
        return df
    except Exception as e:
        st.error(f"Error al leer el Excel: {e}")
        return pd.DataFrame()

# --- 5. INTERFAZ Y FILTROS ---
geojson = cargar_geometria()
df = cargar_base_datos(geojson)

st.title("🛡️ Control Territorial - San Miguel")

# Sidebar con filtros
st.sidebar.header("Filtros Estratégicos")
lista_sectores_ordenada = sorted(list(MAPEO_SECTORES.values())) + ["Fuera de Jurisdicción"]
f_sector = st.sidebar.multiselect("Sectores:", options=lista_sectores_ordenada, default=lista_sectores_ordenada)

tipos_disp = df['Tipo'].unique().tolist() if not df.empty else []
f_tipo = st.sidebar.multiselect("Categoría:", options=tipos_disp, default=tipos_disp)

search = st.sidebar.text_input("🔍 Buscar por Nombre o Profesión:")

# Aplicar Filtro
if not df.empty:
    mask = (df['Sector'].isin(f_sector)) & (df['Tipo'].isin(f_tipo))
    if search:
        mask = mask & (df['Nombre'].str.contains(search, case=False) | df['Profesion'].str.contains(search, case=False))
    df_final = df[mask]
else:
    df_final = pd.DataFrame()

# --- VISTAS ---
tab_mapa, tab_datos = st.tabs(["🗺️ Mapa de Control", "📋 Base de Datos"])

with tab_mapa:
    # Este mensaje te dirá si realmente hay puntos listos para mostrar
    if len(df_final) == 0:
        st.warning("⚠️ No hay puntos que coincidan con los filtros seleccionados.")
    else:
        st.success(f"✅ Mostrando {len(df_final)} puntos en el mapa.")

    m = folium.Map(location=[-12.078, -77.09], zoom_start=14)

    if geojson:
        folium.GeoJson(
            geojson,
            style_function=lambda x: {
                'fillColor': x['properties'].get('fill', 'gray'),
                'color': 'black', 'weight': 2, 'fillOpacity': 0.5 
            },
            tooltip=folium.GeoJsonTooltip(fields=['sector_label'], aliases=['Zona:'])
        ).add_to(m)

    # Dibujar los puntos del Excel
    for _, row in df_final.iterrows():
        # Selección de iconos por tipo
        t = str(row['Tipo']).strip()
        # Reemplaza tu línea por esta:
        color, icon = ("orange", "star") if t == "Aliado estraategico" else ("blue", "user") if t == "Aliado" else ("red", "bullhorn") if t == "Carteles" else ("green", "leaf")

        pop_html = f"<b>{row['Nombre']}</b><br>Sector: {row['Sector']}<br>Prof: {row['Profesion']}<br>Cel: {row['Celular']}"
        
        folium.Marker(
            [row['lat'], row['lon']],
            popup=folium.Popup(pop_html, max_width=200),
            icon=folium.Icon(color=color, icon=icon, prefix='fa')
        ).add_to(m)

    st_folium(m, width="100%", height=600, returned_objects=[], key="mapa_final_sm")

with tab_datos:
    st.dataframe(df_final, use_container_width=True, hide_index=True)