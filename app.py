import streamlit as st
import random

# 1. SƏHİFƏ VƏ RƏNGLİ DÜYMƏ AYARLARI
st.set_page_config(page_title="Huseyn Elpasayev Ultimate", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    
    /* Bütün düymələrin rəngini tünd və parlayan edirik */
    div.stButton > button {
        background: linear-gradient(45deg, #0077b6, #00b4d8) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #90e0ef !important;
        font-weight: bold !important;
        box-shadow: 0 0 10px rgba(0, 180, 216, 0.5) !important;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(45deg, #fb8500, #ffb703) !important;
        box-shadow: 0 0 20px #ffb703 !important;
    }

    .game-card {
        background: rgba(0, 0, 0, 0.5);
        border: 2px solid #00b4d8;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. YADDAŞ SİSTEMİ
if 'balonlar' not in st.session_state: st.session_state.balonlar = 100
if 'istifadeci_adi' not in st.session_state: st.session_state.istifadeci_adi = ""
if 'karakter' not in st.session_state: st.session_state.karakter = "Standart"
if 'mesajlar' not in st.session_state: st.session_state.mesajlar = []
if 'qazandi' not in st.session_state: st.session_state.qazandi = False

# --- GİRİŞ ---
if not st.session_state.istifadeci_adi:
    st.title("🌐 Huseyn Elpasayev Dünyası")
    ad = st.text_input("Adını yaz:")
    if st.button("Başla 🚀"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- SİDEBAR ---
st.sidebar.header(f"👤 {st.session_state.istifadeci_adi}")
st.sidebar.metric("💰 Balonun", st.session_state.balonlar)
st.sidebar.info(f"🎭 Karakter: {st.session_state.karakter}")
st.sidebar.write("---")
st.sidebar.write("🛠️ Yapımcı: **Huseyn Elpasayev**")

# --- PULT (SAĞDA GİZLİ) ---
col_p1, col_p2 = st.columns([10, 1])
if col_p2.button("🎮"):
    st.session_state.qazandi = True
    st.toast("Pult aktivdir!")

# --- TABLAR ---
tab1, tab2, tab3, tab4 = st.tabs(["🎮 Oyun", "🛒 Mağaza", "💬 Chat", "⭐ Reytinq"])

with tab1:
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.subheader("🔭 3D Məkanda Rəqəmi Tap!")
    # İSTƏDİYİN O VACİB YAZI:
    st.markdown("<h4 style='color: #ffb703;'>⚠️ Diqqət: Hər səhv təxmin 5-15 balon aparır!</h4>", unsafe_allow_html=True)
    
    if 'gizli' not in st.session_state: st.session_state.gizli = random.randint(1, 100)
    
    if not st.session_state.qazandi:
        texmin = st.number_input("Rəqəmi yaz (1-100):", 1, 100, key="n_in")
        if st.button("Təxmin Et"):
            if texmin == st.session_state.gizli:
                st.session_state.qazandi = True
                st.rerun()
            else:
                cixilan = random.randint(5, 15)
                st.session_state.balonlar -= cixilan
                if texmin < st.session_state.gizli: st.warning("🔭 Daha YUXARI!")
                else: st.warning("🔭 Daha AŞAĞI!")
    
    if st.session_state.qazandi:
        st.balloons()
        st.success("🎊 Qələbə!")
        if st.button("Yeni Oyun 🔄"):
            st.session_state.balonlar += 30
            del st.session_state.gizli
            st.session_state.qazandi = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("🛒 Bütün Karakterlər")
    k_list = {
        "Standart": 0, 
        "Şanslı Hüseyn": 0, 
        "İnadkar İbrahim": 30, 
        "Dəqiqlik Ustası": 60, 
        "Kral Qalib": 100
    }
    for k, p in k_list.items():
        c1, c2 = st.columns([3, 1])
        c1.write(f"**{k}** ({p} 💰)")
        if c2.button(f"Al/Seç", key=f"k_{k}"):
            if st.session_state.balonlar >= p:
                st.session_state.karakter = k
                st.success(f"{k} seçildi!")
            else: st.error("Pulun çatmır!")

with tab3:
    st.subheader("💬 Canlı Chat")
    # MESAJ YAZMAQ ÜÇÜN YER
    yeni_mesaj = st.text_input("Mesajını bura yaz:", placeholder="Salam dostlar...")
    if st.button("Göndər ✉️"):
        if yeni_mesaj:
            st.session_state.mesajlar.append(f"**{st.session_state.istifadeci_adi}**: {yeni_mesaj}")
    
    st.write("---")
    for m in reversed(st.session_state.mesajlar):
        st.write(m)

with tab4:
    st.subheader("⭐ Reytinq Cədvəli")
    st.write(f"1. **Huseyn Elpasayev** - 999,999 🎈")
    st.write(f"2. **{st.session_state.istifadeci_adi}** - {st.session_state.balonlar} 🎈")
    st.write(f"3. **Dostun** - 50 🎈")
    st.divider()
    st.write("🌍 Global Reytinq: 4.9/5.0")
