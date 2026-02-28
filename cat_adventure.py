import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HuseynCraft Pro", layout="wide")

# OYUNUN MASTER KODU
mc_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Arial', sans-serif; }
        #crosshair { position: absolute; top: 50%; left: 50%; width: 10px; height: 10px; border: 2px solid white; transform: translate(-50%, -50%); pointer-events: none; z-index: 10; }
        #ui { position: absolute; top: 10px; left: 10px; color: white; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; }
        #progress-bar { position: absolute; bottom: 20%; left: 50%; transform: translateX(-50%); width: 200px; height: 10px; background: rgba(0,0,0,0.5); display: none; border: 1px solid white; }
        #progress-fill { width: 0%; height: 100%; background: lime; }
    </style>
</head>
<body>
    <div id="crosshair"></div>
    <div id="progress-bar"><div id="progress-fill"></div></div>
    <div id="ui"><b>HuseynCraft v2.0</b><br>Sağ Klik: Qoymaq | Sol Klik (Saxla): Sındırmaq</div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene, camera, renderer, clock, objects = [];
        let moveF = false, moveB = false, moveL = false, moveR = false, canJ = true, velY = 0;
        let isBreaking = false, breakProgress = 0, currentTarget = null;

        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            clock = new THREE.Clock();

            const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1);
            scene.add(light);

            // TORPAQ
            const ground = new THREE.Mesh(new THREE.PlaneGeometry(1000, 1000), new THREE.MeshPhongMaterial({color: 0x4d8a31}));
            ground.rotation.x = -Math.PI / 2;
            scene.add(ground);
            objects.push(ground);

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // SİÇAN KONTROLU
            document.addEventListener('mousedown', onMouseDown);
            document.addEventListener('mouseup', onMouseUp);
            document.addEventListener('contextmenu', e => e.preventDefault());
            document.body.onclick = () => document.body.requestPointerLock();

            document.addEventListener('mousemove', (e) => {
                if (document.pointerLockElement === document.body) {
                    camera.rotation.y -= e.movementX * 0.002;
                    camera.rotation.x -= e.movementY * 0.002;
                    camera.rotation.x = Math.max(-Math.PI/2, Math.min(Math.PI/2, camera.rotation.x));
                }
            });

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
                const block = new THREE.Mesh(new THREE.BoxGeometry(4, 4, 4), new THREE.MeshPhongMaterial({color: 0x8b5a2b}));
                block.position.copy(intersect.point).add(intersect.face.normal);
                block.position.divideScalar(4).floor().multiplyScalar(4).addScalar(2);
                scene.add(block);
                objects.push(block);
            } 
            else if (e.button === 0) { // SOL KLİK - SINDIRMAQ (BAŞLA)
                if (intersect.object.geometry.type !== "PlaneGeometry") {
                    isBreaking = true;
                    currentTarget = intersect.object;
                    document.getElementById('progress-bar').style.display = 'block';
                }
            }
        }

        function onMouseUp() {
            isBreaking = false;
            breakProgress = 0;
            document.getElementById('progress-bar').style.display = 'none';
        }

        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta();

            // Sındırma mexanikası (5-10 saniyə arası)
            if (isBreaking) {
                breakProgress += delta * 30; // Bu rəqəmi azaltsan daha gec sınar
                document.getElementById('progress-fill').style.width = breakProgress + '%';
                if (breakProgress >= 100) {
                    scene.remove(currentTarget);
                    objects = objects.filter(o => o !== currentTarget);
                    onMouseUp();
                }
            }

            // Hərəkət
            const speed = 150 * delta;
            const dir = new THREE.Vector3();
            camera.getWorldDirection(dir);
            dir.y = 0; dir.normalize();

            if(moveF) camera.position.addScaledVector(dir, speed * delta * 10);
            if(moveB) camera.position.addScaledVector(dir, -speed * delta * 10);

            renderer.render(scene, camera);
        }

        window.onkeydown = (e) => {
            if(e.code === 'KeyW') moveF = true;
            if(e.code === 'KeyS') moveB = true;
        };
        window.onkeyup = (e) => {
            if(e.code === 'KeyW') moveF = false;
            if(e.code === 'KeyS') moveB = false;
        };
    </script>
</body>
</html>
"""

components.html(mc_code, height=800)
