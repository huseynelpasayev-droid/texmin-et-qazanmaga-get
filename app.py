import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Sosial Rəqəm Oyunu", page_icon="👥")

# 1. Yaddaş (Database simulyasiyası)
if 'istifadeci_adi' not in st.session_state:
    st.session_state.istifadeci_adi = ""
if 'dostlar' not in st.session_state:
    st.session_state.dostlar = []
if 'istekler' not in st.session_state:
    st.session_state.istekler = []
if 'ozel_mesajlar' not in st.session_state:
    st.session_state.ozel_mesajlar = {} # { "dost_adi": ["mesaj1", "mesaj2"] }

# 2. Giriş Ekranı
if not st.session_state.istifadeci_adi:
    st.title("🚀 Xoş Gəldin!")
    ad = st.text_input("Oyunda və Chatda istifadə edəcəyin adını yaz:")
    if st.button("Başla"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# 3. Əsas Menyu (Tablar)
tab1, tab2, tab3 = st.tabs(["🎮 Oyun", "🤝 Dostluq", "💬 Şəxsi Chat"])

# --- OYUN TABI ---
with tab1:
    st.title(f"Uğurlar, {st.session_state.istifadeci_adi}!")
    if 'gizli' not in st.session_state:
        st.session_state.gizli = random.randint(1, 100)
    
    texmin = st.number_input("Rəqəmi tap:", 1, 100)
    if st.button("Yoxla"):
        if texmin == st.session_state.gizli:
            st.success("Təbriklər! Tapdın!")
            st.balloons()
            del st.session_state.gizli
        else:
            st.info("Yenidən yoxla!")

# --- DOSTLUQ TABI ---
with tab2:
    st.subheader("👥 Yeni Dostlar Tap")
    yeni_dost = st.text_input("Dostluq atmaq istədiyin adamın adını yaz:")
    if st.button("İstək Göndər"):
        if yeni_dost and yeni_dost != st.session_state.istifadeci_adi:
            st.session_state.istekler.append(yeni_dost)
            st.toast(f"{yeni_dost} adına istək göndərildi!")
    
    st.divider()
    st.subheader("📥 Gələn İstəklər")
    if not st.session_state.istekler:
        st.write("Hələ ki, istək yoxdur.")
    else:
        for idx, ad in enumerate(st.session_state.istekler):
            col1, col2 = st.columns([2, 1])
            col1.write(f"**{ad}** sənə dostluq göndərdi.")
            if col2.button("Qəbul et", key=f"acc_{idx}"):
                st.session_state.dostlar.append(ad)
                st.session_state.istekler.remove(ad)
                st.rerun()

# --- ŞƏXSİ CHAT TABI ---
with tab3:
    st.subheader("💬 Şəxsi Mesajlar")
    if not st.session_state.dostlar:
        st.info("Mesajlaşmaq üçün əvvəlcə dost əlavə etməlisən.")
    else:
        secilen_dost = st.selectbox("Kiminlə danışmaq istəyirsən?", st.session_state.dostlar)
        
        # Mesaj yazma yeri
        mesaj = st.text_input(f"{secilen_dost} üçün mesajın:")
        if st.button("Göndər"):
            if mesaj:
                if secilen_dost not in st.session_state.ozel_mesajlar:
                    st.session_state.ozel_mesajlar[secilen_dost] = []
                st.session_state.ozel_mesajlar[secilen_dost].append(f"Mən: {mesaj}")
                st.toast("Göndərildi!")
        
        # Mesajları göstər
        st.divider()
        if secilen_dost in st.session_state.ozel_mesajlar:
            for m in st.session_state.ozel_mesajlar[secilen_dost]:
                st.write(m)
