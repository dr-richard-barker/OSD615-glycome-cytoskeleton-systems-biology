"""
05_network_modeling.py
Systems Biology Network Modeling of Cytoskeleton–Glycome Coupling in Spaceflight:
- Reconstructs Subcellular Compartmental Interactome across 5 distinct cellular zones:
  1. Golgi & Trans-Golgi Network (TGN)
  2. Cytoplasm & Actin Streaming Cables
  3. Cortical Microtubule Guide Array
  4. Plasma Membrane Complex
  5. Apoplastic Cell Wall Matrix
- Incorporates detailed Catalytic Reactions, Donor/Acceptor Substrates, and Products Made
- Generates Multi-Panel Publication Figure 5:
  * Panel A: Subcellular Compartmental Interactome Graph
  * Panel B: Enzymatic Reaction, Substrate, and Product Reference Matrix
- Exports Cytoscape.js JSON for the interactive web dashboard
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx

# Comprehensive biochemical catalog for all interactome nodes
BIOCHEMICAL_CATALOG = {
    # 1. Secondary & Primary Cellulose Synthases (Plasma Membrane)
    "CESA4": {
        "compartment": "Plasma Membrane",
        "subcellular_zone": "Plasma Membrane",
        "reaction": "β-(1,4)-D-glucan polymerization (Secondary Wall)",
        "substrates": "UDP-α-D-glucose (donor)",
        "products": "Crystalline cellulose microfibril (secondary wall) + UDP",
        "cofactors": "Mg2+, Cellobiose-lipid primer",
        "ec_number": "EC 2.4.1.12",
        "log2fc": 2.65
    },
    "CESA7": {
        "compartment": "Plasma Membrane",
        "subcellular_zone": "Plasma Membrane",
        "reaction": "β-(1,4)-D-glucan polymerization (Secondary Wall)",
        "substrates": "UDP-α-D-glucose (donor)",
        "products": "Crystalline cellulose microfibril (secondary wall) + UDP",
        "cofactors": "Mg2+",
        "ec_number": "EC 2.4.1.12",
        "log2fc": 2.45
    },
    "CESA1": {
        "compartment": "Plasma Membrane",
        "subcellular_zone": "Plasma Membrane",
        "reaction": "β-(1,4)-D-glucan polymerization (Primary Wall)",
        "substrates": "UDP-α-D-glucose (donor)",
        "products": "Primary wall amorphous/crystalline cellulose + UDP",
        "cofactors": "Mg2+",
        "ec_number": "EC 2.4.1.12",
        "log2fc": -0.85
    },
    "CESA3": {
        "compartment": "Plasma Membrane",
        "subcellular_zone": "Plasma Membrane",
        "reaction": "β-(1,4)-D-glucan polymerization (Primary Wall)",
        "substrates": "UDP-α-D-glucose (donor)",
        "products": "Primary wall cellulose microfibrils + UDP",
        "cofactors": "Mg2+",
        "ec_number": "EC 2.4.1.12",
        "log2fc": -0.72
    },
    "CSI1": {
        "compartment": "Plasma Membrane",
        "subcellular_zone": "Plasma Membrane",
        "reaction": "CSC-Microtubule physical linking & trajectory alignment",
        "substrates": "Plasma membrane CesA catalytic core + Cortical Microtubule",
        "products": "Guided, linear cellulose microfibril deposition trajectory",
        "cofactors": "Phospholipid binding (C2 domain)",
        "ec_number": "Structural Linker",
        "log2fc": -1.15
    },

    # 2. Golgi & Trans-Golgi Network Matrix Synthases
    "IRX9": {
        "compartment": "Golgi / TGN",
        "subcellular_zone": "Golgi Lumen",
        "reaction": "β-(1,4)-xylosyltransferase (Xylan backbone chain elongation)",
        "substrates": "UDP-α-D-xylose (donor) + (1,4)-β-D-xylan acceptor",
        "products": "Elongated (1,4)-β-D-xylan polysaccharide backbone + UDP",
        "cofactors": "Mn2+",
        "ec_number": "EC 2.4.2.24",
        "log2fc": 2.80
    },
    "IRX10": {
        "compartment": "Golgi / TGN",
        "subcellular_zone": "Golgi Lumen",
        "reaction": "Glycosyltransferase family 47 (Xylan backbone elongation)",
        "substrates": "UDP-α-D-xylose (donor) + Xylo-oligosaccharide acceptor",
        "products": "Linear xylan backbone polymer + UDP",
        "cofactors": "Mn2+",
        "ec_number": "EC 2.4.2.24",
        "log2fc": 2.35
    },
    "CSLC4": {
        "compartment": "Golgi / TGN",
        "subcellular_zone": "Golgi Lumen",
        "reaction": "β-(1,4)-glucan synthase (Xyloglucan backbone synthesis)",
        "substrates": "UDP-α-D-glucose (donor) + Oligo-glucan acceptor",
        "products": "Cellotetraose / xyloglucan glucan backbone + UDP",
        "cofactors": "Mg2+",
        "ec_number": "EC 2.4.1.12",
        "log2fc": 0.65
    },
    "GAUT1": {
        "compartment": "Golgi / TGN",
        "subcellular_zone": "Golgi Lumen",
        "reaction": "α-(1,4)-galacturonosyltransferase (Pectin HG synthesis)",
        "substrates": "UDP-D-galacturonic acid (donor) + Homogalacturonan chain",
        "products": "(1,4)-α-D-galacturonan (HG backbone) + UDP",
        "cofactors": "Mn2+",
        "ec_number": "EC 2.4.1.43",
        "log2fc": 0.45
    },
    "MUR3": {
        "compartment": "Golgi / TGN",
        "subcellular_zone": "Golgi Lumen",
        "reaction": "Galactosyltransferase (Xyloglucan side-chain galactosylation)",
        "substrates": "UDP-D-galactose + Xyloglucan side chain",
        "products": "Galactosylated xyloglucan (XLFG/XXLG) + UDP",
        "cofactors": "Mn2+",
        "ec_number": "EC 2.4.1.-",
        "log2fc": 0.52
    },

    # 3. Cytoplasm & Actin-Myosin Streaming Machinery
    "MYA1": {
        "compartment": "Cytoplasm",
        "subcellular_zone": "Actin Cables",
        "reaction": "High-velocity ATP-driven vesicle transport along F-actin",
        "substrates": "ATP + Mg2+ + Post-Golgi Secretory Vesicle Cargo",
        "products": "ADP + Pi + Directional mechanical motive force (~5-7 pN)",
        "cofactors": "Ca2+ / Calmodulin light chains",
        "ec_number": "EC 3.6.4.4",
        "log2fc": 2.15
    },
    "MYA2": {
        "compartment": "Cytoplasm",
        "subcellular_zone": "Actin Cables",
        "reaction": "Class XI Myosin motor organelle & vesicle streaming",
        "substrates": "ATP + F-actin tracks + Membrane vesicles",
        "products": "ADP + Pi + Rapid cytoplasmic streaming (~5-10 µm/s)",
        "cofactors": "Ca2+",
        "ec_number": "EC 3.6.4.4",
        "log2fc": 1.74
    },
    "XI-K": {
        "compartment": "Cytoplasm",
        "subcellular_zone": "Actin Cables",
        "reaction": "Primary driver of post-Golgi vesicle targeting & streaming",
        "substrates": "ATP + Rab-GTPase vesicle cargo complex",
        "products": "Targeted matrix vesicle delivery to plasma membrane",
        "cofactors": "Mg2+",
        "ec_number": "EC 3.6.4.4",
        "log2fc": 1.95
    },
    "ACT7": {
        "compartment": "Cytoplasm",
        "subcellular_zone": "Subcortical Cytoplasm",
        "reaction": "Filamentous actin (F-actin) track polymerization",
        "substrates": "G-actin-ATP monomers",
        "products": "Polarized F-actin double-helical cable tracks + ADP",
        "cofactors": "Mg2+, K+",
        "ec_number": "Structural Cytoskeleton",
        "log2fc": 1.25
    },
    "VLN1": {
        "compartment": "Cytoplasm",
        "subcellular_zone": "Actin Cables",
        "reaction": "Calcium-insensitive actin filament bundling & stabilization",
        "substrates": "Individual F-actin filaments",
        "products": "Thick longitudinal subcortical actin cables",
        "cofactors": "None (Ca2+-independent)",
        "ec_number": "Actin Bundler",
        "log2fc": 0.95
    },
    "PRF1": {
        "compartment": "Cytoplasm",
        "subcellular_zone": "Cytosol",
        "reaction": "G-actin ADP/ATP nucleotide exchange and barbed-end delivery",
        "substrates": "G-actin-ADP + ATP",
        "products": "G-actin-ATP:Profilin complex ready for Formin elongation",
        "cofactors": "PIP2 signaling",
        "ec_number": "Actin Monomer Regulator",
        "log2fc": 0.88
    },
    "ARP2": {
        "compartment": "Cytoplasm",
        "subcellular_zone": "Cortex / Cytosol",
        "reaction": "Actin filament branching nucleation at 70° angles",
        "substrates": "Mother F-actin filament + G-actin-ATP monomers",
        "products": "Branched 70° cortical actin filament network",
        "cofactors": "WASP/SCAR nucleation promoting factors",
        "ec_number": "Actin Nucleator",
        "log2fc": 0.65
    },
    "ARP3": {
        "compartment": "Cytoplasm",
        "subcellular_zone": "Cortex / Cytosol",
        "reaction": "Core subunit of heptameric ARP2/3 nucleation complex",
        "substrates": "Mother F-actin filament + G-actin",
        "products": "Branched daughter actin filaments",
        "cofactors": "ATP",
        "ec_number": "Actin Nucleator",
        "log2fc": 0.58
    },
    "FH1": {
        "compartment": "Cytoplasm",
        "subcellular_zone": "Plasma Membrane / Cortex",
        "reaction": "Processive unbranched actin cable elongation from membrane",
        "substrates": "Profilin-actin complexes + Membrane lipids",
        "products": "Fast-growing unbranched F-actin streaming tracks",
        "cofactors": "Rho/ROP GTPases",
        "ec_number": "Formin Nucleator",
        "log2fc": 0.72
    },

    # 4. Intracellular Glycosyltransferases (Cytosol / Nucleus)
    "SEC": {
        "compartment": "Cytoplasm",
        "subcellular_zone": "Nucleocytoplasm",
        "reaction": "Protein O-GlcNAcylation (O-GlcNAc transferase)",
        "substrates": "UDP-N-acetyl-D-glucosamine (donor) + Target Ser/Thr",
        "products": "O-GlcNAcylated motor/cytoskeletal target protein + UDP",
        "cofactors": "TPR repeat domain binding",
        "ec_number": "EC 2.4.1.255",
        "log2fc": 1.55
    },
    "SPY": {
        "compartment": "Cytoplasm",
        "subcellular_zone": "Nucleocytoplasm",
        "reaction": "Protein O-fucosylation / O-GlcNAc regulator",
        "substrates": "GDP-β-L-fucose / UDP-GlcNAc + Target Ser/Thr",
        "products": "O-fucosylated signaling & cytoskeletal proteins + GDP",
        "cofactors": "TPR repeat scaffold",
        "ec_number": "EC 2.4.1.-",
        "log2fc": 1.35
    },

    # 5. Cortical Microtubule Array & Kinesins
    "SPR1": {
        "compartment": "Cortical MTs",
        "subcellular_zone": "Microtubule Lattice",
        "reaction": "Cortical MT plus-end tracking & directional array stability",
        "substrates": "Polymerizing MT plus-ends (+TIPs) + Tubulin dimers",
        "products": "Stabilized, parallel transverse cortical MT array",
        "cofactors": "Phosphorylation / O-GlcNAc",
        "ec_number": "Microtubule Plus-End (+TIP)",
        "log2fc": -2.40
    },
    "MAP65-1": {
        "compartment": "Cortical MTs",
        "subcellular_zone": "Microtubule Lattice",
        "reaction": "Antiparallel cortical microtubule cross-linking & bundling",
        "substrates": "Adjacent cortical microtubule filaments",
        "products": "Ordered, bundled 25-nm spaced MT arrays",
        "cofactors": "Cyclin-dependent kinase (CDK) phosphorylation",
        "ec_number": "MT Crosslinker (MAP65)",
        "log2fc": -1.35
    },
    "CLASP": {
        "compartment": "Cortical MTs",
        "subcellular_zone": "Cell Cortex / MTs",
        "reaction": "Microtubule rescue factor and sharp cell-edge transition guide",
        "substrates": "Depolymerizing MT ends + Sharp membrane curvature",
        "products": "Suppression of MT catastrophe; seam-crossing MT arrays",
        "cofactors": "TOG domains",
        "ec_number": "+TIP Rescue Factor",
        "log2fc": -0.92
    },
    "MOR1": {
        "compartment": "Cortical MTs",
        "subcellular_zone": "Microtubule Lattice",
        "reaction": "Microtubule polymerase (XMAP215 family)",
        "substrates": "Free α/β-tubulin heterodimers-GTP",
        "products": "Rapid plus-end MT elongation (10-fold acceleration)",
        "cofactors": "TOG1-TOG5 domains",
        "ec_number": "MT Polymerase",
        "log2fc": -0.68
    },
    "FRA1": {
        "compartment": "Cortical MTs",
        "subcellular_zone": "Microtubule Lattice",
        "reaction": "Kinesin-4 motor directing cellulose microfibril order",
        "substrates": "ATP + Cortical Microtubule + Matrix vesicles",
        "products": "ADP + Pi + Oriented secondary wall microfibril packing",
        "cofactors": "Mg2+",
        "ec_number": "EC 3.6.4.4",
        "log2fc": 1.42
    },
    "KIN12A": {
        "compartment": "Cortical MTs",
        "subcellular_zone": "Phragmoplast / MTs",
        "reaction": "Phragmoplast & cortical kinesin motor transport",
        "substrates": "ATP + Plus-end oriented MT tracks",
        "products": "Targeted matrix vesicle delivery to cell division/expansion plate",
        "cofactors": "Mg2+",
        "ec_number": "EC 3.6.4.4",
        "log2fc": 1.82
    },
    "KIN14A": {
        "compartment": "Cortical MTs",
        "subcellular_zone": "Microtubule Lattice",
        "reaction": "Minus-end directed kinesin-14 motor array organizer",
        "substrates": "ATP + Overlapping MT filaments",
        "products": "Focused, convergent microtubule arrays",
        "cofactors": "Calmodulin-like tail domain",
        "ec_number": "EC 3.6.4.4",
        "log2fc": 1.45
    },

    # 6. Apoplastic Cell Wall Matrix Modifiers
    "XTH4": {
        "compartment": "Cell Wall",
        "subcellular_zone": "Apoplastic Matrix",
        "reaction": "Xyloglucan endotransglucosylase/hydrolase (XTH)",
        "substrates": "High-MW xyloglucan polymer + Xylo-oligosaccharide acceptor",
        "products": "Re-ligated / loosened xyloglucan-cellulose tether network",
        "cofactors": "Apoplastic pH (5.0 - 5.5)",
        "ec_number": "EC 2.4.1.207",
        "log2fc": 1.85
    },
    "EXPA1": {
        "compartment": "Cell Wall",
        "subcellular_zone": "Apoplastic Matrix",
        "reaction": "Non-enzymatic cell wall loosening (hydrogen-bond disruption)",
        "substrates": "Cellulose-xyloglucan non-covalent junction zones",
        "products": "Turgor-driven irreversible cell wall creep & expansion",
        "cofactors": "Acidic apoplastic pH (< 5.5)",
        "ec_number": "Wall Loosening Protein",
        "log2fc": 1.65
    },
    "PME3": {
        "compartment": "Cell Wall",
        "subcellular_zone": "Apoplastic Matrix",
        "reaction": "Pectin methylesterase (Demethylesterification of HG)",
        "substrates": "Methyl-esterified homogalacturonan (HG) pectin",
        "products": "De-esterified HG + Methanol (facilitates Ca2+ crosslinking / pectin gelation)",
        "cofactors": "Apoplastic cations",
        "ec_number": "EC 3.1.1.11",
        "log2fc": 0.78
    }
}

def run_network_modeling():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fig_dir = os.path.join(base_dir, 'analysis', 'figures')
    docs_dir = os.path.join(base_dir, 'docs', 'data')
    manuscript_fig_dir = os.path.join(base_dir, 'manuscript', 'figures')
    docs_fig_dir = os.path.join(base_dir, 'docs', 'figures')
    
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(manuscript_fig_dir, exist_ok=True)
    os.makedirs(docs_fig_dir, exist_ok=True)

    print("Reconstructing Subcellular Compartmental Systems Interactome...")

    # Build High-Confidence Functional Interaction Graph
    interactions = [
        # Golgi & Trans-Golgi Network interactions
        ("IRX9", "IRX10", 0.98, "Golgi Core Xylan Synthase Complex"),
        ("IRX9", "CSLC4", 0.75, "Hemicellulose Matrix Coordination"),
        ("IRX10", "GAUT1", 0.72, "Matrix Polysaccharide Packaging"),
        ("CSLC4", "MUR3", 0.85, "Xyloglucan Backbone Galactosylation"),
        
        # Golgi-to-Vesicle-to-Myosin Coupling
        ("IRX9", "MYA1", 0.82, "Post-Golgi Matrix Vesicle Loading"),
        ("IRX10", "MYA2", 0.79, "Secretory Vesicle Translocation"),
        ("CSLC4", "XI-K", 0.84, "XG Vesicle Targeting to Membrane"),
        
        # Actin-Myosin Secretory Streaming Cable
        ("MYA1", "MYA2", 0.95, "Class XI Myosin Heterodimer Streaming"),
        ("MYA1", "XI-K", 0.93, "Post-Golgi Vesicle Motility"),
        ("MYA1", "ACT7", 0.96, "Actin-Activated ATP Hydrolysis"),
        ("MYA2", "VLN1", 0.86, "Subcortical Cable Translocation"),
        ("ACT7", "VLN1", 0.94, "Longitudinal Actin Cable Bundling"),
        ("ACT7", "PRF1", 0.91, "G-Actin Monomer Sequestration & Feeding"),
        ("FH1", "ACT7", 0.95, "Formin-Mediated Cable Nucleation"),
        ("FH1", "PRF1", 0.88, "Profilin-Actin Polymerization"),
        ("ARP2", "ARP3", 0.99, "ARP2/3 Branching Complex"),
        ("ARP2", "ACT7", 0.92, "70° Actin Branching Nucleation"),
        
        # Intracellular Glycosylation Regulatory Axis (SEC / SPY)
        ("SEC", "MYA1", 0.88, "O-GlcNAcylation of Myosin Motor"),
        ("SEC", "KIN14A", 0.82, "O-GlcNAcylation of Kinesin Motor"),
        ("SEC", "MAP65-1", 0.85, "O-GlcNAcylation of MT Bundler"),
        ("SPY", "SPR1", 0.84, "Intracellular Glycosylation of Plus-End Tracker"),
        ("SPY", "CSI1", 0.80, "O-Fucosylation of CSC Guide Linker"),
        ("SEC", "SPY", 0.92, "Co-regulatory Glycosylation Cascade"),
        
        # Cortical Microtubule Array & Plus-End Steering
        ("SPR1", "CLASP", 0.94, "Cortical MT Plus-End Tracking (+TIP)"),
        ("SPR1", "MOR1", 0.90, "MT Polymerase Acceleration"),
        ("CLASP", "MAP65-1", 0.87, "Edge-Crossing MT Array Anchoring"),
        ("MAP65-1", "KIN14A", 0.83, "Antiparallel MT Bundle Organization"),
        ("FRA1", "MAP65-1", 0.81, "Kinesin-4 MT Lattice Crosslinking"),
        ("KIN12A", "CLASP", 0.78, "Phragmoplast MT Motor Docking"),
        
        # Plasma Membrane: CSC Complexes & CSI1 Guidance
        ("CSI1", "CESA1", 0.99, "CSI1/POM2 Guiding Primary Wall CSC"),
        ("CSI1", "CESA3", 0.98, "CSI1/POM2 Guiding Primary Wall CSC"),
        ("CSI1", "CESA7", 0.92, "CSI1/POM2 Guiding Secondary Wall CSC"),
        ("CSI1", "SPR1", 0.86, "Cortical MT-to-CSC Trajectory Coordination"),
        ("CESA1", "CESA3", 0.99, "Catalytic Primary Wall CSC Rosette"),
        ("CESA4", "CESA7", 0.99, "Catalytic Secondary Wall CSC Rosette"),
        ("FRA1", "CSI1", 0.85, "Kinesin-4 Driven CSC Insertion"),
        
        # Apoplastic Cell Wall Matrix Assembly & Loosening
        ("CESA1", "XTH4", 0.84, "Cellulose-Xyloglucan Network Interweaving"),
        ("CESA7", "IRX9", 0.89, "Vascular Secondary Wall Co-deposition"),
        ("XTH4", "EXPA1", 0.88, "Coordinated Acid Growth Wall Loosening"),
        ("PME3", "EXPA1", 0.82, "Pectin De-esterification & Wall Porosity"),
        ("GAUT1", "PME3", 0.80, "Pectin Secretion & Maturation")
    ]

    G = nx.Graph()
    for symbol, data in BIOCHEMICAL_CATALOG.items():
        G.add_node(
            symbol,
            label=symbol,
            compartment=data['compartment'],
            subcellular_zone=data['subcellular_zone'],
            reaction=data['reaction'],
            substrates=data['substrates'],
            products=data['products'],
            cofactors=data['cofactors'],
            ec_number=data['ec_number'],
            log2fc=data['log2fc']
        )

    for src, tgt, score, itype in interactions:
        if src in G and tgt in G:
            G.add_edge(src, tgt, weight=score, score=score, interaction_type=itype)

    print(f"Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} interactions.")

    # Export Cytoscape.js format JSON with rich biochemical metadata
    cyto_elements = {"nodes": [], "edges": []}
    for n in G.nodes():
        d = G.nodes[n]
        color = '#E85D50' if d['log2fc'] > 1.0 else '#3FB6A8' if d['log2fc'] < -0.5 else '#F59E0B'
        cyto_elements["nodes"].append({
            "data": {
                "id": n,
                "label": n,
                "compartment": d['compartment'],
                "subcellular_zone": d['subcellular_zone'],
                "reaction": d['reaction'],
                "substrates": d['substrates'],
                "products": d['products'],
                "cofactors": d['cofactors'],
                "ec_number": d['ec_number'],
                "log2fc": d['log2fc'],
                "color": color
            }
        })

    for u, v, d in G.edges(data=True):
        cyto_elements["edges"].append({
            "data": {
                "id": f"{u}_{v}",
                "source": u,
                "target": v,
                "score": d['score'],
                "interaction_type": d['interaction_type']
            }
        })

    with open(os.path.join(docs_dir, 'network_graph.json'), 'w', encoding='utf-8') as f:
        json.dump({"elements": cyto_elements}, f, indent=2)

    # ------------------ MULTI-PANEL PUBLICATION FIGURE 5 ------------------
    fig = plt.figure(figsize=(18, 13), dpi=300)
    fig.patch.set_facecolor('#ffffff')

    # PANEL A: Subcellular Compartmental Interactome Graph
    ax_net = fig.add_axes([0.04, 0.40, 0.92, 0.56])
    ax_net.set_title("A | Subcellular Compartmental Systems Interactome: Cytoskeleton-to-Cell-Wall Coupling", 
                     fontsize=13, fontweight='bold', color='#004D73', pad=15)
    ax_net.axis('off')

    # Draw Subcellular Compartment Background Zones
    zones = [
        {"name": "1. Golgi & Trans-Golgi Network (TGN)\n[Matrix Hemicellulose & Pectin Synthesis]", "x": 0.02, "w": 0.17, "color": "#FEF3C7", "border": "#D97706"},
        {"name": "2. Cytoplasm & Subcortical Cables\n[Actin-Myosin Streaming & O-GlcNAc]", "x": 0.21, "w": 0.25, "color": "#FEE2E2", "border": "#DC2626"},
        {"name": "3. Cortical Microtubule Array\n[MT Lattice Alignment & Kinesins]", "x": 0.48, "w": 0.20, "color": "#CCFBF1", "border": "#0D9488"},
        {"name": "4. Plasma Membrane\n[CesA Rosettes & CSI1 Guide Linker]", "x": 0.70, "w": 0.13, "color": "#E0E7FF", "border": "#4F46E5"},
        {"name": "5. Apoplastic Cell Wall\n[Matrix Assembly & Creep Loosening]", "x": 0.85, "w": 0.13, "color": "#F1F5F9", "border": "#475569"}
    ]

    for z in zones:
        rect = patches.Rectangle((z["x"], 0.02), z["w"], 0.96, transform=ax_net.transAxes, 
                                 facecolor=z["color"], edgecolor=z["border"], linewidth=1.8, linestyle='--', alpha=0.55, zorder=1)
        ax_net.add_patch(rect)
        ax_net.text(z["x"] + z["w"]/2, 0.95, z["name"], transform=ax_net.transAxes, 
                    fontsize=8.5, fontweight='bold', color=z["border"], ha='center', va='top', linespacing=1.2)

    # Defined Compartmental Layout Coordinates (x, y)
    fixed_pos = {
        # 1. Golgi / TGN
        "IRX9": (0.07, 0.75), "IRX10": (0.13, 0.75), "CSLC4": (0.06, 0.45), "GAUT1": (0.14, 0.45), "MUR3": (0.10, 0.20),
        # 2. Cytoplasm & Actin Cables
        "MYA1": (0.26, 0.78), "MYA2": (0.33, 0.78), "XI-K": (0.40, 0.78),
        "ACT7": (0.28, 0.50), "VLN1": (0.38, 0.50), "PRF1": (0.24, 0.30), "FH1": (0.34, 0.30),
        "ARP2": (0.42, 0.30), "ARP3": (0.43, 0.15),
        "SEC": (0.25, 0.12), "SPY": (0.34, 0.12),
        # 3. Cortical MTs
        "SPR1": (0.52, 0.75), "MAP65-1": (0.62, 0.75), "CLASP": (0.57, 0.52), "MOR1": (0.51, 0.32),
        "FRA1": (0.64, 0.52), "KIN12A": (0.58, 0.20), "KIN14A": (0.64, 0.20),
        # 4. Plasma Membrane
        "CSI1": (0.74, 0.75), "CESA1": (0.79, 0.60), "CESA3": (0.79, 0.42), "CESA4": (0.73, 0.28), "CESA7": (0.79, 0.20),
        # 5. Cell Wall
        "XTH4": (0.91, 0.75), "EXPA1": (0.91, 0.50), "PME3": (0.91, 0.25)
    }

    # Draw Edges
    for u, v, d in G.edges(data=True):
        p1 = fixed_pos[u]
        p2 = fixed_pos[v]
        score = d['score']
        ax_net.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#475569', alpha=0.45, 
                    linewidth=0.8 + (score - 0.7) * 4, linestyle='-', zorder=2)

    # Draw Nodes
    for n in G.nodes():
        pos = fixed_pos[n]
        d = G.nodes[n]
        fc = d['log2fc']
        node_color = '#E85D50' if fc > 1.0 else '#3FB6A8' if fc < -0.5 else '#F59E0B'
        
        # Node circle
        circ = patches.Circle(pos, 0.022, facecolor=node_color, edgecolor='#004D73', linewidth=1.5, zorder=3)
        ax_net.add_patch(circ)
        
        # Label
        ax_net.text(pos[0], pos[1], n, fontsize=8, fontweight='bold', color='#ffffff', ha='center', va='center', zorder=4)
        
        # Log2FC badge below node
        fc_str = f"+{fc:.2f}" if fc > 0 else f"{fc:.2f}"
        ax_net.text(pos[0], pos[1] - 0.035, fc_str, fontsize=6.5, fontweight='bold', 
                    color='#004D73' if abs(fc) < 1 else '#991B1B' if fc > 0 else '#0F766E', ha='center', zorder=4)

    # PANEL B: Biochemical Substrate, Catalytic Reaction, and Product Reference Matrix
    ax_tab = fig.add_axes([0.04, 0.04, 0.92, 0.32])
    ax_tab.set_title("B | Catalytic Reactions, Donor/Acceptor Substrates, and Products of Key Nodes", 
                     fontsize=11.5, fontweight='bold', color='#004D73', pad=8)
    ax_tab.axis('off')

    table_data = [
        ["Gene", "Subcellular Site", "Catalytic Reaction / Biochemical Function", "Donor / Required Substrates", "Products Made & Physiological Role"],
        ["CESA4/7", "Plasma Membrane", "β-(1,4)-D-glucan polymerization (Secondary Wall)", "UDP-α-D-glucose + Mg2+", "Crystalline cellulose microfibril; xylem vessel wall thickening (+192% CCRC-M140 xylan co-deposition)"],
        ["IRX9/10", "Golgi Lumen", "β-(1,4)-xylosyltransferase (Xylan elongation)", "UDP-α-D-xylose + (1,4)-β-D-xylan", "Glucuronoxylan backbone polymer; co-upregulated with CESA4/7 in spaceflight roots (+2.80 log2FC)"],
        ["MYA1/2", "Actin Cables", "Class XI Myosin motor vesicle translocation", "ATP + Mg2+ + Post-Golgi Cargo", "ADP + Pi + Directional mechanical motive force (~5 pN); speeds vesicle delivery to plasma membrane"],
        ["SEC / SPY", "Nucleocytoplasm", "O-GlcNAc transferase / O-Fucosyltransferase", "UDP-GlcNAc / GDP-Fucose + Ser/Thr", "O-GlcNAcylated / O-fucosylated motors (MYA1, KIN14A, MAP65-1); modulates motor processivity and MT stability"],
        ["SPR1", "Cortical MTs", "Plus-end tracking (+TIP) and array alignment", "Polymerizing MT plus-ends (+TIPs)", "Stabilized parallel MT arrays; spaceflight downregulation (-2.40 log2FC) causes CMT disorientation"],
        ["CSI1", "Plasma Membrane", "CSC-Microtubule physical linking & steering", "Plasma membrane CesA + Cortical MT", "Linear cellulose microfibril alignment along cortical MT guide tracks; bridges MT lattice to CesA"],
        ["XTH4", "Apoplastic Wall", "Xyloglucan endotransglucosylation (XET)", "High-MW XG + Xylo-oligosaccharides", "Cleaved and re-ligated xyloglucan cross-links; permits turgor-driven cell wall remodeling & creep"]
    ]

    tab = ax_tab.table(cellText=table_data, loc='center', cellLoc='left', colWidths=[0.08, 0.12, 0.28, 0.24, 0.28])
    tab.auto_set_font_size(False)
    tab.set_fontsize(7.5)
    tab.scale(1.0, 1.42)

    # Style table header and cells
    for (r, c), cell in tab.get_celld().items():
        if r == 0:
            cell.set_facecolor('#004D73')
            cell.set_text_props(color='#ffffff', weight='bold')
        else:
            cell.set_facecolor('#F8FAFC' if r % 2 == 0 else '#ffffff')
            cell.set_edgecolor('#CBD5E1')
            if c == 0:
                cell.set_text_props(weight='bold', color='#004D73')

    fig5_out = os.path.join(fig_dir, '05_cytoskeleton_glycome_interactome.png')
    fig.savefig(fig5_out, dpi=300, bbox_inches='tight')
    plt.close()

    # Synchronize to docs/figures and manuscript/figures
    import shutil
    shutil.copy(fig5_out, os.path.join(manuscript_fig_dir, '05_cytoskeleton_glycome_interactome.png'))
    shutil.copy(fig5_out, os.path.join(docs_fig_dir, '05_cytoskeleton_glycome_interactome.png'))

    print(f"Successfully generated expanded Figure 5: {fig5_out}")

if __name__ == '__main__':
    run_network_modeling()
