import streamlit as st
import random

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="Huseyn Elpasayev Games", page_icon="🚀", layout="wide")

# 2. ŞARLAR VƏ SƏS EFFEKTİ
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            var duration = 3 * 1000;
            var end = Date.now() + duration;
            (function frame() {
              confetti({ particleCount: 10, angle: 60, spread: 55, origin: { x: 0 } });
              confetti({ particleCount: 10, angle: 120, spread: 55, origin: { x: 1 } });
              if (Date.now() < end) { requestAnimationFrame(frame); }
            }());
            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
        </script>
        """, height=0,
    )

# 3. YADDAŞI TƏMİZLƏYƏK VƏ QURAQ
if 'istifadeci_adi' not in st.session_state:
    st.session_state.istifadeci_adi = ""
if 'balonlar' not in st.session_state:
    st.session_state.balonlar = 0
if 'qazandi' not in st.session_state:
    st.session_state.qazandi = False

# --- GİRİŞ EKRANI (AD YARATMAQ HİSSƏSİ) ---
# Əgər ad yoxdursa, ancaq bu hissə görünəcək
if st.session_state.istifadeci_adi == "":
    st.title("🌟 Huseyn Elpasayevin Oyun Dünyası")
    st.subheader("Xoş gəldin! Oyuna başlamaq üçün profil yarat.")
    
    yeni_ad = st.text_input("Adını yaz:", placeholder="Məsələn: Huseyn777")
    
    if st.button("Dünyaya Giriş Et 🚀"):
        if yeni_ad.strip() != "":
            st.session_state.istifadeci_adi = yeni_ad
            st.success(f"Profil yaradıldı! Xoş gəldin, {yeni_ad}!")
            st.rerun() # Səhifəni yeniləyir və oyunu açır
        else:
            st.error("Zəhmət olmasa bir ad daxil et!")
    
    # Giriş ekranında yapımcı qeydi
    st.info("Redaktor & Yapımcı: Huseyn Elpasayev")
    st.stop() # Kodun qalan hissəsinin işləməsini dayandırır

# --- OYUN AÇILDIQDAN SONRA GÖRÜNƏN HİSSƏ ---
st.sidebar.title(f"👤 {st.session_state.istifadeci_adi}")
st.sidebar.metric("🎈 Balonların", st.session_state.balonlar)
st.sidebar.markdown("---")
st.sidebar.write("🛠️ **Yapımcı: Huseyn Elpasayev**")

if st.sidebar.button("Hesabdan Çıx"):
    st.session_state.istifadeci_adi = ""
    st.rerun()

# Əsas Oyun Sahəsi
st.title(f"🎮 Huseyn Elpasayev Games")
tab1, tab2 = st.tabs(["🎯 Rəqəmi Tap", "💬 Chat"])

with tab1:
    if 'gizli' not in st.session_state:
        st.session_state.gizli = random.randint(1, 100)
    
    c1, c2 = st.columns([10, 1])
    if c2.button("🎮"): # Mavi pult gizli düymə
        st.session_state.qazandi = True
    
    if not st.session_state.qazandi:
        texmin = st.number_input("1-100 arası rəqəm seç:", 1, 100)
        if st.button("Yoxla"):
            if texmin == st.session_state.gizli:
                st.session_state.qazandi = True
                st.rerun()
            elif texmin < st.session_state.gizli: st.warning("⬆️ DAHA BÖYÜK!")
            else: st.warning("⬇️ DAHA KİÇİK!")
    else:
        st.success(f"🎊 Möhtəşəm qələbə, {st.session_state.istifadeci_adi}!")
        qelebe_effekti()
        if st.button("Yenidən Başla"):
            del st.session_state.gizli
            st.session_state.qazandi = False
            st.session_state.balonlar += 10
            st.rerun()

with tab2:
    st.write("Dostlarınla söhbət etmək üçün onları linklə oyuna dəvət et!")
    st.text_input("Mesaj yaz:")
    st.button("Göndər")
