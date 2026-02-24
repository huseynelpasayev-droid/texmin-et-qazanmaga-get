import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Balon Ustası", page_icon="🎈")

# 1. Konfetti və Səs Funksiyası
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            confetti({ particleCount: 250, spread: 100, origin: { y: 0.6 } });
            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
        </script>
        """, height=0,
    )

# 2. Karakter Bazası
karakter_bazasi = {
    "Standart": {"desc": "Sadiqcə oynayır.", "price": 0},
    "Şanslı Hüseyn": {"desc": "✨ Yaxınlaşanda 'İstidir' deyir!", "price": 0},
    "İnadkar İbrahim": {"desc": "⏳ Hər səhvdə motivasiya verir.", "price": 10},
    "Dəqiqlik Ustası": {"desc": "🎯 Tək/Cüt olduğunu bilir.", "price": 30},
    "Kral Qalib": {"desc": "👑 Hər qələbədə 2 qat balon verir!", "price": 100}
}

# 3. Yaddaşın (Session State) Qurulması
if 'balonlar' not in st.session_state:
    st.session_state.balonlar = 0
if 'aciq_karakterler' not in st.session_state:
    st.session_state.aciq_karakterler = ["Standart", "Şanslı Hüseyn"]
if 'istifadeci_adi' not in st.session_state:
    st.session_state.istifadeci_adi = ""
if 'karakter' not in st.session_state:
    st.session_state.karakter = ""

# --- GİRİŞ EKRANI ---
if not st.session_state.istifadeci_adi:
    st.title("🎈 Balon Yığ və Karakter Aç!")
    ad = st.text_input("Adını yaz:")
    if st.button("Dünyaya Giriş Et"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- SİDEBAR (Profil, Balon Sayğacı və Mağaza) ---
st.sidebar.title(f"👤 {st.session_state.istifadeci_adi}")
st.sidebar.markdown(f"### 🎈 Balon Sayı: **{st.session_state.balonlar}**")
st.sidebar.divider()

st.sidebar.subheader("🛒 Karakter Mağazası")
for k, v in karakter_bazasi.items():
    if k in st.session_state.aciq_karakterler:
        if st.sidebar.button(f"Seç: {k}", key=f"sel_{k}"):
            st.session_state.karakter = k
            st.rerun()
    else:
        if st.sidebar.button(f"Aç: {k} (💰 {v['price']})", key=f"buy_{k}"):
            if st.session_state.balonlar >= v['price']:
                st.session_state.balonlar -= v['price']
                st.session_state.aciq_karakterler.append(k)
                st.toast(f"🎉 {k} açıldı!")
                st.rerun()
            else:
                st.sidebar.error("Balonun çatmır!")

# --- OYUN HİSSƏSİ ---
if not st.session_state.karakter:
    st.info("Sol tərəfdən bir karakter seç!")
    st.stop()

if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)
    st.session_state.say = 0
    st.session_state.qazandi = False

# MAVİ PULT GİZLİ DÜYMƏSİ
col_title, col_secret = st.columns([10, 1])
col_title.title(f"{st.session_state.karakter} {st.session_state.istifadeci_adi}")

# Bura diqqət: Mavi pulta basanda gizli qazanma funksiyası
if col_secret.button("🎮", help="Gizli Hiylə"):
    st.session_state.qazandi = True
    st.toast("🤫 Hiylə Aktiv Edildi!")

st.write(f"_{karakter_bazasi[st.session_state.karakter]['desc']}_")

# Oyun məntiqi
if not st.session_state.qazandi:
    texmin = st.number_input("Təxminin (1-100):", 1, 100)
    if st.button("Yoxla"):
        st.session_state.say += 1
        if texmin < st.session_state.gizli:
            st.warning("⬆️ Daha BÖYÜK!")
        elif texmin > st.session_state.gizli:
            st.warning("⬇️ Daha KİÇİK!")
        else:
            st.session_state.qazandi = True
            st.rerun()
else:
    # QALİBİYYƏT ANI
    q_balon = random.randint(5, 15)
    if st.session_state.karakter == "Kral Qalib":
        q_balon *= 2
    
    st.success(f"🎊 TƏBRİKLƏR! {q_balon} Balon qazandın!")
    st.session_state.balonlar += q_balon
    qelebe_effekti()
    
    if st.button("Növbəti Raund"):
        del st.session_state.gizli
        st.session_state.qazandi = False
        st.rerun()
