function createScene() {
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB); // Light blue background

    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    // Add directional light
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(1, 1, 1).normalize();
    scene.add(directionalLight);

    return scene;
}

export { createScene };