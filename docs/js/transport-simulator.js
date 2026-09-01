// Dual-Condition Plant Cell Vesicle Transport Simulator
// Simulates 1g Ground Control (Top Cell) vs 0g Microgravity (Bottom Cell)
// with authentic plant cell anatomy: Central Vacuole, Cytoplasmic Streaming Sleeve,
// Golgi/TGN Stacks, Layered Cell Walls, and Cytoskeletal Networks.

const canvas = document.getElementById('sim-canvas');
const ctx = canvas ? canvas.getContext('2d') : null;

let isRunning = false;
let animFrameId = null;
let motorCount = 28;

// Simulation State for 1g (Top) and 0g (Bottom)
class CellSimulation {
    constructor(isMicrogravity, yOffset, height) {
        this.isMicrogravity = isMicrogravity;
        this.yOffset = yOffset;
        this.height = height;
        this.width = canvas ? canvas.width : 850;
        
        // Physics constants
        this.trackDensity = isMicrogravity ? 0.45 : 0.85;
        this.detachRate = isMicrogravity ? 0.075 : 0.025;
        this.reattachRate = isMicrogravity ? 0.04 : 0.12;
        this.baseVel = isMicrogravity ? 1.0 : 1.4;
        
        this.vesicles = [];
        this.totalDelivered = 0;
        this.deliveryTimestamps = [];
        this.stalledCount = 0;
        this.meanVelocity = 0;
        
        // Plant cell geometry
        this.wallThickness = 18;
        this.vacuole = {
            x: 160,
            y: this.yOffset + 50,
            w: this.width - 320,
            h: this.height - 100,
            r: 25
        };
        
        this.initTracks();
        this.initVesicles();
    }
    
    initTracks() {
        this.tracks = [];
        const numTracks = Math.floor(6 * this.trackDensity);
        
        // Upper and lower subcortical actin channels around the central vacuole
        const channels = [
            { yMin: this.yOffset + 22, yMax: this.vacuole.y - 6 },
            { yMin: this.vacuole.y + this.vacuole.h + 6, yMax: this.yOffset + this.height - 22 }
        ];
        
        channels.forEach(ch => {
            const step = (ch.yMax - ch.yMin) / 3;
            for (let i = 0; i < 3; i++) {
                const y = ch.yMin + i * step + 4;
                this.tracks.push({
                    y: y,
                    type: 'actin',
                    wavy: this.isMicrogravity,
                    amp: this.isMicrogravity ? 3 + Math.random() * 4 : 0
                });
            }
        });
    }
    
    initVesicles() {
        this.vesicles = [];
        for (let i = 0; i < motorCount; i++) {
            this.spawnVesicle();
        }
        this.totalDelivered = 0;
        this.deliveryTimestamps = [];
    }
    
    spawnVesicle(v = null) {
        const isUpper = Math.random() > 0.5;
        const targetTrackY = isUpper 
            ? this.yOffset + 24 + Math.random() * (this.vacuole.y - this.yOffset - 30)
            : this.vacuole.y + this.vacuole.h + 8 + Math.random() * (this.yOffset + this.height - this.vacuole.y - this.vacuole.h - 30);
            
        const newV = v || {};
        newV.x = 45 + Math.random() * 50; // Golgi emission zone
        newV.y = targetTrackY;
        newV.targetY = targetTrackY;
        newV.vx = this.baseVel * (0.85 + Math.random() * 0.4);
        newV.vy = (Math.random() - 0.5) * 0.2;
        newV.attached = true;
        newV.cargo = Math.random() > 0.5 ? 'xylan' : 'xyloglucan';
        newV.radius = 4 + Math.random() * 2;
        newV.stallTimer = 0;
        newV.color = newV.cargo === 'xylan' ? '#F59E0B' : '#3FB6A8';
        
        if (!v) this.vesicles.push(newV);
        return newV;
    }
    
