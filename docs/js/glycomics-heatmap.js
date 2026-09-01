// Glycomics Explorer Heatmap Module
let rawData = null;

export function initGlycomicsHeatmap() {
    fetch('data/glycomics_heatmap.json')
        .then(r => r.json())
        .then(data => {
            rawData = data;
            renderHeatmap('all', 'YlOrRd');
            setupControls();
        })
        .catch(err => console.error('Error loading glycomics heatmap data:', err));
}

function renderHeatmap(classFilter, colorscale) {
    if (!rawData) return;

    let mabs = rawData.x;
    let zValues = rawData.z; // 12 samples × 155 mAbs

    if (classFilter !== 'all') {
        const filteredIndices = [];
        mabs = [];
        rawData.x.forEach((m, idx) => {
            if (rawData.glycan_classes[m] === classFilter) {
                mabs.push(m);
                filteredIndices.push(idx);
            }
        });
        zValues = rawData.z.map(row => filteredIndices.map(i => row[i]));
    }

    const trace = {
        z: zValues,
        x: mabs,
        y: rawData.y.map(s => s.replace('_roots', '')),
        type: 'heatmap',
        colorscale: colorscale,
        hoverongaps: false,
        hovertemplate: '<b>Sample:</b> %{y}<br><b>mAb:</b> %{x}<br><b>OD450:</b> %{z:.3f}<extra></extra>'
    };

    const layout = {
        title: { text: `Cell Wall Glycome Profiling (${mabs.length} Monoclonal Antibodies)`, font: { size: 14 } },
        xaxis: { title: 'CCRC Monoclonal Antibodies', tickangle: -45, tickfont: { size: 8 } },
        yaxis: { title: 'Arabidopsis Root Samples (ISS Flight vs Ground Control)', tickfont: { size: 10 } },
        margin: { l: 140, r: 40, t: 50, b: 120 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: document.documentElement.dataset.theme === 'dark' ? '#f1f5f9' : '#2c3e50' }
    };

    const config = { responsive: true, displayModeBar: true, displaylogo: false };
    Plotly.newPlot('heatmap', [trace], layout, config);
}

function setupControls() {
    const classFilter = document.getElementById('glycan-class-filter');
    const colorFilter = document.getElementById('heatmap-colorscale');

    if (classFilter) {
        classFilter.addEventListener('change', e => {
            renderHeatmap(e.target.value, colorFilter.value);
        });
    }
    if (colorFilter) {
        colorFilter.addEventListener('change', e => {
            renderHeatmap(classFilter.value, e.target.value);
        });
    }
}

// Auto init
initGlycomicsHeatmap();