import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HuseynCraft 3D - Biomes & Trees", layout="wide")

# OYUNUN MASTER KODU
mc_extreme_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Courier New', Courier, monospace; }
        #menu { position: absolute; width: 100%; height: 100%; background: url('https://wallpaperaccess.com/full/15105.jpg'); background-size: cover; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 100; color: white; text-shadow: 4px 4px #000; }
        .btn { background: #5a5a5a; border: 4px solid #000; color: white; padding: 20px 40px; font-size: 30px; cursor: pointer; margin: 10px; }
        .btn:hover { background: #828282; }
        #crosshair { position: absolute; top: 50%; left: 50%; width: 20px; height: 2px; background: white; transform: translate(-50%, -50%); pointer-events: none; z-index: 10; }
        #crosshair::after { content: ''; position: absolute; top: 50%; left: 50%; width: 2px; height: 20px; background: white; transform: translate(-50%, -50%); }
    </style>
</head>
<body>
    <div id="menu">
        <h1>HUSEYN CRAFT PRO</h1>
        <button class="btn" onclick="startGame()">DÜNYAYA GİR</button>
        <p>W,A,S,D - Hərəkət | SPACE - Tullan | SOL KLİK - Sındır | SAĞ KLİK - Qoy</p>
    </div>
    <div id="crosshair"></div>

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
            scene.fog = new THREE.Fog(0x87CEEB, 20, 150);

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            clock = new THREE.Clock();

            const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2);
            scene.add(light);

            // --- 3D RELYEF (DAĞLAR VƏ TƏPƏLƏR) ---
            const geometry = new THREE.PlaneGeometry(400, 400, 60, 60);
            geometry.rotateX(-Math.PI / 2);
            
            const vertices = geometry.attributes.position.array;
            for (let i = 0; i < vertices.length; i += 3) {
                // Riyazi dalğalarla dağlar yaradılır
                let x = vertices[i];
                let z = vertices[i + 2];
                vertices[i + 1] = Math.sin(x / 10) * Math.cos(z / 10) * 5 + Math.sin(x / 5) * 2;
            }
            geometry.computeVertexNormals();
            
            const ground = new THREE.Mesh(geometry, new THREE.MeshPhongMaterial({color: 0x3d6e1d}));
            scene.add(ground);
            objects.push(ground);

            // --- AĞACLAR ƏLAVƏ EDİLMƏSİ ---
            for(let i=0; i<40; i++) {
                createTree(Math.random()*300-150, Math.random()*300-150);
            }

            // --- 3D PLAYER MODELİ ---
            player = new THREE.Group();
            const body = new THREE.Mesh(new THREE.BoxGeometry(1, 2, 0.5), new THREE.MeshPhongMaterial({color: 0x0000ff}));
            body.position.y = 1;
            player.add(body);
            scene.add(player);

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // İDARƏETMƏ
            document.addEventListener('mousemove', (e) => {
                if (document.pointerLockElement === document.body) {
                    player.rotation.y -= e.movementX * 0.002;
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
        }

        function createTree(x, z) {
            const trunk = new THREE.Mesh(new THREE.BoxGeometry(1, 5, 1), new THREE.MeshPhongMaterial({color: 0x5d4037}));
            trunk.position.set(x, 2.5, z);
            const leaves = new THREE.Mesh(new THREE.BoxGeometry(4, 4, 4), new THREE.MeshPhongMaterial({color: 0x2e7d32}));
            leaves.position.set(x, 6, z);
            scene.add(trunk);
            scene.add(leaves);
            objects.push(trunk, leaves);
        }

        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta();

            const speed = 12;
            if(moveF) player.translateZ(speed * delta);
            if(moveB) player.translateZ(-speed * delta);
            if(moveL) player.translateX(speed * delta);
            if(moveR) player.translateX(-speed * delta);

            velY -= 35 * delta;
            player.position.y += velY * delta;
            if(player.position.y < 0) { player.position.y = 0; velY = 0; canJ = true; }

            // Kamera TPS (Oyunçunun arxasından)
            const camOffset = new THREE.Vector3(0, 5, -10
