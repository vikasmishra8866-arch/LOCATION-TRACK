import streamlit as st
import streamlit.components.v1 as components
import qrcode
import base64
from io import BytesIO

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Premium UPI QR Generator",
    page_icon="💎",
    layout="centered"
)

# ================= PREMIUM CSS =================

st.markdown("""

<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.stApp{
    background:
    radial-gradient(circle at top left,#7c3aed33,transparent 30%),
    radial-gradient(circle at bottom right,#06b6d433,transparent 30%),
    linear-gradient(135deg,#070b14,#111827,#0f172a);
    color:white;
}

/* HIDE STREAMLIT MENU */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* MAIN CARD */

.main-box{
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    border-radius:32px;
    padding:35px;
    box-shadow:0 25px 50px rgba(0,0,0,0.35);
    margin-top:25px;
}

/* TITLE */

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:800;
    background:linear-gradient(to right,#8b5cf6,#06b6d4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:10px;
}

.subtitle{
    text-align:center;
    color:#94a3b8;
    font-size:16px;
    margin-bottom:35px;
}

/* INPUT */

.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"]{
    background:#0f172a !important;
    color:white !important;
    border-radius:14px !important;
    border:1px solid #334155 !important;
}

/* BUTTON */

.stButton button{
    width:100%;
    border:none;
    border-radius:18px;
    background:linear-gradient(to right,#7c3aed,#06b6d4);
    color:white;
    font-size:18px;
    font-weight:700;
    padding:14px;
    transition:0.3s;
}

.stButton button:hover{
    transform:scale(1.02);
    box-shadow:0 0 30px rgba(139,92,246,0.6);
}

/* PREMIUM CARD */

.qr-card{
    width:100%;
    max-width:430px;
    margin:auto;
    margin-top:35px;
    border-radius:34px;
    overflow:hidden;
    background:
    linear-gradient(145deg,#0b1120,#131c31,#1e1b4b);
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:
    0 0 40px rgba(139,92,246,0.35),
    0 0 80px rgba(6,182,212,0.15);
}

/* TOP AREA */

.card-top{
    padding:40px 25px 30px;
    text-align:center;
    position:relative;
}

.card-top::before{
    content:"";
    position:absolute;
    inset:0;
    background:
    radial-gradient(circle at top left,#8b5cf655,transparent 35%),
    radial-gradient(circle at bottom right,#06b6d455,transparent 35%);
    z-index:0;
}

.card-content{
    position:relative;
    z-index:1;
}

/* TEXT */

.scan-text{
    font-size:30px;
    font-weight:800;
    color:white;
    letter-spacing:1px;
}

.sub-text{
    margin-top:12px;
    color:#67e8f9;
    font-size:16px;
    font-weight:500;
}

/* QR BOX */

.qr-box{
    margin-top:30px;
    background:white;
    padding:18px;
    border-radius:28px;
    display:inline-block;
    border:4px solid #8b5cf6;
    box-shadow:
    0 0 25px rgba(139,92,246,0.6),
    0 0 50px rgba(6,182,212,0.25);
}

/* AMOUNT */

.amount-label{
    margin-top:35px;
    color:#94a3b8;
    font-size:18px;
    font-weight:500;
}

.amount{
    font-size:54px;
    font-weight:800;
    color:white;
    margin-top:8px;
}

/* UPI */

.upi-id{
    margin-top:22px;
    font-size:18px;
    color:#e2e8f0;
    word-break:break-word;
}

/* NOTE */

.note{
    margin-top:12px;
    color:#94a3b8;
    font-size:16px;
}

/* FOOTER */

.card-footer{
    background:#0f172a;
    text-align:center;
    padding:22px;
    color:#67e8f9;
    font-size:16px;
    font-weight:600;
    border-top:1px solid rgba(255,255,255,0.05);
}

/* WEBSITE CUSTOM FOOTER */

.website-footer {
    text-align: center;
    padding: 30px 10px;
    color: #67e8f9;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 1px;
    margin-top: 50px;
    border-top: 1px solid rgba(255,255,255,0.05);
}

</style>

""", unsafe_allow_html=True)

# ================= TITLE =================

st.markdown(
    '<div class="main-title">UPI QR Generator By Vikas Mishra</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Luxury Neon Payment Standee</div>',
    unsafe_allow_html=True
)

# ================= FORM =================

