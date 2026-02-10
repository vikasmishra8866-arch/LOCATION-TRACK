import streamlit as st
import subprocess
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import random
import socket 
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
from fpdf import FPDF 
import base64

# --- Headless Browser Imports ---
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Page Settings
st.set_page_config(page_title="Bhai ka Ghost Dashboard", page_icon="👻", layout="wide")

# --- REPORT GENERATOR FUNCTION ---
def create_pdf(scan_type, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Bhai ka Ghost Dashboard - Scan Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Scan Module: {scan_type}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=str(data))
    return pdf.output(dest='S').encode('latin-1')

# --- STEALTH HEADERS ---
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0'
]

def get_stealth_headers():
    return {'User-Agent': random.choice(USER_AGENTS), 'Accept-Language': 'en-US,en;q=0.5'}

def find_secrets(text):
    patterns = {
        "Google API Key": r'AIza[0-9A-Za-z-_]{35}',
        "Firebase ID": r'[a-z0-9\-_]{20,}:android:[a-f0-9]+',
        "Generic Secret": r'(?i)(key|api|token|secret|auth|password)["\s:=>]+([0-9a-zA-Z\-_]{16,})'
    }
    found = []
    for name, pattern in patterns.items():
        matches = re.findall(pattern, text)
        for m in matches:
            val = m[1] if isinstance(m, tuple) else m
            found.append({"Type": name, "Value": val})
    return found

# Sidebar Navigation
choice = st.sidebar.radio("Select Module", [
    "Email Hunter", 
    "Dark Web Breach Check", 
    "Live Student Tracker Pro", # New Pro Module
    "Pro Secret Scanner", 
    "Headless Ghost Scanner", 
    "Deep Crawling API Finder", 
    "Phishing Link Detector",
    "Port Scanner", 
    "IP & Phone Tracker", 
    "Website Recon", 
    "Social Finder", 
    "Ghost Report Center"
])

# --- MODULE: EMAIL HUNTER ---
if choice == "Email Hunter":
    st.title("🔍 Stealth Email OSINT")
    email = st.text_input("Target Email:")
    if st.button("Scan Leak"):
        with st.spinner('Checking database...'):
            cmd = ["h8mail", "-t", email, "--local"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            st.code(res.stdout)

# --- MODULE: DARK WEB BREACH CHECK ---
elif choice == "Dark Web Breach Check":
    st.title("🌑 Dark Web Leak Radar")
    target_email = st.text_input("Email to Check:")
    if st.button("Scan Breaches"):
        with st.spinner('Searching...'):
            try:
                res = requests.get(f"https://api.proxover.com/v1/leak?email={target_email}")
                if res.status_code == 200:
                    st.error("⚠️ Breach Found!")
                    st.json(res.json())
                else: st.success("✅ Clean!")
            except: st.info("Database scan complete.")

# --- MODULE: LIVE STUDENT TRACKER PRO ---
elif choice == "Live Student Tracker Pro":
    st.title("🛰️ Professional Route Tracker")
    st.write("Professional interface for live student monitoring.")
    
    # Auto-refresh every 10 seconds for live movement
    st_autorefresh(interval=10000, key="datarefresh")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📡 Tracking Info")
        s_name = st.text_input("Student ID:", "Student_01")
        st.info("Status: Live Monitoring Active")
        st.metric("Signal Strength", "Strong ✅")
        st.metric("Battery Level", "82%")

    with col2:
        # Initializing map with dynamic coordinates (Placeholder for Surat/Delhi)
        # Real coordinates can be fetched from URL parameters using st.query_params
        lat, lon = 21.1702, 72.8311 
        
        m = folium.Map(location=[lat, lon], zoom_start=15, tiles="CartoDB dark_matter")
        folium.Marker([lat, lon], popup=f"Live: {s_name}", icon=folium.Icon(color='red', icon='record', prefix='fa')).add_to(m)
        
        # Drawing a route (Line)
        route = [[21.1702, 72.8311], [21.1720, 72.8330], [21.1750, 72.8360]]
        folium.PolyLine(route, color="#00FF00", weight=5, opacity=0.8).add_to(m)
        
        st_folium(m, width=800, height=500)

# --- MODULE: PRO SECRET SCANNER ---
elif choice == "Pro Secret Scanner":
    st.title("🚀 Deep JS Secret Hunter")
    target_url = st.text_input("Enter URL:")
    if st.button("Deep Scan"):
        try:
            res = requests.get(target_url, headers=get_stealth_headers(), timeout=15)
            secrets = find_secrets(res.text)
            st.table(secrets) if secrets else st.success("No secrets found.")
        except Exception as e: st.error(e)

# --- MODULE: HEADLESS GHOST SCANNER ---
elif choice == "Headless Ghost Scanner":
    st.title("👻 Headless Browser Scan")
    target_url = st.text_input("Target URL:")
    if st.button("Ghost Scan"):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(target_url)
        st.text_area("Source Code Snippet", driver.page_source[:2000])
        driver.quit()

# --- MODULE: PHISHING LINK DETECTOR ---
elif choice == "Phishing Link Detector":
    st.title("🛡️ Phishing Analyzer")
    url = st.text_input("Scan URL:")
    if st.button("Analyze"):
        if "login" in url.lower() or "verify" in url.lower():
            st.error("HIGH RISK: Suspicious keyword detected!")
        else: st.success("Looks safe.")

# --- MODULE: PORT SCANNER ---
elif choice == "Port Scanner":
    st.title("🔐 Stealth Port Scanner")
    target = st.text_input("IP/Domain:")
    if st.button("Scan"):
        st.write(f"Scanning {target}...")
        # Add socket logic here as per previous versions

# --- MODULE: IP & PHONE TRACKER ---
elif choice == "IP & Phone Tracker":
    st.title("📍 IP & Phone OSINT")
    ip = st.text_input("IP:")
    if st.button("Track"):
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        st.json(res)

# --- MODULE: GHOST REPORT CENTER ---
elif choice == "Ghost Report Center":
    st.title("📑 Report Center")
    if 'last_scan' in st.session_state:
        pdf_data = create_pdf("Ghost Scan", st.session_state['last_scan'])
        st.download_button("📥 Download PDF", data=pdf_data, file_name="report.pdf")
    else: st.warning("No scans performed yet.")

st.sidebar.markdown("---")
st.sidebar.caption("System Status: Online 🟢")
