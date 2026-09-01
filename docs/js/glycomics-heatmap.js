// Glycomics Explorer Heatmap Module
let rawData = null;

export function initGlycomicsHeatmap() {
    const container = document.getElementById('heatmap');
    if (!container) return;

    fetch('data/glycomics_heatmap.json')
        .then(r => r.json())
        .then(data => {
            rawData = data;
            const colorFilter = document.getElementById('heatmap-colorscale');
            const initialColor = colorFilter ? colorFilter.value : 'RdBu_r';
            renderHeatmap('all', initialColor);
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
    const gridColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)';

    // Resolve color scale (Blue to White to Red diverging)
    let selectedScale = colorscale || 'RdBu_r';
    if (selectedScale === 'RdBu_r') {
        // High contrast diverging Blue-White-Red
        selectedScale = [
            [0.0, '#1d4ed8'],   // Deep Blue (repressed / low)
            [0.25, '#93c5fd'],  // Light Blue
            [0.5, '#ffffff'],   // Clean White (baseline)
            [0.75, '#fca5a5'],  // Light Coral / Pink
            [1.0, '#b91c1c']    // Deep Red (spaceflight accumulated)
        ];
    }

    const trace = {
        z: zValues,
        x: mabs,
        y: rawData.y.map(s => s.replace('_roots', '')),
        type: 'heatmap',
        colorscale: selectedScale,
        colorbar: {
            title: { text: 'OD450', font: { color: textColor, size: 11 } },
            tickfont: { color: textColor, size: 10 }
        },
        hoverongaps: false,
        hovertemplate: '<b>Sample:</b> %{y}<br><b>mAb:</b> %{x}<br><b>OD450:</b> %{z:.3f}<extra></extra>'
    };

    const layout = {
        title: { text: `Cell Wall Glycome Profiling (${mabs.length} Monoclonal Antibodies)`, font: { size: 14, color: textColor } },
        xaxis: { 
            title: { text: 'CCRC Monoclonal Antibodies', font: { size: 12, color: textColor } },
            tickangle: -45, 
            tickfont: { size: mabs.length > 50 ? 8 : 10, color: textColor },
            automargin: true
        },
        yaxis: { 
            title: { text: 'Arabidopsis Root Samples (ISS Flight vs Ground Control)', font: { size: 12, color: textColor } },
            tickfont: { size: 10.5, color: textColor },
            automargin: true
        },
        margin: { l: 160, r: 50, t: 60, b: 140 },
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
            const colorVal = colorFilter ? colorFilter.value : 'RdBu_r';
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

    // Reactive listener on theme changes
    window.addEventListener('themeChanged', () => {
        const classVal = classFilter ? classFilter.value : 'all';
        const colorVal = colorFilter ? colorFilter.value : 'RdBu_r';
        renderHeatmap(classVal, colorVal);
    });
}

// Safe DOM initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGlycomicsHeatmap);
} else {
    initGlycomicsHeatmap();
}