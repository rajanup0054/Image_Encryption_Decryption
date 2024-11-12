// Check if Three.js is loaded
if (THREE) {
    let scene, camera, renderer, particleSystem;

    function init() {
        // Create the scene and set the camera
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 5;

        // Set up renderer and attach it to the document
        renderer = new THREE.WebGLRenderer({ alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // Create a particle system
        const particles = new THREE.BufferGeometry();
        const particleCount = 1000;
        const particlePositions = [];

        for (let i = 0; i < particleCount; i++) {
            const x = (Math.random() - 0.5) * 10;
            const y = (Math.random() - 0.5) * 10;
            const z = (Math.random() - 0.5) * 10;
            particlePositions.push(x, y, z);
        }

        particles.setAttribute('position', new THREE.Float32BufferAttribute(particlePositions, 3));

        const particleMaterial = new THREE.PointsMaterial({
            color: 0x888888,
            size: 0.05,
            opacity: 0.8,
            transparent: true,
        });

        particleSystem = new THREE.Points(particles, particleMaterial);
        scene.add(particleSystem);

        // Adjust for window resizing
        window.addEventListener('resize', onWindowResize, false);

        // Start the animation loop
        animate();
    }

    function animate() {
        // Rotate the particle system slightly
        particleSystem.rotation.y += 0.002;
        particleSystem.rotation.x += 0.001;

        // Render the scene
        renderer.render(scene, camera);
        requestAnimationFrame(animate);
    }

    function onWindowResize() {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }

    // Initialize on window load
    window.onload = init;
} else {
    console.error("Three.js not found.");
}
