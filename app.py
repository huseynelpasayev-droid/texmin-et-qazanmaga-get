import streamlit as st
import random

# 1. GOOGLE AXTARIŞI VƏ PLAY STORE ÜÇÜN BAŞLIQ
st.set_page_config(
    page_title="Huseyn Elpasayevin Texmin Et Oyunu - Rəsmi", 
    page_icon="🚀", 
    layout="wide"
)

# 2. ƏTRAFDAN ŞARLAR VƏ KONFETTİ SƏSİ (JavaScript)
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

# 3. KARAKTER MƏLUMATLARI (Mağaza və Kilid sistemi)
karakter_bazasi = {
    "Standart": {"desc": "Sadiqcə oynayır.", "price": 0},
    "Şanslı Hüseyn": {"desc": "✨ Yaxınlaşanda 'İstidir' deyir!", "price": 0},
    "İnadkar İbrahim": {"desc": "⏳ Hər səhvdə motivasiya verir.", "price": 20},
    "Dəqiqlik Ustası": {"desc": "🎯 Tək/Cüt olduğunu bilir.", "price": 50},
    "Kral Qalib": {"desc": "👑 Hər qələbədə 2 qat balon verir!", "price": 100}
}

# 4. YADDAŞ (Session State)
if 'balonlar' not in st.session_state: st.session_state.balonlar = 0
if 'istifadeci_adi' not in st.session_state: st.session_state.istifadeci_adi = ""
if 'aciq_karakterler' not in st.session_state: st.session_state.aciq_karakterler = ["Standart", "Şanslı Hüseyn"]
if 'karakter' not in st.session_state: st.session_state.karakter = "Standart"
if 'qazandi' not in st.session_state: st.session_state.qazandi = False

# --- GİRİŞ EKRANI (AD YARATMAQ) ---
if not st.session_state.istifadeci_adi:
    st.title("🌟 Huseyn Elpasayevin Oyun Dünyası")
    ad = st.text_input("Adını yaz və oyuna daxil ol:")
    if st.button("Dünyaya Giriş Et 🚀"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.info("Redaktor & Yapımcı: Huseyn Elpasayev")
    st.stop()

# --- SİDEBAR (Yapımcı və Balon Sayğacı) ---
st.sidebar.markdown("# 🛠️ YAPIMCI")
st.sidebar.info(f"✨ **Huseyn Elpasayev**")
st.sidebar.metric("🎈 Balon Sayı", st.session_state.balonlar)
st.sidebar.divider()

# --- ƏSAS MENYU (TABLAR) ---
tab1, tab2, tab3, tab4 = st.tabs(["🎮 Oyun", "🛒 Mağaza", "💬 Chat", "⭐ Reytinq"])

# --- TAB 1: OYUN (Rəqəmi Tap) ---
with tab1:
    c1, c2 = st.columns([10, 1])
    c1.title(f"{st.session_state.karakter} Rejimi")
    if c2.button("🎮"): # Mavi pult gizli düymə
        st.session_state.qazandi = True

    if 'gizli' not in st.session_state: st.session_state.gizli = random.randint(1, 100)

    if not st.session_state.qazandi:
        texmin = st.number_input("1-100 arası rəqəmi tap:", 1, 100)
        if st.button("Yoxla"):
            if texmin == st.session_state.gizli:
                st.session_state.qazandi = True
                st.rerun()
            elif texmin < st.session_state.gizli: st.warning("⬆️ DAHA BÖYÜK!")
            else: st.warning("⬇️ DAHA KİÇİK!")
    else:
        st.success("🎊 TƏBRİKLƏR! Qalib gəldin!")
        q_balon = random.randint(10, 20)
        if st.session_state.karakter == "Kral Qalib": q_balon *= 2
        st.session_state.balonlar += q_balon
        qelebe_effekti()
        if st.button("Növbəti Raund"):
            del st.session_state.gizli
            st.session_state.qazandi = False
            st.rerun()

# --- TAB 2: MAĞAZA (Karakter Kilidləri) ---
with tab2:
    st.subheader("🛒 Karakter Mağazası")
    for k, v in karakter_bazasi.items():
        col1, col2 = st.columns([3, 1])
        col1.write(f"**{k}** - {v['desc']}")
        if k in st.session_state.aciq_karakterler:
            if col2.button(f"Seç", key=f"sel_{k}"):
                st.session_state.karakter = k
                st.toast(f"{k} seçildi!")
        else:
            if col2.button(f"💰 {v['price']}", key=f"buy_{k}"):
                if st.session_state.balonlar >= v['price']:
                    st.session_state.balonlar -= v['price']
                    st.session_state.aciq_karakterler.append(k)
                    st.rerun()
                else: st.error("Balonun çatmır!")

# --- TAB 3: CHAT ---
with tab3:
    st.subheader("💬 Şəxsi Chat")
    st.text_input("Mesajını yaz:")
    if st.button("Göndər"): st.toast("Mesaj göndərildi!")

# --- TAB 4: REYTİNQ ---
with tab4:
    st.subheader("⭐ Google Play Reytinqi")
    st.write("Reytinq: **4.9 / 5.0**")
    st.write("- 'Möhtəşəm oyundur!' - Ali")
    st.write("- 'Huseyn Elpasayev əsl ustadır.' - Vəli")
