import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Super Rəqəm Oyunu", page_icon="🏆", layout="wide")

# 1. Rəngli Konfetti Funksiyası (JavaScript)
def konfetti_partlat():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 150,
                spread: 70,
                origin: { y: 0.6 },
                colors: ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff']
            });
        </script>
        """, height=0,
    )

# 2. Ad və Karakter Sistemi
if 'istifadeci_adi' not in st.session_state:
    st.session_state.istifadeci_adi = ""
if 'secilen_karakter' not in st.session_state:
    st.session_state.secilen_karakter = "Standart"
if 'mesajlar' not in st.session_state:
    st.session_state.mesajlar = []

# Giriş Ekranı
if not st.session_state.istifadeci_adi:
    st.title("👋 Xoş Gəldin! Oyuna başlamaq üçün:")
    ad = st.text_input("Adını yaz:")
    karakter = st.selectbox("Karakterini seç:", ["Standart", "Şanslı Hüseyn", "Dəqiqlik Ustası"])
    if st.button("Dünyaya Giriş Et"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.session_state.secilen_karakter = karakter
            st.rerun()
    st.stop()

# Əsas Menyu
tab1, tab2 = st.tabs(["🎯 Oyun və Karakter", "🌐 Dünya Çatı"])

with tab1:
    st.title(f"🚀 {st.session_state.secilen_karakter} {st.session_state.istifadeci_adi} iş başında!")
    
    if 'gizli' not in st.session_state:
        st.session_state.gizli = random.randint(1, 100)
        st.session_state.say = 0

    # Karakter özəlliyi məlumatı
    if st.session_state.secilen_karakter == "Şanslı Hüseyn":
        st.info("✨ Özəllik: Rəqəmə çox yaxınlaşanda sənə xüsusi xəbərdarlıq gələcək!")
    
    texmin = st.number_input("1-100 arası rəqəm yaz:", 1, 100, key="main_game")

    if st.button("🔥 Təxmin Et"):
        st.session_state.say += 1
        fərq = abs(texmin - st.session_state.gizli)
        
        if texmin < st.session_state.gizli:
            msg = "⬆️ DAHA BÖYÜK!"
            if st.session_state.secilen_karakter == "Şanslı Hüseyn" and fərq <= 10:
                msg += " (Çox yaxınsan! 🔥)"
            st.warning(msg)
            
        elif texmin > st.session_state.gizli:
            msg = "⬇️ DAHA KİÇİK!"
            if st.session_state.secilen_karakter == "Şanslı Hüseyn" and fərq <= 10:
                msg += " (Çox yaxınsan! 🔥)"
            st.warning(msg)
            
        else:
            st.success(f"🎊 HALALDIR! {st.session_state.gizli} rəqəmini {st.session_state.say} cəhddə tapdın!")
            konfetti_partlat()
            st.balloons()
            if st.button("Yenidən Başla"):
                del st.session_state.gizli
                st.session_state.say = 0
                st.rerun()

with tab2:
    st.subheader("🌐 Qlobal Mesajlaşma")
    msg_input = st.text_input("Hamıya bir söz de:")
    if st.button("Göndər"):
        if msg_input:
            formatted_msg = f"**[{st.session_state.secilen_karakter}] {st.session_state.istifadeci_adi}**: {msg_input}"
            st.session_state.mesajlar.insert(0, formatted_msg)
            st.rerun()
    
    st.divider()
    for m in st.session_state.mesajlar:
        st.write(m)

# Sidebar Ayarları
st.sidebar.title("👤 Profilim")
st.sidebar.write(f"Ad: {st.session_state.istifadeci_adi}")
st.sidebar.write(f"Karakter: {st.session_state.secilen_karakter}")
if st.sidebar.button("Çıxış Et / Sıfırla"):
    st.session_state.istifadeci_adi = ""
    st.rerun()
