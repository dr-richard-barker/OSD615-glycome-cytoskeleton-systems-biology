// Interactive ggPlantmap Spatial Root Map Viewer
// Implements SVG-based anatomical maps of Arabidopsis thaliana roots
// with quantitative overlays from the Salk Single-Cell Atlas (Lee et al. 2025, Nature Plants)

let plantmapData = null;
let currentFeature = 'IRX9';

export function initGGPlantmapViewer() {
    fetch('data/ggplantmap_data.json')
        .then(r => r.json())
        .then(data => {
            plantmapData = data;
            setupControls();
            renderMaps();
        })
        .catch(err => console.error('Error loading ggPlantmap data:', err));
}

function setupControls() {
    const selGene = document.getElementById('plantmap-feature-select');
    if (!selGene || !plantmapData) return;

    let html = '<optgroup label="Secondary Cell Wall & Motors (Xylem-Enriched)">';
    ['IRX9', 'IRX10', 'CESA4', 'CESA7', 'MYA1', 'MYA2', 'KIN12A'].forEach(g => {
        html += `<option value="${g}" ${g === 'IRX9' ? 'selected' : ''}>${g} (Secondary Wall)</option>`;
    });
    html += '</optgroup><optgroup label="Primary Cell Wall & MT Direction (Epidermis/Elongation)">';
    ['SPR1', 'MAP65-1', 'CESA1', 'CSI1', 'CLASP', 'XTH4', 'EXPA1'].forEach(g => {
        html += `<option value="${g}">${g} (Primary Wall & MTs)</option>`;
    });
    html += '</optgroup><optgroup label="Intracellular Glycosylation & Microfilaments">';
    ['SEC', 'SPY', 'ACT7', 'ARP2', 'PRF1'].forEach(g => {
        html += `<option value="${g}">${g} (O-GlcNAc / Actin)</option>`;
    });
    html += '</optgroup><optgroup label="Glycan In Situ Epitope Predictions">';
    html += '<option value="glycan_xylan">Xylan Backbone (CCRC-M140)</option>';
    html += '<option value="glycan_xg">Fucosylated XG (CCRC-M1)</option>';
    html += '<option value="glycan_agp">Arabinogalactan AG-2 (JIM19)</option>';
    html += '<option value="glycan_gal">β-6-Galactan (CCRC-M79)</option>';
    html += '</optgroup>';

    selGene.innerHTML = html;
    selGene.addEventListener('change', e => {
        currentFeature = e.target.value;
        renderMaps();
    });
}

function getColor(val, minVal = 0, maxVal = 6) {
    const norm = Math.max(0, Math.min(1, (val - minVal) / (maxVal - minVal)));
    // Coral to Teal gradient
    // 0 = Dark Slate (#1e293b), 0.5 = Teal (#3FB6A8), 1.0 = Bright Coral (#E85D50)
    if (norm < 0.5) {
        const t = norm * 2;
        const r = Math.round(30 + t * (63 - 30));
        const g = Math.round(41 + t * (182 - 41));
        const b = Math.round(59 + t * (168 - 59));
        return `rgb(${r},${g},${b})`;
    } else {
        const t = (norm - 0.5) * 2;
        const r = Math.round(63 + t * (232 - 63));
        const g = Math.round(182 + t * (93 - 182));
        const b = Math.round(168 + t * (80 - 168));
        return `rgb(${r},${g},${b})`;
    }
}

