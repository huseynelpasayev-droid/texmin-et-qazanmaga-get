import streamlit as st
import random

# Sayt ayarları
st.set_page_config(page_title="Secret & Unlock Game", page_icon="🎈")

# 1. Konfetti və Səs Funksiyası
def qelebe_effekti():
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            confetti({ particleCount: 200, spread: 90, origin: { y: 0.6 } });
            var audio = new Audio('https://www.myinstants.com/media/sounds/tada.mp3');
            audio.play();
        </script>
        """, height=0,
    )

# 2. Karakter Məlumatları (Kilid sistemi ilə)
# Qiyməti 0 olanlar açıqdır, digərləri balonla açılır.
karakter_bazasi = {
    "Standart": {"desc": "Sadiqcə oynayır.", "price": 0},
    "Şanslı Hüseyn": {"desc": "✨ Yaxınlaşanda 'İstidir' deyir!", "price": 0},
    "Dəqiqlik Ustası": {"desc": "🎯 Tək/Cüt olduğunu bilir.", "price": 20},
    "Kral Rəşad": {"desc": "👑 Hər zaman düzgün cavaba 5 addım yaxınlaşdırır!", "price": 50},
    "Əfsanəvi Qalib": {"desc": "💎 Hər qələbədə 2 qat balon verir!", "price": 100}
}

# 3. Session State (Yaddaş)
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
    if st.button("Başla"):
        if ad:
            st.session_state.istifadeci_adi = ad
            st.rerun()
    st.stop()

# --- SİDEBAR (Profil və Mağaza) ---
st.sidebar.title(f"👤 {st.session_state.istifadeci_adi}")
st.sidebar.metric("Mövcud Balonların", f"🎈 {st.session_state.balonlar}")

st.sidebar.subheader("🛒 Karakter Mağazası")
for k, v in karakter_bazasi.items():
    if k in st.session_state.aciq_karakterler:
        if st.sidebar.button(f"Seç: {k}", key=f"sel_{k}"):
            st.session_state.karakter = k
    else:
        if st.sidebar.button(f"Aç: {k} (💰 {v['price']})", key=f"buy_{k}"):
            if st.session_state.balonlar >= v['price']:
                st.session_state.balonlar -= v['price']
                st.session_state.aciq_karakterler.append(k)
                st.toast(f"🎉 {k} kilidi açıldı!")
                st.rerun()
            else:
                st.sidebar.error("Kifayət qədər balonun yoxdur!")

# --- OYUN HİSSƏSİ ---
if not st.session_state.karakter:
    st.info("Sol tərəfdən bir karakter seçərək oyuna başla!")
    st.stop()

st.title(f"🎮 {st.session_state.karakter} rejimi")
if 'gizli' not in st.session_state:
    st.session_state.gizli = random.randint(1, 100)
    st.session_state.say = 0

# --- SECRET CONSOLE (Gizli Hiylə) ---
with st.expander("🛠️"): # Bu balaca işarənin içində gizli düymə olacaq
    if st.button("ADMIN: QAZAN"):
        texmin = st.session_state.gizli # Avtomatik düz rəqəmi seçir
else:
    texmin = st.number_input("Təxminin (1-100):", 1, 100)

if st.button("Yoxla"):
    st.session_state.say += 1
    if texmin < st.session_state.gizli:
        st.warning("⬆️ Daha BÖYÜK!")
    elif texmin > st.session_state.gizli:
        st.warning("⬇️ Daha KİÇİK!")
    else:
        # QALİBİYYƏT
        qazanilan_balon = random.randint(5, 15)
        if st.session_state.karakter == "Əfsanəvi Qalib":
            qazanilan_balon *= 2
            
        st.session_state.balonlar += qazanilan_balon
        st.success(f"🎊 Təbriklər! {qazanilan_balon} balon qazandın!")
        qelebe_effekti()
        
        if st.button("Növbəti Raund"):
            del st.session_state.gizli
            st.rerun()
            
st.sidebar.button("Karakteri Sıfırla", on_click=lambda: st.session_state.clear())
