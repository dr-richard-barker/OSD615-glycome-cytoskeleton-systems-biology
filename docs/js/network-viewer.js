// Cytoscape.js Network Viewer Module
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
                            'text-outline-color': isDark ? '#0f172a' : '#ffffff',
                            'width': 'mapData(degree, 1, 6, 28, 55)',
                            'height': 'mapData(degree, 1, 6, 28, 55)',
                            'border-width': 2,
                            'border-color': '#ffffff'
                        }
                    },
                    {
                        selector: 'edge',
                        style: {
                            'width': 'mapData(score, 0.7, 1.0, 1.5, 4)',
                            'line-color': isDark ? '#64748b' : '#94a3b8',
                            'curve-style': 'bezier',
                            'opacity': 0.7
                        }
                    },
                    {
                        selector: 'node:selected',
                        style: {
                            'border-width': 4,
                            'border-color': '#F4A261'
                        }
                    }
                ],
                layout: {
                    name: 'cose',
                    idealEdgeLength: 100,
                    nodeOverlap: 20,
                    refresh: 20,
                    fit: true,
                    padding: 30,
                    randomize: false,
                    componentSpacing: 100,
                    nodeRepulsion: 400000,
                    edgeElasticity: 100,
                    nestingFactor: 5
                }
            });

            // Node click handler
            cyInstance.on('tap', 'node', function(evt) {
                const node = evt.target;
                const d = node.data();
                alert(`Gene: ${d.label} (${d.gene_id})\nFamily: ${d.gene_family}\nPathway: ${d.pathway}\nLog2FC (Space/Ground): ${d.log2FC}\nRole: ${d.role}`);
            });

            setupNetworkControls();
        })
        .catch(err => console.error('Error loading network graph:', err));
}

function setupNetworkControls() {
    const filter = document.getElementById('net-pathway-filter');
    const btnCose = document.getElementById('net-layout-cose');
    const btnCircle = document.getElementById('net-layout-circle');
    const btnReset = document.getElementById('net-reset');

    if (filter && cyInstance) {
        filter.addEventListener('change', e => {
            const val = e.target.value;
            if (val === 'all') {
                cyInstance.elements().show();
            } else {
                cyInstance.nodes().forEach(n => {
                    if (n.data('pathway') === val) {
                        n.show();
                    } else {
                        n.hide();
                    }
                });
                cyInstance.edges().forEach(edge => {
                    if (edge.source().visible() && edge.target().visible()) {
                        edge.show();
                    } else {
                        edge.hide();
                    }
                });
            }
        });
    }

    if (btnCose && cyInstance) {
        btnCose.addEventListener('click', () => {
            cyInstance.layout({ name: 'cose', animate: true }).run();
        });
    }
    if (btnCircle && cyInstance) {
        btnCircle.addEventListener('click', () => {
            cyInstance.layout({ name: 'circle', animate: true }).run();
        });
    }
    if (btnReset && cyInstance) {
        btnReset.addEventListener('click', () => {
            if (filter) filter.value = 'all';
            cyInstance.elements().show();
            cyInstance.fit();
        });
    }
}

// Window resize listener
window.addEventListener('resize', () => {
    if (cyInstance) cyInstance.resize();
});

// Auto init
initNetworkViewer();