import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HuseynCraft PRO 3D", layout="wide")

# OYUNUN TAM KODU - DİQQƏTLƏ KOPYALA
mc_ultimate_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Segoe UI', sans-serif; }
        #menu { position: absolute; width: 100%; height: 100%; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://wallpaperaccess.com/full/15105.jpg'); background-size: cover; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 100; color: white; }
        .btn { background: #4CAF50; border: 4px solid #2e7d32; color: white; padding: 15px 30px; font-size: 24px; cursor: pointer; margin: 10px; font-weight: bold; }
        #crosshair { position: absolute; top: 50%; left: 50%; width: 20px; height: 20px; border: 2px solid white; border-radius: 50%; transform: translate(-50%, -50%); pointer-events: none; z-index: 10; }
        #ui { position: absolute; top: 10px; left: 10px; color: white; background: rgba(0,0,0,0.6); padding: 10px; border-radius: 5px; pointer-events: none; }
    </style>
</head>
<body>
    <div id="menu">
        <h1>HUSEYN CRAFT: BIOMES & 3D</h1>
        <button class="btn" onclick="startGame()">OYUNA BAŞLA</button>
        <p>W,A,S,D: Hərəkət | SPACE: Tullanmaq | Siçan: Baxış</p>
    </div>
    <div id="crosshair"></div>
    <div id="ui">Biom: Meşə / Dağlıq</div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene, camera, renderer, player, clock;
        let moveF = false, moveB = false, moveL = false, moveR = false, canJ = true, velY = 0;
        let objects = [];

        function startGame() {
            document.getElementById('menu').style.display = 'none';
            document.body.requestPointerLock();
            init();
            animate();
        }

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            scene.fog = new THREE.Fog(0x87CEEB, 20, 100);

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            clock = new THREE.Clock();

            const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2);
            scene.add(light);

            // --- DAĞLIQ RELYEF ---
            const geo = new THREE.PlaneGeometry(300, 300, 50, 50);
            geo.rotateX(-Math.PI / 2);
            const pos = geo.attributes.position.array;
            for (let i = 0; i < pos.length; i += 3) {
                let x = pos[i], z = pos[i+2];
                pos[i+1] = Math.sin(x/8) * Math.cos(z/8) * 4; // Təpələr
            }
            geo.computeVertexNormals();
            const ground = new THREE.Mesh(geo, new THREE.MeshPhongMaterial({color: 0x4d8a31}));
            scene.add(ground);
            objects.push(ground);

            // --- AĞACLAR ---
            for(let i=0; i<30; i++) {
                let tx = Math.random()*200-100;
                let tz = Math.random()*200-100;
                const trunk = new THREE.Mesh(new THREE.BoxGeometry(0.8, 4, 0.8), new THREE.MeshPhongMaterial({color: 0x5d4037}));
                trunk.position.set(tx, 2, tz);
                const leaves = new THREE.Mesh(new THREE.BoxGeometry(3, 3, 3), new THREE.MeshPhongMaterial({color: 0x2e7d32}));
                leaves.position.set(tx, 5, tz);
                scene.add(trunk, leaves);
            }

            // --- 3D OYUNÇU MODELİ ---
            player = new THREE.Group();
            const body = new THREE.Mesh(new THREE.BoxGeometry(1, 1.8, 0.6), new THREE.MeshPhongMaterial({color: 0x0066ff}));
            body.position.y = 0.9;
            player.add(body);
            const head = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.8, 0.8), new THREE.MeshPhongMaterial({color: 0xffdbac}));
            head.position.y = 2.2;
            player.add(head);
            scene.add(player);

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            document.addEventListener('mousemove', (e) => {
                if (document.pointerLockElement === document.body) {
                    player.rotation.y -= e.movementX * 0.002;
                }
            });

            window.addEventListener('keydown', (e) => {
                if(e.code === 'KeyW') moveF = true; if(e.code === 'KeyS') moveB = true;
                if(e.code === 'KeyA') moveL = true; if(e.code === 'KeyD') moveR = true;
                if(e.code === 'Space' && canJ) { velY = 12; canJ = false; }
            });
            window.addEventListener('keyup', (e) => {
                if(e.code === 'KeyW') moveF = false; if(e.code === 'KeyS') moveB = false;
                if(e.code === 'KeyA') moveL = false; if(e.code === 'KeyD') moveR = false;
            });
        }

        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta();

            const speed = 10;
            if(moveF) player.translateZ(speed * delta);
            if(moveB) player.translateZ(-speed * delta);
            if(moveL) player.translateX(speed * delta);
            if(moveR) player.translateX(-speed * delta);

            velY -= 30 * delta;
            player.position.y += velY * delta;
            if(player.position.y < 0) { player.position.y = 0; velY = 0; canJ = true; }

            // Üçüncü Şəxs Kamerası (TPS)
            const camOffset = new THREE.Vector3(0, 5, -8).applyQuaternion(player.quaternion);
            camera.position.copy(player.position).add(camOffset);
            camera.lookAt(player.position.x, player.position.y + 1.5, player.position.z);

            renderer.render(scene, camera);
        }
    </script>
</body>
</html>
"""

components.html(mc_ultimate_code, height=800)
