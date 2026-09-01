// Differential Analysis Charts Module

export function initDifferentialCharts() {
    fetch('data/differential_results.json')
        .then(r => r.json())
        .then(data => {
            renderVolcanoPlot(data.items);
            renderBarChart(data.items);
        })
        .catch(err => console.error('Error loading differential results:', err));
}

function renderVolcanoPlot(items) {
    const isDark = document.documentElement.dataset.theme === 'dark';
    const textColor = isDark ? '#f1f5f9' : '#2c3e50';

    const traceSig = {
        x: items.filter(d => d.pvalue < 0.05).map(d => d.log2FC),
        y: items.filter(d => d.pvalue < 0.05).map(d => -Math.log10(d.pvalue)),
        text: items.filter(d => d.pvalue < 0.05).map(d => `<b>${d.mAb}</b><br>${d.Glycan_Class}<br>FC: ${d.Fold_Change.toFixed(2)}x<br>p: ${d.pvalue.toExponential(2)}`),
        mode: 'markers',
        type: 'scatter',
        name: 'Significant (p < 0.05)',
        marker: { color: '#E85D50', size: 10, opacity: 0.85 }
    };

    const traceNonSig = {
        x: items.filter(d => d.pvalue >= 0.05).map(d => d.log2FC),
        y: items.filter(d => d.pvalue >= 0.05).map(d => -Math.log10(d.pvalue)),
        text: items.filter(d => d.pvalue >= 0.05).map(d => `<b>${d.mAb}</b><br>${d.Glycan_Class}<br>p: ${d.pvalue.toFixed(3)}`),
        mode: 'markers',
        type: 'scatter',
        name: 'Not Significant',
        marker: { color: isDark ? '#64748b' : '#94a3b8', size: 6, opacity: 0.5 }
    };

    const layout = {
        title: { text: 'Volcano Plot: Spaceflight vs Ground (OSD-615)', font: { size: 13 } },
        xaxis: { title: 'Log2 Fold Change (Spaceflight / Ground)' },
        yaxis: { title: '-Log10 p-value' },
        margin: { l: 60, r: 20, t: 40, b: 60 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: textColor },
        shapes: [
            { type: 'line', x0: -3, x1: 3, y0: -Math.log10(0.05), y1: -Math.log10(0.05), line: { color: 'gray', dash: 'dot', width: 1 } }
        ]
    };

    Plotly.newPlot('volcano', [traceNonSig, traceSig], layout, { responsive: true, displaylogo: false });
}

function renderBarChart(items) {
    const isDark = document.documentElement.dataset.theme === 'dark';
    const textColor = isDark ? '#f1f5f9' : '#2c3e50';

    // Sort by absolute log2FC
    const sorted = [...items].sort((a, b) => Math.abs(b.log2FC) - Math.abs(a.log2FC)).slice(0, 15);

    const trace = {
        x: sorted.map(d => d.log2FC),
        y: sorted.map(d => `${d.mAb} (${d.Glycan_Class.split('/')[0].trim()})`),
        type: 'bar',
        orientation: 'h',
        marker: {
            color: sorted.map(d => d.log2FC > 0 ? '#E85D50' : '#2F5985')
        },
        text: sorted.map(d => `${d.log2FC > 0 ? '+' : ''}${d.log2FC.toFixed(2)}`),
        textposition: 'auto'
    };

    const layout = {
        title: { text: 'Top 15 Altered Cell Wall Epitopes (Spaceflight vs Ground)', font: { size: 13 } },
        xaxis: { title: 'Log2 Fold Change' },
        yaxis: { automargin: true, tickfont: { size: 10 } },
        margin: { l: 150, r: 30, t: 40, b: 50 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: textColor }
    };

    Plotly.newPlot('bar-chart', [trace], layout, { responsive: true, displaylogo: false });
}

// Auto init
initDifferentialCharts();