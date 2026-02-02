import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import time
import os
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="SM Arena | Official",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ULTRA-PRO CSS STYLING ---
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap'); 
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* --- ANIMATED BACKGROUND --- */
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #f8fafc;
    }
    
    /* --- REMOVE DEFAULT PADDING --- */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 120px !important;
    }

    /* --- HIDE DEFAULT ELEMENTS --- */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* --- HERO BACKGROUND BOX --- */
    .hero-box {
        position: relative;
        width: 100%;
        padding: 60px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        border: 1px solid rgba(255,255,255,0.1);
        overflow: hidden;
    }
    .hero-logo-img {
        width: 140px;
        filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.8));
        margin-bottom: 15px;
        transition: transform 0.3s;
    }
    .hero-logo-img:hover { transform: scale(1.1); }

    /* --- BRAND TITLE STYLING --- */
    .brand-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 52px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        text-shadow: 0px 0px 20px rgba(99, 102, 241, 0.8);
        letter-spacing: -2px;
        line-height: 1.0;
        margin: 0;
    }
    .brand-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 18px;
        color: #fbbf24;
        font-weight: 800;
        letter-spacing: 8px;
        text-transform: uppercase;
        margin-top: 10px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
    }

    /* --- NEWS TICKER --- */
    .news-ticker-container {
        width: 100%;
        background: rgba(99, 102, 241, 0.2);
        border-bottom: 1px solid rgba(99, 102, 241, 0.5);
        overflow: hidden;
        white-space: nowrap;
        padding: 8px 0;
        margin-bottom: 20px;
    }
    .news-ticker-text {
        display: inline-block;
        padding-left: 100%;
        animation: ticker 20s linear infinite;
        font-family: 'Orbitron', sans-serif;
        color: #fbbf24;
        font-weight: bold;
        font-size: 12px;
    }
    @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }

    /* --- PRO LIVE SCHEDULE GRID (CSS) --- */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-top: 15px;
    }
    @media (max-width: 768px) {
        .grid-container { grid-template-columns: repeat(3, 1fr) !important; }
    }
    
    .grid-item {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 12px 5px;
        text-align: center;
        transition: transform 0.2s;
    }
    
    /* STATUS: OPEN */
    .item-open {
        border-bottom: 3px solid #10b981;
    }
    .item-open:hover { background: rgba(16, 185, 129, 0.1); transform: scale(1.02); }
    .text-open { color: #10b981; font-size: 10px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; margin-top:5px; }
    
    /* STATUS: BOOKED */
    .item-booked {
        border-bottom: 3px solid #ef4444;
        background: rgba(0,0,0,0.3);
        opacity: 0.8;
    }
    .text-booked { color: #ef4444; font-size: 10px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; margin-top:5px; }
    
    .time-font { font-family: 'Orbitron', sans-serif; color: white; font-size: 16px; margin-bottom: 4px; font-weight:bold; }
    .player-name { color: #94a3b8; font-size: 10px; margin-top: 2px; font-style: italic; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    /* --- FACILITIES CARDS --- */
    .facility-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .facility-card:hover { transform: scale(1.05); border-color: #6366f1; }
    .facility-icon { font-size: 35px; margin-bottom: 8px; }
    .facility-text { font-size: 11px; color: #cbd5e1; font-weight: 700; text-transform: uppercase; }

    /* --- DIGITAL PRICE --- */
    .digital-price {
        font-family: 'Orbitron', sans-serif;
        color: #10b981;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.8);
        font-size: 32px;
        text-align: right;
        font-weight: bold;
    }

    /* --- COMPACT SOCIAL MEDIA BAR --- */
    .social-bar {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 10px 0;
    }
    .social-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.05);
        color: white;
        font-size: 14px;
        text-decoration: none;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .social-icon:hover { transform: translateY(-3px); color: white; border-color:white; }
    .tiktok:hover { background: #000000; border-color: #ff0050; }
    .facebook:hover { background: #1877F2; border-color: #1877F2; }
    .instagram:hover { background: #E4405F; border-color: #E4405F; }
    .youtube:hover { background: #FF0000; border-color: #FF0000; }

    /* --- FOOTER --- */
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(2, 6, 23, 0.98);
        color: #64748b;
        text-align: center;
        padding: 8px;
        font-size: 10px;
        border-top: 1px solid #1e293b;
        z-index: 998;
    }
    
    /* --- FLOATING WHATSAPP BUTTON --- */
    .float-wa {
        position: fixed;
        width: 55px;
        height: 55px;
        bottom: 60px;
        right: 20px;
        background-color: #25d366;
        color: #FFF;
        border-radius: 50px;
        text-align: center;
        font-size: 28px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        transition: transform 0.3s;
    }
    .float-wa:hover { transform: scale(1.1); background-color: #1ebd56; }

    /* --- GLASSY INPUTS & TEXTAREA --- */
    .stTextInput input, .stSelectbox div, .stNumberInput input, .stDateInput input, .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        font-size: 16px;
    }
    .stTextInput input { height: 55px; }
</style>
<a href="https://wa.me/923002434074" class="float-wa" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="30" height="30">
</a>
""", unsafe_allow_html=True)

# --- 3. SMART IMAGE FINDER ---
def find_image(filename_base):
    # This smart function looks for action1.jpg, Action1.jpg, action1.png, etc.
    possible_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    possible_names = [filename_base, filename_base.capitalize(), filename_base.upper(), filename_base.lower()]
    
    # Check inside 'assets' folder
    if os.path.exists("assets"):
        for name in possible_names:
            for ext in possible_extensions:
                full_path = f"assets/{name}{ext}"
                if os.path.exists(full_path):
                    return full_path
    return None

def get_image_as_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- 4. DATABASE ---
def init_db():
    conn = sqlite3.connect("arena_pro.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, sport TEXT, 
        date TEXT, time TEXT, hours INTEGER, bill INTEGER, status TEXT, note TEXT)""")
    try:
        c.execute("SELECT note FROM bookings LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("ALTER TABLE bookings ADD COLUMN note TEXT")
        conn.commit()
    conn.commit()
    conn.close()

def get_daily_schedule(selected_date):
    conn = sqlite3.connect("arena_pro.db")
    c = conn.cursor()
    c.execute("SELECT time, name, sport FROM bookings WHERE date LIKE ? AND status != 'Cancelled'", (f"{selected_date}%",))
    rows = c.fetchall()
    conn.close()
    return {row[0]: {'name': row[1], 'sport': row[2]} for row in rows}

def add_booking(name, phone, sport, day, time_slot, hours, bill, status="Pending", note=""):
    conn = sqlite3.connect("arena_pro.db")
    c = conn.cursor()
    full_date = f"{day} {time_slot}"
    c.execute("SELECT * FROM bookings WHERE date=? AND sport=?", (full_date, sport))
    if c.fetchone():
        conn.close()
        return False
    c.execute("INSERT INTO bookings (name, phone, sport, date, time, hours, bill, status, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (name, phone, sport, str(day), time_slot, hours, bill, status, note))
    conn.commit()
    conn.close()
    return True

init_db()

PRICES = {"Cricket 🏏": 2000, "Football ⚽": 1500, "Hockey 🏑": 1000, "Badminton 🏸": 800}
TIMESLOTS = [
    "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
    "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM",
    "05:00 PM", "06:00 PM", "07:00 PM", "08:00 PM",
    "09:00 PM", "10:00 PM", "11:00 PM", "12:00 AM",
    "01:00 AM", "02:00 AM"
]

# --- 5. NAVIGATION ---
page = st.radio("Main Menu", ["Home", "Admin Panel"], horizontal=True, label_visibility="collapsed")

# ==========================================
# PAGE 1: HOME (Customer View)
# ==========================================
if page == "Home":
    
    # --- NEWS TICKER (TOP) ---
    st.markdown("""
    <div class="news-ticker-container">
        <div class="news-ticker-text">
            📢 BREAKING: Night Cricket Tournament Registration Open! | ⚡ WEEKEND SPECIAL: 10% OFF on 2+ Hours | 🏏 New Pro Turf Installed! | ⚽ Football League Starting Soon...
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- HERO SECTION ---
    with st.container():
        # Smart Image Loading
        bg_path = find_image("action1")
        if bg_path:
            bg_b64 = get_image_as_base64(bg_path)
            bg_css = f"url('data:image/jpg;base64,{bg_b64}')"
        else:
            bg_css = "url('https://images.unsplash.com/photo-1519861531473-9200263931a2?q=80&w=2560&auto=format&fit=crop')"

        logo_html = ""
        logo_path = find_image("banner")
        if logo_path:
            logo_b64 = get_image_as_base64(logo_path)
            logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="hero-logo-img">'

        st.markdown(f"""
        <div class="hero-box" style="background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), {bg_css}; background-size: cover; background-position: center;">
            {logo_html}
            <div class="brand-title">SM ARENA</div>
            <div class="brand-subtitle">SHUJABAD</div>
            <p style="color: #cbd5e1; font-size: 14px; font-style: italic; margin-top: 15px; font-weight: 500;">The Ultimate Indoor Sports Experience</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 15px; margin-bottom: 25px;">
            <a href="https://www.google.com/maps/search/?api=1&query=SM+Arena+Shujabad" style="text-decoration: none; color: white; background: #2563eb; padding: 10px 20px; border-radius: 30px; font-size: 14px; font-weight: bold; border: 1px solid #3b82f6;">📍 Directions</a>
            <a href="mailto:sm.arena.shujabad@gmail.com" style="text-decoration: none; color: white; background: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 30px; font-size: 14px; font-weight: bold; border: 1px solid rgba(255,255,255,0.2);">📧 Email</a>
        </div>
        """, unsafe_allow_html=True)

    # --- FACILITIES ---
    st.markdown("### 🌟 Premium Facilities")
    f1, f2, f3, f4 = st.columns(4)
    with f1: st.markdown("""<div class="facility-card"><div class="facility-icon">🏏</div><div class="facility-text">Pro Cricket</div></div>""", unsafe_allow_html=True)
    with f2: st.markdown("""<div class="facility-card"><div class="facility-icon">⚽</div><div class="facility-text">Turf Football</div></div>""", unsafe_allow_html=True)
    with f3: st.markdown("""<div class="facility-card"><div class="facility-icon">🏸</div><div class="facility-text">Badminton</div></div>""", unsafe_allow_html=True)
    with f4: st.markdown("""<div class="facility-card"><div class="facility-icon">🧤</div><div class="facility-text">Pro Gear</div></div>""", unsafe_allow_html=True)

    # --- PRO LIVE SCHEDULE (3 COLUMNS ON MOBILE) ---
    st.markdown("### 📅 Live Schedule")
    view_date = st.date_input("Check Availability For:", min_value=date.today())
    schedule_data = get_daily_schedule(view_date)
    
    # Building the HTML Grid string
    grid_html = '<div class="grid-container">'
    
    for slot in TIMESLOTS:
        if slot in schedule_data:
            # BOOKED
            name = schedule_data[slot]['name'][:8]
            sport = schedule_data[slot]['sport']
            grid_html += f'<div class="grid-item item-booked"><div class="time-font">{slot}</div><div class="text-booked">🔒 Booked</div><div class="player-name">{name}</div></div>'
        else:
            # OPEN
            grid_html += f'<div class="grid-item item-open"><div class="time-font">{slot}</div><div class="text-open">⚡ Available</div><div class="player-name">-</div></div>'
    
    grid_html += '</div>'
    
    # RENDER GRID
    st.markdown(grid_html, unsafe_allow_html=True)

    st.markdown("---")

    # --- BOOKING FORM ---
    with st.container(border=True):
        st.markdown("### ⚡ Fast Booking")
        c_name = st.text_input("Full Name", placeholder="e.g. Ali Khan")
        c_phone = st.text_input("Phone Number", placeholder="03xx-xxxxxxx")
        
        r1, r2 = st.columns(2)
        sport = r1.selectbox("Select Sport", list(PRICES.keys()), index=None, placeholder="Choose a Sport...")
        hours = r2.number_input("Hours to Play", 1, 6, 1)
        
        r3, r4 = st.columns(2)
        book_date = r3.date_input("Booking Date", min_value=date.today(), value=view_date)
        
        booked_on_date = get_daily_schedule(book_date)
        available_slots = [t for t in TIMESLOTS if t not in booked_on_date]
        
        if sport:
            time_slot = r4.selectbox("Select Time Slot", available_slots, placeholder="Select an open slot", index=None)
        else:
            time_slot = r4.selectbox("Select Time Slot", [], placeholder="Select Sport first")
        
        if sport: total = PRICES[sport] * hours
        else: total = 0
        
        st.markdown("---")
        
        # MESSAGE TO MANAGER
        st.markdown("##### 📝 Message to Manager (Optional)")
        user_note = st.text_area("Write any special request here...", height=80, placeholder="e.g. Need extra bats, booking for tournament, etc.", label_visibility="collapsed")
        
        st.markdown("---")
        
        # --- PAYMENT LOGO LOGIC ---
        jazz_path = find_image("jazzcash")
        if jazz_path:
            jazz_b64 = get_image_as_base64(jazz_path)
            jazz_html = f'<img src="data:image/png;base64,{jazz_b64}" width="80" style="border-radius:5px;">'
        else:
            # Safe Fallback Logo (Google Logo for stability or Text)
            jazz_html = '<div style="color:#10b981; font-weight:bold; font-size:20px;">JazzCash</div>'

        st.markdown(f"""
        <div class="payment-box">
            <div style="color: #10b981; font-weight: 800; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">💳 Payment Method</div>
            <div style="background: white; border-radius: 5px; display: inline-block; padding: 5px; margin-top: 5px;">
                {jazz_html}
            </div>
            <div class="account-number">0301-2434717</div>
            <p style="font-size: 11px; color: #94a3b8; margin-top: 5px;">* Please send payment proof to 0300-2434074</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("###")
        p1, p2 = st.columns([1, 1])
        with p1: st.markdown("<div style='margin-top: 10px; color: #94a3b8; font-size: 14px;'>Total Payable Amount</div>", unsafe_allow_html=True)
        with p2: st.markdown(f"<div class='digital-price'>PKR {total:,}</div>", unsafe_allow_html=True)
        
        st.markdown("###")
        if st.button("🔒 CONFIRM & BOOK", use_container_width=True):
            if c_name and c_phone and sport and time_slot:
                with st.spinner("Connecting to Arena Server..."):
                    time.sleep(1.5)
                    if add_booking(c_name, c_phone, sport, book_date, time_slot, hours, total, "Pending Verification", user_note):
                        st.balloons()
                        st.markdown(f"""
                        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; padding: 25px; border-radius: 20px; text-align: center; margin-top: 20px; box-shadow: 0 0 30px rgba(16, 185, 129, 0.2);">
                            <h1 style="color: #10b981; margin:0; font-size: 50px;">✅</h1>
                            <h2 style="color: white; margin: 10px 0;">Booking Received!</h2>
                            <p style="color: #cbd5e1; font-size: 16px;">Hey <strong>{c_name}</strong>, we have held your slot.</p>
                            <p style="color: #fbbf24; font-weight:bold;">Status: Pending Payment</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        wa_msg = f"Hi Hassan! I just booked {sport} for {total} PKR on {book_date} at {time_slot}. Name: {c_name}."
                        if user_note: wa_msg += f" Note: {user_note}"
                        st.link_button("📲 Click here to Send Proof on WhatsApp", f"https://wa.me/923002434074?text={wa_msg}", use_container_width=True)
                        time.sleep(2)
                        st.rerun()
                    else: st.error("❌ OOPS! That slot was just taken.")
            else: st.warning("⚠️ Please select a valid Time Slot and fill in all details.")

    # --- FAQ SECTION ---
    st.markdown("### ❓ Frequently Asked Questions")
    with st.expander("🤔 Do you provide bats and balls?"):
        st.write("Yes! We provide professional hard tennis balls and bats. However, players are welcome to bring their own gear if they prefer.")
    with st.expander("🚗 Is parking available?"):
        st.write("Absolutely. We have a dedicated parking area for both bikes and cars right outside the arena.")
    with st.expander("💳 Can I pay cash on spot?"):
        st.write("For advance booking, we require an online deposit via JazzCash to secure your slot. Walk-ins can pay cash, but slots are subject to availability.")
    with st.expander("👟 What shoes should I wear?"):
        st.write("Please wear non-marking sports shoes or joggers. Spikes or formal shoes are not allowed on the turf to prevent damage.")

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
                if st.button("Unlock Dashboard", use_container_width=True):
                    if pwd == "admin123":
                        st.session_state.admin_ok = True
                        st.rerun()
                    else: st.error("⛔ Access Denied")
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
        
        tab_manage, tab_add = st.tabs(["📋 Manage & Verify", "➕ Manual Booking"])
        
        with tab_manage:
            st.info("💡 Tip: Double-click on 'Status' to change 'Pending' to 'Payment Confirmed'.")
            edited_df = st.data_editor(
                df,
                column_config={
                    "status": st.column_config.SelectboxColumn("Payment Status", options=["Pending Verification", "Payment Confirmed", "Cancelled"], required=True, width="medium"),
                    "bill": st.column_config.NumberColumn("Bill (PKR)", format="Rs %d"),
                    "note": st.column_config.TextColumn("User Note", disabled=True)
                },
                use_container_width=True, hide_index=True, num_rows="fixed"
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

# --- FOOTER ---
st.markdown("""
<div class="custom-footer">
    <div style="color: #cbd5e1; font-size: 10px; margin-bottom: 8px; letter-spacing: 1px;">CONNECT WITH US</div>
    <div class="social-bar">
        <a href="#" class="social-icon tiktok" title="TikTok"><i class="fab fa-tiktok"></i></a>
        <a href="#" class="social-icon facebook" title="Facebook"><i class="fab fa-facebook-f"></i></a>
        <a href="#" class="social-icon instagram" title="Instagram"><i class="fab fa-instagram"></i></a>
        <a href="#" class="social-icon youtube" title="YouTube"><i class="fab fa-youtube"></i></a>
    </div>
    © 2026 SM Arena Shujabad | Developed by <b>Hassan Nisar Rao</b>
</div>
""", unsafe_allow_html=True)
