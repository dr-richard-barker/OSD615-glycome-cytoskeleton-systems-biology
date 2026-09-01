// Interactive HTML5 Canvas Vesicle Transport Simulator

const canvas = document.getElementById('sim-canvas');
const ctx = canvas ? canvas.getContext('2d') : null;

let running = false;
let animId = null;
let vesicles = [];
let tracks = [];
let deliveryCount = 0;
let startTime = 0;

// Simulation parameters
let motorCount = 25;
let trackDensity = 0.85;
let gravityBias = 1.0;
let detachRate = 0.03;

function setupTracks() {
    tracks = [];
    if (!canvas) return;
    const spacing = Math.max(25, Math.floor(60 / trackDensity));

    // Longitudinal Actin cables (Red)
    for (let y = 30; y < canvas.height - 20; y += spacing) {
        tracks.push({
            type: 'actin',
            y: y,
            color: '#E85D50',
            direction: 1 // Left to right
        });
    }

    // Transverse Cortical Microtubules (Green)
    for (let x = 80; x < canvas.width - 60; x += spacing * 1.5) {
        tracks.push({
            type: 'microtubule',
            x: x,
            color: '#3FB6A8'
        });
    }
}

function initVesicles() {
    vesicles = [];
    if (!canvas) return;
    for (let i = 0; i < motorCount; i++) {
        vesicles.push({
            x: 20 + Math.random() * 50, // Originates near Golgi
            y: 30 + Math.random() * (canvas.height - 60),
            vx: 0.8 + Math.random() * 0.8,
            vy: (Math.random() - 0.5) * 0.4,
            attached: true,
            cargo: Math.random() > 0.5 ? 'xylan' : 'xyloglucan',
            radius: 5 + Math.random() * 2
        });
    }
    deliveryCount = 0;
    startTime = performance.now();
}

function updatePhysics() {
    let activeVels = 0;
    let stalledCount = 0;

    vesicles.forEach(v => {
        if (v.attached) {
            // Forward transport along actin cable
            v.x += v.vx * 1.5;
            // Slight vertical steering along MT lattice
            v.y += v.vy + (gravityBias * 0.15);

            activeVels += v.vx;

            // Check detachment probability (higher in microgravity / low track density)
            if (Math.random() < detachRate) {
                v.attached = false;
            }
        } else {
            // Detached: slow Brownian diffusion
            v.x += (Math.random() - 0.4) * 0.8;
            v.y += (Math.random() - 0.5) * 0.8 + (gravityBias * 0.2);
            stalledCount++;

            // Check reattachment to nearest track
            if (Math.random() < (trackDensity * 0.15)) {
                v.attached = true;
                v.vx = 0.8 + Math.random() * 0.8;
            }
        }

        // Boundary conditions: Wall delivery target at x = canvas.width - 40
        if (v.x >= canvas.width - 40) {
            deliveryCount++;
            // Recycle to Golgi stack
            v.x = 20 + Math.random() * 30;
            v.y = 30 + Math.random() * (canvas.height - 60);
            v.attached = true;
        }

        if (v.x < 10) v.x = 10;
        if (v.y < 20) v.y = 20;
        if (v.y > canvas.height - 20) v.y = canvas.height - 20;
    });

    // Update real-time stats
    const elapsedSec = (performance.now() - startTime) / 1000;
    const meanVel = vesicles.length > 0 ? (activeVels / vesicles.length) : 0;
    const deliveryRate = elapsedSec > 0 ? (deliveryCount / elapsedSec) : 0;

    const elVel = document.getElementById('stat-vel');
    const elDel = document.getElementById('stat-del');
    const elTot = document.getElementById('stat-total');
    const elStall = document.getElementById('stat-stalled');

    if (elVel) elVel.innerText = (meanVel * 0.85).toFixed(2) + ' µm/s';
    if (elDel) elDel.innerText = deliveryRate.toFixed(2) + ' /s';
    if (elTot) elTot.innerText = deliveryCount + ' vesicles';
    if (elStall) elStall.innerText = stalledCount;
}

