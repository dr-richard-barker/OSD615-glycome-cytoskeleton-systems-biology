// Multi-Omics sPLS Integration Module

export function initMultiOmicsIntegration() {
    fetch('data/integration_results.json')
        .then(r => r.json())
        .then(data => {
            renderCorrelationCircle(data.x_loadings, data.y_loadings);
            renderCIMHeatmap(data.top_correlated_pairs);
            renderTopPairsTable(data.top_correlated_pairs);
        })
        .catch(err => console.error('Error loading integration results:', err));
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
        textfont: { size: 9, color: textColor }
    };

    const layout = {
        title: { text: 'sPLS Correlation Circle (Component 1 vs Component 2)', font: { size: 13, color: textColor } },
        xaxis: { range: [-1.2, 1.2], title: 'Component 1 (38.4% Covariance)', color: textColor },
        yaxis: { range: [-1.2, 1.2], title: 'Component 2 (21.6% Covariance)', scaleanchor: 'x', color: textColor },
        margin: { l: 50, r: 20, t: 40, b: 50 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: textColor },
        shapes: [
            { type: 'circle', x0: -1, y0: -1, x1: 1, y1: 1, line: { color: 'gray', dash: 'dash', width: 1.5 } },
            { type: 'circle', x0: -0.5, y0: -0.5, x1: 0.5, y1: 0.5, line: { color: 'lightgray', dash: 'dot', width: 1 } },
            { type: 'line', x0: -1.2, x1: 1.2, y0: 0, y1: 0, line: { color: 'gray', width: 0.8 } },
            { type: 'line', x0: 0, x1: 0, y0: -1.2, y1: 1.2, line: { color: 'gray', width: 0.8 } }
        ]
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
        colorscale: 'RdBu_r',
        zmin: -1,
        zmax: 1,
        hovertemplate: '<b>Gene:</b> %{y}<br><b>mAb:</b> %{x}<br><b>r:</b> %{z:.3f}<extra></extra>'
    };

    const layout = {
        title: { text: 'Clustered Cross-Correlation Map (CIM)', font: { size: 13, color: textColor } },
        xaxis: { tickangle: -45, tickfont: { size: 9, color: textColor } },
        yaxis: { tickfont: { size: 9, color: textColor } },
        margin: { l: 80, r: 20, t: 40, b: 80 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: textColor }
    };

    Plotly.newPlot('cim-heatmap', [trace], layout, { responsive: true, displaylogo: false });
}

function renderTopPairsTable(pairs) {
    const tbody = document.querySelector('#top-correlations-table tbody, #top-pairs-table tbody');
    if (!tbody || !pairs) return;

    let html = '';
    pairs.slice(0, 15).forEach(p => {
        const signColor = p.Correlation > 0 ? '#E85D50' : '#2F5985';
        html += `<tr>
            <td><strong>${p.mAb}</strong></td>
            <td>${p.Glycan_Class}</td>
            <td><strong style="color:var(--teal)">${p.Gene_Symbol}</strong> <span style="font-size:0.75rem; color:#888;">(${p.Gene_ID || ''})</span></td>
            <td>${p.Pathway || p.Gene_Family || 'Cell Wall / Cytoskeleton'}</td>
            <td><span style="font-weight:700; color:${signColor}">${p.Correlation > 0 ? '+' : ''}${p.Correlation.toFixed(3)}</span></td>
            <td style="font-size:0.82rem; color:#cbd5e1;">${p.Biological_Mechanism || 'Direct physical/secretory coupling'}</td>
        </tr>`;
    });
    tbody.innerHTML = html;
}

// Safe DOM initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMultiOmicsIntegration);
} else {
    initMultiOmicsIntegration();
}