import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Huseyn Elpasayev Games", page_icon="🚀", layout="wide")

# 1. ƏTRAFDAN UÇAN ŞARLAR/KONFETTİ (JavaScript)
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            var duration = 3 * 1000;
            var end = Date.now() + duration;
            (function frame() {
              confetti({ particleCount: 5, angle: 60, spread: 55, origin: { x: 0 }, colors: ['#bb0000', '#ffffff'] });
              confetti({ particleCount: 5, angle: 120, spread: 55, origin: { x: 1 }, colors: ['#bb0000', '#ffffff'] });
              if (Date.now() < end) { requestAnimationFrame(frame); }
            }());
            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
        </script>
        """, height=0,
    )

# 2. SESSION STATE (Yaddaşın Sıfırdan Qurulması)
# Xətaların qarşısını almaq üçün bütün dəyişənləri əvvəlcədən təyin edirik
if 'balonlar' not in st.session_state: st.session_state.balonlar = 0
if 'istifadeci_adi' not in st.session_state: st.session_state.istifadeci_adi = ""
if 'dostlar' not in st.session_state: st.session_state.dostlar = []
if 'mesajlar' not in st.session_state: st.session_state.mesajlar = {}
if 'oyun_modu' not in st.session_state: st.session_state.oyun_modu = "Reqem"
if 'qazandi' not in st.session_state: st.session_state.qazandi = False

# --- SİDEBAR (Yapımcı İmzası) ---
st.sidebar.markdown("### 🛠️ Redaktor & Yapımcı:")
st.sidebar.info("✨ **Huseyn Elpasayev**")
st.sidebar.divider()

if st.session_state.istifadeci_adi:
    st.sidebar.title(f"👤 {st.session_state.istifadeci_adi}")
    st.sidebar.header(f"🎈 Balon Sayı: {st.session_state.balonlar}")
    if st.sidebar.button("Hesabdan Çıx"):
        st.session_state.clear()
        st.rerun()

# --- GİRİŞ EKRANI ---
if not st.session_state.istifadeci_adi:
    st.title("🚀 Huseyn Elpasayev Games Dünyasına Xoş Gəldin!")
    ad = st.text_input("Adını yaz və oyuna daxil ol:")
    if st.button("Dünyaya Giriş Et"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- ƏSAS MENYU (TABLAR) ---
tab1, tab2, tab3 = st.tabs(["🎮 Oyunlar", "🤝 Dostluq & Chat", "🛒 Mağaza"])

# --- TAB 1: OYUNLAR ---
with tab1:
    c1, c2 = st.columns([10, 1])
    c1.subheader(f"Hazırkı Oyun: {st.session_state.oyun_modu}")
    
    # Mavi Pult - Gizli Düymə
    if c2.button("🎮", help="Gizli Qazanma!"):
        st.session_state.qazandi = True
        st.toast("🤫 Hiylə işlədildi!")

    if st.session_state.oyun_modu == "Reqem":
        if 'gizli' not in st.session_state:
            st.session_state.gizli = random.randint(1, 100)
        
        if not st.session_state.qazandi:
            texmin = st.number_input("1-100 arası rəqəm tap:", 1, 100, key="reqem_input")
            if st.button("Yoxla"):
                if texmin == st.session_state.gizli:
                    st.session_state.qazandi = True
                    st.rerun()
                elif texmin < st.session_state.gizli: st.warning("⬆️ Daha BÖYÜK!")
                else: st.warning("⬇️ Daha KİÇİK!")
    
    elif st.session_state.oyun_modu == "Silah":
        st.write("🎯 **Hədəfi vur və balon qazan!**")
        target = random.choice(["🎯", "👾", "🦖"])
        st.title(f"Hədəf: {target}")
        if st.button("🔥 ATEŞ ET!"):
            st.session_state.qazandi = True
            st.rerun()

    # QALİBİYYƏT ANI
    if st.session_state.qazandi:
        q_balon = random.randint(10, 30)
        st.session_state.balonlar += q_balon
        st.success(f"🎊 Möhtəşəm! +{q_balon} Balon qazandın!")
        qelebe_effekti()
        
        if st.button("Növbəti Oyun (Random)"):
            st.session_state.oyun_modu = random.choice(["Reqem", "Silah"])
            if 'gizli' in st.session_state: del st.session_state.gizli
            st.session_state.qazandi = False
            st.rerun()

# --- TAB 2: DOSTLUQ & CHAT ---
with tab2:
    st.subheader("👥 Dostluq Paneli")
    d_ad = st.text_input("Dostluq atmaq üçün ad yaz:", key="dost_input")
    if st.button("İstək Göndər"):
        st.toast(f"✅ {d_ad} istifadəçisinə istək göndərildi!")

    st.divider()
    if not st.session_state.dostlar:
        if st.button("Huseyn Elpasayev ilə dost ol (Sınaq)"):
            st.session_state.dostlar.append("Huseyn Elpasayev")
            st.rerun()
    else:
        secilen = st.selectbox("Dost seç:", st.session_state.dostlar)
        msg = st.text_input(f"{secilen} üçün mesaj yaz:", key="msg_input")
        if st.button("Göndər"):
            if msg:
                if secilen not in st.session_state.mesajlar:
                    st.session_state.mesajlar[secilen] = []
                st.session_state.mesajlar[secilen].append(f"Mən: {msg}")
                st.rerun()
        
        # Mesajları göstər (Xəta yoxlanışı ilə)
        if secilen in st.session_state.mesajlar:
            for m in st.session_state.mesajlar[secilen]:
                st.write(m)

# --- TAB 3: MAĞAZA ---
with tab3:
    st.subheader("🛒 Karakter Mağazası")
    st.info("Çox yaxında yeni güclü karakterlər bura əlavə olunacaq!")
    st.metric("Sənin Balonun", f"🎈 {st.session_state.balonlar}")
