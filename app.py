import streamlit as st
import random

# 1. GOOGLE AXTARIŞI ÜÇÜN BAŞLIQ (SEO)
st.set_page_config(
    page_title="Huseyn Elpasayevin Texmin Et Oyunu - Oyna və Qazan", 
    page_icon="🚀", 
    layout="wide"
)

# 2. YAPIMCI İMZASI (Saytın hər yerində)
st.sidebar.markdown("# 🛠️ YAPIMCI")
st.sidebar.info("### ✨ Huseyn Elpasayev")
st.sidebar.write("Bu oyun rəsmi olaraq Huseyn Elpasayev tərəfindən redaktə olunub.")

# --- ƏTRAFDAN ŞARLAR FUNKSİYASI ---
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            var duration = 3 * 1000;
            var end = Date.now() + duration;
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

# --- YADDAŞ ---
if 'balonlar' not in st.session_state: st.session_state.balonlar = 0
if 'istifadeci_adi' not in st.session_state: st.session_state.istifadeci_adi = ""

# --- GİRİŞ ---
if not st.session_state.istifadeci_adi:
    st.title("🌟 Huseyn Elpasayevin Texmin Et Dünyası")
    st.subheader("Google & Play Store Stilində Oyun Platforması")
    ad = st.text_input("Oyunçu Adın:")
    if st.button("Oyuna Başla"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- OYUN SAHƏSİ ---
st.title(f"🎮 Huseyn Elpasayevin Texmin Et... (Xoş gəldin, {st.session_state.istifadeci_adi}!)")

# Mavi Pult (Gizli Cheat)
c1, c2 = st.columns([10, 1])
if c2.button("🎮"):
    st.session_state.qazandi = True

if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)
    st.session_state.qazandi = False

if not st.session_state.qazandi:
    texmin = st.number_input("1-100 arası rəqəmi tap:", 1, 100)
    if st.button("Yoxla"):
        if texmin == st.session_state.gizli:
            st.session_state.qazandi = True
            st.rerun()
        elif texmin < st.session_state.gizli: st.warning("⬆️ Daha BÖYÜK!")
        else: st.warning("⬇️ Daha KİÇİK!")
else:
    st.success("🎊 HALALDIR! Sən Huseyn Elpasayevin oyununda qalib gəldin!")
    st.session_state.balonlar += 20
    qelebe_effekti()
    if st.button("Yenidən Oyna"):
        del st.session_state.gizli
        st.session_state.qazandi = False
        st.rerun()

st.sidebar.divider()
st.sidebar.metric("🎈 Topladığın Balonlar", st.session_state.balonlar)
