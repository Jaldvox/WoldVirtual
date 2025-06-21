/**
 * Archivo principal de JavaScript para Wold Virtual 3D
 * Maneja la interfaz de usuario y la interacción con la escena 3D
 */

// Variables globales de la interfaz
let isVRMode = false;
let isRecording = false;

// Inicialización de la interfaz
function initInterface() {
    console.log('Inicializando interfaz de usuario...');
    
    // Crear controles de la interfaz
    createControls();
    
    // Crear información de la escena
    createSceneInfo();
    
    // Crear controles flotantes
    createFloatingControls();
    
    console.log('Interfaz inicializada correctamente');
}

// Crear controles de la interfaz
function createControls() {
    const controlsDiv = document.createElement('div');
    controlsDiv.className = 'controls';
    controlsDiv.innerHTML = `
        <h3>Controles</h3>
        <div>
            <h4>Rotar</h4>
            <p>Click y arrastrar para rotar la vista</p>
        </div>
        <div>
            <h4>Zoom</h4>
            <p>Rueda del mouse para acercar/alejar</p>
        </div>
        <div>
            <h4>Pan</h4>
            <p>Click derecho y arrastrar para mover</p>
        </div>
        <div>
            <h4>Reset</h4>
            <p>Doble click para resetear la vista</p>
        </div>
        
        <h3>Objetos</h3>
        <button onclick="addCube()">Agregar Cubo</button>
        <button onclick="addSphere()">Agregar Esfera</button>
        <button onclick="addPlane()">Agregar Plano</button>
        
        <h3>Luces</h3>
        <button onclick="toggleAmbientLight()">Luz Ambiental</button>
        <button onclick="toggleDirectionalLight()">Luz Direccional</button>
        <button onclick="togglePointLight()">Luz Puntual</button>
        
        <h3>Configuración</h3>
        <label>FOV</label>
        <input type="range" min="30" max="120" value="75" onchange="updateFOV(this.value)">
        
        <label>Velocidad de Rotación</label>
        <input type="range" min="0" max="2" step="0.1" value="0.01" onchange="updateRotationSpeed(this.value)">
    `;
    
    document.getElementById('root').appendChild(controlsDiv);
}

// Crear información de la escena
function createSceneInfo() {
    const infoDiv = document.createElement('div');
    infoDiv.className = 'scene-info';
    infoDiv.innerHTML = `
        <h3>Información de la Escena</h3>
        <p>Objetos: <span id="object-count" class="font-bold">3</span></p>
        <p>FPS: <span id="fps-counter" class="font-bold">60</span></p>
        <p>Memoria: <span id="memory-usage" class="font-bold">45MB</span></p>
    `;
    
    document.getElementById('root').appendChild(infoDiv);
}

// Crear controles flotantes
function createFloatingControls() {
    const floatingDiv = document.createElement('div');
    floatingDiv.style.position = 'absolute';
    floatingDiv.style.bottom = '20px';
    floatingDiv.style.left = '20px';
    floatingDiv.style.zIndex = '100';
    
    floatingDiv.innerHTML = `
        <button onclick="toggleVR()" style="margin-right: 10px; padding: 10px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">🎮</button>
        <button onclick="takeScreenshot()" style="margin-right: 10px; padding: 10px; background: #2196F3; color: white; border: none; border-radius: 5px; cursor: pointer;">📷</button>
        <button onclick="startRecording()" style="padding: 10px; background: #f44336; color: white; border: none; border-radius: 5px; cursor: pointer;">🎬</button>
    `;
    
    document.getElementById('root').appendChild(floatingDiv);
}

// Funciones de control
function toggleVR() {
    isVRMode = !isVRMode;
    console.log('Modo VR:', isVRMode ? 'Activado' : 'Desactivado');
    
    if (isVRMode) {
        // Implementar funcionalidad VR
        alert('Modo VR activado (funcionalidad en desarrollo)');
    }
}

function takeScreenshot() {
    console.log('Tomando screenshot...');
    
    // Crear un enlace para descargar la imagen
    const link = document.createElement('a');
    link.download = 'wold-virtual-3d-screenshot.png';
    
    // Capturar el canvas
    renderer.domElement.toBlob(function(blob) {
        link.href = URL.createObjectURL(blob);
        link.click();
    });
}

function startRecording() {
    isRecording = !isRecording;
    console.log('Grabación:', isRecording ? 'Iniciada' : 'Detenida');
    
    if (isRecording) {
        alert('Grabación iniciada (funcionalidad en desarrollo)');
    } else {
        alert('Grabación detenida');
    }
}

function updateFOV(value) {
    if (camera) {
        camera.fov = parseFloat(value);
        camera.updateProjectionMatrix();
    }
}

// Función para actualizar el uso de memoria (simulación)
function updateMemoryUsage() {
    const memoryElement = document.getElementById('memory-usage');
    if (memoryElement) {
        const memory = Math.floor(40 + Math.random() * 20);
        memoryElement.textContent = memory + 'MB';
    }
}

// Inicializar la interfaz cuando se carga la página
window.addEventListener('load', function() {
    // Esperar un poco para que la escena se inicialice
    setTimeout(initInterface, 1000);
    
    // Actualizar memoria cada 5 segundos
    setInterval(updateMemoryUsage, 5000);
});

// Exportar funciones para uso global
window.toggleVR = toggleVR;
window.takeScreenshot = takeScreenshot;
window.startRecording = startRecording;
window.updateFOV = updateFOV; 