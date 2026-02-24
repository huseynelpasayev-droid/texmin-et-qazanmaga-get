import streamlit as st
import random

# 1. GOOGLE AXTARIŞI VƏ PLAY STORE ÜÇÜN BAŞLIQ
st.set_page_config(
    page_title="Huseyn Elpasayevin Texmin Et Oyunu - Rəsmi", 
    page_icon="🚀", 
    layout="wide"
)

# 2. ƏTRAFDAN ŞARLAR VƏ SƏS (JavaScript)
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            var end = Date.now() + (3 * 1000);
            (function frame() {
              confetti({ particleCount: 10, angle: 60, spread: 55, origin: { x: 0 }, colors: ['#00ff00', '#ff0000', '#0000ff'] });
              confetti({ particleCount: 10, angle: 120, spread: 55, origin: { x: 1 }, colors: ['#ffff00', '#ff00ff', '#00ffff'] });
              if (Date.now() < end) { requestAnimationFrame(frame); }
            }());
            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
        </script>
        """, height=0,
    )

# 3. YADDAŞ SİSTEMİ (Session State)
if 'balonlar' not in st.session_state: st.session_state.balonlar = 0
if 'istifadeci_adi' not in st.session_state: st.session_state.istifadeci_adi = ""
if 'oyun_modu' not in st.session_state: st.session_state.oyun_modu = "Reqem"
if 'qazandi' not in st.session_state: st.session_state.qazandi = False
if 'dostlar' not in st.session_state: st.session_state.dostlar = ["Huseyn Elpasayev"]

# --- SİDEBAR (Yapımcı Paneli) ---
st.sidebar.markdown("# 🛠️ YAPIMCI")
st.sidebar.info("### ✨ **Huseyn Elpasayev**")
st.sidebar.write("Bu oyun rəsmi olaraq Huseyn Elpasayev tərəfindən idarə olunur.")
st.sidebar.divider()
if st.session_state.istifadeci_adi:
    st.sidebar.metric("🎈 Mövcud Balonların", st.session_state.balonlar)
    if st.sidebar.button("Hesabı Sıfırla"):
        st.session_state.clear()
        st.rerun()

# --- GİRİŞ EKRANI ---
if not st.session_state.istifadeci_adi:
    st.title("🌟 Huseyn Elpasayevin Texmin Et Dünyası")
    st.markdown("#### 📥 Google Play: 4.9⭐ | 1M+ Yükləmə (Simulyasiya)")
    ad = st.text_input("Oyunçu Adını Daxil Et:")
    if st.button("Dünyaya Giriş Et"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- ƏSAS MENYU (TABLAR) ---
tab1, tab2, tab3 = st.tabs(["🎮 Oyunlar", "👥 Sosial & Chat", "🏆 Reytinq"])

# --- TAB 1: OYUNLAR ---
with tab1:
    c1, c2 = st.columns([10, 1])
    c1.title(f"Hazırkı Oyun: {st.session_state.oyun_modu}")
    
    # Mavi Pult (Gizli Cheat)
    if c2.button("🎮", help="Huseyn Mode: ON"):
        st.session_state.qazandi = True
        st.toast("🤫 Yapımcı hiyləsi aktivdir!")

    if st.session_state.oyun_modu == "Reqem":
        if 'gizli' not in st.session_state: st.session_state.gizli = random.randint(1, 100)
        
        if not st.session_state.qazandi:
            texmin = st.number_input("1-100 arası rəqəmi tap:", 1, 100)
            if st.button("Yoxla"):
                if texmin == st.session_state.gizli:
                    st.session_state.qazandi = True
                    st.rerun()
                elif texmin < st.session_state.gizli: st.warning("⬆️ Daha BÖYÜK!")
                else: st.warning("⬇️ Daha KİÇİK!")
    
    elif st.session_state.oyun_modu == "Silah":
        st.write("🎯 **Hədəfi vur və balon qazan!**")
        target = random.choice(["👾", "🦖", "🛸", "🤖"])
        st.title(f"Hədəf: {target}")
        if st.button("🔥 ATEŞ ET!"):
            st.session_state.qazandi = True
            st.rerun()

    # QALİBİYYƏT
    if st.session_state.qazandi:
        st.success(f"🎊 TƏBRİKLƏR! {st.session_state.istifadeci_adi}, sən qazandın!")
        q_balon = random.randint(15, 35)
        st.session_state.balonlar += q_balon
        qelebe_effekti()
        
        if st.button("Növbəti Oyun (Random)"):
            st.session_state.oyun_modu = random.choice(["Reqem", "Silah"])
            if 'gizli' in st.session_state: del st.session_state.gizli
            st.session_state.qazandi = False
            st.rerun()

# --- TAB 2: SOSİAL ---
with tab2:
    st.subheader("💬 Şəxsi Chat")
    dost = st.selectbox("Dost siyahın:", st.session_state.dostlar)
    mesaj = st.text_input(f"{dost} üçün mesaj yaz:")
    if st.button("Göndər"):
        st.toast("✅ Mesaj göndərildi!")
    st.info("Dostlarınla söhbət etmək üçün onları oyuna dəvət et!")

# --- TAB 3: REYTİNQ (Google Play Stilində) ---
with tab3:
    st.subheader("⭐ Rəsmi Rəylər")
    st.write("---")
    st.write("**⭐⭐⭐⭐⭐ - Ali M.**")
    st.write("> 'Huseyn Elpasayevin hazırladığı ən yaxşı oyundur, çox əyləncəlidir!'")
    st.write("**⭐⭐⭐⭐⭐ - Ayxan.**")
    st.write("> 'Şarların hər tərəfdən çıxması möhtəşəmdir!'")
    st.divider()
    st.write("Oyun Reytinqi: **4.9 / 5.0** 🚀")

# ALT HİSSƏ
st.write("---")
st.caption("© 2026 Huseyn Elpasayev Games - Bütün hüquqlar qorunur.")
