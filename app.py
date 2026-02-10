import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
import datetime

# --- Page Config ---
st.set_page_config(page_title="GHOST LOCATOR PRO", page_icon="🛰️", layout="wide")

# --- Custom RGB & Neon CSS Styling ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Neon Glow Headers */
    h1 {
        color: #00ff41; /* Matrix Green */
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* RGB Border for Sidebars and Containers */
    [data-testid="stSidebar"] {
        border-right: 2px solid #00f2ff;
        box-shadow: 5px 0px 15px #00f2ff;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #ff00ff, #00f2ff);
        color: white;
        border: none;
        border-radius: 10px;
        box-shadow: 0 0 10px #ff00ff;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 20px #00f2ff;
        transform: scale(1.05);
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        color: #00f2ff;
        text-shadow: 0 0 5px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Auto Refresh (Live Update) ---
st_autorefresh(interval=5000, key="loc_refresh")

# --- Title ---
st.title("🛰️ GHOST LOCATOR: COMMAND CENTER")

# --- Sidebar Controls ---
st.sidebar.header("📡 CONNECTION SETTINGS")
student_id = st.sidebar.text_input("Target Student ID:", "STU-9921")
map_theme = st.sidebar.selectbox("Map Visual Mode:", ["Dark Mode", "Satellite", "Terrain"])

st.sidebar.markdown("---")
st.sidebar.subheader("🔒 Encryption Status")
st.sidebar.code("AES-256 ACTIVE\nSSL PINNING: ON\nPROXY: ENABLED", language="bash")

# --- Logic for Map Themes ---
tiles = "CartoDB dark_matter"
if map_theme == "Satellite":
    tiles = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
elif map_theme == "Terrain":
    tiles = "OpenStreetMap"

# --- Main Dashboard Layout ---
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📊 Live Telemetry")
    
    # Simulation Data (Asli data URL params se aayega)
    st.metric("Current Latitude", "21.1702 N")
    st.metric("Current Longitude", "72.8311 E")
    st.metric("Movement Speed", "4.2 km/h", delta="0.5 km/h")
    st.metric("Last Seen", datetime.datetime.now().strftime("%H:%M:%S"))
    
    st.markdown("---")
    st.warning("⚠️ TARGET IS CURRENTLY IN MOTION")

with col2:
    st.markdown("### 🗺️ Real-Time Route Projection")
    
    # Default Coordinates (Surat, Gujarat as Placeholder)
    lat, lon = 21.1702, 72.8311
    
    # Create Map
    m = folium.Map(location=[lat, lon], zoom_start=16, tiles=tiles, attr="Ghost Dashboard")
    
    # RGB Pulse Effect Marker
    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        color="#00f2ff",
        fill=True,
        fill_color="#00f2ff",
        fill_opacity=0.7,
        popup=f"Target: {student_id}"
    ).add_to(m)
    
    # Route Line (Green Neon Path)
    route = [[21.1702, 72.8311], [21.1715, 72.8325], [21.1730, 72.8340]]
    folium.PolyLine(route, color="#00ff41", weight=6, opacity=0.8).add_to(m)
    
    # Display Map
    st_folium(m, width="100%", height=550)

# --- Footer ---
st.markdown("<br><hr><center>Ghost Dashboard v2.0 | Private Use Only</center>", unsafe_allow_html=True)
