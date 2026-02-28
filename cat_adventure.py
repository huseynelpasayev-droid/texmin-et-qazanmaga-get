import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HuseynCraft Survival Edition", layout="wide")

mc_survival_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Arial', sans-serif; }
        #overlay { position: absolute; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: flex; justify-content: center; align-items: center; z-index: 1000; color: white; flex-direction: column; }
        
        /* Survival Barları */
        #hud { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 20px; z-index: 100; pointer-events: none; }
        .stat-bar { width: 150px; height: 20px; border: 2px solid #fff; background: #000; position: relative; }
        .fill { height: 100%; transition: width 0.3s; }
        #hp-fill { background: red; width: 100%; }
        #hunger-fill { background: orange; width: 100%; }
        #thirst-fill { background: blue; width: 100%; }

        /* Mağaza və Ayarlar Menyusu */
        #shop-menu { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 400px; background: #333; border: 5px solid #000; padding: 20px; display: none; z-index: 2000; color: white; text-align: center; }
        .shop-item { background: #555; margin: 10px; padding: 10px; cursor: pointer; border: 2px solid #eee; }
        .shop-item:hover { background: #777; }
        
        #crosshair { position: absolute; top: 50%; left: 50%; width: 15px; height: 15px; border: 2px solid white; transform: translate(-50%, -50%); pointer-events: none; z-index: 10; }
    </style>
</head>
<body>
    <div id="overlay">
        <h1>HUSEYNCRAFT SURVIVAL</h1>
        <button onclick="startGame()" style="padding:15px 30px; font-size:20px; cursor:pointer;">DÜNYAYA GİR</button>
        <div style="margin-top:20px;">
            <h3>MAĞAZA (ANA MENYU)</h3>
            <div class="shop-item" onclick="buyItem('speed')">Sürət Artırımı (10 Qızıl)</div>
            <div class="shop-item" onclick="buyItem('skin')">Mavi Kostyum Değiş</div>
        </div>
    </div>

    <div id="shop-menu">
        <h2>AYARLAR & MAĞAZA</h2>
        <div class="shop-item" onclick="buyItem('speed')">Sürəti 2X Et</div>
        <div class="shop-item" onclick="buyItem('heal')">Canı Yenilə</div>
        <button onclick="toggleShop()" style="margin-top:20px;">Bağla</button>
    </div>

    <div id="hud">
        <div>Can: <div class="stat-bar"><div id="hp-fill" class="fill"></div></div></div>
        <div>Aclıq: <div class="stat-bar"><div id="hunger-fill" class="fill"></div></div></div>
        <div>Su: <div class="stat-bar"><div id="thirst-fill" class="fill"></div></div></div>
    </div>
    
    <div id="crosshair"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene, camera, renderer, player, clock;
        let moveF = false, moveB = false, moveL = false, moveR = false, velY = 0, canJ = true;
        let objects = [], speedMult = 1;
        let stats = { hp: 100, hunger: 100, thirst: 100 };

        function startGame() {
            document.getElementById('overlay').style.display = 'none';
            document.body.requestPointerLock();
            init();
            animate();
            startDegradation(); // Aclıq və susuzluq başlasın
        }

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
            clock = new THREE.Clock();

            const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1);
            scene.add(light);

            // Relyefli Yer
            const ground = new THREE.Mesh(new THREE.PlaneGeometry(500, 500), new THREE.MeshPhongMaterial({color: 0x4d8a31}));
            ground.rotation.x = -Math.PI/2;
            scene.add(ground);
            objects.push(ground);

            // 3D Player (Gözləri və Üzü olan)
            player = new THREE.Group();
            const body = new THREE.Mesh(new THREE.BoxGeometry(1, 2, 0.6), new THREE.MeshPhongMaterial({color: 0x0000ff}));
            const head = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.8, 0.8), new THREE.MeshPhongMaterial({color: 0xffdbac}));
            head.position.y = 1.4;
            const eye = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.1, 0.1), new THREE.MeshPhongMaterial({color: 0x000}));
            eye.position.set(0.2, 1.5, 0.4);
            player.add(body, head, eye);
            scene.add(player);

            renderer = new THREE.WebGLRenderer({antialias: true});
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            document.addEventListener('keydown', (e) => {
                if(e.code === 'KeyW') moveF = true;
                if(e.code === 'KeyS') moveB = true;
                if(e.code === 'Space' && canJ) { velY = 15; canJ = false; }
                if(e.key === '`') toggleShop();
            });
            document.addEventListener('keyup', (e) => {
                if(e.code === 'KeyW') moveF = false;
                if(e.code === 'KeyS') moveB = false;
            });
            
            document.addEventListener('mousemove', (e) => {
                if(document.pointerLockElement === document.body) {
                    player.rotation.y -= e.movementX * 0.003;
                }
            });
        }

        function toggleShop() {
            const menu = document.getElementById('shop-menu');
            if(menu.style.display === 'block') {
                menu.style.display = 'none';
                document.body.requestPointerLock();
            } else {
                menu.style.display = 'block';
                document.exitPointerLock();
            }
        }

        function buyItem(type) {
            if(type === 'speed') speedMult = 2;
            if(type === 'heal') stats.hp = 100;
            alert(type + " alındı!");
        }

        function startDegradation() {
            setInterval(() => {
                stats.hunger -= 1;
                stats.thirst -= 2;
                if(stats.hunger <= 0 || stats.thirst <= 0) stats.hp -= 5;
                updateHUD();
            }, 3000);
        }

        function updateHUD() {
            document.getElementById('hp-fill').style.width = stats.hp + "%";
            document.getElementById('hunger-fill').style.width = stats.hunger + "%";
            document.getElementById('thirst-fill').style.width = stats.thirst + "%";
            if(stats.hp <= 0) alert("ÖLDÜNÜZ!");
        }

        function animate() {
            requestAnimationFrame(animate);
            let delta = clock.getDelta();
            let moveSpeed = 15 * speedMult;

            if(moveF) player.translateZ(moveSpeed * delta);
            if(moveB) player.translateZ(-moveSpeed * delta);

            velY -= 35 * delta;
            player.position.y += velY * delta;
            if(player.position.y < 0) { player.position.y = 0; velY = 0; canJ = true; }

            const camPos = new THREE.Vector3(0, 5, -10).applyQuaternion(player.quaternion);
            camera.position.copy(player.position).add(camPos);
            camera.lookAt(player.position.x, player.position.y + 2, player.position.z);

            renderer.render(scene, camera);
        }
    </script>
</body>
</html>
"""

components.html(mc_survival_code, height=800)
