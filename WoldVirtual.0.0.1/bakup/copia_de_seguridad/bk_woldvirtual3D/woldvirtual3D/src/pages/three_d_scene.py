"""
Página de Escena 3D de Wold Virtual 3D
Página principal para la experiencia 3D interactiva
"""

from reflex import html, link, script
from components import Header, Footer, Navigation, Container, Button, Scene3D, Object3D, Camera3D, Light3D


def ThreeDScenePage():
    """Página de escena 3D interactiva"""
    
    # Datos de navegación
    nav_items = [
        {"text": "Inicio", "url": "/"},
        {"text": "Escena 3D", "url": "/3d-scene"},
        {"text": "Acerca de", "url": "/about"},
        {"text": "Dashboard", "url": "/dashboard"}
    ]
    
    # Controles de la escena
    scene_controls = [
        {"name": "Rotar", "description": "Click y arrastrar para rotar la vista"},
        {"name": "Zoom", "description": "Rueda del mouse para acercar/alejar"},
        {"name": "Pan", "description": "Click derecho y arrastrar para mover"},
        {"name": "Reset", "description": "Doble click para resetear la vista"}
    ]
    
    return html.div(
        # Encabezado
        Header.main(
            title="Escena 3D Interactiva",
            subtitle="Explora y experimenta con el mundo virtual",
            actions=[
                Button.primary("Nueva Escena", on_click="createNewScene()"),
                Button.secondary("Guardar", on_click="saveScene()")
            ]
        ),
        
        # Navegación
        Navigation.main(
            items=nav_items,
            active_item="/3d-scene"
        ),
        
        # Contenido principal
        Container.fluid([
            # Panel de controles lateral
            html.aside(
                html.div(
                    html.h3(
                        "Controles",
                        class_name="text-lg font-semibold text-gray-900 mb-4"
                    ),
                    html.div(
                        [
                            html.div(
                                html.div(
                                    html.h4(
                                        control["name"],
                                        class_name="font-medium text-gray-900"
                                    ),
                                    html.p(
                                        control["description"],
                                        class_name="text-sm text-gray-600"
                                    ),
                                    class_name="mb-3"
                                ) for control in scene_controls
                            ],
                            class_name="space-y-4"
                        ),
                        class_name="mb-6"
                    ),
                    
                    html.h3(
                        "Objetos",
                        class_name="text-lg font-semibold text-gray-900 mb-4"
                    ),
                    html.div(
                        [
                            Button.secondary("Agregar Cubo", on_click="addCube()", size="small"),
                            Button.secondary("Agregar Esfera", on_click="addSphere()", size="small"),
                            Button.secondary("Agregar Plano", on_click="addPlane()", size="small")
                        ],
                        class_name="space-y-2"
                    ),
                    
                    html.h3(
                        "Luces",
                        class_name="text-lg font-semibold text-gray-900 mb-4 mt-6"
                    ),
                    html.div(
                        [
                            Button.secondary("Luz Ambiental", on_click="toggleAmbientLight()", size="small"),
                            Button.secondary("Luz Direccional", on_click="toggleDirectionalLight()", size="small"),
                            Button.secondary("Luz Puntual", on_click="togglePointLight()", size="small")
                        ],
                        class_name="space-y-2"
                    ),
                    
                    html.h3(
                        "Configuración",
                        class_name="text-lg font-semibold text-gray-900 mb-4 mt-6"
                    ),
                    html.div(
                        [
                            html.div(
                                html.label(
                                    "FOV",
                                    class_name="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                html.input(
                                    type="range",
                                    min="30",
                                    max="120",
                                    value="75",
                                    on_change="updateFOV(this.value)",
                                    class_name="w-full"
                                ),
                                class_name="mb-4"
                            ),
                            html.div(
                                html.label(
                                    "Velocidad de Rotación",
                                    class_name="block text-sm font-medium text-gray-700 mb-1"
                                ),
                                html.input(
                                    type="range",
                                    min="0",
                                    max="2",
                                    step="0.1",
                                    value="0.01",
                                    on_change="updateRotationSpeed(this.value)",
                                    class_name="w-full"
                                ),
                                class_name="mb-4"
                            )
                        ],
                        class_name="space-y-4"
                    ),
                    class_name="p-6"
                ),
                class_name="w-80 bg-white border-r border-gray-200 h-screen overflow-y-auto"
            ),
            
            # Área principal de la escena 3D
            html.main(
                html.div(
                    # Escena 3D principal
                    Scene3D.interactive(
                        scene_id="main-scene",
                        controls=True,
                        lights=True,
                        class_name="w-full h-full"
                    ),
                    
                    # Overlay de información
                    html.div(
                        html.div(
                            html.h3(
                                "Información de la Escena",
                                class_name="text-lg font-semibold text-white mb-2"
                            ),
                            html.div(
                                [
                                    html.p(
                                        "Objetos: ",
                                        html.span("3", id="object-count", class_name="font-bold"),
                                        class_name="text-white text-sm"
                                    ),
                                    html.p(
                                        "FPS: ",
                                        html.span("60", id="fps-counter", class_name="font-bold"),
                                        class_name="text-white text-sm"
                                    ),
                                    html.p(
                                        "Memoria: ",
                                        html.span("45MB", id="memory-usage", class_name="font-bold"),
                                        class_name="text-white text-sm"
                                    )
                                ],
                                class_name="space-y-1"
                            ),
                            class_name="p-4"
                        ),
                        class_name="absolute top-4 right-4 bg-black bg-opacity-50 rounded-lg"
                    ),
                    
                    # Controles flotantes
                    html.div(
                        html.div(
                            [
                                Button.primary("🎮", on_click="toggleVR()", size="small"),
                                Button.secondary("📷", on_click="takeScreenshot()", size="small"),
                                Button.secondary("🎬", on_click="startRecording()", size="small")
                            ],
                            class_name="flex space-x-2"
                        ),
                        class_name="absolute bottom-4 left-4"
                    ),
                    
                    class_name="relative w-full h-full"
                ),
                class_name="flex-1 h-screen"
            )
        ], padding="p-0"),
        
        # Scripts de Three.js
        script(src="/static/js/three.min.js"),
        script(src="/static/js/OrbitControls.js"),
        script(src="/static/js/three-scene.js"),
        
        # Script personalizado para la página
        script("""
            // Variables globales de la escena
            let scene, camera, renderer, controls;
            let objects = [];
            let lights = [];
            let animationId;
            
            // Inicialización de la escena
            function initScene() {
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
                document.getElementById('main-scene').appendChild(renderer.domElement);
                
                // Crear controles
                controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;
                
                // Agregar luces por defecto
                addDefaultLights();
                
                // Agregar objetos por defecto
                addDefaultObjects();
                
                // Iniciar animación
                animate();
                
                // Event listeners
                window.addEventListener('resize', onWindowResize);
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
                        object.rotation.x += 0.01;
                        object.rotation.y += 0.01;
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
                document.getElementById('object-count').textContent = objects.length;
            }
            
            function updateFPS() {
                // Simulación de FPS
                const fps = Math.floor(60 + Math.random() * 10);
                document.getElementById('fps-counter').textContent = fps;
            }
            
            function onWindowResize() {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            }
            
            // Inicializar cuando se carga la página
            window.addEventListener('load', initScene);
        """),
        
        # Metadatos
        link(rel="stylesheet", href="/static/css/tailwind.css"),
        class_name="min-h-screen bg-gray-900"
    ) 