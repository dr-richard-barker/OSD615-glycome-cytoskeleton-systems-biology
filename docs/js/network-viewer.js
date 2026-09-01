// Cytoscape.js Network Viewer Module with Subcellular & Biochemical Details

let cyInstance = null;

export function initNetworkViewer() {
    const container = document.getElementById('cy');
    if (!container) return;

    fetch('data/network_graph.json')
        .then(r => r.json())
        .then(data => {
            const isDark = document.documentElement.dataset.theme === 'dark';
            const nodeLabelColor = isDark ? '#f1f5f9' : '#0f172a';

            cyInstance = cytoscape({
                container: container,
                elements: data.elements,
                style: [
                    {
                        selector: 'node',
                        style: {
                            'label': 'data(label)',
                            'background-color': 'data(color)',
                            'color': nodeLabelColor,
                            'font-size': '11px',
                            'font-weight': 'bold',
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'text-outline-width': 2,
                            'text-outline-color': isDark ? '#070d18' : '#ffffff',
                            'width': 44,
                            'height': 44,
                            'border-width': 2,
                            'border-color': '#ffffff'
                        }
                    },
                    {
                        selector: 'edge',
                        style: {
                            'width': 'mapData(score, 0.7, 1.0, 1.5, 4.5)',
                            'line-color': '#475569',
                            'curve-style': 'bezier',
                            'opacity': 0.75
                        }
                    },
                    {
                        selector: 'node:selected',
                        style: {
                            'border-width': 4,
                            'border-color': '#3FB6A8',
                            'width': 52,
                            'height': 52
                        }
                    }
                ],
                layout: {
                    name: 'cose',
                    idealEdgeLength: 85,
                    nodeOverlap: 20,
                    refresh: 20,
                    fit: true,
                    padding: 30,
                    randomize: false,
                    componentSpacing: 80,
                    nodeRepulsion: 400000,
                    edgeElasticity: 100,
                    nestingFactor: 5
                }
            });

            // Node click / tap handler -> Show full biochemical card
            cyInstance.on('tap', 'node', function(evt) {
                const d = evt.target.data();
                displayNodeDetails(d);
            });

            setupNetworkControls();
        })
        .catch(err => console.error('Error loading network graph:', err));
}

function displayNodeDetails(d) {
    const titleEl = document.getElementById('node-detail-title');
    const bodyEl = document.getElementById('node-detail-body');
    if (!titleEl || !bodyEl) return;

    const fcColor = d.log2fc > 0 ? '#E85D50' : '#3FB6A8';
    const fcSign = d.log2fc > 0 ? '+' : '';

    titleEl.innerHTML = `${d.label} <span style="font-size:0.85rem; color:#94a3b8; font-weight:normal;">[${d.ec_number || 'Structural / Motor'}]</span>`;
    
    bodyEl.innerHTML = `
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:12px; margin-top:8px;">
            <div>
                <p><strong>Subcellular Site of Action:</strong> <span class="badge">${d.compartment || 'Cytoplasm'}</span> ➔ <em>${d.subcellular_zone || 'Subcortical'}</em></p>
                <p style="margin-top:6px;"><strong>Catalytic Reaction / Function:</strong> ${d.reaction || 'Cytoskeletal organization'}</p>
                <p style="margin-top:6px;"><strong>Spaceflight Response:</strong> <strong style="color:${fcColor};">${fcSign}${d.log2fc.toFixed(2)} log2FC</strong> in spaceflight roots</p>
            </div>
            <div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:6px; border:1px solid rgba(255,255,255,0.06);">
                <p><strong>Donor / Required Substrates:</strong></p>
                <p style="color:#38bdf8; font-family:monospace; font-size:0.85rem; margin-bottom:6px;">${d.substrates || 'ATP / Cytoskeletal track'}</p>
                <p><strong>Products Made & Physiological Output:</strong></p>
                <p style="color:#3FB6A8; font-family:monospace; font-size:0.85rem;">${d.products || 'Polarized transport'}</p>
            </div>
        </div>
    `;
}

function setupNetworkControls() {
    const searchInput = document.getElementById('network-search');
    const layoutSelect = document.getElementById('network-layout');
    const scoreSlider = document.getElementById('network-score');
    const scoreVal = document.getElementById('network-score-val');

    if (searchInput && cyInstance) {
        searchInput.addEventListener('input', e => {
            const q = e.target.value.toLowerCase().trim();
            if (!q) {
                cyInstance.nodes().style('opacity', 1);
                cyInstance.edges().style('opacity', 0.75);
                return;
            }
            cyInstance.nodes().forEach(n => {
                const match = n.data('label').toLowerCase().includes(q) || 
                              (n.data('compartment') && n.data('compartment').toLowerCase().includes(q)) ||
                              (n.data('reaction') && n.data('reaction').toLowerCase().includes(q));
                if (match) {
                    n.style('opacity', 1);
                    n.select();
                    displayNodeDetails(n.data());
                } else {
                    n.style('opacity', 0.2);
                    n.unselect();
                }
            });
        });
    }

    if (layoutSelect && cyInstance) {
        layoutSelect.addEventListener('change', e => {
            const layoutName = e.target.value;
            cyInstance.layout({ name: layoutName, animate: true, animationDuration: 500 }).run();
        });
    }

    if (scoreSlider && cyInstance) {
        scoreSlider.addEventListener('input', e => {
            const minScore = parseFloat(e.target.value);
            if (scoreVal) scoreVal.innerText = `> ${minScore.toFixed(2)}`;
            cyInstance.edges().forEach(edge => {
                if (edge.data('score') >= minScore) {
                    edge.show();
                } else {
                    edge.hide();
                }
            });
        });
    }
}

// Safe DOM initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNetworkViewer);
} else {
    initNetworkViewer();
}