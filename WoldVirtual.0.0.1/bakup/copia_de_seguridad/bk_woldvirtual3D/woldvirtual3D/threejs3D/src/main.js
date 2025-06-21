import * as THREE from 'three';
import { createScene } from './scene';
import { createCamera } from './camera';
import { createRenderer } from './renderer';
import { createCube } from './objects/cube';

let scene = createScene();
let camera = createCamera();
let renderer = createRenderer();

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

animate();