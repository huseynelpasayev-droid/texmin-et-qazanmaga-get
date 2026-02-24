import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Karakterli Rəqəm Oyunu", page_icon="👤")

# Konfetti funksiyası
def konfetti_partlat(say=150):
    st.components.v1.html(
        f"""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            confetti({{ particleCount: {say}, spread: 70, origin: {{ y: 0.6 }} }});
        </script>
        """, height=0,
    )

st.title("🎭 Karakterini Seç və Tap!")

# Karakter seçimi
karakter = st.selectbox("Hansı karakterlə oynamaq istəyirsən?", 
                        ["Standart Oyunçu", "Şanslı Hüseyn", "Dəqiqlik Ustası"])

if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)
    st.session_state.say = 0

st.divider()

# Karakter özəllikləri haqqında məlumat
if karakter == "Şanslı Hüseyn":
    st.caption("✨ Özəllik: Bu karakter çox şanslıdır! Düzgün cavaba yaxınlaşanda rəng dəyişir.")
elif karakter == "Dəqiqlik Ustası":
    st.caption("🎯 Özəllik: Səhv edəndə daha dəqiq istiqamət alır.")

texmin = st.number_input("1-100 arası rəqəm seç:", min_value=1, max_value=100, step=1)

if st.button("🔥 Təxmin et"):
    st.session_state.say += 1
    fərq = abs(texmin - st.session_state.gizli)
    
    if texmin < st.session_state.gizli:
        mesaj = "⬆️ Daha BÖYÜK!"
        # Şanslı Hüseyn özəlliyi
        if karakter == "Şanslı Hüseyn" and fərq < 10:
            mesaj += " (Çox yaxınsan! 🔥)"
        st.warning(mesaj)
        
    elif texmin > st.session_state.gizli:
        mesaj = "⬇️ Daha KİÇİK!"
        if karakter == "Şanslı Hüseyn" and fərq < 10:
            mesaj += " (Çox yaxınsan! 🔥)"
        st.warning(mesaj)
        
    else:
        # QALİBİYYƏT!
        st.success(f"🎊 Möhtəşəm! {st.session_state.gizli} rəqəmini {st.session_state.say} cəhddə tapdın!")
        
        # Karakterə görə mükafat
        if karakter == "Dəqiqlik Ustası":
            konfetti_partlat(300) # Daha çox konfetti
        else:
            konfetti_partlat(150)
            
        st.balloons()
        
        if st.button("🔄 Yenidən Oyna"):
            del st.session_state.gizli
            st.rerun()

st.sidebar.markdown(f"Seçilən Karakter: **{karakter}**")
