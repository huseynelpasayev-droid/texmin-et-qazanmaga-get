import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Balon Ustası Pro", page_icon="🎈", layout="wide")

# 1. ƏTRAFDAN UÇAN ŞARLAR/KONFETTİ (JavaScript)
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            var duration = 3 * 1000;
            var animationEnd = Date.now() + duration;
            var defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

            function randomInRange(min, max) {
                return Math.random() * (max - min) + min;
            }

            var interval = setInterval(function() {
                var timeLeft = animationEnd - Date.now();
                if (timeLeft <= 0) { return clearInterval(interval); }
                var particleCount = 50 * (timeLeft / duration);
                
                // Soldan uçanlar
                confetti(Object.assign({}, defaults, { 
                    particleCount, 
                    origin: { x: randomInRange(0, 0.2), y: Math.random() - 0.2 } 
                }));
                // Sağdan uçanlar
                confetti(Object.assign({}, defaults, { 
                    particleCount, 
                    origin: { x: randomInRange(0.8, 1), y: Math.random() - 0.2 } 
                }));
            }, 250);

            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
        </script>
        """, height=0,
    )

# 2. Karakter Məlumatları
karakter_bazasi = {
    "Standart": {"desc": "Sadiqcə oynayır.", "price": 0},
    "Şanslı Hüseyn": {"desc": "✨ Yaxınlaşanda 'İstidir' deyir!", "price": 0},
    "İnadkar İbrahim": {"desc": "⏳ Motivasiya verir.", "price": 15},
    "Dəqiqlik Ustası": {"desc": "🎯 Tək/Cüt olduğunu bilir.", "price": 40},
    "Kral Qalib": {"desc": "👑 2 qat balon verir!", "price": 100}
}

# 3. Yaddaşın təyin olunması
if 'balonlar' not in st.session_state:
    st.session_state.balonlar = 0
if 'aciq_karakterler' not in st.session_state:
    st.session_state.aciq_karakterler = ["Standart", "Şanslı Hüseyn"]
if 'istifadeci_adi' not in st.session_state:
    st.session_state.istifadeci_adi = ""
if 'karakter' not in st.session_state:
    st.session_state.karakter = ""

# --- GİRİŞ ---
if not st.session_state.istifadeci_adi:
    st.title("🎈 Balon Dünyasına Xoş Gəldin!")
    ad = st.text_input("Adını yaz:")
    if st.button("Daxil Ol"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- SİDEBAR (Balon Sayğacı) ---
st.sidebar.title(f"👤 {st.session_state.istifadeci_adi}")
st.sidebar.header(f"🎈 Balon Sayı: {st.session_state.balonlar}")
st.sidebar.divider()

st.sidebar.subheader("🛒 Mağaza")
for k, v in karakter_bazasi.items():
    if k in st.session_state.aciq_karakterler:
        if st.sidebar.button(f"Seç: {k}", key=f"s_{k}"):
            st.session_state.karakter = k
            st.rerun()
    else:
        if st.sidebar.button(f"Aç: {k} (💰 {v['price']})", key=f"b_{k}"):
            if st.session_state.balonlar >= v['price']:
                st.session_state.balonlar -= v['price']
                st.session_state.aciq_karakterler.append(k)
                st.rerun()

# --- OYUN ---
if not st.session_state.karakter:
    st.info("Sol tərəfdən bir karakter seçib başla!")
    st.stop()

if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)
    st.session_state.qazandi = False

# BAŞLIQ VƏ MAVİ PULT
c1, c2 = st.columns([10, 1])
c1.title(f"🎮 {st.session_state.karakter} {st.session_state.istifadeci_adi}")
if c2.button("🎮", help="Gizli Qazanma!"):
    st.session_state.qazandi = True

if not st.session_state.qazandi:
    texmin = st.number_input("Təxminin:", 1, 100)
    if st.button("Yoxla"):
        if texmin == st.session_state.gizli:
            st.session_state.qazandi = True
            st.rerun()
        elif texmin < st.session_state.gizli:
            st.warning("⬆️ Daha BÖYÜK!")
        else:
            st.warning("⬇️ Daha KİÇİK!")
else:
    # QALİBİYYƏT
    balon_hediyye = random.randint(10, 25)
    if st.session_state.karakter == "Kral Qalib":
        balon_hediyye *= 2
    
    st.success(f"🎊 Möhtəşəm! +{balon_hediyye} Balon qazandın!")
    st.session_state.balonlar += balon_hediyye
    qelebe_effekti() # Ətraflardan şarlar uçur
    
    if st.button("Növbəti Raund"):
        del st.session_state.gizli
        st.session_state.qazandi = False
        st.rerun()
