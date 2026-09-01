import os
import json
import random
import shutil
import math

root_dir = '/Users/drb_laptop/Documents/AIRI_to_AIR/OSD615-glycome-cytoskeleton-systems-biology'
docs = os.path.join(root_dir, 'docs')
for d in ['css', 'js', 'data', 'cose']:
    os.makedirs(os.path.join(docs, d), exist_ok=True)

# Copy branding assets
src_logo_1 = '/Users/drb_laptop/Documents/AIRI_to_AIR/docs/cose/cose-logo.png'
src_logo_2 = '/Users/drb_laptop/Documents/AIRI_to_AIR/docs/cose/regolith-logo.png'
if os.path.exists(src_logo_1):
    shutil.copy(src_logo_1, os.path.join(docs, 'cose/cose-logo.png'))
if os.path.exists(src_logo_2):
    shutil.copy(src_logo_2, os.path.join(docs, 'cose/regolith-logo.png'))

def w(path, content):
    with open(os.path.join(docs, path), 'w') as f:
        f.write(content.strip())

# CSS
w('css/style.css', '''
:root { 
    --bg: #ffffff; --text: #333333; --navy: #2F5985; --teal: #3FB6A8; --coral: #E85D50; --border: #dddddd; --panel-bg: #f9f9f9;
}
[data-theme='dark'] { 
    --bg: #121212; --text: #eeeeee; --navy: #1a3a5c; --teal: #3FB6A8; --coral: #E85D50; --border: #333333; --panel-bg: #1e1e1e;
}
body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; background: var(--bg); color: var(--text); height: 100vh; overflow: hidden; }
.sidebar { width: 240px; background: var(--navy); color: white; display: flex; flex-direction: column; padding: 20px; box-sizing: border-box; overflow-y: auto; }
.sidebar img { max-width: 100%; filter: brightness(0) invert(1); margin-bottom: 20px; }
.nav-item { padding: 12px 15px; cursor: pointer; margin-bottom: 5px; border-radius: 6px; display: flex; align-items: center; gap: 10px; transition: background 0.2s; }
.nav-item:hover, .nav-item.active { background: var(--teal); }
.content { flex: 1; padding: 30px; box-sizing: border-box; overflow-y: auto; background: var(--bg); }
.tab-content { display: none; animation: fadeIn 0.3s ease; }
.tab-content.active { display: block; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px; margin-top: 20px; }
.card { background: var(--panel-bg); border-left: 4px solid var(--teal); padding: 20px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
#sim-canvas { background: #000; border: 1px solid var(--border); width: 100%; max-width: 800px; height: 500px; border-radius: 8px; }
button { background: var(--teal); color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; }
button:hover { filter: brightness(1.1); }
.control-panel { background: var(--panel-bg); padding: 15px; border-radius: 8px; margin-bottom: 20px; display: flex; gap: 20px; flex-wrap: wrap; align-items: center; }
''')

