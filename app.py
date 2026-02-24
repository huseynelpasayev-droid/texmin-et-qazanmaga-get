import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Rəqəmi Tap: Səsli Versiya", page_icon="🎭")

# 1. Konfetti və Səs Funksiyası (JavaScript)
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 200,
                spread: 90,
                origin: { y: 0.6 }
            });
            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
        </script>
        """,
        height=0,
    )

# 2. Karakterlərin siyahısı
karakterler = {
    "Standart": "Sadiqcə oynayır.",
    "Şanslı Hüseyn": "✨ Özəllik: Rəqəmə çox yaxınlaşanda xəbər verir!",
    "İnadkar İbrahim": "⏳ Özəllik: Hər səhvdə motivasiya verir.",
    "Dəqiqlik Ustası": "🎯 Özəllik: Rəqəmin tək və ya cüt olduğunu bilir.",
    "Gözüaçıq Günel": "👁️ Özəllik: Rəqəm aralığını daraldır."
}

# 3. Session State Yoxlaması (Xətanın qarşısını alan hissə)
if 'istifadeci_adi' not in st.session_state:
    st.session_state.istifadeci_adi = ""
if 'karakter' not in st.session_state:
    st.session_state.karakter = ""

# 4. Giriş Ekranı
if not st.session_state.istifadeci_adi or not st.session_state.karakter:
    st.title("🎭 Karakterini Seç və Başla!")
    ad_input = st.text_input("Adını yaz:")
    karakter_input = st.selectbox("Bir karakter seç:", list(karakterler.keys()))
    
    if st.button("Oyuna Daxil Ol"):
        if ad_input:
            st.session_state.istifadeci_adi = ad_input
            st.session_state.karakter = karakter_input
            st.rerun()
        else:
            st.error("Zəhmət olmasa adını yaz!")
    st.stop()

# 5. Əsas Oyun Hissəsi
st.title(f"🎮 {st.session_state.karakter} {st.session_state.istifadeci_adi}")
st.write(f"_{karakterler[st.session_state.karakter]}_")

if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)
    st.session_state.say = 0

# Karakter özəlliyi: Dəqiqlik Ustası
if st.session_state.karakter == "Dəqiqlik Ustası" and st.session_state.say == 0:
    tip = "CÜT" if st.session_state.gizli % 2 == 0 else "TƏK"
    st.info(f"🎯 Usta İpucu: Bu rəqəm **{tip}** rəqəmdir.")

texmin = st.number_input("Təxminin (1-100):", 1, 100)

if st.button("Yoxla"):
    st.session_state.say += 1
    ferq = abs(texmin - st.session_state.gizli)
    
    if texmin < st.session_state.gizli:
        msg = "⬆️ Daha BÖYÜK!"
        if st.session_state.karakter == "Şanslı Hüseyn" and ferq <= 10:
            msg += " (Çox istidir! 🔥)"
        st.warning(msg)
        
    elif texmin > st.session_state.gizli:
        msg = "⬇️ Daha KİÇİK!"
        if st.session_state.karakter == "Şanslı Hüseyn" and ferq <= 10:
            msg += " (Çox istidir! 🔥)"
        st.warning(msg)
        
    else:
        st.success(f"🎊 TƏBRİKLƏR! {st.session_state.say} cəhddə tapdın!")
        qelebe_effekti()
        st.balloons()
        if st.button("Yenidən Oyna"):
            del st.session_state.gizli
            st.session_state.say = 0
            st.rerun()

st.sidebar.button("Karakteri Sıfırla", on_click=lambda: st.session_state.clear())
