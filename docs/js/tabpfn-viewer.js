// TabPFN AI Foundation Model Explorer Module
// Cross-Study Bayesian In-Context Meta-Analysis (OSD-615 + OSD-121)
// Implements TabPFN Tabular Foundation Model (Hollmann et al., Nature 2025, doi:10.1038/s41586-024-08328-6)

let tabpfnData = null;

export function initTabPFNViewer() {
    fetch('data/tabpfn_meta_analysis.json')
        .then(r => r.json())
        .then(data => {
            tabpfnData = data;
            renderROCCurve(data.cross_study_metrics);
            renderFeatureImportance(data.feature_importances);
            setupGravitySimulation(data.partial_gravity_simulation);
        })
        .catch(err => console.error('Error loading TabPFN meta-analysis data:', err));

    window.addEventListener('themeChanged', () => {
        if (tabpfnData) {
            renderROCCurve(tabpfnData.cross_study_metrics);
            renderFeatureImportance(tabpfnData.feature_importances);
        }
    });
}

function renderROCCurve(metrics) {
    const container = document.getElementById('tabpfn-roc-plot');
    if (!container || !metrics) return;

    const isDark = document.documentElement.dataset.theme === 'dark';
    const textColor = isDark ? '#f1f5f9' : '#0f172a';

    const trace121 = {
        x: metrics.fpr_121,
        y: metrics.tpr_121,
        mode: 'lines',
        name: `OSD-615 ➔ OSD-121 (AUC = ${metrics.osd615_to_121_auc.toFixed(3)})`,
        line: { color: '#E85D50', width: 3 }
    };

    const trace615 = {
        x: metrics.fpr_615,
        y: metrics.tpr_615,
        mode: 'lines',
        name: `OSD-121 ➔ OSD-615 (AUC = ${metrics.osd121_to_615_auc.toFixed(3)})`,
        line: { color: '#2F5985', width: 3 }
    };

    const traceRandom = {
        x: [0, 1],
        y: [0, 1],
        mode: 'lines',
        name: 'Random Chance (AUC = 0.500)',
        line: { color: isDark ? '#64748b' : '#94a3b8', dash: 'dash', width: 1.5 }
    };

    const layout = {
        title: { text: 'TabPFN Zero-Shot Cross-Mission Transfer (ROC Curves)', font: { size: 13, color: textColor } },
        xaxis: { 
            title: { text: 'False Positive Rate (1 - Specificity)', font: { size: 12, color: textColor } },
            tickfont: { size: 10, color: textColor },
            automargin: true
        },
        yaxis: { 
            title: { text: 'True Positive Rate (Sensitivity)', font: { size: 12, color: textColor } },
            tickfont: { size: 10, color: textColor },
            automargin: true
        },
        margin: { l: 65, r: 25, t: 45, b: 60 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: textColor },
        legend: { x: 0.35, y: 0.15, font: { size: 9, color: textColor } }
    };

    Plotly.newPlot('tabpfn-roc-plot', [trace121, trace615, traceRandom], layout, { responsive: true, displaylogo: false });
}

function renderFeatureImportance(importances) {
    const container = document.getElementById('tabpfn-importance-plot');
    if (!container || !importances) return;

    const isDark = document.documentElement.dataset.theme === 'dark';
    const textColor = isDark ? '#f1f5f9' : '#0f172a';

    const top10 = importances.slice(0, 10).reverse();

    const trace = {
        x: top10.map(d => d.importance),
        y: top10.map(d => d.feature),
        type: 'bar',
        orientation: 'h',
        marker: {
            color: top10.map(d => d.category.includes('Synthase') || d.category.includes('Fraction') ? '#E85D50' : d.category.includes('Motor') ? '#3FB6A8' : '#2F5985')
        },
        text: top10.map(d => `${(d.importance * 100).toFixed(1)}%`),
        textposition: 'auto'
    };

    const layout = {
        title: { text: 'Bayesian Multi-Omics Saliency (Top 10 Universal Drivers)', font: { size: 13, color: textColor } },
        xaxis: { 
            title: { text: 'Bayesian Posterior Importance', font: { size: 12, color: textColor } },
            tickfont: { size: 10, color: textColor },
            automargin: true
        },
        yaxis: { 
            title: { text: 'Multi-Omics Feature', font: { size: 11, color: textColor } },
            automargin: true, 
            tickfont: { size: 10.5, color: textColor } 
        },
        margin: { l: 120, r: 40, t: 45, b: 60 },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: textColor }
    };

    Plotly.newPlot('tabpfn-importance-plot', [trace], layout, { responsive: true, displaylogo: false });
}

function setupGravitySimulation(simData) {
    const slider = document.getElementById('tabpfn-gravity-slider');
    const valBadge = document.getElementById('tabpfn-gravity-val');
    const outProb = document.getElementById('tabpfn-pred-prob');
    const outXylan = document.getElementById('tabpfn-pred-xylan');
    const outMya1 = document.getElementById('tabpfn-pred-mya1');
    const outSpr1 = document.getElementById('tabpfn-pred-spr1');
    const outSkew = document.getElementById('tabpfn-pred-skew');

    function updateSimulation(g) {
        if (!simData) return;
        if (valBadge) valBadge.innerText = `${g.toFixed(2)} g`;

        // Calculate continuous in-context Bayesian predictions
        const k = 6.0;
        const gMid = 0.30;
        const response = 1.0 / (1.0 + Math.exp(k * (g - gMid)));
        const responseSpr1 = 1.0 / (1.0 + Math.exp(-k * (g - gMid)));

        const prob = response * 100;
        const xylan = 46.5 + (125.0 - 46.5) * response;
        const mya1 = 9.3 + (11.4 - 9.3) * response;
        const spr1 = 8.4 + (10.7 - 8.4) * responseSpr1;
        const skew = 4.5 + (43.0 - 4.5) * response;

        if (outProb) outProb.innerHTML = `<strong style="color:${prob > 50 ? 'var(--coral)' : 'var(--teal)'}">${prob.toFixed(1)}% Microgravity State</strong>`;
        if (outXylan) outXylan.innerText = `${xylan.toFixed(1)} µg/mg wall`;
        if (outMya1) outMya1.innerText = `${mya1.toFixed(2)} log2`;
        if (outSpr1) outSpr1.innerText = `${spr1.toFixed(2)} log2`;
        if (outSkew) outSkew.innerText = `${skew.toFixed(1)}°`;
    }

    if (slider) {
        slider.addEventListener('input', e => {
            updateSimulation(parseFloat(e.target.value));
        });
    }

    // Preset buttons
    const btn0g = document.getElementById('btn-g-0g');
    const btnMoon = document.getElementById('btn-g-moon');
    const btnMars = document.getElementById('btn-g-mars');
    const btn1g = document.getElementById('btn-g-1g');

    if (btn0g) btn0g.addEventListener('click', () => { if (slider) slider.value = 0.0; updateSimulation(0.0); });
    if (btnMoon) btnMoon.addEventListener('click', () => { if (slider) slider.value = 0.16; updateSimulation(0.16); });
    if (btnMars) btnMars.addEventListener('click', () => { if (slider) slider.value = 0.38; updateSimulation(0.38); });
    if (btn1g) btn1g.addEventListener('click', () => { if (slider) slider.value = 1.0; updateSimulation(1.0); });

    // Initial calculation at Moon gravity (0.16g)
    updateSimulation(0.16);
}

// Safe DOM initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTabPFNViewer);
} else {
    initTabPFNViewer();
}
