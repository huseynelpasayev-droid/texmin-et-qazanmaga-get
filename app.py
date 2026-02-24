import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Rəqəmi Tap: Səsli Versiya", page_icon="🎭", layout="centered")

# 1. Konfetti və Səs Funksiyası (JavaScript)
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            // Konfetti partlayışı
            confetti({
                particleCount: 200,
                spread: 90,
                origin: { y: 0.6 }
            });
            
            // Qələbə səsi (Audio obyekt yaradılır)
            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
        </script>
        """,
        height=0,
    )

# 2. Karakterlər və Özəllikləri
karakterler = {
    "Standart": "Heç bir özəlliyi yoxdur.",
    "Şanslı Hüseyn": "✨ Özəllik: Rəqəmə 10 rəqəm qalmış sənə 'İstidir!' deyəcək.",
    "İnadkar İbrahim": "⏳ Özəllik: Səhv edəndə hər dəfə fərqli motivasiya mesajı verir.",
    "Dəqiqlik Ustası": "🎯 Özəllik: Rəqəmin tək və ya cüt olduğunu əvvəldən bilir.",
    "Gözüaçıq Günel": "👁️ Özəllik: Hər 3 cəhddən bir rəqəm aralığını daraldır."
}

# 3. Giriş və Profil
if 'istifadeci_adi' not in st.session_state:
    st.session_state.istifadeci_adi = ""

if not st.session_state.istifadeci_adi:
    st.title("🎭 Karakterini Seç və Başla!")
    ad = st.text_input("Adın:")
    secim = st.selectbox("Bir karakter seç:", list(karakterler.keys()))
    if st.button("Oyuna Gir"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.session_state.karakter = secim
            st.rerun()
    st.stop()

# Oyun Başlığı
st.title(f"🎮 {st.session_state.karakter} {st.session_state.istifadeci_adi}")
st.caption(karakterler[st.session_state.karakter])

if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)
    st.session_state.say = 0

# Karakter özəlliyi: Dəqiqlik Ustası üçün ipucu
if st.session_state.karakter == "Dəqiqlik Ustası" and st.session_state.say == 0:
    tip = "CÜT" if st.session_state.gizli % 2 == 0 else "TƏK"
    st.info(f"🎯 Usta İpucu: Bu rəqəm **{tip}** rəqəmdir.")

texmin = st.number_input("Təxminin:", 1, 100)

if st.button("Yoxla"):
    st.session_state.say += 1
    fərq = abs(texmin - st.session_state.gizli)
    
    if texmin < st.session_state.gizli:
        msg = "⬆️ Daha BÖYÜK!"
        if st.session_state.karakter == "Şanslı Hüseyn" and fərq <= 10:
            msg += " (Çox istidir! 🔥)"
        st.warning(msg)
        
    elif texmin > st.session_state.gizli:
        msg = "⬇️ Daha KİÇİK!"
        if st.session_state.karakter == "Şanslı Hüseyn" and fərq <= 10:
            msg += " (Çox istidir! 🔥)"
        st.warning(msg)
        
    else:
        st.success(f"🎊 TƏBRİKLƏR! {st.session_state.say} cəhddə tapdın!")
        qelebe_effekti() # Həm Konfetti, həm SƏS!
        st.balloons()
        
        if st.button("Yenidən Oyna"):
            del st.session_state.gizli
            st.session_state.say = 0
            st.rerun()

# Sidebar
st.sidebar.markdown(f"**Oyunçu:** {st.session_state.istifadeci_adi}")
st.sidebar.markdown(f"**Karakter:** {st.session_state.karakter}")
if st.sidebar.button("Karakteri Dəyiş"):
    st.session_state.istifadeci_adi = ""
    st.rerun()
