import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Cat Adventure - Jump Edition", layout="wide")

# OYUNUN ƏSAS 3D KODU (Hopbanma və Fizika Yeniləndi)
game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; }
        #blocker { position: absolute; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; color: white; cursor: pointer; text-align: center; font-family: sans-serif; }
        #hud { position: absolute; top: 10px; left: 10px; color: white; background: rgba(0,0,0,0.4); padding: 10px; border-radius: 5px; pointer-events: none; }
    </style>
</head>
<body>
    <div id="blocker"><div><h1>PİŞİK MACƏRASI</h1><p>Siçanı kilidləmək üçün bura basın</p><p>W,A,S,D - Qaçmaq | SPACE - HOPBANMAQ</p></div></div>
    <div id="hud"><b>Sahib: Huseyn Elpasayev</b><br>Vəziyyət: Ayaq üstə</div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene, camera, renderer, player, clock;
        let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false;
        let canJump = false;
        let velocityY = 0;
        let yaw = 0;
        const gravity = -35; // Cazibə qüvvəsi
        const jumpStrength = 15; // Hopbanma gücü

        init();
        animate();

        function init() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            clock = new THREE.Clock();

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            
            const light = new THREE.HemisphereLight(0xffffff, 0x444444, 1);
            scene.add(light);

            // YER (Kənd ərazisi)
            const ground = new THREE.Mesh(
                new THREE.PlaneGeometry(1000, 1000),
                new THREE.MeshPhongMaterial({ color: 0x228B22 })
            );
            ground.rotation.x = -Math.PI / 2;
            scene.add(ground);

            // --- PİŞİK MODELİ (Ayaq üstə duran) ---
            player = new THREE.Group();
            
            // Qarın və Bel (Dik dayanması üçün)
            const body = new THREE.Mesh(new THREE.BoxGeometry(1.2, 2.2, 1.2), new THREE.MeshPhongMaterial({color: 0xFFA500}));
            body.position.y = 1.6;
            player.add(body);

            // Baş
            const head = new THREE.Mesh(new THREE.BoxGeometry(1.3, 1.3, 1.3), new THREE.MeshPhongMaterial({color: 0xFFA500}));
            head.position.set(0, 3.2, 0);
            player.add(head);

            // Caynaqlı Əllər və Ayaqlar
            const limbGeo = new THREE.BoxGeometry(0.4, 1.2, 0.