# HTML
w('index.html', '''<!DOCTYPE html>
<html data-theme="dark">
<head>
    <meta charset="UTF-8">
    <title>OSD-615 Systems Biology Dashboard</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
    <div class="sidebar">
        <img src="cose/cose-logo.png" alt="CoSE Branding">
        <h3 style="margin-top:0">OSD-615 Explorer</h3>
        <div class="nav-item active" data-tab="tab-1">📊 Overview</div>
        <div class="nav-item" data-tab="tab-2">🔬 Glycomics</div>
        <div class="nav-item" data-tab="tab-3">📈 Differential Analysis</div>
        <div class="nav-item" data-tab="tab-4">🔗 Multi-Omics</div>
        <div class="nav-item" data-tab="tab-5">🕸 Network Viewer</div>
        <div class="nav-item" data-tab="tab-6">🗺 Pathways</div>
        <div class="nav-item" data-tab="tab-7">🚚 Transport Simulator</div>
        <div class="nav-item" data-tab="tab-8">⚙️ MS Workflow</div>
        <div class="nav-item" data-tab="tab-9">🌱 VEGGIE Studies</div>
        <div class="nav-item" data-tab="tab-10">📄 Manuscript</div>
        <div style="flex:1"></div>
        <button id="theme-toggle" style="width:100%; background:var(--navy); border:1px solid var(--teal);">Toggle Theme</button>
        <div style="font-size: 0.8em; margin-top: 20px; text-align: center; color: #aaa;">NASA OSDR Data</div>
    </div>
    <div class="content">
        <div id="tab-1" class="tab-content active">
            <h1>OSD-615: Glycome-Cytoskeleton Systems Biology</h1>
            <p>Interactive dashboard for analyzing the effects of microgravity on plant cell wall remodeling and vesicular transport.</p>
            <div class="card-grid">
                <div class="card"><h3>Xyloglucan Remodeling</h3><p>Spaceflight increases specific xyloglucan epitopes.</p></div>
                <div class="card"><h3>Accelerated Sec. Wall</h3><p>Early deposition of secondary cell wall components.</p></div>
                <div class="card"><h3>AGP Redistribution</h3><p>Arabinogalactan proteins altered in microgravity.</p></div>
                <div class="card"><h3>Cytoskeletal Correlation</h3><p>Strong link between MT organization and secretion.</p></div>
            </div>
        </div>
        <div id="tab-2" class="tab-content">
            <h2>Glycomics Explorer</h2>
            <div class="control-panel">
                <label><input type="checkbox" checked> Show Xyloglucans</label>
                <label><input type="checkbox" checked> Show Pectins</label>
            </div>
            <div id="heatmap" style="height:700px; width:100%;"></div>
        </div>
        <div id="tab-3" class="tab-content">
            <h2>Differential Analysis</h2>
            <div style="display:flex; gap:20px;">
                <div id="volcano" style="flex:1; height:500px;"></div>
                <div id="bar-chart" style="flex:1; height:500px;"></div>
            </div>
        </div>
        <div id="tab-4" class="tab-content">
            <h2>Multi-Omics Integration</h2>
            <div id="circle-plot" style="height:600px;"></div>
        </div>
        <div id="tab-5" class="tab-content">
            <h2>Cytoskeleton-Cell Wall Network Viewer</h2>
            <div id="cy" style="height:700px; border:1px solid var(--border); background: var(--panel-bg); border-radius: 8px;"></div>
        </div>
        <div id="tab-6" class="tab-content">
            <h2>Pathway Diagrams</h2>
            <div class="control-panel">
                <button>Golgi Transport</button> <button>MT Array</button> <button>O-GlcNAcylation</button>
            </div>
            <svg width="100%" height="500" style="background:var(--panel-bg); border-radius:8px;">
                <text x="50" y="50" fill="var(--text)" font-size="20">Interactive SVG Pathway Viewer (Placeholder)</text>
                <rect x="50" y="100" width="150" height="80" rx="10" fill="var(--teal)" />
                <text x="70" y="145" fill="white">Golgi Body</text>
                <line x1="200" y1="140" x2="350" y2="140" stroke="var(--coral)" stroke-width="4" marker-end="url(#arrow)" />
            </svg>
        </div>
        <div id="tab-7" class="tab-content">
            <h2>Interactive Vesicle Transport Simulator</h2>
            <div class="control-panel">
                <button id="sim-ground" style="background:#4CAF50">1g Ground Preset</button>
                <button id="sim-micro" style="background:#2196F3">0g Microgravity Preset</button>
                <span style="margin: 0 10px;">|</span>
                <label>Motors: <input type="range" id="sim-motors" min="1" max="50" value="20"></label>
                <label>Gravity: <input type="range" id="sim-gravity" min="0" max="1" step="0.1" value="1.0"></label>
                <span style="margin: 0 10px;">|</span>
                <button id="sim-start">Start</button>
                <button id="sim-stop" style="background:#F44336">Stop</button>
            </div>
            <canvas id="sim-canvas" width="800" height="500"></canvas>
            <div class="card-grid" style="max-width: 800px">
                <div class="card"><h3>Mean Velocity</h3><p id="stat-vel">0.0 µm/s</p></div>
                <div class="card"><h3>Delivery Rate</h3><p id="stat-del">0 vesicles/s</p></div>
            </div>
        </div>
        <div id="tab-8" class="tab-content">
            <h2>Mass Spectrometry Workflow</h2>
            <div class="control-panel">
                <button>Workflow A</button> <button>Workflow B</button> <button>Workflow C</button>
            </div>
            <div class="card"><h3>Step 1: Cell Wall Extraction</h3><p>Sequential extraction of AIR using CDTA, Na2CO3, and KOH.</p></div>
        </div>
        <div id="tab-9" class="tab-content">
            <h2>VEGGIE OSDR Study Explorer</h2>
            <div style="overflow-x:auto;">
                <table id="veggie-table" style="width:100%; border-collapse: collapse; text-align: left;"></table>
            </div>
        </div>
        <div id="tab-10" class="tab-content">
            <h2>Manuscript & Exports</h2>
            <div class="card" style="text-align:center; padding: 50px;">
                <h3>Manuscript.pdf</h3>
                <p>Embedded PDF viewer placeholder.</p>
                <button>Download PDF</button> <button>Download DOCX</button>
            </div>
        </div>
    </div>
    <script type="module" src="js/app.js"></script>
</body>
</html>''')