function drawScene() {
    if (!ctx || !canvas) return;

    // Dark cellular interior
    ctx.fillStyle = '#0a0f1d';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw Golgi stack on left
    ctx.fillStyle = '#2F5985';
    ctx.fillRect(10, 20, 30, canvas.height - 40);
    ctx.fillStyle = '#ffffff';
    ctx.font = '10px sans-serif';
    ctx.fillText('GOLGI', 12, 15);

    // Draw Cell Wall / Cortex on right
    ctx.fillStyle = '#2A9D8F';
    ctx.fillRect(canvas.width - 35, 20, 25, canvas.height - 40);
    ctx.fillStyle = '#ffffff';
    ctx.fillText('WALL', canvas.width - 32, 15);

    // Draw Tracks
    tracks.forEach(tr => {
        if (tr.type === 'actin') {
            ctx.strokeStyle = 'rgba(232, 93, 80, 0.4)';
            ctx.lineWidth = 1.5;
            ctx.setLineDash([6, 4]);
            ctx.beginPath();
            ctx.moveTo(40, tr.y);
            ctx.lineTo(canvas.width - 40, tr.y);
            ctx.stroke();
        } else if (tr.type === 'microtubule') {
            ctx.strokeStyle = 'rgba(63, 182, 168, 0.35)';
            ctx.lineWidth = 2.5;
            ctx.setLineDash([]);
            ctx.beginPath();
            ctx.moveTo(tr.x, 20);
            ctx.lineTo(tr.x, canvas.height - 20);
            ctx.stroke();
        }
    });
    ctx.setLineDash([]);

    // Draw Vesicles
    vesicles.forEach(v => {
        ctx.beginPath();
        ctx.arc(v.x, v.y, v.radius, 0, Math.PI * 2);
        
        if (v.attached) {
            ctx.fillStyle = v.cargo === 'xylan' ? '#3FB6A8' : '#F4A261';
            ctx.fill();
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1.5;
            ctx.stroke();
        } else {
            // Diffusing / stalled vesicle (dimmer, red outline)
            ctx.fillStyle = 'rgba(100, 116, 139, 0.6)';
            ctx.fill();
            ctx.strokeStyle = '#E85D50';
            ctx.lineWidth = 1;
            ctx.stroke();
        }
    });
}

function simLoop() {
    if (!running) return;
    updatePhysics();
    drawScene();
    animId = requestAnimationFrame(simLoop);
}

export function initTransportSimulator() {
    if (!canvas) return;

    setupTracks();
    initVesicles();
    drawScene();

    // Event handlers
    const btnStart = document.getElementById('sim-start');
    const btnStop = document.getElementById('sim-stop');
    const btnGround = document.getElementById('sim-ground');
    const btnMicro = document.getElementById('sim-micro');
    const sliderMotors = document.getElementById('sim-motors');
    const sliderDensity = document.getElementById('sim-density');
    const sliderGravity = document.getElementById('sim-gravity');

    if (btnStart) {
        btnStart.addEventListener('click', () => {
            if (!running) {
                running = true;
                startTime = performance.now();
                simLoop();
            }
        });
    }

    if (btnStop) {
        btnStop.addEventListener('click', () => {
            running = false;
            if (animId) cancelAnimationFrame(animId);
        });
    }

    if (btnGround) {
        btnGround.addEventListener('click', () => {
            motorCount = 30;
            trackDensity = 0.85;
            gravityBias = 1.0;
            detachRate = 0.03;

            if (sliderMotors) sliderMotors.value = 30;
            if (sliderDensity) sliderDensity.value = 0.85;
            if (sliderGravity) sliderGravity.value = 1.0;

            document.getElementById('val-motors').innerText = '30';
            document.getElementById('val-density').innerText = '0.85';
            document.getElementById('val-gravity').innerText = '1.0g';

            setupTracks();
            initVesicles();
            drawScene();
        });
    }

    if (btnMicro) {
        btnMicro.addEventListener('click', () => {
            motorCount = 14;
            trackDensity = 0.45;
            gravityBias = 0.0;
            detachRate = 0.08;

            if (sliderMotors) sliderMotors.value = 14;
            if (sliderDensity) sliderDensity.value = 0.45;
            if (sliderGravity) sliderGravity.value = 0.0;

            document.getElementById('val-motors').innerText = '14';
            document.getElementById('val-density').innerText = '0.45';
            document.getElementById('val-gravity').innerText = '0.0g';

            setupTracks();
            initVesicles();
            drawScene();
        });
    }

    if (sliderMotors) {
        sliderMotors.addEventListener('input', e => {
            motorCount = parseInt(e.target.value);
            document.getElementById('val-motors').innerText = motorCount;
            initVesicles();
            drawScene();
        });
    }

    if (sliderDensity) {
        sliderDensity.addEventListener('input', e => {
            trackDensity = parseFloat(e.target.value);
            document.getElementById('val-density').innerText = trackDensity.toFixed(2);
            setupTracks();
            drawScene();
        });
    }

    if (sliderGravity) {
        sliderGravity.addEventListener('input', e => {
            gravityBias = parseFloat(e.target.value);
            document.getElementById('val-gravity').innerText = gravityBias.toFixed(1) + 'g';
        });
    }
}

// Auto init
initTransportSimulator();