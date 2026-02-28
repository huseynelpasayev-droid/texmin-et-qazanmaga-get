import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Cat Adventure 3D - Body Parts", layout="wide")

# OYUNUN ƏSAS 3D KODU
cat_model_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; }
        #instructions { position: absolute; top: 10px; left: 10px; color: white; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 8px; pointer-events: none; }
    </style>
</head>
<body>
    <div id="instructions">
        <b>Huseyn's Advanced Cat Model</b><br>
        Hərəkət: WASD | Baxış: Siçan<br>
        Detallar: Bel, Qarın, Əllər, Üz və Caynaqlar!
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene, camera, renderer, playerGroup;
        let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false;
        let prevTime = performance.now();
        const velocity = new THREE.Vector3();

        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

            // İŞIQ
            const light = new THREE.DirectionalLight(0xffffff, 1);
            light.position.set(5, 10, 7.5);
            scene.add(light);
            scene.add(new THREE.AmbientLight(0x404040));

            // YER (Şəhər və Səhra)
            const groundGeo = new THREE.PlaneGeometry(1000, 1000);
            const groundMat = new THREE.MeshPhongMaterial({ color: 0x32CD32 });
            const ground = new THREE.Mesh(groundGeo, groundMat);
            ground.rotation.x = -Math.PI / 2;
            scene.add(ground);

            // --- PİŞİK MODELİ (Bədən Üzvləri) ---
            playerGroup = new THREE.Group();

            // 1. QARIN VƏ BEL (Əsas Gövdə)
            const bodyGeo = new THREE.BoxGeometry(2, 2, 4);
            const bodyMat = new THREE.MeshPhongMaterial({ color: 0xFFA500 });
            const body = new THREE.Mesh(bodyGeo, bodyMat);
            body.position.y = 1.5;
            playerGroup.add(body);

            // 2. BAŞ VƏ ÜZ
            const headGeo = new THREE.BoxGeometry(1.8, 1.8, 1.8);
            const head = new THREE.Mesh(headGeo, bodyMat);
            head.position.set(0, 2.5, 2);
            playerGroup.add(head);

            // Gözlər (Üz detalları)
            const eyeGeo = new THREE.BoxGeometry(0.3, 0.3, 0.1);
            const eyeMat = new THREE.MeshPhongMaterial({ color: 0x000000 });
            const eyeL = new THREE.Mesh(eyeGeo, eyeMat);
            eyeL.position.set(-0.5, 2.7, 2.9);
            playerGroup.add(eyeL);
            const eyeR = new THREE.Mesh(eyeGeo, eyeMat);
            eyeR.position.set(0.5, 2.7, 2.9);
            playerGroup.add(eyeR);

            // 3. ƏLLƏR VƏ CAYNAQLAR (Ön və Arxa)
            const legGeo = new THREE.BoxGeometry(0.5, 1.5, 0.5);
            const clawGeo = new THREE.BoxGeometry(0.6, 0.2, 0.3);
            const clawMat = new THREE.MeshPhongMaterial({ color: 0xffffff }); // Ağ caynaqlar

            function createLeg(x, z) {
                const leg = new THREE.Mesh(legGeo, bodyMat);
                leg.position.set(x, 0.75, z);
                
                // Caynaqlar (Əllərin ucunda)
                const claw = new THREE.Mesh(clawGeo, clawMat);
                claw.position.set(0, -0.7, 0.3);
                leg.add(claw);
                
                playerGroup.add(leg);
                return leg;
            }

            createLeg(0.7, 1.5);  // Sağ ön əl
            createLeg(-0.7, 1.5); // Sol ön əl
            createLeg(0.7, -1.5); // Sağ arxa ayaq
            createLeg(-0.7, -1.5);// Sol arxa ayaq

            scene.add(playerGroup);

            // CONTROLS
            document.addEventListener('mousedown', () => document.body.requestPointerLock());
            document.addEventListener('mousemove', (e) => {
                if (document.pointerLockElement === document.body) {
                    playerGroup.rotation.y -= e.movementX * 0.003;
                }
            });

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            window.addEventListener('keydown', (e) => {
                if(e.code === 'KeyW') moveForward = true;
                if(e.code === 'KeyS') moveBackward = true;
                if(e.code === 'KeyA') moveLeft = true;
                if(e.code === 'KeyD') moveRight = true;
            });
            window.addEventListener('keyup', (e) => {
                if(e.code === 'KeyW') moveForward = false;
                if(e.code === 'KeyS') moveBackward = false;
                if(e.code === 'KeyA') moveLeft = false;
                if(e.code === 'KeyD') moveRight = false;
            });
        }

        function animate() {
            requestAnimationFrame(animate);
            const time = performance.now();
            const delta = (time - prevTime) / 1000;

            const speed = 15.0;
            if (moveForward) playerGroup.translateZ(speed * delta);
            if (moveBackward) playerGroup.translateZ(-speed * delta);
            if (moveLeft) playerGroup.translateX(speed * delta);
            if (moveRight) playerGroup.translateX(-speed * delta);

            // Kamera izləmə (Third Person)
            const relativeOffset = new THREE.Vector3(0, 8, -15);
            const cameraOffset = relativeOffset.applyMatrix4(playerGroup.matrixWorld);
            camera.position.lerp(cameraOffset, 0.1);
            camera.lookAt(playerGroup.position);

            prevTime = time;
            renderer.render(scene, camera);
        }
    </script>
</body>
</html>
"""

components.html(cat_model_code, height=800)
