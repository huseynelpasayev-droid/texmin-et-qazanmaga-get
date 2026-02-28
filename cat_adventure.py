import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Huseyn's Super Cat 3D", layout="wide")

# OYUNUN ƏSAS KODU
game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; font-family: sans-serif; }
        #blocker { position: absolute; width: 100%; height: 100%; background: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; color: white; cursor: pointer; text-align: center; }
    </style>
</head>
<body>
    <div id="blocker"><div><h1>OYUNA BAŞLA</h1><p>W,A,S,D - Hərəkət | SPACE - Hopbanmaq<br>(Siçanı aktiv etmək üçün bura basın)</p></div></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene, camera, renderer, player, clock, yaw = 0;
        let moveF = false, moveB = false, moveL = false, moveR = false, canJ = false, velY = 0;

        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            clock = new THREE.Clock();
            camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);

            const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2);
            scene.add(light);

            // YER (KƏND)
            const ground = new THREE.Mesh(new THREE.PlaneGeometry(1000, 1000), new THREE.MeshPhongMaterial({color: 0x228B22}));
            ground.rotation.x = -Math.PI/2;
            scene.add(ground);

            // SƏHRA VƏ PİRAMİDALAR
            const sandMat = new THREE.MeshPhongMaterial({color: 0xEDC9AF});
            for(let i=0; i<5; i++) {
                const pyr = new THREE.Mesh(new THREE.ConeGeometry(15 + i*5, 25, 4), sandMat);
                pyr.position.set(50 + i*20, 12.5, -50 - i*30);
                scene.add(pyr);
            }

            // --- PİŞİK (AYAĞÜSTƏ MODEL) ---
            player = new THREE.Group();
            
            // Bədən (Dik duran bel və qarın)
            const body = new THREE.Mesh(new THREE.BoxGeometry(1.2, 2.2, 1.2), new THREE.MeshPhongMaterial({color: 0xFFA500}));
            body.position.y = 1.1;
            player.add(body);

            // Baş
            const head = new THREE.Mesh(new THREE.BoxGeometry(1.3, 1.3, 1.3), body.material);
            head.position.y = 2.8;
            player.add(head);

            // Əllər və Ayaqlar (Detallar)
            const limbGeo = new THREE.BoxGeometry(0.4, 1.2, 0.4);
            function addLimb(x, y, z) {
                const limb = new THREE.Mesh(limbGeo, body.material);
                limb.position.set(x, y, z);
                player.add(limb);
            }
            addLimb(0.5, 0.6, 0); addLimb(-0.5, 0.6, 0); // Ayaqlar
            addLimb(0.8, 2.2, 0); addLimb(-0.8, 2.2, 0); // Əllər

            scene.add(player);

            // İDARƏETMƏ
            document.getElementById('blocker').addEventListener('click', () => document.body.requestPointerLock());
            document.addEventListener('mousemove', (e) => {
                if(document.pointerLockElement === document.body) {
                    yaw -= e.movementX * 0.003;
                    player.rotation.y = yaw;
                }
            });

            window.addEventListener('keydown', (e) => {
                if(e.code === 'KeyW') moveF = true; if(e.code === 'KeyS') moveB = true;
                if(e.code === 'KeyA') moveL = true; if(e.code === 'KeyD') moveR = true;
                if(e.code === 'Space' && canJ) { velY = 15; canJ = false; }
            });
            window.addEventListener('keyup', (e) => {
                if(e.code === 'KeyW') moveF = false; if(e.code === 'KeyS') moveB = false;
                if(e.code === 'KeyA') moveL = false; if(e.code === 'KeyD') moveR = false;
            });

            renderer = new THREE.WebGLRenderer({antialias: true});
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);
        }

        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta();

            const speed = 12;
            if(moveF) player.translateZ(speed * delta);
            if(moveB) player.translateZ(-speed * delta);
            if(moveL) player.translateX(speed * delta);
            if(moveR) player.translateX(-speed * delta);

            velY -= 35 * delta; // Cazibə
            player.position.y += velY * delta;
            if(player.position.y <= 0) { player.position.y = 0; velY = 0; canJ = true; }

            // KAMERA İZLƏMƏ
            const camOffset = new THREE.Vector3(0, 8, -15).applyQuaternion(player.quaternion);
            camera.position.copy(player.position).add(camOffset);
            camera.lookAt(player.position.x, player.position.y + 3, player.position.z);

            renderer.render(scene, camera);
        }
    </script>
</body>
</html>
"""

components.html(game_code, height=800)
