import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Balon Ustası Pro", page_icon="🎈", layout="centered")

# 1. Hər tərəfdən çıxan Şar/Konfetti effekti (JavaScript)
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            var end = Date.now() + (3 * 1000); // 3 saniyə davam etsin

            (function frame() {
              // Soldan şarlar
              confetti({
                particleCount: 3,
                angle: 60,
                spread: 55,
                origin: { x: 0 },
                colors: ['#ff0000', '#00ff00', '#0000ff', '#ffff00']
              });
              // Sağdan şarlar
              confetti({
                particleCount: 3,
                angle: 120,
                spread: 55,
                origin: { x: 1 },
                colors: ['#ff00ff', '#00ffff', '#ff8000', '#8000ff']
              });

              if (Date.now() < end) {
                requestAnimationFrame(frame);
              }
            }());

            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
        </script>
        """, height=0,
    )

# 2. Karakter Bazası
karakter_bazasi = {
    "Standart": {"desc": "Sadiqcə oynayır.", "price": 0},
    "Şanslı Hüseyn": {"desc": "✨ Yaxınlaşanda 'İstidir' deyir!", "price": 0},
    "İnadkar İbrahim": {"desc": "⏳ Hər səhvdə motivasiya verir.", "price": 15},
    "Dəqiqlik Ustası": {"desc": "🎯 Tək/Cüt olduğunu bilir.", "price": 40},
    "Kral Qalib": {"desc": "👑 Hər qələbədə 2 qat balon verir!", "price": 100}
}

# 3. Yaddaş
if 'balonlar' not in st.session_state:
    st.session_state.balonlar = 0
if 'aciq_karakterler' not in st.session_state:
    st.session_state.aciq_karakterler = ["Standart", "Şanslı Hüseyn"]
if 'istifadeci_adi' not in st.session_state:
    st.session_state.istifadeci_adi = ""
if 'karakter' not in st.session_state:
    st.session_state.karakter = ""

# --- GİRİŞ ---
if not st.session_state.istifadeci_adi:
    st.title("🎈 Balon Yığ və Karakter Aç!")
    ad = st.text_input("Adını yaz:")
    if st.button("Dünyaya Giriş Et"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- SİDEBAR ---
st.sidebar.title(f"👤 {st.session_state.istifadeci_adi}")
st.sidebar.markdown(f"### 🎈 Balon Sayı: **{st.session_state.balonlar}**")
st.sidebar.divider()

st.sidebar.subheader("🛒 Mağaza")
for k, v in karakter_bazasi.items():
    if k in st.session_state.aciq_karakterler:
        if st.sidebar.button(f"Seç: {k}", key=f"sel_{k}"):
            st.session_state.karakter = k
            st.rerun()
    else:
        if st.sidebar.button(f"Aç: {k} (💰 {v['price']})", key=f"buy_{k}"):
            if st.session_state.balonlar >= v['
