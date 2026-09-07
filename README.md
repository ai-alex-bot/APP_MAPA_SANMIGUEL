# 🛡️ Control Territorial - San Miguel

Aplicación interactiva desarrollada en **Streamlit** y **Folium** para la visualización, filtrado y análisis de sectores territoriales en el distrito de San Miguel, Lima. Permite mapear puntos de interés estratégicos y asignarlos automáticamente a sus respectivos sectores geográficos mediante polígonos GeoJSON.

---

## 🚀 Características

- **Visualización en Mapa:** Carga de polígonos GeoJSON por sectores y marcadores de ubicaciones personalizadas.
- **Asignación Geoespacial Automática:** Uso de `shapely` para determinar automáticamente a qué sector pertenece un punto en función de sus coordenadas (`lat`, `lon`).
- **Filtros Dinámicos:** Filtrado interactivo por sectores, categorías de aliados y búsqueda textual por nombre o profesión.
- **Vista de Datos Tabular:** Exploración de la base de datos procesada.

---

## 🛠️ Requisitos Previos e Instalación

Este proyecto utiliza [`uv`](https://github.com/astral-sh/uv) como gestor de dependencias y entornos modernos (basado en `pyproject.toml`), lo que garantiza instalaciones ultra rápidas y reproducibilidad exacta.

### 1. Clonar el repositorio
```bash
git clone https://github.com/ai-alex-bot/APP_MAPA_SANMIGUEL.git
cd APP_MAPA_SANMIGUEL
```

### 2. Sincronizar el entorno y dependencias
Con `uv`, no necesitas crear ni activar el entorno virtual manualmente. Solo ejecuta el siguiente comando y `uv` preparará todo utilizando las versiones exactas del archivo `uv.lock`:
```bash
uv sync
```
*(Si prefieres añadir más paquetes en el futuro, simplemente usa `uv add nombre-del-paquete`).*

---

## 📁 Estructura del Proyecto

```text
APP_MAPA_SANMIGUEL/
├── data/
│   ├── data_ejemplo.xlsx   # Estructura de datos de ejemplo (sin información sensible)
│   └── data.xlsx           # Base de datos local real (ignorada en git)
├── sectores.geojson        # Geometría de los sectores de San Miguel
├── app.py                  # Código principal de la aplicación Streamlit
├── pyproject.toml          # Declaración moderna del proyecto y sus dependencias
├── uv.lock                 # Versiones exactas bloqueadas para garantizar que funcione en cualquier PC
└── README.md               # Documentación (este archivo)
```

---

## 💻 Ejecución de la Aplicación

Para iniciar la aplicación localmente, utilizamos `uv run`. Esto le dice a `uv` que ejecute Streamlit asegurándose de utilizar el entorno virtual correcto de forma automática:

```bash
uv run streamlit run app.py
```
