import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Rəqəmi Tap", page_icon="🎯")

# Konfetti effekti üçün balaca bir hiylə (HTML/JS)
def konfetti_partlat():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 150,
                spread: 70,
                origin: { y: 0.6 }
            });
        </script>
        """,
        height=0,
    )

# İstifadəçi adını yoxlayırıq (Xətasız versiya)
user_display = "Dostum"
try:
    # Streamlit Cloud-da giriş edilibsə adı götür
    if hasattr(st, "user_info") and st.user_info.get("email"):
        user_display = st.user_info["email"].split('@')[0].capitalize()
except:
    pass

st.title(f"🚀 Xoş gəldin, {user_display}!")
st.subheader("Şirkətimizin rəsmi oyununa başla!")

# Oyun məntiqi
if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)
    st.session_state.say = 0

st.divider()

texmin = st.number_input("1-100 arası bir rəqəm seç:", min_value=1, max_value=100, step=1)

if st.button("🔥 Təxmin et"):
    st.session_state.say += 1
    
    if texmin < st.session_state.gizli:
        st.warning("⬆️ Daha BÖYÜK bir rəqəm yaz!")
    elif texmin > st.session_state.gizli:
        st.warning("⬇️ Daha KİÇİK bir rəqəm yaz!")
    else:
        # QALİBİYYƏT!
        st.success(f"🎊 Möhtəşəm! {user_display}, {st.session_state.gizli} rəqəmini {st.session_state.say} cəhddə tapdın!")
        konfetti_partlat() # Rəngli konfetti yağışı
        st.balloons()    # Şarlar
        
        if st.button("🔄 Yenidən Oyna"):
            del st.session_state.gizli
            st.rerun()

st.sidebar.markdown(f"👤 Oyunçu: **{user_display}**")
st.sidebar.info("Məqsəd 1-100 arası rəqəmi tapmaqdır. Uğurlar!")
