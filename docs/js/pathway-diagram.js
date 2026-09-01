// Interactive SVG Pathway Diagrams Module

const pathways = {
    1: {
        title: "1. Post-Golgi Vesicle Secretion & Matrix Polysaccharide Delivery",
        desc: "Newly synthesized matrix polysaccharides (xyloglucans, xylans, pectins) and glycoproteins (AGPs) are packaged into secretory vesicles at the trans-Golgi network (TGN). Class XI myosins (MYA1, MYA2, XI-K) drive high-speed vesicle streaming along F-actin cables toward the cell cortex. Kinesin motors (FRA1, KIN12A) assist in phragmoplast delivery and spatial targeting.",
        svg: `<svg viewBox="0 0 800 400" width="100%" height="400" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#3FB6A8"/>
                </marker>
                <linearGradient id="golgiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#2F5985" />
                    <stop offset="100%" stop-color="#1e293b" />
                </linearGradient>
            </defs>
            <!-- Golgi Stack -->
            <rect x="40" y="80" width="140" height="240" rx="15" fill="url(#golgiGrad)" stroke="#3FB6A8" stroke-width="2"/>
            <text x="110" y="120" fill="#ffffff" font-size="14" font-weight="bold" text-anchor="middle">Golgi Apparatus</text>
            <text x="110" y="145" fill="#94a3b8" font-size="11" text-anchor="middle">Xylan Synthase (IRX9/10)</text>
            <text x="110" y="165" fill="#94a3b8" font-size="11" text-anchor="middle">Xyloglucan Synthase</text>
            <text x="110" y="185" fill="#94a3b8" font-size="11" text-anchor="middle">Pectin Methyltransferases</text>

            <!-- Actin Cable -->
            <path d="M 180 200 C 300 120, 500 280, 640 200" fill="none" stroke="#E85D50" stroke-width="4" stroke-dasharray="8,4"/>
            <text x="400" y="140" fill="#E85D50" font-size="12" font-weight="bold" text-anchor="middle">Actin Filament (F-Actin Cable)</text>

            <!-- Secretory Vesicles -->
            <circle cx="260" cy="175" r="18" fill="#3FB6A8" stroke="#ffffff" stroke-width="2"/>
            <text x="260" y="180" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">V1</text>
            
            <circle cx="430" cy="225" r="18" fill="#3FB6A8" stroke="#ffffff" stroke-width="2"/>
            <text x="430" y="230" fill="#ffffff" font-size="10" font-weight="bold" text-anchor="middle">V2</text>

            <!-- Myosin XI Motor Annotations -->
            <rect x="245" y="140" width="80" height="24" rx="4" fill="#F4A261" />
            <text x="285" y="156" fill="#000000" font-size="10" font-weight="bold" text-anchor="middle">MYA1 / XI-K</text>
            
            <!-- Plasma Membrane & Cell Wall -->
            <rect x="640" y="40" width="30" height="320" fill="#457B9D" stroke="#ffffff" stroke-width="1.5"/>
            <text x="655" y="200" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle" transform="rotate(90 655 200)">Plasma Membrane</text>

            <rect x="680" y="40" width="80" height="320" fill="#2A9D8F" opacity="0.6" stroke="#2A9D8F" stroke-width="2"/>
            <text x="720" y="200" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle" transform="rotate(90 720 200)">Apoplastic Cell Wall Matrix</text>
        </svg>`
    },
    2: {
        title: "2. Cortical Microtubule Alignment & Cellulose Synthase (CSC) Guidance",
        desc: "Cellulose Synthase Complexes (CSCs) synthesized in the Golgi are delivered to the plasma membrane. CSCs move processively through the lipid bilayer, synthesizing $\beta$-(1,4)-glucan microfibrils. The direction of CSC movement is physically coupled to underlying cortical microtubules via CSI1/POM2 linkers. Microtubule-associated proteins (MAP65, SPR1, CLASP) maintain array parallelism.",
        svg: `<svg viewBox="0 0 800 400" width="100%" height="400" xmlns="http://www.w3.org/2000/svg">
            <!-- Cortical Microtubule -->
            <rect x="100" y="140" width="600" height="20" rx="10" fill="#3FB6A8" stroke="#ffffff" stroke-width="1.5"/>
            <text x="400" y="130" fill="#3FB6A8" font-size="13" font-weight="bold" text-anchor="middle">Cortical Microtubule (CMT Track)</text>

            <!-- CSI1 Linker -->
            <rect x="360" y="165" width="80" height="40" rx="6" fill="#F4A261" stroke="#ffffff" stroke-width="1.5"/>
            <text x="400" y="190" fill="#000000" font-size="11" font-weight="bold" text-anchor="middle">CSI1 / POM2</text>

            <!-- Plasma Membrane -->
            <rect x="60" y="220" width="680" height="15" fill="#457B9D" opacity="0.7"/>
            <text x="400" y="232" fill="#ffffff" font-size="10" text-anchor="middle">Plasma Membrane Bilayer</text>

            <!-- Cellulose Synthase Rosette (CSC) -->
            <circle cx="400" cy="228" r="28" fill="#E85D50" stroke="#ffffff" stroke-width="2"/>
            <text x="400" y="233" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">CSC</text>

            <!-- Cellulose Microfibril Emerging into Wall -->
            <path d="M 400 256 L 400 340" stroke="#E76F51" stroke-width="6"/>
            <text x="400" y="360" fill="#E76F51" font-size="12" font-weight="bold" text-anchor="middle">Extruded Cellulose Microfibril</text>
            
            <!-- Plus end MAP regulators -->
            <circle cx="680" cy="150" r="16" fill="#9B5DE5"/>
            <text x="680" y="154" fill="#ffffff" font-size="9" font-weight="bold" text-anchor="middle">SPR1</text>
            
            <circle cx="120" cy="150" r="16" fill="#00BBF9"/>
            <text x="120" y="154" fill="#ffffff" font-size="9" font-weight="bold" text-anchor="middle">MAP65</text>
        </svg>`
    },
    3: {
        title: "3. Intracellular O-GlcNAcylation Regulatory Cascade (SEC / SPY)",
        desc: "The plant O-GlcNAc transferase SECRET AGENT (SEC) and O-fucosyltransferase SPINDLY (SPY) post-translationally modify nuclear and cytosolic proteins. In microgravity, SEC and SPY modify motor subunits (Myosin XI, Kinesin-14) and MT regulators (MAP65, SPR1), modulating processivity, phosphorylation cross-talk, and gravitational acclimation.",
        svg: `<svg viewBox="0 0 800 400" width="100%" height="400" xmlns="http://www.w3.org/2000/svg">
            <!-- UDP-GlcNAc Pool -->
            <rect x="80" y="80" width="150" height="70" rx="8" fill="#2F5985" stroke="#3FB6A8" stroke-width="2"/>
            <text x="155" y="115" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">UDP-GlcNAc Pool</text>
            <text x="155" y="135" fill="#3FB6A8" font-size="10" text-anchor="middle">Hexosamine Pathway</text>

            <!-- SEC Transferase -->
            <circle cx="340" cy="115" r="40" fill="#3FB6A8" stroke="#ffffff" stroke-width="2"/>
            <text x="340" y="115" fill="#ffffff" font-size="12" font-weight="bold" text-anchor="middle">SEC (OGT)</text>
            <text x="340" y="130" fill="#0f172a" font-size="9" text-anchor="middle">+1.55 log2FC</text>

            <!-- Arrow from Pool to Enzyme -->
            <path d="M 230 115 L 295 115" stroke="#ffffff" stroke-width="2" marker-end="url(#arrow)"/>

            <!-- Cytoskeletal Target Substrates -->
            <g transform="translate(500, 40)">
                <rect x="0" y="0" width="220" height="50" rx="6" fill="#1e293b" stroke="#E85D50" stroke-width="1.5"/>
                <text x="110" y="25" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">Myosin XI (MYA1 / XI-K)</text>
                <text x="110" y="40" fill="#F4A261" font-size="9" text-anchor="middle">Motor Domain Processivity</text>
                
                <rect x="0" y="70" width="220" height="50" rx="6" fill="#1e293b" stroke="#3FB6A8" stroke-width="1.5"/>
                <text x="110" y="95" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">MAP65-1 & SPR1</text>
                <text x="110" y="110" fill="#3FB6A8" font-size="9" text-anchor="middle">Microtubule Bundling & Skewing</text>

                <rect x="0" y="140" width="220" height="50" rx="6" fill="#1e293b" stroke="#9B5DE5" stroke-width="1.5"/>
                <text x="110" y="165" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">CESA / CSI1 Complexes</text>
                <text x="110" y="180" fill="#9B5DE5" font-size="9" text-anchor="middle">Cellulose Deposition Directionality</text>
            </g>

            <!-- Arrows to targets -->
            <path d="M 380 115 L 490 65" stroke="#3FB6A8" stroke-width="2"/>
            <path d="M 380 115 L 490 100" stroke="#3FB6A8" stroke-width="2"/>
            <path d="M 380 115 L 490 165" stroke="#3FB6A8" stroke-width="2"/>
        </svg>`
    }
};

export function initPathwayViewer() {
    const container = document.getElementById('pathway-diagram-container');
    const descBox = document.getElementById('pathway-description');
    if (!container || !descBox) return;

    function renderPathway(id) {
        const p = pathways[id];
        if (!p) return;
        container.innerHTML = p.svg;
        descBox.innerHTML = `<h4>${p.title}</h4><p>${p.desc}</p>`;

        ['btn-pathway-1', 'btn-pathway-2', 'btn-pathway-3'].forEach((btnId, idx) => {
            const btn = document.getElementById(btnId);
            if (btn) {
                if (idx + 1 === id) {
                    btn.className = 'btn-primary';
                } else {
                    btn.className = 'btn-secondary';
                }
            }
        });
    }

    const b1 = document.getElementById('btn-pathway-1');
    const b2 = document.getElementById('btn-pathway-2');
    const b3 = document.getElementById('btn-pathway-3');

    if (b1) b1.addEventListener('click', () => renderPathway(1));
    if (b2) b2.addEventListener('click', () => renderPathway(2));
    if (b3) b3.addEventListener('click', () => renderPathway(3));

    // Initial render
    renderPathway(1);
}

// Auto init
initPathwayViewer();