# JS App
w('js/app.js', '''
import './glycomics-heatmap.js';
import './charts.js';
import './multiomics-integration.js';
import './network-viewer.js';
import './transport-simulator.js';
import './veggie-study-explorer.js';

document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', e => {
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
        e.currentTarget.classList.add('active');
        const tabId = e.currentTarget.getAttribute('data-tab');
        document.getElementById(tabId).classList.add('active');
        window.dispatchEvent(new Event('resize'));
    });
});

const themeToggle = document.getElementById('theme-toggle');
themeToggle.addEventListener('click', () => {
    const html = document.documentElement;
    html.dataset.theme = html.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', html.dataset.theme);
});
if(localStorage.getItem('theme')) document.documentElement.dataset.theme = localStorage.getItem('theme');
''')

# JS Heatmap
w('js/glycomics-heatmap.js', '''
fetch('data/glycomics_heatmap.json').then(r => r.json()).then(data => {
    const layout = { title: 'Glycome Profiling (155 mAbs)', margin: {l: 150}, paper_bgcolor: 'transparent', font: {color: 'var(--text)'} };
    Plotly.newPlot('heatmap', [{ z: data.z, x: data.x, y: data.y, type: 'heatmap', colorscale: 'Viridis' }], layout);
});
''')

# JS Charts
w('js/charts.js', '''
fetch('data/differential_results.json').then(r => r.json()).then(data => {
    const layout = { title: 'Space vs Ground (Volcano)', paper_bgcolor: 'transparent', font: {color: 'var(--text)'} };
    Plotly.newPlot('volcano', [{ x: data.volcano.map(d=>d.logFC), y: data.volcano.map(d=>-Math.log10(d.pval)), mode: 'markers', text: data.volcano.map(d=>d.id), type: 'scatter', marker: {color: 'var(--teal)'} }], layout);
    
    Plotly.newPlot('bar-chart', [{ x: ['Xyloglucan', 'Pectin', 'AGP', 'Xylan'], y: [1.2, -0.5, 0.8, 1.5], type: 'bar', marker: {color: 'var(--coral)'} }], { title: 'Class Enrichment', paper_bgcolor: 'transparent', font: {color: 'var(--text)'} });
});
''')

# JS Multiomics
w('js/multiomics-integration.js', '''
fetch('data/integration_results.json').then(r => r.json()).then(data => {
    const layout = { title: 'sPLS Correlation Circle', paper_bgcolor: 'transparent', font: {color: 'var(--text)'}, shapes: [{type: 'circle', x0: -1, y0: -1, x1: 1, y1: 1, line: {color: 'var(--border)'}}] };
    Plotly.newPlot('circle-plot', [{ x: data.correlations.map(d=>d.x), y: data.correlations.map(d=>d.y), mode: 'markers+text', text: data.correlations.map(d=>d.label), type: 'scatter' }], layout);
});
''')

# JS Network
w('js/network-viewer.js', '''
fetch('data/network_graph.json').then(r => r.json()).then(data => {
    cytoscape({
        container: document.getElementById('cy'),
        elements: data.elements,
        style: [
            { selector: 'node', style: { 'label': 'data(id)', 'background-color': 'var(--teal)', 'color': 'var(--text)', 'text-valign': 'center' } },
            { selector: 'edge', style: { 'width': 'data(score)', 'line-color': 'var(--coral)', 'opacity': 0.6 } }
        ],
        layout: { name: 'cose', padding: 30 }
    });
});
''')

