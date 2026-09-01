// Multi-Omics sPLS Integration Module
let multiomicsData = null;

export function initMultiOmicsIntegration() {
    fetch('data/integration_results.json')
        .then(r => r.json())
        .then(data => {
            multiomicsData = data;
            renderCorrelationCircle(data.x_loadings, data.y_loadings);
            renderCIMHeatmap(data.top_correlated_pairs);
            renderTopPairsTable(data.top_correlated_pairs);
        })
        .catch(err => console.error('Error loading integration results:', err));

    window.addEventListener('themeChanged', () => {
        if (multiomicsData) {
            renderCorrelationCircle(multiomicsData.x_loadings, multiomicsData.y_loadings);
            renderCIMHeatmap(multiomicsData.top_correlated_pairs);
        }
    });
}

function renderCorrelationCircle(xLoadings, yLoadings) {
    const container = document.getElementById('circle-plot');
    if (!container || !xLoadings || !yLoadings) return;

    const isDark = document.documentElement.dataset.theme === 'dark';
    const textColor = isDark ? '#f1f5f9' : '#0f172a';

    // Glycans trace
    const traceGlycans = {
        x: xLoadings.map(d => d.comp1),
        y: xLoadings.map(d => d.comp2),
        text: xLoadings.map(d => `<b>${d.name}</b><br>${d.class}`),
        mode: 'markers',
        type: 'scatter',
        name: 'Glycan Epitopes (155 mAbs)',
        marker: { color: '#2F5985', size: 7, opacity: 0.6 }
    };

    // Genes trace
    const traceGenes = {
        x: yLoadings.map(d => d.comp1),
        y: yLoadings.map(d => d.comp2),
        text: yLoadings.map(d => `<b>${d.symbol}</b> (${d.id})<br>${d.pathway}`),
        mode: 'markers+text',
        textposition: 'top center',
        type: 'scatter',
        name: 'Cytoskeletal Transcripts (28 Genes)',
        marker: { color: '#E85D50', size: 10, symbol: 'triangle-up' },
        textfont: { size: 9.5, color: textColor }
    };

    const layout = {
        title: { text: 'sPLS Correlation Circle (Component 1 vs Component 2)', font: { size: 13, color: textColor } },
        xaxis: { 
            range: [-1.2, 1.2], 
            title: { text: 'Component 1 (38.4% Covariance)', font: { size: 12, color: textColor } },
            tickfont: { size: 10, color: textColor },
            automargin: true
        },
        yaxis: { 
            range: [-1.2, 1.2], 
            title: { text: 'Component 2 (21.6% Covariance)', font: { size: 12, color: textColor } },
            scaleanchor: 'x', 
            tickfont: { size: 10, color: textColor },
            automargin: true
        },
        margin: { l: 60, r: 30, t: 45, b: 60 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: textColor },
        shapes: [
            { type: 'circle', x0: -1, y0: -1, x1: 1, y1: 1, line: { color: isDark ? '#475569' : '#94a3b8', dash: 'dash', width: 1.5 } },
            { type: 'circle', x0: -0.5, y0: -0.5, x1: 0.5, y1: 0.5, line: { color: isDark ? '#334155' : '#cbd5e1', dash: 'dot', width: 1 } },
            { type: 'line', x0: -1.2, x1: 1.2, y0: 0, y1: 0, line: { color: isDark ? '#334155' : '#cbd5e1', width: 0.8 } },
            { type: 'line', x0: 0, x1: 0, y0: -1.2, y1: 1.2, line: { color: isDark ? '#334155' : '#cbd5e1', width: 0.8 } }
        ],
        legend: { font: { color: textColor, size: 9.5 } }
    };

    Plotly.newPlot('circle-plot', [traceGlycans, traceGenes], layout, { responsive: true, displaylogo: false });
}

function renderCIMHeatmap(pairs) {
    const container = document.getElementById('cim-heatmap');
    if (!container || !pairs) return;

    const isDark = document.documentElement.dataset.theme === 'dark';
    const textColor = isDark ? '#f1f5f9' : '#0f172a';

    const topPairs = pairs.slice(0, 15);
    const mabs = [...new Set(topPairs.map(p => p.mAb))];
    const genes = [...new Set(topPairs.map(p => p.Gene_Symbol))];

    const z = genes.map(g => {
        return mabs.map(m => {
            const match = topPairs.find(p => p.mAb === m && p.Gene_Symbol === g);
            return match ? match.Correlation : 0;
        });
    });

    const trace = {
        z: z,
        x: mabs,
        y: genes,
        type: 'heatmap',
        colorscale: [
            [0.0, '#1d4ed8'],
            [0.5, '#ffffff'],
            [1.0, '#b91c1c']
        ],
        zmin: -1,
        zmax: 1,
        colorbar: {
            title: { text: 'r', font: { color: textColor, size: 11 } },
            tickfont: { color: textColor, size: 10 }
        },
        hovertemplate: '<b>Gene:</b> %{y}<br><b>mAb:</b> %{x}<br><b>r:</b> %{z:.3f}<extra></extra>'
    };

    const layout = {
        title: { text: 'Clustered Cross-Correlation Map (CIM)', font: { size: 13, color: textColor } },
        xaxis: { 
            title: { text: 'Monoclonal Antibodies', font: { size: 11, color: textColor } },
            tickangle: -45, 
            tickfont: { size: 9.5, color: textColor },
            automargin: true
        },
        yaxis: { 
            title: { text: 'Cytoskeletal & Synthase Genes', font: { size: 11, color: textColor } },
            tickfont: { size: 10, color: textColor },
            automargin: true
        },
        margin: { l: 110, r: 30, t: 45, b: 90 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: textColor }
    };

    Plotly.newPlot('cim-heatmap', [trace], layout, { responsive: true, displaylogo: false });
}

function renderTopPairsTable(pairs) {
    const tbody = document.querySelector('#top-pairs-table tbody');
    if (!tbody || !pairs) return;

    tbody.innerHTML = '';
    pairs.slice(0, 10).forEach(pair => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${pair.mAb}</strong></td>
            <td><span class="badge badge-primary">${pair.Glycan_Class || 'Unknown'}</span></td>
            <td><code>${pair.Gene_Symbol}</code> (${pair.Gene_ID || ''})</td>
            <td>${pair.Pathway || ''}</td>
            <td style="font-weight:bold; color:${pair.Correlation > 0 ? 'var(--coral)' : 'var(--teal)'}">${pair.Correlation > 0 ? '+' : ''}${pair.Correlation.toFixed(3)}</td>
        `;
        tbody.appendChild(tr);
    });
}

// Safe DOM initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMultiOmicsIntegration);
} else {
    initMultiOmicsIntegration();
}