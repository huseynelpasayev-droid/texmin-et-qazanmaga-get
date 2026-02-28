import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HuseynCraft 3D", layout="wide")

minecraft_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; font-family: sans-serif; }
        #overlay { position: absolute; bottom: 20px; left: 20px; color: white; background: rgba(0,0,0,0.5); padding: 15px; border-radius: 10px; pointer-events: none; }
        #crosshair { position: absolute; top: 50%; left: 50%; width: 20px; height: 20px; border: 2px solid white; border-radius: 50%; transform: translate(-50%, -50%); pointer-events: none; }
    </style>
</head>
<body>
    <div id="crosshair"></div>
    <div id="overlay">
        <h2>⛏️ HuseynCraft v1.0</h2>
        <b>W,A,S,D:</b> Gəzmək | <b>SPACE:</b> Tullanmaq<br>
        <b>SOL KLİK:</b> Blok Qoymaq | <b>SAĞ KLİK:</b> Blok Silmək<br>
        <b>Siçan:</b> Ətrafa baxmaq (Kilidləmək üçün ekrana bas)
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene, camera, renderer, clock, velocity, direction, moveForward, moveBackward, moveLeft, moveRight, canJump;
        let objects = []; // Blokları saxlamaq üçün

        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB); // Göy üzü
            scene.fog = new THREE.Fog(0x87CEEB, 0, 100);

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            clock = new THREE.Clock();

            const light = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(light);
            const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
            dirLight.position.set(10, 20, 10);
            scene.add(dirLight);

            // Torpaq (Göy qat)
            const floorGeo = new THREE.PlaneGeometry(200, 200, 20, 20);
            const floorMat = new THREE.MeshPhongMaterial({ color: 0x228B22 });
            const floor = new THREE.Mesh(floorGeo, floorMat);
            floor.rotation.x = -Math.PI / 2;
            scene.add(floor);
            objects.push(floor);

            // İdarəetmə Fizikası
            velocity = new THREE.Vector3();
            direction = new THREE.Vector3();

            // SİÇAN KİLİDİ
            document.body.addEventListener('click', () => {
                document.body.requestPointerLock();
            });

            document.addEventListener('mousemove', (e) => {
                if (document.pointerLockElement === document.body) {
                    camera.rotation.y -= e.movementX * 0.002;
                    camera.rotation.x -= e.movementY * 0.002;
                    camera.rotation.x = Math.max(-Math.PI/2, Math.min(Math.PI/2, camera.rotation.x));
                }
            });

            // BLOK QOYMAQ (Minecraft Məntiqi)
            window.addEventListener('mousedown', (e) => {
                if (document.pointerLockElement !== document.body) return;

                const raycaster = new THREE.Raycaster();
                const center = new THREE.Vector2(0, 0); // Ekranın ortası
                raycaster.setFromCamera(center, camera);
                const intersects = raycaster.intersectObjects(objects);

                if (intersects.length > 0) {
                    const intersect = intersects[0];
                    
                    if (e.button === 0) { // SOL KLİK - BLOK QOY
                        const voxel = new THREE.Mesh(
                            new THREE.BoxGeometry(2, 2, 2),
                            new THREE.MeshPhongMaterial({ color: Math.random() * 0xffffff })
                        );
                        voxel.position.copy(intersect.point).add(intersect.face.normal);
                        voxel.position.divideScalar(2).floor().multiplyScalar(2).addScalar(1);
                        scene.add(voxel);
                        objects.push(voxel);
                    } 
                    else if (e.button === 2) { // SAĞ KLİK - BLOK SİL
                        if (intersect.object !== floor) {
                            scene.remove(intersect.object);
                            objects.splice(objects.indexOf(intersect.object), 1);
                        }
                    }
                }
            });

            // Sağ klik menyusunu bağla
            window.addEventListener('contextmenu', e => e.preventDefault());

            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            camera.position.y = 5;
            
            // Klaviatura
            const onKeyDown = (e) => {
                if(e.code === 'KeyW') moveForward = true;
                if(e.code === 'KeyS') moveBackward = true;
                if(e.code === 'KeyA') moveLeft = true;
                if(e.code === 'KeyD') moveRight = true;
                if(e.code === 'Space' && canJump) { velocity.y += 15; canJump = false; }
            };
            const onKeyUp = (e) => {
                if(e.code === 'KeyW') moveForward = false;
                if(e.code === 'KeyS') moveBackward = false;
                if(e.code === 'KeyA') moveLeft = false;
                if(e.code === 'KeyD') moveRight = false;
            };
            document.addEventListener('keydown', onKeyDown);
            document.addEventListener('keyup', onKeyUp);
        }

        function animate() {
            requestAnimationFrame(animate);
            const delta = clock.getDelta();

            velocity.x -= velocity.x * 10.0 * delta;
            velocity.z -= velocity.z * 10.0 * delta;
            velocity.y -= 9.8 * 4.0 * delta; 

            direction.z = Number(moveForward) - Number(moveBackward);
            direction.x = Number(moveRight) - Number(moveLeft);
            direction.normalize();

            if (moveForward || moveBackward) velocity.z -= direction.z * 100.0 * delta;
            if (moveLeft || moveRight) velocity.x -= direction.x * 100.0 * delta;

            camera.translateX(-velocity.x * delta);
            camera.translateZ(-velocity.z * delta);
            camera.position.y += (velocity.y * delta);

            if (camera.position.y < 5) {
                velocity.y = 0;
                camera.position.y = 5;
                canJump = true;
            }

            renderer.render(scene, camera);
        }
    </script>
</body>
</html>
"""

components.html(minecraft_code, height=800)
