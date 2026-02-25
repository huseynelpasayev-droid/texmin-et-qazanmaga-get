import streamlit as st
import random

# 1. GOOGLE AXTARIŞI ÜÇÜN BAŞLIQ
st.set_page_config(page_title="Huseyn Elpasayevin Texmin Et Oyunu", page_icon="🚀", layout="wide")

# 2. ŞARLAR VƏ SƏS
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            var end = Date.now() + (3 * 1000);
            (function frame() {
              confetti({ particleCount: 7, angle: 60, spread: 55, origin: { x: 0 } });
              confetti({ particleCount: 7, angle: 120, spread: 55, origin: { x: 1 } });
              if (Date.now() < end) { requestAnimationFrame(frame); }
            }());
            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
        </script>
        """, height=0,
    )

# 3. YADDAŞI QURAQ (Xətasız giriş üçün)
if 'balonlar' not in st.session_state: st.session_state.balonlar = 0
if 'istifadeci_adi' not in st.session_state: st.session_state.istifadeci_adi = ""
if 'qazandi' not in st.session_state: st.session_state.qazandi = False

# --- GİRİŞ EKRANI ---
if not st.session_state.istifadeci_adi:
    st.title("🌟 Huseyn Elpasayevin Oyun Dünyası")
    ad = st.text_input("Adını yaz:")
    if st.button("Daxil Ol"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- OYUN SAHƏSİ ---
st.sidebar.title(f"👤 {st.session_state.istifadeci_adi}")
st.sidebar.metric("🎈 Balonlar", st.session_state.balonlar)
st.sidebar.write("🛠️ **Yapımcı: Huseyn Elpasayev**")

st.title(f"🎮 Texmin Et və Qazan!")

if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)

c1, c2 = st.columns([10, 1])
if c2.button("🎮"): st.session_state.qazandi = True

if not st.session_state.qazandi:
    texmin = st.number_input("1-100 arası rəqəm:", 1, 100)
    if st.button("Yoxla"):
        if texmin == st.session_state.gizli:
            st.session_state.qazandi = True
            st.rerun()
        elif texmin < st.session_state.gizli: st.warning("⬆️ BÖYÜK!")
        else: st.warning("⬇️ KİÇİK!")
else:
    st.success("🎊 Qələbə!")
    st.session_state.balonlar += 20
    qelebe_effekti()
    if st.button("Yenidən Oyna"):
        del st.session_state.gizli
        st.session_state.qazandi = False
        st.rerun()
