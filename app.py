import streamlit as st
import random
import time

# Sayt ayarları
st.set_page_config(page_title="Şirkət Oyunu", page_icon="🎉")

# İstifadəçi adını Google hesabından götürməyə çalışırıq
# Əgər daxil olmayıbsa, sadəcə "Dostum" deyə müraciət edirik
if st.user.email:
    user_name = st.user.email.split('@')[0].capitalize()
else:
    user_name = "Dostum"

st.title(f"🚀 Xoş gəldin, {user_name}!")

if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)
    st.session_state.say = 0

st.write("---")
texmin = st.number_input("1-100 arası rəqəm yaz:", min_value=1, max_value=100, step=1)

if st.button("🔥 Şansını Yoxla"):
    st.session_state.say += 1
    
    if texmin < st.session_state.gizli:
        st.info("⬆️ Daha BÖYÜK!")
    elif texmin > st.session_state.gizli:
        st.info("⬇️ Daha KİÇİK!")
    else:
        # QALİBİYYƏT ANI
        st.balloons() # Şarlar
        st.snow() # Qar/Konfetti effekti üçün
        st.success(f"🏆 Təbriklər, {user_name}! {st.session_state.gizli} rəqəmini {st.session_state.say} cəhddə tapdın!")
        
        # Yenidən başlama düyməsi
        if st.button("🔄 Yenidən Oyna"):
            del st.session_state.gizli
            st.rerun()

st.sidebar.write(f"👤 Hazırda aktiv: **{user_name}**")