    update() {
        let activeVels = 0;
        let attachedCount = 0;
        let stalled = 0;
        const now = performance.now();
        
        // Clean delivery timestamps older than 5 seconds
        this.deliveryTimestamps = this.deliveryTimestamps.filter(t => now - t < 5000);
        
        this.vesicles.forEach(v => {
            if (v.attached) {
                v.x += v.vx;
                // Keep inside cytoplasmic sleeve around vacuole
                if (v.y > this.vacuole.y && v.y < this.vacuole.y + this.vacuole.h) {
                    if (v.y < this.vacuole.y + this.vacuole.h / 2) {
                        v.y -= 1.2;
                    } else {
                        v.y += 1.2;
                    }
                }
                
                // Microgravity wavy steering
                if (this.isMicrogravity) {
                    v.y += Math.sin(v.x * 0.05) * 0.4;
                }
                
                activeVels += v.vx;
                attachedCount++;
                
                // Stochastic detachment
                if (Math.random() < this.detachRate) {
                    v.attached = false;
                    v.stalled = true;
                }
            } else {
                // Detached Brownian diffusion (stalled)
                v.x += (Math.random() - 0.45) * 0.6;
                v.y += (Math.random() - 0.5) * 0.6;
                stalled++;
                v.stallTimer++;
                
                // Prevent entering central vacuole
                if (v.x > this.vacuole.x && v.x < this.vacuole.x + this.vacuole.w &&
                    v.y > this.vacuole.y && v.y < this.vacuole.y + this.vacuole.h) {
                    if (v.y < this.vacuole.y + this.vacuole.h / 2) {
                        v.y = this.vacuole.y - 4;
                    } else {
                        v.y = this.vacuole.y + this.vacuole.h + 4;
                    }
                }
                
                // Stochastic reattachment to actin track
                if (Math.random() < this.reattachRate) {
                    v.attached = true;
                    v.stalled = false;
                    v.vx = this.baseVel * (0.85 + Math.random() * 0.4);
                }
            }
            
            // Delivery to right plasma membrane / cell wall target
            if (v.x >= this.width - this.wallThickness - 20) {
                this.totalDelivered++;
                this.deliveryTimestamps.push(now);
                // Recycle back to Golgi
                this.spawnVesicle(v);
            }
        });
        
        this.stalledCount = stalled;
        this.meanVelocity = attachedCount > 0 ? (activeVels / attachedCount) : 0;
    }
    
    getDeliveryRate() {
        return (this.deliveryTimestamps.length / 5.0); // Delivered per second over 5s window
    }
    
