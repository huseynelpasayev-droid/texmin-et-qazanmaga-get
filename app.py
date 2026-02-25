import streamlit as st
import random

# 1. SƏHİFƏ VƏ NEON CSS AYARLARI
st.set_page_config(page_title="Huseyn Elpasayev Neon World", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    /* Arxa fon */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* BÜTÜN DÜYMƏLƏR ÜÇÜN RƏNG (AĞ OLMASIN DEYƏ) */
    div.stButton > button {
        background: linear-gradient(45deg, #005f73, #0a9396) !important;
        color: #ffffff !important;
        border: 2px solid #94d2bd !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        box-shadow: 0 0 10px rgba(10, 147, 150, 0.5) !important;
        transition: all 0.3s ease !important;
    }

    /* Pult Düyməsi (Xüsusi Stil - Sağda və Parlayan) */
    .pult-button {
        position: fixed;
        top: 60px;
        right: 20px;
        z-index: 999;
    }

    /* Düymə üzərinə gələndə */
    div.stButton > button:hover {
        background: linear-gradient(45deg, #ee9b00, #ca6702) !important;
        box-shadow: 0 0 20px #e9d8a6 !important;
        transform: scale(1.05);
    }

    /* Oyun Qutusu */
    .game-card {
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid #00d2ff;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def qelebe_effekti():
    st.components.v1.html("""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
            confetti({ particleCount: 200, spread: 100, origin: { y: 0.6 } });
        </script>""", height=0)

# 2. YADDAŞ (SESSION STATE)
if 'balonlar' not in st.session_state: st.session_state.balonlar = 100
if 'istifadeci_adi' not in st.session_state: st.session_state.istifadeci_adi = ""
if 'karakter' not in st.session_state: st.session_state.karakter = "Standart"
if 'qazandi' not in st.session_state: st.session_state.qazandi = False

# --- GİRİŞ EKRANI ---
if not st.session_state.istifadeci_adi:
    st.title("🌐 Huseyn Elpasayev Neon World")
    ad = st.text_input("Profil Adın:", placeholder="Adını bura yaz...")
    if st.button("Dünyaya Daxil Ol 🚀"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- SİDEBAR ---
st.sidebar.title(f"👤 {st.session_state.istifadeci_adi}")
st.sidebar.metric("💰 Balon Pulun", st.session_state.balonlar)
st.sidebar.info(f"🎭 Karakter: {st.session_state.karakter}")
st.sidebar.write("🛠️ Yapımcı: **Huseyn Elpasayev**")

# --- PULT (GİZLİ DÜYMƏ) ---
# Sağ yuxarıda həmişə görünməsi üçün
with st.container():
    st.markdown('<div class="pult-button">', unsafe_allow_html=True)
    if st.button("🎮 PULT"):
        st.session_state.qazandi = True
        st.toast("Hiylə aktiv edildi! 😉")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TABLAR ---
tab1, tab2, tab3, tab4 = st.tabs(["🎯 3D Oyun", "🛒 Mağaza", "💬 Chat", "⭐ Reytinq"])

with tab1:
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    if 'gizli' not in st.session_state: st.session_state.gizli = random.randint(1, 100)

    if not st.session_state.qazandi:
        texmin = st.number_input("Rəqəmi tap (1-100):", 1, 100)
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
        qelebe_effekti()
        st.success("🎊 Möhtəşəm! Qalib gəldin!")
        if st.button("Yeni Raund 🔄"):
            st.session_state.balonlar += 30
            del st.session_state.gizli
            st.session_state.qazandi = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("🛒 Mağaza")
    if st.button("Dəqiqlik Ustası (60 💰)"):
        if st.session_state.balonlar >= 60:
            st.session_state.karakter = "Dəqiqlik Ustası"
            st.session_state.balonlar -= 60
            st.rerun()
