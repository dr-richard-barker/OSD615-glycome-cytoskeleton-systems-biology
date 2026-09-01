// Differential Analysis Charts Module (Volcano Plot & Bar Chart)

let diffData = [];

export function initDifferentialCharts() {
    fetch('data/differential_results.json')
        .then(r => r.json())
        .then(data => {
            diffData = data.items || [];
            updateCharts();
            setupControls();
        })
        .catch(err => console.error('Error loading differential results:', err));
}

function updateCharts() {
    const timepointSelect = document.getElementById('diff-timepoint');
    const pthreshSlider = document.getElementById('diff-pthresh');
    const timepoint = timepointSelect ? timepointSelect.value : 'both';
    const pthresh = pthreshSlider ? parseFloat(pthreshSlider.value) : 0.01;

    renderVolcanoPlot(diffData, timepoint, pthresh);
    renderBarChart(diffData, timepoint);
}

function renderVolcanoPlot(items, timepoint, pthresh) {
    const container = document.getElementById('volcano');
    if (!container || items.length === 0) return;

    const isDark = document.documentElement.dataset.theme === 'dark';
    const textColor = isDark ? '#f1f5f9' : '#0f172a';

    const getFC = d => timepoint === '6d' ? d.log2FC_6d : timepoint === '11d' ? d.log2FC_11d : d.log2FC;
    const getP = d => timepoint === '6d' ? d.pvalue_6d : timepoint === '11d' ? d.pvalue_11d : d.pvalue;

    const sigItems = items.filter(d => getP(d) < pthresh);
    const nonSigItems = items.filter(d => getP(d) >= pthresh);

    const traceSig = {
        x: sigItems.map(d => getFC(d)),
        y: sigItems.map(d => -Math.log10(Math.max(getP(d), 1e-10))),
        text: sigItems.map(d => `<b>${d.mAb}</b><br>${d.Glycan_Class}<br>log2FC: ${getFC(d).toFixed(2)}<br>p: ${getP(d).toExponential(2)}`),
        mode: 'markers',
        type: 'scatter',
        name: `Significant (p < ${pthresh})`,
        marker: { color: '#E85D50', size: 9, opacity: 0.9 }
    };

    const traceNonSig = {
        x: nonSigItems.map(d => getFC(d)),
        y: nonSigItems.map(d => -Math.log10(Math.max(getP(d), 1e-10))),
        text: nonSigItems.map(d => `<b>${d.mAb}</b><br>${d.Glycan_Class}<br>log2FC: ${getFC(d).toFixed(2)}<br>p: ${getP(d).toFixed(3)}`),
        mode: 'markers',
        type: 'scatter',
        name: 'Not Significant',
        marker: { color: isDark ? '#64748b' : '#94a3b8', size: 6, opacity: 0.5 }
    };

    const layout = {
        title: { text: `Volcano Plot: Spaceflight vs Ground (${timepoint.toUpperCase()})`, font: { size: 13, color: textColor } },
        xaxis: { 
            title: { text: 'Log2 Fold Change (Spaceflight / Ground)', font: { size: 12, color: textColor } },
            tickfont: { size: 10.5, color: textColor },
            automargin: true
        },
        yaxis: { 
            title: { text: '-Log10 p-value', font: { size: 12, color: textColor } },
            tickfont: { size: 10.5, color: textColor },
            automargin: true
        },
        margin: { l: 70, r: 30, t: 45, b: 60 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: textColor },
        shapes: [
            { type: 'line', x0: -3, x1: 3, y0: -Math.log10(pthresh), y1: -Math.log10(pthresh), line: { color: '#f59e0b', dash: 'dot', width: 1.5 } }
        ]
    };

    Plotly.newPlot('volcano', [traceNonSig, traceSig], layout, { responsive: true, displaylogo: false });
}

function renderBarChart(items, timepoint) {
    const container = document.getElementById('bar-chart');
    if (!container || items.length === 0) return;

    const isDark = document.documentElement.dataset.theme === 'dark';
    const textColor = isDark ? '#f1f5f9' : '#0f172a';

    const getFC = d => timepoint === '6d' ? d.log2FC_6d : timepoint === '11d' ? d.log2FC_11d : d.log2FC;

    // Top 15 by absolute log2FC
    const sorted = [...items].sort((a, b) => Math.abs(getFC(b)) - Math.abs(getFC(a))).slice(0, 15).reverse();

    const trace = {
        x: sorted.map(d => getFC(d)),
        y: sorted.map(d => `${d.mAb} (${(d.Glycan_Class || '').split('(')[0].trim()})`),
        type: 'bar',
        orientation: 'h',
        marker: {
            color: sorted.map(d => getFC(d) > 0 ? '#E85D50' : '#2F5985')
        },
        text: sorted.map(d => `${getFC(d) > 0 ? '+' : ''}${getFC(d).toFixed(2)}`),
        textposition: 'auto'
    };

    const layout = {
        title: { text: `Top 15 Altered Cell Wall Epitopes (${timepoint.toUpperCase()})`, font: { size: 13, color: textColor } },
        xaxis: { 
            title: { text: 'Log2 Fold Change (Spaceflight vs Ground)', font: { size: 12, color: textColor } },
            tickfont: { size: 10.5, color: textColor },
            automargin: true
        },
        yaxis: { 
            title: { text: 'Monoclonal Antibody & Glycan Target', font: { size: 11, color: textColor } },
            tickfont: { size: 10, color: textColor },
            automargin: true
        },
        margin: { l: 190, r: 40, t: 45, b: 60 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: textColor }
    };

    Plotly.newPlot('bar-chart', [trace], layout, { responsive: true, displaylogo: false });
}

function setupControls() {
    const timepointSelect = document.getElementById('diff-timepoint');
    const pthreshSlider = document.getElementById('diff-pthresh');
    const pthreshVal = document.getElementById('pthresh-val');

    if (timepointSelect) {
        timepointSelect.addEventListener('change', updateCharts);
    }
    if (pthreshSlider) {
        pthreshSlider.addEventListener('input', e => {
            if (pthreshVal) pthreshVal.innerText = e.target.value;
            updateCharts();
        });
    }

    // Reactive listener on theme changes
    window.addEventListener('themeChanged', updateCharts);
}

// Safe DOM initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDifferentialCharts);
} else {
    initDifferentialCharts();
}