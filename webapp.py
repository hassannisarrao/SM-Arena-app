import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import time
import os

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="SM Arena | Official",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TITANIUM CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 10%, #2e1065, #020617 60%);
        color: #f8fafc;
    }
    
    /* Navigation Bar */
    div[role="radiogroup"] {
        display: flex;
        justify-content: center;
        gap: 20px;
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 50px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 20px;
    }
    div[role="radiogroup"] label {
        border-radius: 30px;
        padding: 10px 25px !important;
        transition: all 0.3s;
        border: 1px solid transparent;
    }
    div[role="radiogroup"] > label > div:first-child { display: none !important; }
    div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
        color: white !important;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);
    }
    
    /* Payment Box */
    .payment-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid #10b981;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        text-align: center;
    }
    .account-number {
        font-size: 24px;
        font-weight: 900;
        color: white;
        letter-spacing: 2px;
        background: #020617;
        padding: 10px;
        border-radius: 8px;
        display: inline-block;
        margin: 10px 0;
    }
    
    /* Inputs */
    .stTextInput input, .stSelectbox div, .stDateInput input, .stNumberInput input {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        color: white !important;
        border-radius: 12px;
        height: 50px;
        font-weight: 500;
    }
    .stTextInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
    }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        border: none;
        padding: 16px 32px;
        border-radius: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.4);
    }

    /* Defaults */
    #MainMenu, footer, header {visibility: hidden;}
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #020617;
        color: #64748b;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 1px solid #1e293b;
        z-index: 100;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATABASE ---
def init_db():
    conn = sqlite3.connect("arena_pro.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, sport TEXT, 
        date TEXT, time TEXT, hours INTEGER, bill INTEGER, status TEXT)""")
    conn.commit()
    conn.close()

def add_booking(name, phone, sport, day, time_slot, hours, bill, status="Pending"):
    conn = sqlite3.connect("arena_pro.db")
    c = conn.cursor()
    full_date = f"{day} {time_slot}"
    c.execute("SELECT * FROM bookings WHERE date=? AND sport=?", (full_date, sport))
    if c.fetchone():
        conn.close()
        return False
    c.execute("INSERT INTO bookings (name, phone, sport, date, time, hours, bill, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (name, phone, sport, str(day), time_slot, hours, bill, status))
    conn.commit()
    conn.close()
    return True

init_db()

PRICES = {"Cricket 🏏": 2000, "Football ⚽": 1500, "Hockey 🏑": 1000, "Badminton 🏸": 800}
TIMESLOTS = ["05:00 PM", "06:00 PM", "07:00 PM", "08:00 PM", "09:00 PM", "10:00 PM", "11:00 PM", "12:00 AM"]

# --- 4. TOP BANNER ---
col_spacer1, col_img, col_spacer2 = st.columns([1, 2, 1])
with col_img:
    image_path = "assets/banner.jpg"
    if not os.path.exists(image_path): image_path = "assets/banner.png"
    if os.path.exists(image_path):
        st.image(image_path, width=None, use_column_width=True) 

# --- 5. NOTICE ---
st.markdown("""
<div style="background-color: #6366f1; color: white; padding: 8px; font-weight: bold; text-align: center; border-radius: 5px; margin-bottom: 20px; font-size: 14px;">
    📢 NOTICE: Send payment screenshot to WhatsApp for instant confirmation!
</div>
""", unsafe_allow_html=True)

# --- 6. NAVIGATION ---
page = st.radio("Main Menu", ["Home", "Admin Panel"], horizontal=True)
st.markdown("###")

# ==========================================
# PAGE 1: HOME (Customer View)
# ==========================================
if page == "Home":
    
    with st.container():
        st.markdown("<h1 style='text-align: center;'>SM ARENA <span style='color:#6366f1;'>SHUJABAD</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>The Ultimate Indoor Sports Experience.</p>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.info("📍 Location: Near Iqra College, Jalalpur Bypass Road")
            st.success("📞 Booking Hotline: 0300-2434074")

    st.markdown("###")

    # --- BOOKING FORM (NO FORM WRAPPER FOR LIVE MATH) ---
    with st.container(border=True):
        st.markdown("### ⚡ Fast Booking")
        
        # NOTE: Removed 'with st.form' so math updates instantly
        c_name = st.text_input("Full Name", placeholder="e.g. Ali Khan")
        c_phone = st.text_input("Phone Number", placeholder="03xx-xxxxxxx")
        
        r1, r2 = st.columns(2)
        sport = r1.selectbox("Select Sport", list(PRICES.keys()))
        hours = r2.number_input("Hours to Play", 1, 6, 1)
        
        r3, r4 = st.columns(2)
        day = r3.date_input("Date", min_value=date.today())
        time_slot = r4.selectbox("Time Slot", TIMESLOTS)
        
        # LIVE CALCULATION HAPPENS HERE
        total = PRICES[sport] * hours
        
        st.markdown("---")
        
        # Payment Info
        st.markdown("""
        <div class="payment-box">
            <div class="payment-title">💳 Online Payment Options</div>
            <p style="color: #cbd5e1; margin-bottom:5px;">JazzCash | EasyPaisa | Bank Transfer</p>
            <div class="account-number">0301 3042747 4433</div>
            <p style="font-size: 12px; color: #94a3b8;">* Please send screenshot to 0300-2434074</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("###")
        
        p1, p2 = st.columns([1.5, 1])
        with p1:
            st.markdown("##### 🧾 Payable Amount")
        with p2:
            # Displays the LIVE updated total
            st.markdown(f"<h2 style='color:#10b981; text-align:right;'>PKR {total:,}</h2>", unsafe_allow_html=True)
        
        # Button is now standalone
        if st.button("🔒 CONFIRM & BOOK"):
            if c_name and c_phone:
                with st.spinner("Processing..."):
                    time.sleep(1)
                    if add_booking(c_name, c_phone, sport, day, time_slot, hours, total, "Pending Verification"):
                        st.balloons()
                        st.success(f"✅ BOOKING RECEIVED! Status: Pending. Please pay to confirm.")
                    else:
                        st.error("❌ OOPS! That slot is already taken.")
            else:
                st.warning("⚠️ Please fill in all details.")

