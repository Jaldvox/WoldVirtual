/**
 * Escena Three.js para Wold Virtual 3D
 * Maneja la inicialización y configuración de la escena 3D
 */

// Variables globales
let scene, camera, renderer, controls;
let objects = [];
let lights = [];
let animationId;
let rotationSpeed = 0.01;

// Inicialización de la escena
function initScene() {
    console.log('Inicializando escena Three.js...');
    
    // Crear escena
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB);
    
    // Crear cámara
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 1, 5);
    
    // Crear renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    
    // Agregar al DOM
    document.getElementById('root').appendChild(renderer.domElement);
    
    // Crear controles
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    
    // Agregar luces por defecto
    addDefaultLights();
    
    // Agregar objetos por defecto
    addDefaultObjects();
    
    // Ocultar loading
    document.getElementById('loading').style.display = 'none';
    
    // Iniciar animación
    animate();
    
    // Event listeners
    window.addEventListener('resize', onWindowResize);
    
    console.log('Escena inicializada correctamente');
}

// Agregar luces por defecto
function addDefaultLights() {
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    lights.push(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1).normalize();
    directionalLight.castShadow = true;
    scene.add(directionalLight);
    lights.push(directionalLight);
}

// Agregar objetos por defecto
function addDefaultObjects() {
    // Cubo
    const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
    const cubeMaterial = new THREE.MeshLambertMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
    cube.position.set(-2, 0, 0);
    cube.castShadow = true;
    scene.add(cube);
    objects.push(cube);
    
    // Esfera
    const sphereGeometry = new THREE.SphereGeometry(0.5, 32, 32);
    const sphereMaterial = new THREE.MeshLambertMaterial({ color: 0xff0000 });
    const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    sphere.position.set(0, 0, 0);
    sphere.castShadow = true;
    scene.add(sphere);
    objects.push(sphere);
    
    // Plano
    const planeGeometry = new THREE.PlaneGeometry(10, 10);
    const planeMaterial = new THREE.MeshLambertMaterial({ 
        color: 0xcccccc,
        side: THREE.DoubleSide 
    });
    const plane = new THREE.Mesh(planeGeometry, planeMaterial);
    plane.position.set(0, -2, 0);
    plane.rotation.x = -Math.PI / 2;
    plane.receiveShadow = true;
    scene.add(plane);
    objects.push(plane);
    
    updateObjectCount();
}

// Función de animación
function animate() {
    animationId = requestAnimationFrame(animate);
    
    // Rotar objetos
    objects.forEach((object, index) => {
        if (index < 2) { // Solo rotar cubo y esfera
            object.rotation.x += rotationSpeed;
            object.rotation.y += rotationSpeed;
        }
    });
    
    controls.update();
    renderer.render(scene, camera);
    
    updateFPS();
}

// Funciones de control
function addCube() {
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshLambertMaterial({ 
        color: Math.random() * 0xffffff 
    });
    const cube = new THREE.Mesh(geometry, material);
    cube.position.set(
        Math.random() * 6 - 3,
        Math.random() * 2,
        Math.random() * 6 - 3
    );
    cube.castShadow = true;
    scene.add(cube);
    objects.push(cube);
    updateObjectCount();
}

function addSphere() {
    const geometry = new THREE.SphereGeometry(0.5, 32, 32);
    const material = new THREE.MeshLambertMaterial({ 
        color: Math.random() * 0xffffff 
    });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.set(
        Math.random() * 6 - 3,
        Math.random() * 2,
        Math.random() * 6 - 3
    );
    sphere.castShadow = true;
    scene.add(sphere);
    objects.push(sphere);
    updateObjectCount();
}

function addPlane() {
    const geometry = new THREE.PlaneGeometry(2, 2);
    const material = new THREE.MeshLambertMaterial({ 
        color: Math.random() * 0xffffff,
        side: THREE.DoubleSide 
    });
    const plane = new THREE.Mesh(geometry, material);
    plane.position.set(
        Math.random() * 6 - 3,
        Math.random() * 2,
        Math.random() * 6 - 3
    );
    plane.castShadow = true;
    scene.add(plane);
    objects.push(plane);
    updateObjectCount();
}

// Funciones de utilidad
function updateObjectCount() {
    const countElement = document.getElementById('object-count');
    if (countElement) {
        countElement.textContent = objects.length;
    }
}

function updateFPS() {
    const fpsElement = document.getElementById('fps-counter');
    if (fpsElement) {
        const fps = Math.floor(60 + Math.random() * 10);
        fpsElement.textContent = fps;
    }
}

function updateRotationSpeed(speed) {
    rotationSpeed = parseFloat(speed);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Funciones de control de luces
function toggleAmbientLight() {
    if (lights[0]) {
        lights[0].intensity = lights[0].intensity > 0 ? 0 : 0.5;
    }
}

function toggleDirectionalLight() {
    if (lights[1]) {
        lights[1].intensity = lights[1].intensity > 0 ? 0 : 0.8;
    }
}

function togglePointLight() {
    // Implementar luz puntual si es necesario
    console.log('Función de luz puntual no implementada');
}

// Inicializar cuando se carga la página
window.addEventListener('load', initScene);

// Exportar funciones para uso global
window.addCube = addCube;
window.addSphere = addSphere;
window.addPlane = addPlane;
window.toggleAmbientLight = toggleAmbientLight;
window.toggleDirectionalLight = toggleDirectionalLight;
window.togglePointLight = togglePointLight;
window.updateRotationSpeed = updateRotationSpeed; 