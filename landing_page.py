import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
import geopandas as gpd
from shapely.geometry import Polygon
from pyproj import CRS

# Mapbox Token
MAPBOX_TOKEN = ""


#st.set_page_config(layout="wide")
with st.sidebar:
    st.title("API Token Section")
    MAPBOX_TOKEN = st.text_input("Enter your Mapbox token:", value=MAPBOX_TOKEN, type="password")
st.title("📍 Address Search + Polygon Drawing Map")
st.caption("Powered by Mapbox, Folium, Shapely, GeoPandas, and Streamlit!")

# Autocomplete + Geocode Address 
# --- Autocomplete search ---
query = st.text_input("Search for an address:", "")
selected_location = None
center = [37.7749, -122.4194]  # default

suggestions = []
if query:
    if MAPBOX_TOKEN == "":
        print("Yuh")
        st.error("Please enter your Mapbox token in the sidebar.")
        st.stop()
    print(f"Query?{query}")
    mapbox_resp = requests.get(
        f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json",
        params={"access_token": MAPBOX_TOKEN, "autocomplete": "true", "limit": 5},
    )
    print(f"are you running? {MAPBOX_TOKEN}")
    if mapbox_resp.ok:
        data = mapbox_resp.json()
        suggestions = data.get("features", [])

# Display suggestions
suggestion_labels = [f['place_name'] for f in suggestions]
selected_place = st.selectbox("Suggestions:", suggestion_labels) if suggestion_labels else None

if selected_place:
    idx = suggestion_labels.index(selected_place)
    coords = suggestions[idx]["center"]  # lon, lat
    center = [coords[1], coords[0]]      # lat, lon
    selected_location = suggestions[idx]["place_name"]
    st.info(f"Selected: {selected_location}")
# Folium Map
m = folium.Map(location=center, zoom_start=13)

# Add draw tool
Draw(export=False, draw_options={"polyline": False, "circle": False, "marker": False, "rectangle": False}).add_to(m)

# Display map and return last drawn polygon
map_data = st_folium(m, height=600, width=700)
print("huh?")


if st.button("Calculate Area"):
    print(f"st_data:{map_data['all_drawings']}")
    print("???")
    if map_data and map_data['all_drawings']:
        print("bwuh")
        area_acres = 0
        for polygon in map_data['all_drawings']:
            geojson = polygon["geometry"]
            coords = geojson["coordinates"][0]  # Outer ring of polygon

            # GeoDataFrame from polygon
            gdf = gpd.GeoDataFrame(index=[0], geometry=[Polygon(coords)], crs="EPSG:4326")

            # Project to metric CRS for accurate area (Web Mercator or UTM)
            gdf_proj = gdf.to_crs(epsg=3857)  # Web Mercator meters

            # Calculate area in square meters, then convert to acres
            area_m2 = gdf_proj.geometry[0].area
            area_acres += area_m2 * 0.000247105

        st.info(f"Area of drawn polygons: **{area_acres:.2f} acres**")
        st.success(f"Total CO2 Saved: **{area_acres*0.077:.2f} tons**")
    else:
        st.warning("Please draw a polygon on the map.")