# ==========================================
# PAGE 2: ADMIN PANEL
# ==========================================
elif page == "Admin Panel":
    
    if "admin_ok" not in st.session_state: st.session_state.admin_ok = False
    
    if not st.session_state.admin_ok:
        cl1, cl2, cl3 = st.columns([1,1,1])
        with cl2:
            st.markdown("####")
            with st.container(border=True):
                st.markdown("<h3 style='text-align:center;'>🛡️ Manager Login</h3>", unsafe_allow_html=True)
                pwd = st.text_input("Enter Passkey", type="password")
                if st.button("Unlock Dashboard"):
                    if pwd == "admin123":
                        st.session_state.admin_ok = True
                        st.rerun()
                    else:
                        st.error("⛔ Access Denied")
    else:
        dh1, dh2 = st.columns([3, 1])
        dh1.title("📊 Arena Stats")
        if dh2.button("Log Out"):
            st.session_state.admin_ok = False
            st.rerun()
            
        conn = sqlite3.connect("arena_pro.db")
        df = pd.read_sql_query("SELECT * FROM bookings", conn)
        conn.close()
        
        m1, m2, m3 = st.columns(3)
        rev = df[df['status']=='Payment Confirmed']['bill'].sum() if not df.empty else 0
        m1.metric("💰 Real Revenue", f"PKR {rev:,}")
        m2.metric("📅 Total Bookings", len(df))
        m3.metric("⏳ Pending", len(df[df['status']!='Payment Confirmed']))
        
        st.markdown("---")
        
        tab_manage, tab_add = st.tabs(["📋 Manage & Verify Payments", "➕ Manual Booking"])
        
        with tab_manage:
            st.info("💡 Tip: Double-click on 'Status' to change 'Pending' to 'Payment Confirmed'.")
            
            edited_df = st.data_editor(
                df,
                column_config={
                    "status": st.column_config.SelectboxColumn(
                        "Payment Status",
                        options=["Pending Verification", "Payment Confirmed", "Cancelled"],
                        required=True,
                        width="medium"
                    ),
                    "bill": st.column_config.NumberColumn("Bill (PKR)", format="Rs %d")
                },
                use_container_width=True,
                hide_index=True,
                num_rows="fixed"
            )
            
            if st.button("💾 Save Changes"):
                conn = sqlite3.connect("arena_pro.db")
                c = conn.cursor()
                for index, row in edited_df.iterrows():
                    c.execute("UPDATE bookings SET status=? WHERE id=?", (row['status'], row['id']))
                conn.commit()
                conn.close()
                st.success("Database Updated Successfully!")
                time.sleep(1)
                st.rerun()
            
        with tab_add:
            # Manual add can keep the form because live price isn't as critical for admin speed
            with st.form("quick_add"):
                st.write("Add Walk-in Customer")
                qa1, qa2 = st.columns(2)
                nm = qa1.text_input("Name")
                ph = qa2.text_input("Phone")
                sp = st.selectbox("Sport", list(PRICES.keys()))
                tm = st.selectbox("Time", TIMESLOTS)
                if st.form_submit_button("Save Record"):
                    add_booking(nm, ph, sp, date.today(), tm, 1, PRICES[sp], "Payment Confirmed")
                    st.success("Saved!")
                    time.sleep(0.5)
                    st.rerun()

st.markdown("""
<div class="footer">
    © 2026 SM Arena Shujabad | Developed by Tayyab Experts
</div>
""", unsafe_allow_html=True)