# JS Simulator (The complex part)
w('js/transport-simulator.js', '''
const canvas = document.getElementById('sim-canvas');
const ctx = canvas.getContext('2d');
let running = false;
let vesicles = [];
let gravityVal = 1.0;
let deliveryCount = 0;
let startTime = 0;

function initSim() {
    const motorCount = parseInt(document.getElementById('sim-motors').value);
    gravityVal = parseFloat(document.getElementById('sim-gravity').value);
    vesicles = Array.from({length: motorCount}, () => ({
        x: Math.random() * canvas.width * 0.2,
        y: Math.random() * canvas.height,
        vx: 2 + Math.random(),
        vy: (Math.random() - 0.5) * 2,
        state: 'attached'
    }));
    deliveryCount = 0;
    startTime = performance.now();
}

function loop() {
    if(!running) return;
    
    // Draw background and tracks
    ctx.fillStyle = 'rgba(0,0,0,0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.strokeStyle = '#440000'; ctx.lineWidth = 1;
    for(let i=0; i<canvas.height; i+=40) { ctx.beginPath(); ctx.moveTo(0, i); ctx.lineTo(canvas.width, i); ctx.stroke(); }
    
    ctx.strokeStyle = '#004400'; ctx.lineWidth = 2;
    for(let i=0; i<canvas.width; i+=40) { ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke(); }

    ctx.fillStyle = '#3FB6A8';
    let totalVel = 0;

    vesicles.forEach(v => {
        // Physics update
        v.x += v.vx;
        v.y += v.vy + (gravityVal * 0.5); // Gravity bias downwards
        
        // Boundaries and Delivery
        if(v.x > canvas.width) {
            v.x = 0; // Recycle to Golgi
            deliveryCount++;
        }
        if(v.y < 0) v.y = canvas.height;
        if(v.y > canvas.height) v.y = 0;
        
        totalVel += Math.sqrt(v.vx*v.vx + v.vy*v.vy);

        // Draw vesicle
        ctx.beginPath();
        ctx.arc(v.x, v.y, 6, 0, Math.PI*2);
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.stroke();
    });

    // Update stats
    const elapsed = (performance.now() - startTime) / 1000;
    document.getElementById('stat-vel').innerText = (totalVel / vesicles.length).toFixed(2) + ' µm/s';
    if(elapsed > 0) document.getElementById('stat-del').innerText = (deliveryCount / elapsed).toFixed(2) + ' vesicles/s';

    requestAnimationFrame(loop);
}

document.getElementById('sim-start').onclick = () => { if(!running){ running=true; startTime = performance.now(); loop(); }};
document.getElementById('sim-stop').onclick = () => { running=false; };
document.getElementById('sim-ground').onclick = () => { document.getElementById('sim-motors').value = 40; document.getElementById('sim-gravity').value = 1.0; initSim(); };
document.getElementById('sim-micro').onclick = () => { document.getElementById('sim-motors').value = 15; document.getElementById('sim-gravity').value = 0.0; initSim(); };
document.getElementById('sim-motors').oninput = initSim;
document.getElementById('sim-gravity').oninput = initSim;

initSim();
''')

# JS Veggie
w('js/veggie-study-explorer.js', '''
fetch('data/veggie_studies.json').then(r => r.json()).then(data => {
    const table = document.getElementById('veggie-table');
    let html = '<tr style="background:var(--navy); color:white;"><th>Accession</th><th>Title</th><th>Organism</th></tr>';
    data.forEach(d => {
        html += `<tr style="border-bottom:1px solid var(--border);">
            <td style="padding:10px;"><a href="#" style="color:var(--teal)">${d.Accession}</a></td>
            <td style="padding:10px;">${d.Title}</td>
            <td style="padding:10px;"><em>${d.Organism}</em></td>
        </tr>`;
    });
    table.innerHTML = html;
});
''')

# Generate Mock Data JSONs
data_dir = os.path.join(docs, 'data')
samples = ['R7_roots', 'R11_roots', 'R10_roots', 'R9_roots', 'R2_roots', 'R4_roots', 'R6_roots', 'R1_roots', 'R3_roots', 'R5_roots', 'R8_roots', 'R12_roots']
mabs = [f"CCRC-M{i}" for i in range(1, 156)]
glycan_classes = ["Xyloglucan", "Xylan", "AGP", "Pectin", "Cellulose"]

z = [[random.uniform(0, 10) for _ in samples] for _ in mabs]
g_classes = {m: random.choice(glycan_classes) for m in mabs}
meta = {s: {"spaceflight": "Space" if "R" in s else "Ground"} for s in samples}

with open(f'{data_dir}/glycomics_heatmap.json', 'w') as f:
    json.dump({"z": z, "x": samples, "y": mabs, "glycan_classes": g_classes, "metadata": meta}, f)

with open(f'{data_dir}/differential_results.json', 'w') as f:
    json.dump({"volcano": [{"id": m, "logFC": random.uniform(-2, 2), "pval": random.uniform(0.0001, 1), "class": g_classes[m]} for m in mabs]}, f)

nodes = [{"data": {"id": f"gene{i}", "gene_family": "Cytoskeleton", "score": random.uniform(0,1)}} for i in range(50)]
edges = [{"data": {"source": f"gene{random.randint(0,49)}", "target": f"gene{random.randint(0,49)}", "score": random.uniform(1, 5)}} for _ in range(120)]
with open(f'{data_dir}/network_graph.json', 'w') as f:
    json.dump({"elements": {"nodes": nodes, "edges": edges}}, f)

with open(f'{data_dir}/integration_results.json', 'w') as f:
    json.dump({"correlations": [{"x": random.uniform(-1, 1), "y": random.uniform(-1, 1), "label": m} for m in mabs]}, f)

with open(f'{data_dir}/veggie_studies.json', 'w') as f:
    json.dump([{"Accession": f"OSD-{i}", "Title": f"Spaceflight transcriptomics of Arabidopsis {i}", "Organism": "Arabidopsis thaliana"} for i in range(600, 620)], f)

print("Dashboard generation complete!")
