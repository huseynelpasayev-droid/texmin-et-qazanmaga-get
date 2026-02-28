import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HuseynCraft - The Final Version", layout="wide")

# ƏSL MINECRAFT MƏNTİQLİ WEB KODU
mc_final_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Arial', sans-serif; }
        #crosshair { position: absolute; top: 50%; left: 50%; width: 15px; height: 15px; border: 2px solid white; transform: translate(-50%, -50%); pointer-events: none; z-index: 10; }
        #mining-bar { position: absolute; bottom: 30%; left: 50%; transform: translateX(-50%); width: 150px; height: 8px; background: rgba(0,0,0,0.5); display: none; border: 1px solid white; }
        #mining-fill { width: 0%; height: 100%; background: #ffcc00; }
        #info { position: absolute; top: 20px; left: 20px; color: white; background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; pointer-events: none; }
    </style>
</head>
<body>
    <div id="crosshair"></div>
    <div id="mining-bar"><div id="mining-fill"></div></div>
    <div id="info">
        <b>⛏️ HuseynCraft v3.0</b><br>
        - SAĞ KLİK: Blok Qoy (Yerləşdir)<br>
        - SOL KLİK: BASIB SAXLA (Sındır)<br>
        - W,A,S,D: Hərəkət | SPACE: Tullan
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene, camera, renderer, clock, objects = [];
        let moveF = false, moveB = false, moveL = false, moveR = false, canJ = true, velY = 0;
        let isMining = false, mineTime = 0, currentTarget = null;

        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            clock = new THREE.Clock();

            scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, 1.2));

            // OT TORPAQ
            const ground = new THREE.Mesh(new THREE.PlaneGeometry(1000, 1000), new THREE.MeshPhongMaterial({color: 0x3d6e1d}));
            ground.rotation.x = -Math.PI / 2;
            scene.add(ground);
            objects.push(ground);

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // SİÇAN KİLİDİ
            document.body.onclick = () => document.body.requestPointerLock();
            document.addEventListener('mousemove', (e) => {
                if (document.pointerLockElement === document.body) {
                    camera.rotation.y -= e.movementX * 0.002;
                    camera.rotation.x -= e.movementY * 0.002;
                    camera.rotation.x = Math.max(-Math.PI/2, Math.min(Math.PI/2, camera.rotation.x));
                }
            });

            document.addEventListener('mousedown', onMouseDown);
            document.addEventListener('mouseup', onMouseUp);
            document.addEventListener('contextmenu', e => e.preventDefault());

            camera.position.y = 5;
        }

        function onMouseDown(e) {
            if (document.pointerLockElement !== document.body) return;
            const ray = new THREE.Raycaster();
            ray.setFromCamera(new THREE.Vector2(0,0), camera);
            const intersects = ray.intersectObjects(objects);
            if (intersects.length === 0) return;
            const intersect = intersects[0];

            if (e.button === 2) { // SAĞ KLİK - QOYMAQ
                const block = new THREE.Mesh(
                    new THREE.BoxGeometry(4, 4, 4), 
                    new THREE.MeshPhongMaterial({color: 0x8b5a2b, flatShading: true})
                );
                block.position.copy(intersect.point).add(intersect.face.normal);
                block.position.divideScalar(4).floor().multiplyScalar(4).addScalar(2);
                scene.add(block);
                objects.push(block);
            } 
            else if (e.button === 0) { // SOL KLİK - SINDIRMAQ (BAŞLA)
                if (intersect.object.geometry.type !== "PlaneGeometry") {
                    isMining = true;
                    currentTarget = intersect.object;
                    document.getElementById('mining-bar').style.display = 'block';
                }
            }
        }

        function onMouseUp() {
            isMining = false;
            mineTime = 0;
            document.getElementById('mining-bar').style.display = 'none';
        }

        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta();

            // SINDIRMA MEXANİKASI (EYNİ MINECRAFT)
            if (isMining) {
                mineTime += delta * 40; // Bu sındırma sürətidir
                document.getElementById('mining-fill').style.width = mineTime + '%';
                if (mineTime >= 100) {
                    scene.remove(currentTarget);
                    objects = objects.filter(o => o !== currentTarget);
                    onMouseUp();
                }
            }

            // HƏRƏKƏT
            const speed = 25 * delta;
            const dir = new THREE.Vector3();
            camera.getWorldDirection(dir);
            dir.y = 0; dir.normalize();

            if(moveF) camera.position.addScaledVector(dir, speed);
            if(moveB) camera.position.addScaledVector(dir, -speed);

            // JUMP & GRAVITY
            velY -= 40 * delta;
            camera.position.y += velY * delta;
            if (camera.position.y < 5) { camera.position.y = 5; velY = 0; canJ = true; }

            renderer.render(scene, camera);
        }

        window.onkeydown = (e) => { if(e.code === 'KeyW') moveF = true; if(e.code === 'KeyS') moveB = true; if(e.code === 'Space' && canJ){velY=18; canJ=false;} };
        window.onkeyup = (e) => { if(e.code === 'KeyW') moveF = false; if(e.code === 'KeyS') moveB = false; };
    </script>
</body>
</html>
"""

components.html(mc_final_code, height=800)
