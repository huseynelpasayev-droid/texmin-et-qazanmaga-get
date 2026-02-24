import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Rəqəmi Tap: Xüsusi Ad", page_icon="🏷️")

# 1. Rəngli Konfetti Funksiyası
def konfetti_partlat():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            var duration = 3 * 1000;
            var animationEnd = Date.now() + duration;
            var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };
            function randomInRange(min, max) { return Math.random() * (max - min) + min; }
            var interval = setInterval(function() {
              var timeLeft = animationEnd - Date.now();
              if (timeLeft <= 0) { return clearInterval(interval); }
              var particleCount = 50 * (timeLeft / duration);
              confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
              confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
            }, 250);
        </script>
        """, height=0,
    )

# 2. Adın idarə olunması
# Əgər yaddaşda ad yoxdursa, Google hesabını yoxla, o da yoxdursa boş saxla
if 'istifadeci_adi' not in st.session_state:
    try:
        if st.user_info and st.user_info.get("email"):
            st.session_state.istifadeci_adi = st.user_info["email"].split('@')[0].capitalize()
        else:
            st.session_state.istifadeci_adi = ""
    except:
        st.session_state.istifadeci_adi = ""

# Sidebar-da adı dəyişdirmək bölməsi
st.sidebar.title("⚙️ Ayarlar")
yeni_ad = st.sidebar.text_input("Oyundakı adını dəyiş:", value=st.session_state.istifadeci_adi)

if yeni_ad:
    st.session_state.istifadeci_adi = yeni_ad

# Əgər ad hələ də boşdursa, istifadəçidən adını soruşan bir ekran göstər
if not st.session_state.istifadeci_adi:
    st.title("👋 Xoş gəlmisən!")
    ad_girisi = st.text_input("Zəhmət olmasa, oyunda görünəcək adını daxil et:")
    if st.button("Oyuna Başla"):
        if ad_girisi:
            st.session_state.istifadeci_adi = ad_girisi
            st.rerun()
        else:
            st.error("Ad boş ola bilməz!")
    st.stop() # Ad daxil edilənə qədər oyunun qalanını göstərmə

# OYUNUN ƏSAS HİSSƏSİ
st.title(f"🎮 Uğurlar, {st.session_state.istifadeci_adi}!")
st.write("---")

if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)
    st.session_state.say = 0

texmin = st.number_input("1-100 arası bir rəqəm yaz:", min_value=1, max_value=100, step=1)

if st.button("🔥 Yoxla"):
    st.session_state.say += 1
    
    if texmin < st.session_state.gizli:
        st.info("⬆️ Daha BÖYÜK!")
    elif texmin > st.session_state.gizli:
        st.info("⬇️ Daha KİÇİK!")
    else:
        st.success(f"🎊 Möhtəşəm! {st.session_state.istifadeci_adi}, {st.session_state.gizli} rəqəmini {st.session_state.say} cəhddə tapdın!")
        konfetti_partlat()
        st.balloons()
        
        if st.button("🔄 Yenidən Oyna"):
            del st.session_state.gizli
            st.rerun()

st.sidebar.markdown(f"👤 Hazırkı Oyunçu: **{st.session_state.istifadeci_adi}**")
