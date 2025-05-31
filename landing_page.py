import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
import geopandas as gpd
from shapely.geometry import Polygon
from pyproj import CRS

# Mapbox Token
MAPBOX_TOKEN = "YOUR_MAPBOX_TOKEN_HERE"

st.set_page_config(layout="wide")
st.title("📍 Address Search + Polygon Drawing Map")
st.caption("Powered by Mapbox, Folium, and GeoPandas")

# Autocomplete + Geocode Address 
query = st.text_input("Enter address:", "")
default_center = [37.7749, -122.4194]  # San Francisco default
center = default_center

# Folium Map
m = folium.Map(location=center, zoom_start=13)

# Add draw tool
Draw(export=True, draw_options={"polyline": False, "circle": False, "marker": False, "rectangle": False}).add_to(m)

# Display map and return last drawn polygon
st_data = st_folium(m, height=600, width=700, returned_objects=["last_drawn"])