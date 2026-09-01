// Glycomics Explorer Heatmap Module
let rawData = null;

export function initGlycomicsHeatmap() {
    const container = document.getElementById('heatmap');
    if (!container) return;

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
    const container = document.getElementById('heatmap');
    if (!container) return;

    let mabs = [...rawData.x];
    let zValues = rawData.z; // 12 samples × 155 mAbs

    if (classFilter !== 'all') {
        const filteredIndices = [];
        mabs = [];
        rawData.x.forEach((m, idx) => {
            const cls = rawData.glycan_classes[m] || '';
            if (cls.toLowerCase().includes(classFilter.toLowerCase()) || 
                (classFilter === 'Xylan / Arabinoxylan' && cls.toLowerCase().includes('xylan')) ||
                (classFilter === 'Xyloglucan' && cls.toLowerCase().includes('xyloglucan')) ||
                (classFilter === 'AGPs' && cls.toLowerCase().includes('agp')) ||
                (classFilter === 'Homogalacturonan Pectin' && cls.toLowerCase().includes('hg')) ||
                (classFilter === 'RG-I / Arabinan / Galactan' && (cls.toLowerCase().includes('rg') || cls.toLowerCase().includes('galactan')))) {
                mabs.push(m);
                filteredIndices.push(idx);
            }
        });
        zValues = rawData.z.map(row => filteredIndices.map(i => row[i]));
    }

    const isDark = document.documentElement.dataset.theme === 'dark';
    const textColor = isDark ? '#f1f5f9' : '#0f172a';

    const trace = {
        z: zValues,
        x: mabs,
        y: rawData.y.map(s => s.replace('_roots', '')),
        type: 'heatmap',
        colorscale: colorscale || 'YlOrRd',
        hoverongaps: false,
        hovertemplate: '<b>Sample:</b> %{y}<br><b>mAb:</b> %{x}<br><b>OD450:</b> %{z:.3f}<extra></extra>'
    };

    const layout = {
        title: { text: `Cell Wall Glycome Profiling (${mabs.length} Monoclonal Antibodies)`, font: { size: 14, color: textColor } },
        xaxis: { title: 'CCRC Monoclonal Antibodies', tickangle: -45, tickfont: { size: 8, color: textColor } },
        yaxis: { title: 'Arabidopsis Root Samples (ISS Flight vs Ground Control)', tickfont: { size: 10, color: textColor } },
        margin: { l: 140, r: 40, t: 50, b: 120 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: textColor }
    };

    const config = { responsive: true, displayModeBar: true, displaylogo: false };
    Plotly.newPlot('heatmap', [trace], layout, config);
}

function setupControls() {
    const classFilter = document.getElementById('glycan-class-filter');
    const colorFilter = document.getElementById('heatmap-colorscale');
    const exportBtn = document.getElementById('btn-export-heatmap');

    if (classFilter) {
        classFilter.addEventListener('change', e => {
            const colorVal = colorFilter ? colorFilter.value : 'YlOrRd';
            renderHeatmap(e.target.value, colorVal);
        });
    }
    if (colorFilter) {
        colorFilter.addEventListener('change', e => {
            const classVal = classFilter ? classFilter.value : 'all';
            renderHeatmap(classVal, e.target.value);
        });
    }
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            Plotly.downloadImage('heatmap', { format: 'png', width: 1400, height: 800, filename: 'OSD615_Glycome_Heatmap' });
        });
    }
}

// Safe DOM initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGlycomicsHeatmap);
} else {
    initGlycomicsHeatmap();
}