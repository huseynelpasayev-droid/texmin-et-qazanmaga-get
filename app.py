import streamlit as st
import random

# 1. SƏHİFƏ VƏ 3D DİZAYN AYARLARI
st.set_page_config(page_title="Huseyn Elpasayev Ultimate World", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        color: white;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #00d2ff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 15px #00d2ff;
    }
    </style>
    """, unsafe_allow_html=True)

def qelebe_effekti():
    st.components.v1.html("""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
            confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
        </script>""", height=0)

# 2. YADDAŞ (SESSION STATE)
if 'balonlar' not in st.session_state: st.session_state.balonlar = 100
if 'istifadeci_adi' not in st.session_state: st.session_state.istifadeci_adi = ""
if 'karakter' not in st.session_state: st.session_state.karakter = "Standart"
if 'qazandi' not in st.session_state: st.session_state.qazandi = False
if 'dostlar' not in st.session_state: st.session_state.dostlar = ["Huseyn Elpasayev"]

# --- GİRİŞ EKRANI ---
if not st.session_state.istifadeci_adi:
    st.title("🚀 Huseyn Elpasayev Games-ə Giriş")
    ad = st.text_input("Profil adını yarat:")
    if st.button("Dünyaya Daxil Ol"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- SİDEBAR ---
st.sidebar.title(f"👤 {st.session_state.istifadeci_adi}")
st.sidebar.metric("💰 Balon Pulun", st.session_state.balonlar)
st.sidebar.info(f"🎭 Karakter: {st.session_state.karakter}")
st.sidebar.write("---")
st.sidebar.write("🛠️ Yapımcı: **Huseyn Elpasayev**")

# --- ƏSAS TABLAR (HAMISI BURADADIR) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 3D Oyun", "🛒 Mağaza", "🤝 Dostluq", "💬 Chat", "⭐ Reytinq"])

# --- TAB 1: 3D OYUN ---
with tab1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🔭 3D Məkanda Rəqəmi Tap!")
    st.write("Diqqət: Hər səhv təxmin 5-15 balon aparır!")
    
    if 'gizli' not in st.session_state: st.session_state.gizli = random.randint(1, 100)

    # Karakter Köməyi
    if st.session_state.karakter == "Dəqiqlik Ustası":
        tip = "Cüt" if st.session_state.gizli % 2 == 0 else "Tək"
        st.info(f"🎯 Usta deyir: Rəqəm {tip} rəqəmdir!")

    texmin = st.number_input("Rəqəmi təxmin et (1-100):", 1, 100, key="game_in")
    if st.button("Təxmini Göndər"):
        if texmin == st.session_state.gizli:
            st.session_state.qazandi = True
            st.rerun()
        else:
            cixilan = random.randint(5, 15)
            st.session_state.balonlar -= cixilan
            st.error(f"❌ Səhvdir! -{cixilan} 💰")
            if texmin < st.session_state.gizli: st.write("🔭 Daha YUXARI bax!")
            else: st.write("🔭 Daha AŞAĞI bax!")
    
    if st.session_state.qazandi:
        qelebe_effekti()
        hediyye = 50 if st.session_state.karakter == "Kral Qalib" else 25
        st.success(f"🎊 Qələbə! +{hediyye} balon!")
        if st.button("Yeni Raund"):
            st.session_state.balonlar += hediyye
            del st.session_state.gizli
            st.session_state.qazandi = False
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: MAĞAZA ---
with tab2:
    st.subheader("🛒 Karakter Mağazası")
    karakterler = {"Standart": 0, "Şanslı Hüseyn": 0, "İnadkar İbrahim": 30, "Dəqiqlik Ustası": 60, "Kral Qalib": 100}
    for k, p in karakterler.items():
        if st.button(f"Seç: {k} ({p} 💰)"):
            if st.session_state.balonlar >= p:
                st.session_state.karakter = k
                st.toast(f"{k} seçildi!")
            else: st.error("Balonun çatmır!")

# --- TAB 3: DOSTLUQ ---
with tab3:
    st.subheader("🤝 Dostluq Sistemi")
    yeni_dost = st.text_input("Dostluq atmaq üçün ad yaz:")
    if st.button("İstək Göndər"):
        st.toast(f"✅ {yeni_dost} istifadəçisinə istək yollandı!")

# --- TAB 4: CHAT ---
with tab4:
    st.subheader("💬 Şəxsi Mesajlar")
    secilen_dost = st.selectbox("Dost seç:", st.session_state.dostlar)
    mesaj = st.text_input(f"{secilen_dost} üçün mesaj yaz:")
    if st.button("Göndər"):
        st.toast("Mesaj göndərildi! ✅")

# --- TAB 5: REYTİNQ ---
with tab5:
    st.subheader("⭐ Reytinq və Rəylər")
    st.write("1. Huseyn Elpasayev - 999,999 🎈")
    st.write(f"2. {st.session_state.istifadeci_adi} - {st.session_state.balonlar} 🎈")
    st.divider()
    st.write("Google Play Reytinqi: 4.9/5.0 ⭐")
