import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Huseyn 3D Cat WASD", layout="wide")

st.title("🐾 Huseyn's WASD Cat Adventure")
st.write("Klaviaturada **W, A, S, D** düymələri ilə pişiyi hərəkət etdir!")

# OYUNUN KODU (HTML/JS)
game_code = """
<div id="game-container" style="width: 100%; height: 500px; background: #87CEEB; position: relative; border: 5px solid #555; overflow: hidden;">
    <div id="cat" style="width: 50px; height: 50px; background: orange; position: absolute; top: 200px; left: 200px; border-radius: 10px; font-size: 40px; text-align: center; line-height: 50px;">🐱</div>
    
    <div style="width: 100px; height: 200px; background: gray; position: absolute; bottom: 0; left: 500px;"></div>
    <div style="width: 100px; height: 150px; background: gray; position: absolute; bottom: 0; left: 100px;"></div>
</div>

<script>
    const cat = document.getElementById('cat');
    let posX = 200;
    let posY = 200;
    const speed = 10;

    window.addEventListener('keydown', (e) => {
        const key = e.key.toLowerCase();
        if (key === 'w') posY -= speed;
        if (key === 's') posY += speed;
        if (key === 'a') posX -= speed;
        if (key === 'd') posX += speed;

        cat.style.top = posY + 'px';
        cat.style.left = posX + 'px';
    });
</script>
"""

# Oyunu ekrana veririk
components.html(game_code, height=600)

# Statlar və Mağaza (Altda)
st.sidebar.header("📊 Pişik Statusu")
st.sidebar.write("Level: 1")
st.sidebar.button("Rəngi Dəyiş")
