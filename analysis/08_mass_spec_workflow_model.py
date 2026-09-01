"""
08_mass_spec_workflow_model.py
Mass Spectrometry & Glycomics Workflow Modeling:
1. O-GlcNAc Motor Complex Site-Mapping Workflow (EThcD / Lectin / Click-Chemistry)
2. CCRC Plant Cell Wall Glycome Profiling (Sequential Chemical Fractionation & ELISA)
3. Proposed Integrative Cytoskeleton–Glycoproteomics Mass Spectrometry Architecture
- Publication Workflow Diagrams (Matplotlib)
- Pre-computed JSON export for interactive web step-through
"""

import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_ms_workflows():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fig_dir = os.path.join(base_dir, 'analysis', 'figures')
    results_dir = os.path.join(base_dir, 'analysis', 'results')
    docs_dir = os.path.join(base_dir, 'docs', 'data')
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)

    print("Generating Mass Spectrometry workflow diagrams...")

    # 1. Publication Figure: 3-Panel High-Resolution Architecture
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))

    # Workflow 1: O-GlcNAc Motor Mapping
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 3)
    ax1.axis('off')
    ax1.set_title('A. Mass Spectrometry Workflow for O-GlcNAcylation Mapping on Motor Complexes (Actin / Tubulin / Dynein / Kinesin)', fontsize=11, fontweight='bold', loc='left', color='#2F5985')
    
    steps_1 = [
        ("1. Protein Extraction\n& Lysis", "Native isolation of\nmotor complexes\n(Myosins, Dynactin, KIFs)"),
        ("2. Glyco-Enrichment", "sWGA Lectin Affinity or\nMetabolic Click-Chemistry\n(UDP-GalNAz / BEMAD)"),
        ("3. Dual Digestion", "Sequential Trypsin +\nGlu-C digestion for\noptimal site coverage"),
        ("4. EThcD LC-MS/MS", "Electron-Transfer/\nHCD Fragmentation\n(Preserves labile O-GlcNAc)"),
        ("5. PTM Site Mapping", "Byonic / O-GlcNAcAtlas\nlocalization & crosstalk\nwith phosphorylation")
    ]
    for i, (title, desc) in enumerate(steps_1):
        x = i * 2.0 + 0.2
        rect = patches.FancyBboxPatch((x, 0.4), 1.6, 2.0, boxstyle="round,pad=0.1", fc="#EBF2FA", ec="#2F5985", lw=1.5)
        ax1.add_patch(rect)
        ax1.text(x + 0.8, 1.8, title, ha='center', va='center', fontsize=9, fontweight='bold', color='#2F5985')
        ax1.text(x + 0.8, 1.0, desc, ha='center', va='center', fontsize=8, color='#333333')
        if i < 4:
            ax1.annotate('', xy=(x + 1.95, 1.4), xytext=(x + 1.65, 1.4), arrowprops=dict(arrowstyle="->", color="#E85D50", lw=2))

    # Workflow 2: Plant Cell Wall Glycome Profiling (OSD-615)
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 3)
    ax2.axis('off')
    ax2.set_title('B. CCRC High-Throughput Glycome Profiling Workflow (NASA OSD-615 / APEX-03-1)', fontsize=11, fontweight='bold', loc='left', color='#2A9D8F')
    
    steps_2 = [
        ("1. Alcohol Insoluble\nResidue (AIR)", "Liquid N2 ground roots;\nremoval of small\nmetabolites / pigments"),
        ("2. Sequential Extraction", "Oxalate → Na2CO3 →\n1M KOH → 4M KOH →\nChlorite → post-chlorite"),
        ("3. Dialysis & Plating", "Exhaustive dialysis\nagainst ddH2O &\n384-well plate coating"),
        ("4. Automated ELISA", "155 Monoclonal mAbs\nscreening non-cellulosic\nmatrix epitopes"),
        ("5. Heatmap Generation", "Optical density (OD450)\nreflects epitope extractability\n& wall remodeling")
    ]
    for i, (title, desc) in enumerate(steps_2):
        x = i * 2.0 + 0.2
        rect = patches.FancyBboxPatch((x, 0.4), 1.6, 2.0, boxstyle="round,pad=0.1", fc="#E8F8F5", ec="#2A9D8F", lw=1.5)
        ax2.add_patch(rect)
        ax2.text(x + 0.8, 1.8, title, ha='center', va='center', fontsize=9, fontweight='bold', color='#2A9D8F')
        ax2.text(x + 0.8, 1.0, desc, ha='center', va='center', fontsize=8, color='#333333')
        if i < 4:
            ax2.annotate('', xy=(x + 1.95, 1.4), xytext=(x + 1.65, 1.4), arrowprops=dict(arrowstyle="->", color="#E76F51", lw=2))

    # Workflow 3: Proposed Integrative Glycoproteomics Architecture
    ax3 = axes[2]
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 3)
    ax3.axis('off')
    ax3.set_title('C. Proposed Systems Biology Framework: Spaceflight Plant Glycome–Cytoskeleton Multi-Omics Integration', fontsize=11, fontweight='bold', loc='left', color='#6A4C93')
    
    steps_3 = [
        ("1. Flight Harvest\n(Veggie / ISS)", "Synchronous ground control;\nRNAlater & aldehyde fixation\nin KFT hardware"),
        ("2. Parallel Omics", "Cell wall glycomics (ELISA)\n+ RNA-Seq transcriptomics\n+ Target Proteomics"),
        ("3. Statistical Integration", "mixOmics (DIABLO / sPLS)\n+ MOFA2 latent factors\n+ WGCNA module eigengenes"),
        ("4. Network Topology", "AraNet / STRING PPI\n+ OmicsIntegrator PCST\n(Hidden signaling nodes)"),
        ("5. Dynamic Modeling", "Cytosim / MEDYAN\nstochastic particle simulation\nof vesicle trafficking")
    ]
    for i, (title, desc) in enumerate(steps_3):
        x = i * 2.0 + 0.2
        rect = patches.FancyBboxPatch((x, 0.4), 1.6, 2.0, boxstyle="round,pad=0.1", fc="#F3EBF6", ec="#6A4C93", lw=1.5)
        ax3.add_patch(rect)
        ax3.text(x + 0.8, 1.8, title, ha='center', va='center', fontsize=9, fontweight='bold', color='#6A4C93')
        ax3.text(x + 0.8, 1.0, desc, ha='center', va='center', fontsize=8, color='#333333')
        if i < 4:
            ax3.annotate('', xy=(x + 1.95, 1.4), xytext=(x + 1.65, 1.4), arrowprops=dict(arrowstyle="->", color="#3A86FF", lw=2))

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '08_mass_spec_and_glycomics_workflows.png'), dpi=300)
    plt.close()
    print("Saved 08_mass_spec_and_glycomics_workflows.png")

    # 2. Export JSON for Interactive Dashboard Step-Through
    workflow_json = {
        "workflows": [
            {
                "id": "oglcnac_ms",
                "title": "Intracellular O-GlcNAc Mass Spectrometry on Motor Complexes",
                "steps": [
                    {"step": 1, "name": "Protein Extraction & Immunoprecipitation", "details": "Native lysis of root or cell cultures to preserve cytoskeletal complexes (e.g. Myosin XI, Dynactin p150Glued, Kinesin-4/12). OGA inhibitor (Thiamet-G) added to prevent post-lysis deglycosylation."},
                    {"step": 2, "name": "Chemoenzymatic or Lectin Enrichment", "details": "Concanavalin A (ConA) or succinylated Wheat Germ Agglutinin (sWGA) affinity chromatography, or metabolic labeling with UDP-GalNAz followed by copper-free click chemistry biotinylation."},
                    {"step": 3, "name": "Protease Digestion (Trypsin / Glu-C)", "details": "Orthogonal protease digestion to produce ideal peptide lengths (8-25 amino acids) surrounding Ser/Thr O-GlcNAc sites in motor neck and tail domains."},
                    {"step": 4, "name": "Stepped HCD-EThcD Mass Spectrometry", "details": "Electron-Transfer/Higher-Energy Collision Dissociation (EThcD) fragmentation preserves the labile glycosidic bond (GlcNAc oxonium ion at m/z 204.08) while fragmenting peptide backbone c/z ions for unambiguous site localization."},
                    {"step": 5, "name": "Database Search & Yin-Yang Phosphorylation Mapping", "details": "Byonic and O-GlcNAcAtlas spectral matching. Evaluation of reciprocal O-GlcNAcylation vs phosphorylation switches regulating motor processivity."}
                ]
            },
            {
                "id": "ccrc_glycomics",
                "title": "CCRC High-Throughput Glycome Profiling (OSD-615)",
                "steps": [
                    {"step": 1, "name": "Alcohol Insoluble Residue (AIR) Preparation", "details": "Root tissues from ISS spaceflight and KSC ground controls are homogenized in liquid N2 and washed with ethanol, chloroform, and acetone to isolate cell wall structural matrix."},
                    {"step": 2, "name": "Sequential Chemical Fractionation", "details": "Six-stage chemical extraction: 50mM CDTA (pectin) → 50mM Na2CO3 (pectin) → 1M KOH (loosely bound hemicellulose) → 4M KOH (tightly bound hemicellulose) → Chlorite (lignin) → 4M KOH post-chlorite."},
                    {"step": 3, "name": "Dialysis, Lyophilization & 384-Well Coating", "details": "Extracts are dialyzed exhaustively against water to remove extraction salts and coated at standardized carbohydrate concentrations onto 384-well microplates."},
                    {"step": 4, "name": "Robotic ELISA with 155 Monoclonal mAbs", "details": "Automated ELISA workstation screens the extract against 155 glycan-directed monoclonal antibodies targeting xyloglucan, xylan, HG, RG-I, and AGP epitopes."},
                    {"step": 5, "name": "Optical Density Quantitation & Heatmap Generation", "details": "OD450 optical absorbance quantifies relative epitope abundance across ground and microgravity treatments."}
                ]
            },
            {
                "id": "systems_integration",
                "title": "Systems Biology Multi-Omics & Dynamic Simulation",
                "steps": [
                    {"step": 1, "name": "Data Curation & Harmonization", "details": "Integration of OSD-615 glycomics with companion Veggie RNA-Seq (OSD-218/217) and metadata."},
                    {"step": 2, "name": "Sparse PLS & Factorization", "details": "mixOmics sPLS-DA and Bayesian MOFA2 factorization to find shared variance across transcripts and wall epitopes."},
                    {"step": 3, "name": "Interactome Modeling (STRING / AraNet)", "details": "Network topology connecting differentially expressed kinesins/myosins with matrix synthases."},
                    {"step": 4, "name": "Dynamic Vesicle Transport Simulation", "details": "Stochastic Monte Carlo modeling of motor-driven secretory vesicle flux to cell plate and cell wall in microgravity."}
                ]
            }
        ]
    }

    with open(os.path.join(docs_dir, 'mass_spec_workflow.json'), 'w') as f:
        json.dump(workflow_json, f, indent=2)
    with open(os.path.join(results_dir, 'mass_spec_workflow.json'), 'w') as f:
        json.dump(workflow_json, f, indent=2)

    print("Mass spectrometry workflow modeling completed successfully.")

if __name__ == '__main__':
    generate_ms_workflows()
