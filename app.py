import streamlit as st
import random

st.set_page_config(page_title="Rəqəmi Tap", page_icon="🎮")
st.title("🎮 Rəqəmi Tap Oyunu")

if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)
    st.session_state.say = 0

texmin = st.number_input("1-100 arası rəqəm yaz:", min_value=1, max_value=100, step=1)

if st.button("Yoxla"):
    st.session_state.say += 1
    if texmin < st.session_state.gizli:
        st.warning("⬆️ Daha BÖYÜK!")
    elif texmin > st.session_state.gizli:
        st.warning("⬇️ Daha KİÇİK!")
    else:
        st.success(f"🎉 Tapdın! Cəhd: {st.session_state.say}")
        if st.button("Yenidən"):
            del st.session_state.gizli
            st.rerun()
