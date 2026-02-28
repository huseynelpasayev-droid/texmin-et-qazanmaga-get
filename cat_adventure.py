import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Cat Adventure 3D", layout="wide")

# OYUNUN ƏSAS 3D KODU (HTML/JS/THREE.JS)
three_js_game = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; font-family: sans-serif; }
        #ui { position: absolute; top: 10px; left: 10px; color: white; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; pointer-events: none; }
    </style>
</head>
<body>
    <div id="ui">
        <b>Super Cat Adventure 3D</b><br>
        Hərəkət: WASD | Atılmaq: SPACE<br>
        Tapşırıq: Binaları və Səhranı kəşf et!
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // 1. SƏHNƏ VƏ KAMERA
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x87CEEB); // Səma
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // 2. İŞIQLANDIRMA
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(5, 10, 7.5).normalize();
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040));

        // 3. DÜNYA (ŞƏHƏR VƏ SƏHRA)
        // Yaşıl zona (Kənd)
        const grassGeo = new THREE.PlaneGeometry(100, 100);
        const grassMat = new THREE.MeshPhongMaterial({ color: 0x228B22 });
        const ground = new THREE.Mesh(grassGeo, grassMat);
        ground.rotation.x = -Math.PI / 2;
        scene.add(ground);

        // Səhra zonası
        const sandGeo = new THREE.PlaneGeometry(100, 100);
        const sandMat = new THREE.MeshPhongMaterial({ color: 0xEDC9AF });
        const desert = new THREE.Mesh(sandGeo, sandMat);
        desert.rotation.x = -Math.PI / 2;
        desert.position.z = -100;
        scene.add(desert);

        // 4. BİNALAR (İçinə girmək olar)
        function createBuilding(x, z, color, height) {
            const group = new THREE.Group();
            const geo = new THREE.BoxGeometry(10, height, 10);
            const mat = new THREE.MeshPhongMaterial({ color: color, transparent: true, opacity: 0.8 });
            const box = new THREE.Mesh(geo, mat);
            box.position.y = height / 2;
            group.add(box);
            group.position.set(x, 0, z);
            scene.add(group);
        }
        createBuilding(20, -20, 0x808080, 30); // Şəhər binası
        createBuilding(-20, -80, 0xD2B48C, 10); // Səhra evi

        // 5. PİŞİK (Karakter)
        const playerGeo = new THREE.BoxGeometry(2, 2, 2);
        const playerMat = new THREE.MeshPhongMaterial({ color: 0xFFA500 });
        const player = new THREE.Mesh(playerGeo, playerMat);
        player.position.y = 1;
        scene.add(player);

        // 6. HƏRƏKƏT KONTROLU
        const keys = {};
        window.addEventListener('keydown', (e) => keys[e.code] = true);
        window.addEventListener('keyup', (e) => keys[e.code] = false);

        function animate() {
            requestAnimationFrame(animate);
            
            const speed = 0.5;
            if (keys['KeyW']) player.position.z -= speed;
            if (keys['KeyS']) player.position.z += speed;
            if (keys['KeyA']) player.position.x -= speed;
            if (keys['KeyD']) player.position.x += speed;
            if (keys['Space'] && player.position.y <= 1.1) player.position.y += 2; // Sadə tullanış

            // Təbii cazibə
            if (player.position.y > 1) player.position.y -= 0.1;

            // Kamera pişiyi izləsin (Third Person)
            camera.position.set(player.position.x, player.position.y + 10, player.position.z + 20);
            camera.lookAt(player.position);

            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

components.html(three_js_game, height=800)