    render(ctx) {
        ctx.save();
        
        // 1. Plant Cell Outer Wall (Greenish / Wood layered border)
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(8, this.yOffset + 6, this.width - 16, this.height - 12);
        
        // Primary and Secondary Cell Wall Layers (Right side thick wall deposition)
        ctx.fillStyle = this.isMicrogravity ? '#1e293b' : '#1e3a5f';
        ctx.fillRect(this.width - this.wallThickness - 14, this.yOffset + 8, this.wallThickness + 10, this.height - 16);
        
        // Cell Wall outer boundary
        ctx.strokeStyle = '#2F5985';
        ctx.lineWidth = 3;
        ctx.strokeRect(10, this.yOffset + 8, this.width - 20, this.height - 16);
        
        // Plasma Membrane (Inner glowing green boundary)
        ctx.strokeStyle = '#10B981';
        ctx.lineWidth = 1.5;
        ctx.strokeRect(18, this.yOffset + 14, this.width - 36, this.height - 28);
        
        // 2. Central Vacuole (Tonoplast) - Classic plant cell hallmark
        ctx.fillStyle = 'rgba(79, 70, 229, 0.15)';
        ctx.strokeStyle = 'rgba(129, 140, 248, 0.4)';
        ctx.lineWidth = 2;
        
        ctx.beginPath();
        const vx = this.vacuole.x, vy = this.vacuole.y, vw = this.vacuole.w, vh = this.vacuole.h, vr = this.vacuole.r;
        ctx.moveTo(vx + vr, vy);
        ctx.lineTo(vx + vw - vr, vy);
        ctx.quadraticCurveTo(vx + vw, vy, vx + vw, vy + vr);
        ctx.lineTo(vx + vw, vy + vh - vr);
        ctx.quadraticCurveTo(vx + vw, vy + vh, vx + vw - vr, vy + vh);
        ctx.lineTo(vx + vr, vy + vh);
        ctx.quadraticCurveTo(vx, vy + vh, vx, vy + vh - vr);
        ctx.lineTo(vx, vy + vr);
        ctx.quadraticCurveTo(vx, vy, vx + vr, vy);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        
        // Vacuole internal label
        ctx.fillStyle = 'rgba(199, 210, 254, 0.35)';
        ctx.font = 'bold 12px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('Central Vacuole (Tonoplast Barrier)', vx + vw / 2, vy + vh / 2);
        
        // 3. Golgi Stacks / Trans-Golgi Network (TGN) on Left
        ctx.strokeStyle = '#F59E0B';
        ctx.lineWidth = 3;
        for (let g = 0; g < 4; g++) {
            ctx.beginPath();
            ctx.arc(38 + g * 5, this.yOffset + this.height / 2, 28 - g * 3, -Math.PI / 3, Math.PI / 3);
            ctx.stroke();
        }
        ctx.fillStyle = '#F59E0B';
        ctx.font = '10px sans-serif';
        ctx.fillText('Golgi / TGN', 50, this.yOffset + this.height / 2 + 45);
        
        // 4. Cytoskeletal Tracks
        // Actin cables (Red/Coral)
        this.tracks.forEach(tr => {
            ctx.strokeStyle = tr.wavy ? 'rgba(232, 93, 80, 0.4)' : 'rgba(232, 93, 80, 0.7)';
            ctx.lineWidth = tr.wavy ? 1.5 : 2;
            ctx.beginPath();
            if (tr.wavy) {
                ctx.moveTo(70, tr.y);
                for (let x = 70; x < this.width - 35; x += 15) {
                    ctx.lineTo(x, tr.y + Math.sin(x * 0.1) * tr.amp);
                }
            } else {
                ctx.moveTo(70, tr.y);
                ctx.lineTo(this.width - 35, tr.y);
            }
            ctx.stroke();
        });
        
        // Transverse Cortical Microtubules (Teal)
        const mtSpacing = this.isMicrogravity ? 75 : 45;
        for (let mx = 120; mx < this.width - 45; mx += mtSpacing) {
            ctx.strokeStyle = this.isMicrogravity ? 'rgba(63, 182, 168, 0.25)' : 'rgba(63, 182, 168, 0.5)';
            ctx.lineWidth = 1.5;
            ctx.setLineDash(this.isMicrogravity ? [3, 4] : []);
            ctx.beginPath();
            ctx.moveTo(mx, this.yOffset + 16);
            ctx.lineTo(this.isMicrogravity ? mx + 15 : mx, this.yOffset + this.height - 16);
            ctx.stroke();
            ctx.setLineDash([]);
        }
        
        // 5. Vesicles
        this.vesicles.forEach(v => {
            ctx.beginPath();
            ctx.arc(v.x, v.y, v.radius, 0, Math.PI * 2);
            ctx.fillStyle = v.attached ? v.color : 'rgba(148, 163, 184, 0.7)';
            ctx.fill();
            
            if (v.attached) {
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1;
                ctx.stroke();
            } else {
                // Stalled pulse indicator
                ctx.strokeStyle = 'rgba(239, 68, 68, 0.8)';
                ctx.lineWidth = 1.5;
                ctx.stroke();
            }
        });
        
        // 6. Header Badge & Condition Label
        ctx.fillStyle = this.isMicrogravity ? '#E85D50' : '#3FB6A8';
        ctx.font = 'bold 13px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText(
            this.isMicrogravity ? '🚀 0g Microgravity (Bottom Cell: Disoriented Arrays, +200% Stalling, -28% Delivery)' 
                                : '🌱 1g Ground Control (Top Cell: Organized Subcortical Streaming Sleeve, High Flux)', 
            24, this.yOffset + 24
        );
        