st.markdown('<div class="main-box">', unsafe_allow_html=True)

upi_options = [
    "9696159863-2@ibl",
    "9696159863-3@ybl",
    "9696159863.wallet@phonepe"
]

selected_upi = st.selectbox(
    "Select UPI ID",
    upi_options
)

custom_upi = st.text_input(
    "Or Enter Custom UPI ID"
)

final_upi = custom_upi if custom_upi else selected_upi

amount = st.number_input(
    "Enter Amount",
    min_value=1.0,
    value=100.0,
    step=10.0
)

note = st.text_input(
    "Payment Note / Remark",
    value="Payment"
)

generate = st.button("✨ Generate QR")

st.markdown('</div>', unsafe_allow_html=True)

# ================= GENERATE QR =================

if generate:

    upi_url = (
        f"upi://pay?"
        f"pa={final_upi}"
        f"&pn=UPI Payment"
        f"&am={amount}"
        f"&cu=INR"
        f"&tn={note}"
    )

    qr = qrcode.QRCode(
        version=1,
        box_size=12,
        border=2
    )

    qr.add_data(upi_url)

    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color="#0b1120",
        back_color="white"
    )

    buffer = BytesIO()

    qr_img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode()

    # ================= PREMIUM CARD HTML =================

    card_html = f"""

    <html>

    <head>

    <style>

    body{{
        margin:0;
        padding:0;
        background:transparent;
        font-family:Poppins,sans-serif;
    }}

    .qr-card{{
        width:430px;
        margin:auto;
        border-radius:34px;
        overflow:hidden;
        background:
        linear-gradient(145deg,#0b1120,#131c31,#1e1b4b);
        border:1px solid rgba(255,255,255,0.08);
        box-shadow:
        0 0 40px rgba(139,92,246,0.35),
        0 0 80px rgba(6,182,212,0.15);
    }}

    .card-top{{
        padding:40px 25px 30px;
        text-align:center;
        position:relative;
    }}

    .card-top:before{{
        content:"";
        position:absolute;
        inset:0;
        background:
        radial-gradient(circle at top left,#8b5cf655,transparent 35%),
        radial-gradient(circle at bottom right,#06b6d455,transparent 35%);
        z-index:0;
    }}

    .card-content{{
        position:relative;
        z-index:1;
    }}

    .scan-text{{
        font-size:30px;
        font-weight:800;
        color:white;
        letter-spacing:1px;
    }}

    .sub-text{{
        margin-top:12px;
        color:#67e8f9;
        font-size:16px;
        font-weight:500;
    }}

    .qr-box{{
        margin-top:30px;
        background:white;
        padding:18px;
        border-radius:28px;
        display:inline-block;
        border:4px solid #8b5cf6;
        box-shadow:
        0 0 25px rgba(139,92,246,0.6),
        0 0 50px rgba(6,182,212,0.25);
    }}

    .amount-label{{
        margin-top:35px;
        color:#94a3b8;
        font-size:18px;
        font-weight:500;
    }}

    .amount{{
        font-size:54px;
        font-weight:800;
        color:white;
        margin-top:8px;
    }}

    .upi-id{{
        margin-top:22px;
        font-size:18px;
        color:#e2e8f0;
        word-break:break-word;
    }}

    .note{{
        margin-top:12px;
        color:#94a3b8;
        font-size:16px;
    }}

    .card-footer{{
        background:#0f172a;
        text-align:center;
        padding:22px;
        color:#67e8f9;
        font-size:16px;
        font-weight:600;
        border-top:1px solid rgba(255,255,255,0.05);
    }}

    </style>

    </head>

    <body>

    <div class="qr-card">

        <div class="card-top">

            <div class="card-content">

                <div class="scan-text">
                    SCAN FOR PAYMENT
                </div>

                <div class="sub-text">
                    USING ANY UPI APP
                </div>

                <div class="qr-box">

                    <img
                        src="data:image/png;base64,{qr_base64}"
                        width="260"
                    >

                </div>

                <div class="amount-label">
                    AMOUNT TO PAY
                </div>

                <div class="amount">
                    ₹{amount:,.2f}
                </div>

                <div class="upi-id">
                    {final_upi}
                </div>

                <div class="note">
                    {note}
                </div>

            </div>

        </div>

        <div class="card-footer">
            🔒 SECURE UPI GATEWAY
        </div>

    </div>

    </body>

    </html>

    """

    # ================= SHOW HTML CARD =================

    components.html(
        card_html,
        height=760,
        scrolling=False
    )

    # ================= PREMIUM DOWNLOAD BUTTON =================

    download_html = f"""

    <html>

    <head>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

    <style>

    body{{
        margin:0;
        padding:0;
        background:transparent;
    }}

    .download-btn{{
        width:100%;
        padding:16px;
        border:none;
        border-radius:18px;
        background:linear-gradient(135deg,#8b5cf6,#06b6d4);
        color:white;
        font-size:18px;
        font-weight:700;
        cursor:pointer;
        transition:0.3s;
        box-shadow:
        0 0 20px rgba(139,92,246,0.5),
        0 0 40px rgba(6,182,212,0.2);
    }}

    .download-btn:hover{{
        transform:scale(1.02);
        box-shadow:
        0 0 35px rgba(139,92,246,0.8),
        0 0 60px rgba(6,182,212,0.4);
    }}

    .hidden-card{{
        position:absolute;
        left:-99999px;
        top:-99999px;
    }}

    .qr-card{{
        width:430px;
        border-radius:34px;
        overflow:hidden;
        background:
        linear-gradient(145deg,#0b1120,#131c31,#1e1b4b);
        border:1px solid rgba(255,255,255,0.08);
        box-shadow:
        0 0 40px rgba(139,92,246,0.35),
        0 0 80px rgba(6,182,212,0.15);
        font-family:Poppins,sans-serif;
    }}

    .card-top{{
        padding:40px 25px 30px;
        text-align:center;
        background:
        radial-gradient(circle at top left,#8b5cf655,transparent 35%),
        radial-gradient(circle at bottom right,#06b6d455,transparent 35%);
    }}

    .scan-text{{
        font-size:30px;
        font-weight:800;
        color:white;
    }}

    .sub-text{{
        margin-top:12px;
        color:#67e8f9;
        font-size:16px;
    }}

    .qr-box{{
        margin-top:30px;
        background:white;
        padding:18px;
        border-radius:28px;
        display:inline-block;
        border:4px solid #8b5cf6;
    }}

    .amount-label{{
        margin-top:35px;
        color:#94a3b8;
        font-size:18px;
    }}

    .amount{{
        font-size:54px;
        font-weight:800;
        color:white;
        margin-top:8px;
    }}

    .upi-id{{
        margin-top:22px;
        font-size:18px;
        color:#e2e8f0;
    }}

    .note{{
        margin-top:12px;
        color:#94a3b8;
        font-size:16px;
    }}

    .card-footer{{
        background:#0f172a;
        text-align:center;
        padding:22px;
        color:#67e8f9;
        font-size:16px;
        font-weight:600;
    }}

    </style>

    </head>

    <body>

    <button class="download-btn" onclick="downloadCard()">
    ⬇ Download UPI Card
    </button>

    <div class="hidden-card">

    <div class="qr-card" id="captureCard">

        <div class="card-top">

            <div class="scan-text">
                SCAN FOR PAYMENT
            </div>

            <div class="sub-text">
                USING ANY UPI APP
            </div>

            <div class="qr-box">

                <img
                    src="data:image/png;base64,{qr_base64}"
                    width="260"
                >

            </div>

            <div class="amount-label">
                AMOUNT TO PAY
            </div>

            <div class="amount">
                ₹{amount:,.2f}
            </div>

            <div class="upi-id">
                {final_upi}
            </div>

            <div class="note">
                {note}
            </div>

        </div>

        <div class="card-footer">
            🔒 SECURE UPI GATEWAY
        </div>

    </div>

    </div>

    <script>

    function downloadCard() {{

        const card = document.getElementById("captureCard");

        html2canvas(card, {{
            scale: 4,
            useCORS: true,
            backgroundColor: null
        }}).then(canvas => {{

            const link = document.createElement("a");

            link.download = "premium_upi_card.png";

            link.href = canvas.toDataURL("image/png");

            link.click();

        }});

    }}

    </script>

    </body>

    </html>

    """

    components.html(
        download_html,
        height=90
    )

# ================= WEBSITE CUSTOM FOOTER =================
st.markdown(
    '<div class="website-footer">Vikas Mishra Private Suite</div>',
    unsafe_allow_html=True
)