function renderMaps() {
    if (!plantmapData) return;

    let vals = [];
    if (currentFeature.startsWith('glycan_')) {
        const glyKey = currentFeature === 'glycan_xylan' ? 'Xylan_CCRC_M140' :
                       currentFeature === 'glycan_xg' ? 'Xyloglucan_CCRC_M1' :
                       currentFeature === 'glycan_agp' ? 'AGP_JIM19' : 'Galactan_CCRC_M79';
        vals = plantmapData.glycan_spatial_predictions[glyKey].prediction_score.map(v => v * 6);
    } else {
        vals = plantmapData.expression_matrix[currentFeature] || [];
    }

    // Map values to cell types
    // 0: Columella, 1: LRC, 2: QC, 3: Meristem, 4: Trichoblast, 5: Atrichoblast, 6: Cortex, 7: Endodermis,
    // 8: Pericycle, 9: Procambium, 10: Protoxylem, 11: Metaxylem, 12: Phloem Sieve, 13: Phloem Companion
    const cCol = getColor(vals[0]);
    const cLRC = getColor(vals[1]);
    const cQC = getColor(vals[2]);
    const cMer = getColor(vals[3]);
    const cEpi = getColor((vals[4] + vals[5]) / 2);
    const cCtx = getColor(vals[6]);
    const cEnd = getColor(vals[7]);
    const cPer = getColor(vals[8]);
    const cPro = getColor(vals[9]);
    const cXyP = getColor(vals[10]);
    const cXyM = getColor(vals[11]);
    const cPhl = getColor((vals[12] + vals[13]) / 2);

    // 1. Root Cross-Section SVG
    const svgCross = document.getElementById('plantmap-cross-section');
    if (svgCross) {
        svgCross.innerHTML = `
            <svg viewBox="0 0 400 400" width="100%" height="320" style="background:#0a0f1d; border-radius:8px;">
                <!-- Outermost: Epidermis -->
                <circle cx="200" cy="200" r="175" fill="${cEpi}" stroke="#004D73" stroke-width="3" data-name="Epidermis" data-val="${vals[4].toFixed(2)}"/>
                <text x="200" y="45" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">Epidermis (${vals[4].toFixed(2)})</text>

                <!-- Layer 2: Cortex -->
                <circle cx="200" cy="200" r="135" fill="${cCtx}" stroke="#334155" stroke-width="2" data-name="Cortex" data-val="${vals[6].toFixed(2)}"/>
                <text x="200" y="85" fill="#ffffff" font-size="10" text-anchor="middle">Cortex (${vals[6].toFixed(2)})</text>

                <!-- Layer 3: Endodermis -->
                <circle cx="200" cy="200" r="95" fill="${cEnd}" stroke="#475569" stroke-width="2" data-name="Endodermis" data-val="${vals[7].toFixed(2)}"/>
                <text x="200" y="125" fill="#ffffff" font-size="9" text-anchor="middle">Endodermis (${vals[7].toFixed(2)})</text>

                <!-- Layer 4: Stele / Pericycle -->
                <circle cx="200" cy="200" r="65" fill="${cPer}" stroke="#D97706" stroke-width="2" data-name="Pericycle" data-val="${vals[8].toFixed(2)}"/>

                <!-- Vascular: Phloem Poles -->
                <circle cx="160" cy="200" r="14" fill="${cPhl}" stroke="#ffffff" stroke-width="1" data-name="Phloem" data-val="${vals[12].toFixed(2)}"/>
                <circle cx="240" cy="200" r="14" fill="${cPhl}" stroke="#ffffff" stroke-width="1" data-name="Phloem" data-val="${vals[12].toFixed(2)}"/>

                <!-- Vascular: Metaxylem Core -->
                <circle cx="200" cy="200" r="18" fill="${cXyM}" stroke="#ffffff" stroke-width="2.5" data-name="Metaxylem" data-val="${vals[11].toFixed(2)}"/>
                <circle cx="200" cy="172" r="10" fill="${cXyP}" stroke="#ffffff" stroke-width="1.5" data-name="Protoxylem" data-val="${vals[10].toFixed(2)}"/>
                <circle cx="200" cy="228" r="10" fill="${cXyP}" stroke="#ffffff" stroke-width="1.5" data-name="Protoxylem" data-val="${vals[10].toFixed(2)}"/>

                <text x="200" y="204" fill="#ffffff" font-size="9" font-weight="bold" text-anchor="middle">Xylem</text>
                <text x="200" y="380" fill="#3FB6A8" font-size="11" font-weight="bold" text-anchor="middle">Root Maturation Cross-Section (ggPlantmap)</text>
            </svg>
        `;
    }

    // 2. Root Tip Longitudinal SVG
    const svgLong = document.getElementById('plantmap-longitudinal');
    if (svgLong) {
        svgLong.innerHTML = `
            <svg viewBox="0 0 300 450" width="100%" height="320" style="background:#0a0f1d; border-radius:8px;">
                <!-- Root Body Outline -->
                <path d="M 110,400 L 110,180 Q 120,60 150,20 Q 180,60 190,180 L 190,400 Z" fill="${cEpi}" stroke="#004D73" stroke-width="2"/>
                
                <!-- Cortex Layer -->
                <path d="M 122,400 L 122,180 Q 130,90 150,50 Q 170,90 178,180 L 178,400 Z" fill="${cCtx}" stroke="#334155" stroke-width="1.5"/>

                <!-- Stele -->
                <rect x="142" y="100" width="16" height="300" fill="${cXyM}" stroke="#D97706" stroke-width="1.5"/>

                <!-- QC -->
                <circle cx="150" cy="65" r="10" fill="${cQC}" stroke="#ffffff" stroke-width="2"/>
                <text x="150" y="68" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">QC</text>

                <!-- Columella Root Cap -->
                <path d="M 130,50 Q 150,15 170,50 Q 150,35 130,50 Z" fill="${cCol}" stroke="#3FB6A8" stroke-width="1.5"/>
                <text x="150" y="32" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">Columella</text>

                <!-- Zone Labels -->
                <line x1="40" y1="35" x2="130" y2="35" stroke="#64748b" stroke-dasharray="3,3"/>
                <text x="35" y="38" fill="#94a3b8" font-size="8" text-anchor="end">Root Cap (${vals[0].toFixed(1)})</text>

                <line x1="40" y1="120" x2="120" y2="120" stroke="#64748b" stroke-dasharray="3,3"/>
                <text x="35" y="123" fill="#94a3b8" font-size="8" text-anchor="end">Meristem (${vals[3].toFixed(1)})</text>

                <line x1="40" y1="280" x2="120" y2="280" stroke="#64748b" stroke-dasharray="3,3"/>
                <text x="35" y="283" fill="#94a3b8" font-size="8" text-anchor="end">Elongation Zone (${vals[4].toFixed(1)})</text>

                <text x="150" y="435" fill="#3FB6A8" font-size="11" font-weight="bold" text-anchor="middle">Root Tip Longitudinal Map</text>
            </svg>
        `;
    }

    // Update details card
    const cardEl = document.getElementById('plantmap-details-card');
    if (cardEl) {
        cardEl.innerHTML = `
            <h3>Feature Selected: <span style="color:var(--coral);">${currentFeature}</span></h3>
            <p><strong>Predicted Spatial Peak:</strong> ${vals[11] > 4.5 ? 'Metaxylem & Stele (Secondary Cell Wall)' : vals[4] > 4.0 ? 'Epidermis & Elongation Zone (Primary Wall & MTs)' : 'Ubiquitous / Ground Tissue'}</p>
            <p><strong>Metaxylem Expression:</strong> ${vals[11].toFixed(2)} log2 | <strong>Epidermis Expression:</strong> ${vals[4].toFixed(2)} log2 | <strong>QC/Columella:</strong> ${vals[0].toFixed(2)} log2</p>
            <p style="font-size:0.85rem; color:#64748b; margin-top:8px;">Derived from the Salk Single-Cell Atlas (Lee et al. 2025, <em>Nature Plants</em>). Concordant with in situ spaceflight IHC from Nakashima et al. (PMC10444889).</p>
        `;
    }
}

// Auto init
initGGPlantmapViewer();
