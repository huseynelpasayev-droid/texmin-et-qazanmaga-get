import streamlit as st
import random
import time

# Sayt ayarları
st.set_page_config(page_title="Huseyn Elpasayev Games", page_icon="🚀", layout="wide")

# 1. YAPIMCI MƏLUMATI (Girişdə)
st.sidebar.markdown("### 🛠️ Redaktor & Yapımcı:")
st.sidebar.info("✨ **Huseyn Elpasayev**")

# 2. ƏTRAFDAN ŞARLAR VƏ SƏS
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            var duration = 3 * 1000;
            var end = Date.now() + duration;
            (function frame() {
              confetti({ particleCount: 5, angle: 60, spread: 55, origin: { x: 0 } });
              confetti({ particleCount: 5, angle: 120, spread: 55, origin: { x: 1 } });
              if (Date.now() < end) { requestAnimationFrame(frame); }
            }());
            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
        </script>
        """, height=0,
    )

# 3. YADDAŞ SİSTEMİ
if 'balonlar' not in st.session_state: st.session_state.balonlar = 0
if 'istifadeci_adi' not in st.session_state: st.session_state.istifadeci_adi = ""
if 'dostlar' not in st.session_state: st.session_state.dostlar = []
if 'mesajlar' not in st.session_state: st.session_state.mesajlar = {}
if 'oyun_modu' not in st.session_state: st.session_state.oyun_modu = "Reqem"

# --- GİRİŞ EKRANI ---
if not st.session_state.istifadeci_adi:
    st.title("🚀 Huseyn Elpasayev Games Dünyasına Xoş Gəldin!")
    ad = st.text_input("Adını yaz və daxil ol:")
    if st.button("Dünyaya Giriş Et"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- SİDEBAR ---
st.sidebar.title(f"👤 {st.session_state.istifadeci_adi}")
st.sidebar.metric("Balon Sayı", f"🎈 {st.session_state.balonlar}")
st.sidebar.divider()

# --- TABLAR ---
tab1, tab2, tab3 = st.tabs(["🎮 Oyunlar", "🤝 Dostluq & Chat", "🛒 Mağaza"])

# --- TAB 1: OYUNLAR ---
with tab1:
    # Mavi Pult Gizli Düymə
    c1, c2 = st.columns([10, 1])
    c1.subheader(f"Hazırkı Oyun: {st.session_state.oyun_modu}")
    if c2.button("🎮"):
        st.session_state.qazandi = True

    if st.session_state.oyun_modu == "Reqem":
        if 'gizli' not in st.session_state:
            st.session_state.gizli = random.randint(1, 100)
            st.session_state.qazandi = False
        
        texmin = st.number_input("1-100 arası rəqəm seç:", 1, 100)
        if st.button("Təxmin Et"):
            if texmin == st.session_state.gizli: st.session_state.qazandi = True
            elif texmin < st.session_state.gizli: st.warning("⬆️ Daha BÖYÜK!")
            else: st.warning("⬇️ Daha KİÇİK!")

    elif st.session_state.oyun_modu == "Silah":
        st.write("🎯 **Hədəfi vur və balon qazan!**")
        target = random.choice(["🎯", "👾", "🦖"])
        st.title(f"Hədəf: {target}")
        if st.button("🔥 ATEŞ ET!"):
            st.session_state.qazandi = True

    # QALİBİYYƏT ANI
    if st.session_state.get('qazandi'):
        balon_qazanc = random.randint(10, 30)
        st.session_state.balonlar += balon_qazanc
        st.success(f"🎊 Möhtəşəm! +{balon_qazanc} Balon!")
        qelebe_effekti()
        
        if st.button("Növbəti Oyun (Random)"):
            # Random oyun seçimi
            st.session_state.oyun_modu = random.choice(["Reqem", "Silah"])
            if 'gizli' in st.session_state: del st.session_state.gizli
            st.session_state.qazandi = False
            st.rerun()

# --- TAB 2: DOSTLUQ & CHAT ---
with tab2:
    st.subheader("👥 Dostluq Paneli")
    dost_adi = st.text_input("Dostluq atmaq üçün ad yaz:")
    if st.button("İstək Göndər"):
        st.toast(f"✅ {dost_adi} adına istək yollandı!")

    st.divider()
    if not st.session_state.dostlar:
        if st.button("Huseyn Elpasayev ilə dost ol (Test)"):
            st.session_state.dostlar.append("Huseyn Elpasayev")
            st.rerun()
    else:
        secilen = st.selectbox("Dost seç:", st.session_state.dostlar)
        msg = st.text_input(f"{secilen} üçün mesaj:")
        if st.button("Göndər"):
            if secilen not in st.session_state.mesajlar: st.session_state.mesajlar[secilen] = []
            st.session_state.mesajlar[secilen].append(f"Mən: {msg}")
            st.rerun()
        for m in st.session_state.mesajlar.get(secilen, []):
            st.write(m)

# --- TAB 3: MAĞAZA ---
with tab3:
    st.subheader("🛒 Karakter Mağazası")
    st.write("Tezliklə yeni karakterlər əlavə olunacaq...")
    st.metric("Sənin Balonun", st.session_state.balonlar)
