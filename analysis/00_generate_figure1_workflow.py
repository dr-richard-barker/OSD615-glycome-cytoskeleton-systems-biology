"""
00_generate_figure1_workflow.py
Generates high-resolution publication Figure 1 (01_experimental_design_and_workflow.png):
Multi-Scale Systems Biology Workflow and Experimental Architecture for Spaceflight Glycomics.
Optimized with large, highly legible typography and high-contrast presentation.
"""

import os
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_figure1():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fig_dir = os.path.join(base_dir, 'analysis', 'figures')
    docs_fig_dir = os.path.join(base_dir, 'docs', 'figures')
    manuscript_fig_dir = os.path.join(base_dir, 'manuscript', 'figures')

    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(docs_fig_dir, exist_ok=True)
    os.makedirs(manuscript_fig_dir, exist_ok=True)

    print("Generating Figure 1: Large-Typography Systems Biology Workflow Architecture...")

    # Canvas dimensions: 22 inches wide by 13 inches high for maximum clarity & legibility
    fig = plt.figure(figsize=(22, 13.0), dpi=300)
    fig.patch.set_facecolor('#060b14')

    # Top Header Banner
    fig.text(0.5, 0.972, "NASA OPEN SCIENCE DATA REPOSITORY  •  STUDY OSD-615 / APEX-03-1  •  SYSTEMS BIOLOGY FRAMEWORK", 
             fontsize=12.0, fontweight='bold', color='#38bdf8', ha='center', fontfamily='sans-serif')
    
    fig.text(0.5, 0.940, "Figure 1 | Multi-Scale Systems Biology Workflow & Experimental Architecture", 
             fontsize=25.0, fontweight='bold', color='#ffffff', ha='center', fontfamily='sans-serif')
    
    fig.text(0.5, 0.912, "End-to-end integration of spaceflight glycome ELISA profiling (155 mAbs), companion transcriptomics, single-cell atlas mapping, and AI foundation models", 
             fontsize=14.0, color='#94a3b8', ha='center', fontfamily='sans-serif')

    # 4 Main Columns / Panels across the canvas
    panel_coords = [
        {
            "x": 0.024, "w": 0.228, 
            "title": "A | Spaceflight Sampling", 
            "tag": "NASA OSD-615 / APEX-03-1", 
            "color": "#0284c7", "light_color": "#38bdf8", "bg": "#0c1829"
        },
        {
            "x": 0.268, "w": 0.228, 
            "title": "B | Sequential Glycomics", 
            "tag": "155 Monoclonal Antibodies", 
            "color": "#e11d48", "light_color": "#fb7185", "bg": "#190f1d"
        },
        {
            "x": 0.512, "w": 0.228, 
            "title": "C | Multi-Omics & Spatial", 
            "tag": "Salk Atlas & ggPlantmap", 
            "color": "#0d9488", "light_color": "#2dd4bf", "bg": "#0b1b1a"
        },
        {
            "x": 0.756, "w": 0.228, 
            "title": "D | Interactome & AI", 
            "tag": "Monte Carlo & TabPFN", 
            "color": "#7c3aed", "light_color": "#c084fc", "bg": "#160f26"
        }
    ]

    for p in panel_coords:
        # Main Panel Column Container
        col_box = patches.FancyBboxPatch(
            (p['x'], 0.045), p['w'], 0.840,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor='#0d1726', edgecolor=p['color'], linewidth=2.4, transform=fig.transFigure
        )
        fig.patches.append(col_box)

        # Header Pill Container inside panel
        hdr_box = patches.FancyBboxPatch(
            (p['x'] + 0.008, 0.812), p['w'] - 0.016, 0.062,
            boxstyle="round,pad=0.008,rounding_size=0.012",
            facecolor='#14233a', edgecolor=p['color'], linewidth=1.4, transform=fig.transFigure
        )
        fig.patches.append(hdr_box)

        # Panel Header Typography
        fig.text(p['x'] + 0.016, 0.848, p['title'], fontsize=16.0, fontweight='bold', color='#ffffff', fontfamily='sans-serif')
        fig.text(p['x'] + 0.016, 0.824, p['tag'], fontsize=13.0, fontweight='bold', color=p['light_color'], fontfamily='sans-serif')

    # Connecting Flow Pills between panels
    flow_arrows = [
        {"x": 0.252, "label": "Sequential\nExtraction"},
        {"x": 0.496, "label": "Multi-Omics\nCorrelation"},
        {"x": 0.740, "label": "Predictive\nAI Models"}
    ]
    for fa in flow_arrows:
        arrow_box = patches.FancyBboxPatch(
            (fa['x'] - 0.015, 0.465), 0.030, 0.054,
            boxstyle="round,pad=0.006,rounding_size=0.010",
            facecolor='#1e293b', edgecolor='#64748b', linewidth=1.4, transform=fig.transFigure
        )
        fig.patches.append(arrow_box)
        fig.text(fa['x'], 0.494, "▶", fontsize=13, color='#38bdf8', ha='center', va='center', fontweight='bold')
        fig.text(fa['x'], 0.471, fa['label'], fontsize=8.5, color='#e2e8f0', ha='center', va='center', fontweight='bold', fontfamily='sans-serif')

    # Card layout parameters
    card_h = 0.170
    gap = 0.022
    y_starts = [0.798 - (i * (card_h + gap)) for i in range(4)]

    # ---------------- PANEL A CONTENT ----------------
    xA = panel_coords[0]['x'] + 0.010
    wA = panel_coords[0]['w'] - 0.020
    items_A = [
        ("Flight Environment & Hardware", 
         "• ISS Veggie Facility (0g Microgravity)\n• Low Earth Orbit (400 km altitude, 28,000 km/h)\n• Synchronous KSC 1g Ground Controls\n  (temperature, RH, CO2 matched)"),
        ("Plant Model & Harvest Timing", 
         "• Arabidopsis thaliana (Col-0 wild-type)\n• Seedling roots harvested post-germination:\n  - 6-Day Early Seedling Stage\n  - 11-Day Mature Root Stage"),
        ("12 Biological Replicates", 
         "• Spaceflight 6-day (n = 3: R1, R3, R6)\n• Spaceflight 11-day (n = 3: R5, R8, R12)\n• Ground Control 6-day (n = 3: R7, R10, R11)\n• Ground Control 11-day (n = 3: R2, R4, R9)"),
        ("NASA OSDR Repositories", 
         "• OSD-615 (GLDS-598 Root Glycome ELISA)\n• OSD-218 (Veggie RNA-Seq Transcriptome)\n• OSD-217 (Veggie Methylome & DEG Profiles)\n• Full RO-Crate 1.1 JSON-LD Metadata")
    ]
    for i, (title, desc) in enumerate(items_A):
        y_top = y_starts[i]
        cbox = patches.FancyBboxPatch(
            (xA, y_top - card_h), wA, card_h,
            boxstyle="round,pad=0.008,rounding_size=0.012",
            facecolor='#111f33', edgecolor='#0284c7', linewidth=1.2, transform=fig.transFigure
        )
        fig.patches.append(cbox)
        # Left accent line
        accent = patches.Rectangle((xA, y_top - card_h), 0.004, card_h, facecolor='#38bdf8', edgecolor='none', transform=fig.transFigure)
        fig.patches.append(accent)

        fig.text(xA + 0.010, y_top - 0.028, title, fontsize=13.5, fontweight='bold', color='#38bdf8', fontfamily='sans-serif')
        fig.text(xA + 0.010, y_top - 0.050, desc, fontsize=11.2, color='#f8fafc', linespacing=1.35, fontfamily='sans-serif', va='top')

    # ---------------- PANEL B CONTENT ----------------
    xB = panel_coords[1]['x'] + 0.010
    wB = panel_coords[1]['w'] - 0.020
    items_B = [
        ("Sequential Cell Wall Extraction", 
         "• 6 Chemical Reagent Fractions:\n  1. 50 mM CDTA (Pectin loosening)\n  2. 1 M KOH (Non-fucosylated XG)\n  3. 4 M KOH (Tight Xylan & XG)\n  4. NaClO2, 4M KOHPC, 0.1M H2SO4"),
        ("155 Monoclonal Antibodies (ELISA)", 
         "• High-Throughput OD450 Binding:\n  • Xylan/Arabinoxylan: CCRC-M140, M138\n  • Xyloglucan: CCRC-M1, M84, M95\n  • AGPs & Extensins: JIM13, JIM14, LM2\n  • Pectin HG & RG-I: JIM5, JIM7, M38"),
        ("Automated Ingestion & FAIR Data", 
         "• NASA OSDR REST API automated ingestion\n• Standardized Frictionless CSV & JSON\n• Z-score normalized binding profiles\n• Continuous quality control & curation"),
        ("Rigorous Statistical Framework", 
         "• Two-Way ANOVA (Spaceflight × Age)\n• Benjamini-Hochberg FDR (q < 0.01)\n• Cohen's d Effect Size Estimation (d > 1.5)\n• Hierarchical Ward Clustering & PCA")
    ]
    for i, (title, desc) in enumerate(items_B):
        y_top = y_starts[i]
        cbox = patches.FancyBboxPatch(
            (xB, y_top - card_h), wB, card_h,
            boxstyle="round,pad=0.008,rounding_size=0.012",
            facecolor='#1e1322', edgecolor='#e11d48', linewidth=1.2, transform=fig.transFigure
        )
        fig.patches.append(cbox)
        # Left accent line
        accent = patches.Rectangle((xB, y_top - card_h), 0.004, card_h, facecolor='#fb7185', edgecolor='none', transform=fig.transFigure)
        fig.patches.append(accent)

        fig.text(xB + 0.010, y_top - 0.028, title, fontsize=13.5, fontweight='bold', color='#fb7185', fontfamily='sans-serif')
        fig.text(xB + 0.010, y_top - 0.050, desc, fontsize=11.2, color='#f8fafc', linespacing=1.35, fontfamily='sans-serif', va='top')

    # ---------------- PANEL C CONTENT ----------------
    xC = panel_coords[2]['x'] + 0.010
    wC = panel_coords[2]['w'] - 0.020
    items_C = [
        ("Supervised Multi-Omics Integration", 
         "• Sparse Partial Least Squares (sPLS / mixOmics)\n• Cross-correlates 155 glycan vectors with\n  28 cytoskeletal motors & synthase genes\n• Discovers MYA1, CESA4, SPR1 hub"),
        ("Salk Single-Cell Root Atlas", 
         "• Lee et al. (Nature Plants 2025)\n• snRNA-Seq across 14 root cell types:\n  • Protoxylem & Metaxylem tracheary\n  • Cortex, Endodermis, Epidermis\n  • Root elongation & meristem zones"),
        ("ggPlantmap Vector Spatial Maps", 
         "• Anatomical projection onto root cross-sections\n• Quantitative color-mapping of expression\n• Pinpoints metaxylem as the spatial hub\n  of microgravity xylan hyper-accumulation"),
        ("In Situ IHC Confocal Archive", 
         "• Nakashima et al. (npj Microgravity 2023)\n• 30+ mAb confocal immunofluorescence\n• Direct physical validation:\n  +192% xylan deposition in mature xylem")
    ]
    for i, (title, desc) in enumerate(items_C):
        y_top = y_starts[i]
        cbox = patches.FancyBboxPatch(
            (xC, y_top - card_h), wC, card_h,
            boxstyle="round,pad=0.008,rounding_size=0.012",
            facecolor='#0b1d1c', edgecolor='#0d9488', linewidth=1.2, transform=fig.transFigure
        )
        fig.patches.append(cbox)
        # Left accent line
        accent = patches.Rectangle((xC, y_top - card_h), 0.004, card_h, facecolor='#2dd4bf', edgecolor='none', transform=fig.transFigure)
        fig.patches.append(accent)

        fig.text(xC + 0.010, y_top - 0.028, title, fontsize=13.5, fontweight='bold', color='#2dd4bf', fontfamily='sans-serif')
        fig.text(xC + 0.010, y_top - 0.050, desc, fontsize=11.2, color='#f8fafc', linespacing=1.35, fontfamily='sans-serif', va='top')

    # ---------------- PANEL D CONTENT ----------------
    xD = panel_coords[3]['x'] + 0.010
    wD = panel_coords[3]['w'] - 0.020
    items_D = [
        ("Subcellular Systems Interactome", 
         "• 31-node multi-compartmental network:\n  • Golgi Apparatus (Glycosyltransferases)\n  • Myosin XI Streaming & Cortical MTs\n  • Plasma Membrane (CESA Rosettes)\n  • Cell Wall Apoplast (Enzymatic Assembly)"),
        ("Biophysical Transport Simulation", 
         "• Stochastic Monte Carlo plant cell model\n• 1,000 secretory vesicles simulating transport\n• Quantifies motor stalling & delivery deficits\n• Dual side-by-side 0g vs 1g simulation"),
        ("TabPFN AI Foundation Model", 
         "• Hollmann et al. (Nature 2025)\n• Prior-data Fitted Network (Bayesian in-context)\n• Zero-shot cross-mission validation on\n  OSD-121 (STS-131 BRIC-16, AUC = 1.000)"),
        ("Partial Gravity Imputation", 
         "• Non-linear gravitational threshold modeling:\n  • Moon (0.16g): 98.2% Flight-like phenotype\n  • Mars (0.38g): 14.5% Flight-like phenotype\n  • Earth (1.00g): 0.0% Ground-like baseline")
    ]
    for i, (title, desc) in enumerate(items_D):
        y_top = y_starts[i]
        cbox = patches.FancyBboxPatch(
            (xD, y_top - card_h), wD, card_h,
            boxstyle="round,pad=0.008,rounding_size=0.012",
            facecolor='#170f28', edgecolor='#7c3aed', linewidth=1.2, transform=fig.transFigure
        )
        fig.patches.append(cbox)
        # Left accent line
        accent = patches.Rectangle((xD, y_top - card_h), 0.004, card_h, facecolor='#c084fc', edgecolor='none', transform=fig.transFigure)
        fig.patches.append(accent)

        fig.text(xD + 0.010, y_top - 0.028, title, fontsize=13.5, fontweight='bold', color='#c084fc', fontfamily='sans-serif')
        fig.text(xD + 0.010, y_top - 0.050, desc, fontsize=11.2, color='#f8fafc', linespacing=1.35, fontfamily='sans-serif', va='top')

    # Footer Metadata Bar
    fig.text(0.5, 0.016, 
             "NASA GeneLab / Open Science Data Repository (OSDR)  •  npj Microgravity Systems Biology Architecture  •  FAIR Data RO-Crate 1.1 Compliant", 
             fontsize=11.0, color='#64748b', ha='center', fontfamily='sans-serif')

    fig1_out = os.path.join(fig_dir, '01_experimental_design_and_workflow.png')
    fig.savefig(fig1_out, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    # Synchronize to docs/figures and manuscript/figures
    shutil.copy(fig1_out, os.path.join(docs_fig_dir, '01_experimental_design_and_workflow.png'))
    shutil.copy(fig1_out, os.path.join(manuscript_fig_dir, '01_experimental_design_and_workflow.png'))

    print(f"Figure 1 successfully created and synchronized to docs/ and manuscript/: {fig1_out}")

if __name__ == '__main__':
    generate_figure1()
