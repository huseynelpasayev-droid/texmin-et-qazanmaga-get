import streamlit as st
import time
import random

# 1. SƏHİFƏ VƏ ÜMUMİ DİZAYN
st.set_page_config(page_title="Huseyn's 3D Cat World", page_icon="🐾", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    .game-screen {
        background-color: rgba(0,0,0,0.5);
        border: 3px solid #00d2ff;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        min-height: 400px;
    }
    .stat-card {
        background: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. YADDAŞ SİSTEMİ (SESSION STATE)
if 'acliq' not in st.session_state: st.session_state.acliq = 100
if 'susuzluq' not in st.session_state: st.session_state.susuzluq = 100
if 'enerji' not in st.session_state: st.session_state.enerji = 100
if 'lvl' not in st.session_state: st.session_state.lvl = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'reng' not in st.session_state: st.session_state.reng = "Boz"
if 'paltar' not in st.session_state: st.session_state.paltar = "Yoxdur"
if 'caynaq_gucu' not in st.session_state: st.session_state.caynaq_gucu = 10  # Metrlə dırmaşma limiti

# 3. SİDEBAR - PROFİL VƏ STATİSTİKA
st.sidebar.title("🐈 Pişik Paneli")
st.sidebar.write(f"**Sahib:** Huseyn Elpasayev")
st.sidebar.divider()

st.sidebar.subheader("📊 Ehtiyaclar")
st.sidebar.progress(st.session_state.acliq / 100, text=f"Acmaq: {int(st.session_state.acliq)}%")
st.sidebar.progress(st.session_state.susuzluq / 100, text=f"Susamaq: {int(st.session_state.susuzluq)}%")
st.sidebar.progress(st.session_state.enerji / 100, text=f"Yuxu: {int(st.session_state.enerji)}%")

st.sidebar.divider()
st.sidebar.write(f"🎨 Rəng: **{st.session_state.reng}**")
st.sidebar.write(f"👕 Paltar: **{st.session_state.paltar}**")
st.sidebar.write(f"🧗 Dırmaşma Limiti: **{st.session_state.caynaq_gucu} metr**")

# 4. ƏSAS OYUN MƏNTİQİ
st.title("🏙️ Cat Simulator 3D: Adventure World")

tab1, tab2, tab3, tab4 = st.tabs(["🎮 Macəra", "👗 Geyim & Rəng", "🎯 Görevlər", "📈 Reytinq"])

# --- TAB 1: MACƏRA (ŞƏHƏR, KƏND, SƏHRA) ---
with tab1:
    st.markdown('<div class="game-screen">', unsafe_allow_html=True)
    
    # Pişik vizualı
    emoji = "😺" if st.session_state.enerji > 30 else "😴"
    st.markdown(f"<h1 style='font-size: 100px;'>{emoji}</h1>", unsafe_allow_html=True)
    st.subheader(f"Level: {st.session_state.lvl} | XP: {st.session_state.xp}/100")
    
    mekan = st.selectbox("Məkan seç:", ["🏙️ Şəhər (Binalar)", "🏡 Kənd (Həyət)", "🏜️ Səhra (Parkur)"])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧗 Dırmaş"):
            if st.session_state.enerji > 15:
                yukseklik = random.randint(1, st.session_state.caynaq_gucu)
                st.session_state.xp += 20
                st.session_state.enerji -= 15
                st.success(f"Caynaqlarınla {yukseklik} metr dırmaşdın!")
            else:
                st.error("Çox yorğunsan, yatmalısan!")

    with col2:
        if st.button("🎾 Topla Oyna"):
            st.session_state.xp += 15
            st.session_state.acliq -= 10
            st.info("Topun arxasınca qaçdın və təcrübə qazandın!")

    with col3:
        if st.button("🐟 Yemək & Su"):
            st.session_state.acliq = 100
            st.session_state.susuzluq = 100
            st.toast("Qarnın doydu və susuzluğun keçdi!")

    if st.button("😴 Yat və Enerji Topla"):
        with st.spinner("Pişik yatır..."):
            time.sleep(2)
        st.session_state.enerji = 100
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: GEYİM VƏ RƏNG ---
with tab2:
    st.subheader("👕 Pişik Mağazası")
    c1, c2 = st.columns(2)
    
    with c1:
        st.session_state.reng = st.radio("Pişiyin rəngini seç:", ["Boz", "Ağ", "Narıncı", "Qara"])
        st.success(f"Yeni rəng: {st.session_state.reng}")

    with c2:
        st.session_state.paltar = st.selectbox("Paltar/Aksesuar geyindir:", ["Yoxdur", "Qırmızı Jilet", "Mavi Papaq", "Gün Eynəyi", "Supermen Kostyumu"])
        st.info(f"Hazırkı stil: {st.session_state.paltar}")

# --- TAB 3: GÖREVLƏR ---
with tab3:
    st.subheader("🎯 Günlük Tapşırıqlar")
    st.checkbox("Şəhərdə 50 metr dırmaş (XP: 50)")
    st.checkbox("Səhra parkurunu tamamla (XP: 100)")
    st.checkbox("10 dəfə topla oyna (XP: 30)")
    
    if st.button("🎁 Mükafatları Al"):
        st.balloons()
        st.session_state.xp += 30

# --- TAB 4: REYTİNQ ---
with tab4:
    st.subheader("⭐ Liderlər Cədvəli")
    st.write(f"1. **Huseyn Elpasayev** - Level 999")
    st.write(f"2. **{st.session_state.reng} Pişik** - Level {st.session_state.lvl}")

# 5. SEVİYYƏ ATLAMA MEXANİKASI
if st.session_state.xp >= 100:
    st.session_state.lvl += 1
    st.session_state.xp = 0
    st.session_state.caynaq_gucu += 15 # Səviyyə artdıqca daha yuxarı dırmaşır
    st.snow()
    st.sidebar.success(f"🎉 Təbriklər! Level {st.session_state.lvl} oldun!")
    st.sidebar.info("🚀 Caynaqların gücləndi, artıq daha hündürə çıxa bilərsən!")
