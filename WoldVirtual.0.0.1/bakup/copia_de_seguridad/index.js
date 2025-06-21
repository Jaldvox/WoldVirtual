// Crear la escena
const scene = new THREE.Scene();

// Crear la cámara
const camera = new THREE.PerspectiveCamera(
    75,                                    // Campo de visión
    window.innerWidth / window.innerHeight, // Aspecto
    0.1,                                   // Plano cercano
    1000                                   // Plano lejano
);

// Crear el renderizador
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Crear un cubo de ejemplo
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// Posicionar la cámara
camera.position.z = 5;

// Función de animación
function animate() {
    requestAnimationFrame(animate);
    
    // Rotar el cubo
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
    
    // Renderizar la escena
    renderer.render(scene, camera);
}

// Manejar redimensionamiento de ventana
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Iniciar la animación
animate();