        // Target Cell Wall Label on Right
        ctx.save();
        ctx.translate(this.width - 12, this.yOffset + this.height / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.fillStyle = '#94a3b8';
        ctx.font = 'bold 10px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('Target Cell Wall & Plasma Membrane', 0, 0);
        ctx.restore();
        
        ctx.restore();
    }
}

let groundSim = null;
let spaceSim = null;

function initSimulation() {
    if (!canvas) return;
    const cellHeight = 295;
    groundSim = new CellSimulation(false, 5, cellHeight);
    spaceSim = new CellSimulation(true, 315, cellHeight);
    updateStatsDisplay();
    render();
}

function updateStatsDisplay() {
    if (!groundSim || !spaceSim) return;
    
    // 1g Ground Stats
    const del1g = document.getElementById('stat-del-1g');
    const vel1g = document.getElementById('stat-vel-1g');
    const tot1g = document.getElementById('stat-tot-1g');
    const stall1g = document.getElementById('stat-stall-1g');
    
    if (del1g) del1g.innerText = `${groundSim.getDeliveryRate().toFixed(2)} /s`;
    if (vel1g) vel1g.innerText = `${groundSim.meanVelocity.toFixed(2)} µm/s`;
    if (tot1g) tot1g.innerText = `${groundSim.totalDelivered} vesicles`;
    if (stall1g) stall1g.innerText = groundSim.stalledCount;
    
    // 0g Space Stats
    const del0g = document.getElementById('stat-del-0g');
    const vel0g = document.getElementById('stat-vel-0g');
    const tot0g = document.getElementById('stat-tot-0g');
    const stall0g = document.getElementById('stat-stall-0g');
    
    if (del0g) del0g.innerText = `${spaceSim.getDeliveryRate().toFixed(2)} /s`;
    if (vel0g) vel0g.innerText = `${spaceSim.meanVelocity.toFixed(2)} µm/s`;
    if (tot0g) tot0g.innerText = `${spaceSim.totalDelivered} vesicles`;
    if (stall0g) stall0g.innerText = spaceSim.stalledCount;
}

function render() {
    if (!ctx || !canvas) return;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Divider bar between top and bottom cells
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 302, canvas.width, 10);
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1;
    ctx.strokeRect(0, 302, canvas.width, 10);
    
    if (groundSim) groundSim.render(ctx);
    if (spaceSim) spaceSim.render(ctx);
}

function loop() {
    if (!isRunning) return;
    
    if (groundSim) groundSim.update();
    if (spaceSim) spaceSim.update();
    
    render();
    updateStatsDisplay();
    
    animFrameId = requestAnimationFrame(loop);
}

function startSim() {
    if (isRunning) return;
    isRunning = true;
    loop();
}

function stopSim() {
    isRunning = false;
    if (animFrameId) {
        cancelAnimationFrame(animFrameId);
        animFrameId = null;
    }
}

function resetSim() {
    stopSim();
    initSimulation();
}

// Setup event listeners
function setupListeners() {
    const btnStart = document.getElementById('sim-start');
    const btnStop = document.getElementById('sim-stop');
    const btnReset = document.getElementById('sim-reset');
    const sliderMotors = document.getElementById('sim-motors');
    const valMotors = document.getElementById('val-motors');
    
    if (btnStart) btnStart.addEventListener('click', startSim);
    if (btnStop) btnStop.addEventListener('click', stopSim);
    if (btnReset) btnReset.addEventListener('click', resetSim);
    
    if (sliderMotors) {
        sliderMotors.addEventListener('input', e => {
            motorCount = parseInt(e.target.value);
            if (valMotors) valMotors.innerText = motorCount;
            resetSim();
            startSim();
        });
    }
}

// Initialize on load
setupListeners();
initSimulation();
startSim(); // Auto-start for immediate visual feedback