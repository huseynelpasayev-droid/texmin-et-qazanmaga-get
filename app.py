import streamlit as st
import random

# 1. 3D GÖRÜNÜŞ VƏ KONFETTİ AYARLARI
st.set_page_config(page_title="Huseyn Elpasayev 3D World", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(45deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    .game-box {
        border: 2px solid #00f2fe;
        border-radius: 15px;
        padding: 20px;
        background: rgba(0, 0, 0, 0.5);
        box-shadow: 0 0 20px #00f2fe;
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

# 2. YADDAŞ SİSTEMİ
if 'balonlar' not in st.session_state: st.session_state.balonlar = 50  # Başlanğıc pulu
if 'istifadeci_adi' not in st.session_state: st.session_state.istifadeci_adi = ""
if 'karakter' not in st.session_state: st.session_state.karakter = "Standart"
if 'qazandi' not in st.session_state: st.session_state.qazandi = False

# 3. GİRİŞ EKRANI
if not st.session_state.istifadeci_adi:
    st.title("🌐 3D Huseyn Elpasayev Dünyasına Giriş")
    ad = st.text_input("Oyunçu adını yarat:")
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

# --- TABLAR ---
tab1, tab2, tab3 = st.tabs(["🎮 3D Oyun Sahəsi", "🛒 Mağaza", "⭐ Reytinq"])

with tab1:
    st.markdown(f"### 🚀 Sən bu 3D məkanda gizlənmiş rəqəmi tapmalısan!")
    st.info("💡 Diqqət: Hər səhv təxminində 5-15 arası balonun eksiləcək!")
    
    if 'gizli' not in st.session_state:
        st.session_state.gizli = random.randint(1, 100)

    # KARAKTER XÜSUSİYYƏTLƏRİ (MƏNTİQ)
    if st.session_state.karakter == "Dəqiqlik Ustası":
        tip = "Cüt" if st.session_state.gizli % 2 == 0 else "Tək"
        st.sidebar.success(f"🎯 Ustanın köməyi: Rəqəm {tip} rəqəmdir!")
    
    if st.session_state.karakter == "Şanslı Hüseyn":
        st.sidebar.warning("✨ Hüseyn pıçıldayır: Rəqəm 1-100 arasındadır!")

    # OYUN SAHƏSİ
    with st.container():
        st.markdown('<div class="game-box">', unsafe_allow_html=True)
        texmin = st.number_input("Rəqəmi bura yaz:", 1, 100, key="3d_input")
        
        if st.button("Təxmini Göndər 📡"):
            if texmin == st.session_state.gizli:
                st.session_state.qazandi = True
                st.rerun()
            else:
                # PULUN EKSİLMƏSİ
                cixilan_pul = random.randint(5, 15)
                st.session_state.balonlar -= cixilan_pul
                
                if st.session_state.karakter == "İnadkar İbrahim":
                    st.error(f"❌ Səhvdir! Amma İbrahim deyir: 'Vaz keçmə!' (-{cixilan_pul} 💰)")
                else:
                    st.error(f"❌ Tapmadın! {cixilan_pul} balon itirdin!")
                
                if texmin < st.session_state.gizli: st.write("🔭 Sensorlar: Daha YUXARI bax!")
                else: st.write("🔭 Sensorlar: Daha AŞAĞI bax!")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.qazandi:
        st.balloons()
        qelebe_effekti()
        hediyye = 50 if st.session_state.karakter == "Kral Qalib" else 25
        st.success(f"🎊 Qələbə! {hediyye} balon qazandın!")
        if st.button("Yeni 3D Raund"):
            st.session_state.balonlar += hediyye
            del st.session_state.gizli
            st.session_state.qazandi = False
            st.rerun()

with tab2:
    st.subheader("🛒 Karakter Mağazası")
    karakterler = {
        "Standart": 0,
        "Şanslı Hüseyn": 0,
        "İnadkar İbrahim": 30,
        "Dəqiqlik Ustası": 60,
        "Kral Qalib": 100
    }
    for k, p in karakterler.items():
        if st.button(f"Aç/Seç: {k} ({p} 💰)"):
            if st.session_state.balonlar >= p:
                st.session_state.karakter = k
                st.toast(f"{k} seçildi!")
            else:
                st.error("Kifayət qədər balonun yoxdur!")

with tab3:
    st.write("🌟 **Huseyn Elpasayev Games** tərəfindən təqdim olundu.")
    st.write("Reytinq: ⭐⭐⭐⭐⭐ (5/5)")
