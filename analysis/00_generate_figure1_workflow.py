"""
00_generate_figure1_workflow.py
Generates publication Figure 1 (01_experimental_design_and_workflow.png):
Multi-Scale Systems Biology Workflow and Experimental Architecture for Spaceflight Glycomics.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil

def generate_figure1():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fig_dir = os.path.join(base_dir, 'analysis', 'figures')
    docs_fig_dir = os.path.join(base_dir, 'docs', 'figures')
    manuscript_fig_dir = os.path.join(base_dir, 'manuscript', 'figures')

    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(docs_fig_dir, exist_ok=True)
    os.makedirs(manuscript_fig_dir, exist_ok=True)

    print("Generating Figure 1: Systems Biology Workflow & Experimental Architecture...")

    fig = plt.figure(figsize=(19, 10.5), dpi=300)
    fig.patch.set_facecolor('#070d18')

    # Main Title
    fig.text(0.5, 0.96, "Figure 1 | Multi-Scale Systems Biology Workflow & Experimental Architecture (NASA OSD-615 / APEX-03-1)", 
             fontsize=16, fontweight='bold', color='#ffffff', ha='center')
    fig.text(0.5, 0.93, "End-to-end integration of spaceflight glycome ELISA profiling, companion transcriptomics, single-cell atlas mapping, and AI foundation models", 
             fontsize=10.5, color='#94a3b8', ha='center')

    # 4 Main Panels across the canvas
    panel_coords = [
        {"x": 0.03, "w": 0.22, "title": "A | Spaceflight Hardware & Sampling", "tag": "NASA OSD-615 / APEX-03-1", "color": "#0284c7"},
        {"x": 0.27, "w": 0.22, "title": "B | Sequential CCRC Glycome Profiling", "tag": "155 Monoclonal Antibodies", "color": "#E85D50"},
        {"x": 0.51, "w": 0.22, "title": "C | Multi-Omics & Single-Cell Spatial", "tag": "Salk Atlas & ggPlantmap", "color": "#3FB6A8"},
        {"x": 0.75, "w": 0.22, "title": "D | Systems Interactome & AI Models", "tag": "Monte Carlo & TabPFN (Nature 2025)", "color": "#8B5CF6"}
    ]

    for p in panel_coords:
        # Container Card
        rect = patches.FancyBboxPatch((p['x'], 0.06), p['w'], 0.83, boxstyle="round,pad=0.015,rounding_size=0.02",
                                      facecolor='#0f1c2e', edgecolor=p['color'], linewidth=2.0, transform=fig.transFigure)
        fig.patches.append(rect)

        # Header Badge
        fig.text(p['x'] + 0.015, 0.855, p['title'], fontsize=11, fontweight='bold', color='#ffffff')
        fig.text(p['x'] + 0.015, 0.832, p['tag'], fontsize=8.5, fontweight='bold', color=p['color'])

    # ---------------- PANEL A CONTENT ----------------
    xA = panel_coords[0]['x'] + 0.015
    items_A = [
        ("[Flight Environment]", "ISS Veggie Facility (0g Microgravity)\nLow Earth Orbit, 400 km altitude\nSynchronous KSC 1g Ground Controls"),
        ("[Plant Biological Model]", "Arabidopsis thaliana (Col-0 WT)\nRoots harvested at 6-day (early)\nand 11-day (maturation) post-germ"),
        ("[Experimental Design]", "12 Biological Replicate Samples:\n• 3x Spaceflight 6-day (R1, R3, R6)\n• 3x Spaceflight 11-day (R5, R8, R12)\n• 3x Ground Control 6-day (R7, R10, R11)\n• 3x Ground Control 11-day (R2, R4, R9)"),
        ("[NASA OSDR Repositories]", "OSD-615 (GLDS-598 Glycomics)\nOSD-218 (Veggie RNA-Seq Transcripts)\nOSD-217 (Veggie Methylome & DEG)")
    ]
    y = 0.77
    for title, desc in items_A:
        box = patches.FancyBboxPatch((xA, y - 0.12), 0.19, 0.13, boxstyle="round,pad=0.008,rounding_size=0.01",
                                     facecolor='#16263d', edgecolor=(1.0, 1.0, 1.0, 0.15), linewidth=1.0, transform=fig.transFigure)
        fig.patches.append(box)
        fig.text(xA + 0.008, y - 0.025, title, fontsize=9.5, fontweight='bold', color='#38bdf8')
        fig.text(xA + 0.008, y - 0.105, desc, fontsize=8.0, color='#cbd5e1', linespacing=1.25)
        y -= 0.175

    # ---------------- PANEL B CONTENT ----------------
    xB = panel_coords[1]['x'] + 0.015
    items_B = [
        ("[Sequential Wall Extraction]", "6 Chemical Reagent Fractions:\n1. 50mM CDTA (Pectin loosening)\n2. 1M KOH (Non-fucosylated XG)\n3. 4M KOH (Tight Xylan & XG)\n4. 100mM NaClO2 (Lignin/Phenolics)\n5. 4M KOHPC (Crystalline matrix)\n6. 0.1M H2SO4 (Residual matrix)"),
        ("[155 Monoclonal Antibodies]", "High-Throughput ELISA (OD450):\n• Xylan/Arabinoxylan (CCRC-M140, M138)\n• Xyloglucan (CCRC-M1, M84, M95)\n• Arabinogalactan Proteins (JIM13, JIM14)\n• Pectin HG & RG-I (JIM5, JIM7, CCRC-M38)"),
        ("[Automated Data Ingestion]", "NASA OSDR REST API Ingestion\nFrictionless CSV Matrices & JSON\nFull FAIR Compliance (RO-Crate 1.1)"),
        ("[Statistical Framework]", "Two-Way ANOVA (Flight × Age)\nBenjamini-Hochberg FDR (q < 0.01)\nCohen's d Effect Size Estimation")
    ]
    y = 0.77
    for title, desc in items_B:
        box = patches.FancyBboxPatch((xB, y - 0.12), 0.19, 0.13, boxstyle="round,pad=0.008,rounding_size=0.01",
                                     facecolor='#16263d', edgecolor=(1.0, 1.0, 1.0, 0.15), linewidth=1.0, transform=fig.transFigure)
        fig.patches.append(box)
        fig.text(xB + 0.008, y - 0.025, title, fontsize=9.5, fontweight='bold', color='#f87171')
        fig.text(xB + 0.008, y - 0.105, desc, fontsize=8.0, color='#cbd5e1', linespacing=1.25)
        y -= 0.175

    # ---------------- PANEL C CONTENT ----------------
    xC = panel_coords[2]['x'] + 0.015
    items_C = [
        ("[Multi-Omics Integration]", "Supervised sparse PLS (mixOmics)\nCross-correlates 155 glycan vectors\nwith 28 cytoskeletal motor/synthase\ntranscripts (MYA1, CESA4, SPR1)"),
        ("[Salk Single-Cell Atlas]", "Lee et al. (Nature Plants 2025)\nsnRNA-Seq resolution across 14 root cell\ntypes (protoxylem, metaxylem, cortex,\nepidermis, elongation zone)"),
        ("[ggPlantmap Vector Anatomy]", "Spatial projection onto anatomical root\ncross-sections and longitudinal tips.\nMetaxylem xylan accumulation hub"),
        ("[In Situ IHC Confocal Archive]", "Nakashima et al. (PMC10444889)\n30+ mAb confocal immunofluorescence\nvalidation (+192% xylem xylan)")
    ]
    y = 0.77
    for title, desc in items_C:
        box = patches.FancyBboxPatch((xC, y - 0.12), 0.19, 0.13, boxstyle="round,pad=0.008,rounding_size=0.01",
                                     facecolor='#16263d', edgecolor=(1.0, 1.0, 1.0, 0.15), linewidth=1.0, transform=fig.transFigure)
        fig.patches.append(box)
        fig.text(xC + 0.008, y - 0.025, title, fontsize=9.5, fontweight='bold', color='#2dd4bf')
        fig.text(xC + 0.008, y - 0.105, desc, fontsize=8.0, color='#cbd5e1', linespacing=1.25)
        y -= 0.175

    # ---------------- PANEL D CONTENT ----------------
    xD = panel_coords[3]['x'] + 0.015
    items_D = [
        ("[Systems Interactome]", "Subcellular compartmental network:\n31 nodes across Golgi, Actin Streaming,\nCortical MTs, PM, and Cell Wall Apoplast.\nCatalytic reactions, donors & substrates"),
        ("[Biophysical Transport Sim]", "Stochastic Monte Carlo Vesicle Model\n1000 secretory vesicles simulating\nmotor stalling & delivery deficits (0g vs 1g)\nDual side-by-side plant cell animation"),
        ("[TabPFN Foundation Model]", "Hollmann et al. (Nature 2025)\nBayesian in-context prior-data learning\nZero-shot cross-mission validation on\nOSD-121 (STS-131 BRIC-16, AUC=1.000)"),
        ("[Partial Gravity Imputation]", "Continuous non-linear dose-response:\n• Moon (0.16g): 98.2% Flight phenotype\n• Mars (0.38g): 14.5% Flight phenotype\n• Earth (1.00g): 0.0% Ground phenotype")
    ]
    y = 0.77
    for title, desc in items_D:
        box = patches.FancyBboxPatch((xD, y - 0.12), 0.19, 0.13, boxstyle="round,pad=0.008,rounding_size=0.01",
                                     facecolor='#16263d', edgecolor=(1.0, 1.0, 1.0, 0.15), linewidth=1.0, transform=fig.transFigure)
        fig.patches.append(box)
        fig.text(xD + 0.008, y - 0.025, title, fontsize=9.5, fontweight='bold', color='#c084fc')
        fig.text(xD + 0.008, y - 0.105, desc, fontsize=8.0, color='#cbd5e1', linespacing=1.25)
        y -= 0.175

    fig1_out = os.path.join(fig_dir, '01_experimental_design_and_workflow.png')
    fig.savefig(fig1_out, dpi=300, bbox_inches='tight')
    plt.close()

    # Synchronize to docs/figures and manuscript/figures
    shutil.copy(fig1_out, os.path.join(docs_fig_dir, '01_experimental_design_and_workflow.png'))
    shutil.copy(fig1_out, os.path.join(manuscript_fig_dir, '01_experimental_design_and_workflow.png'))

    print(f"Figure 1 successfully created: {fig1_out}")

if __name__ == '__main__':
    generate_figure1()
