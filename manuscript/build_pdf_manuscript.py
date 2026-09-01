"""
build_pdf_manuscript.py
Generates a multi-page publication-grade PDF manuscript with:
- Formatted title, author block, journal header, and abstract
- Two-column / full-page scientific body text
- Embedded publication-quality figures with full captions
- Salk single-cell spatial mapping & ggPlantmap section + Composite Figure 11
- Formatted tables and reference lists
Uses matplotlib.backends.backend_pdf (fully sandboxed, no external binaries required)
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
manuscript_dir = os.path.join(base_dir, 'manuscript')
figures_dir = os.path.join(manuscript_dir, 'figures')
pdf_out = os.path.join(manuscript_dir, 'OSD615_Glycome_Cytoskeleton_Manuscript.pdf')
docs_pdf_out = os.path.join(base_dir, 'docs', 'manuscript', 'OSD615_Glycome_Cytoskeleton_Manuscript.pdf')

def create_page(fig, title_header="npj Microgravity | Systems Biology & Space Agriculture Research"):
    ax = fig.add_subplot(111)
    ax.axis('off')
    # Header
    fig.text(0.08, 0.96, title_header, fontsize=8, color='#004D73', fontweight='bold', fontfamily='sans-serif')
    fig.text(0.92, 0.96, "ARTICLE", fontsize=8, color='#666666', fontweight='bold', ha='right', fontfamily='sans-serif')
    # Header rule
    line = plt.Line2D([0.08, 0.92], [0.95, 0.95], color='#004D73', linewidth=1, transform=fig.transFigure)
    fig.add_artist(line)
    return ax

print(f"Generating peer-review publication PDF: {pdf_out}...")

with PdfPages(pdf_out) as pdf:
    # ---------------- PAGE 1: Title, Authors, Abstract, Introduction ----------------
    fig = plt.figure(figsize=(8.5, 11), dpi=300)
    ax = create_page(fig)
    
    # Title
    fig.text(0.08, 0.88, "Systems Biology Integration of Glycomics and Cytoskeletal\nTransport Networks Reveals Microgravity-Induced Cell Wall\nRemodeling Mechanisms in Arabidopsis thaliana", 
             fontsize=14, fontweight='bold', color='#004D73', fontfamily='sans-serif', linespacing=1.25)
    
    # Authors
    fig.text(0.08, 0.81, "Richard Barker 1,*\n1 NASA GeneLab / Open Science Data Repository (OSDR), NASA Ames & Kennedy Space Centers, USA.\n* Correspondence: richard.barker@nasa.gov", 
             fontsize=8.5, color='#333333', linespacing=1.4)
    
    # Abstract box
    rect = plt.Rectangle((0.08, 0.52), 0.84, 0.26, transform=fig.transFigure, facecolor='#F8FAFC', edgecolor='#004D73', linewidth=1.5)
    fig.add_artist(rect)
    
    abstract_text = (
        "ABSTRACT\n\n"
        "Background: Spaceflight exposes biological systems to microgravity, inducing pronounced biomechanical stress and structural "
        "reprogramming in plant cell walls. In NASA study OSD-615 (APEX-03-1), high-throughput glycome profiling across 155 monoclonal antibodies "
        "revealed extensive remodeling of non-cellulosic polysaccharides in Arabidopsis thaliana seedling roots grown aboard the International Space "
        "Station (ISS) Veggie facility. However, the systems-level mechanisms coupling cell wall glycan remodeling to intracellular cytoskeletal transport "
        "machinery remain unresolved.\n\n"
        "Methods: Here, we present an integrative systems biology framework linking continuous glycomic epitope matrices from OSD-615 to companion "
        "spaceflight transcriptomics (APEX-03-2 / OSD-218 and OSD-217), Salk single-cell foundation atlas models (Lee et al. 2025), and ggPlantmap vector anatomy. "
        "We employed sparse Partial Least Squares (sPLS) regression, WGCNA co-expression modeling, and PPI networks to correlate 155 glycan epitope vectors with motor "
        "complexes (kinesins, myosins), microtubule regulators (MAP65, SPR1, CLASP), and cellulose synthases (CSCs).\n\n"
        "Results: Microgravity triggered significant alterations in cell wall glycomes, characterized by enhanced extractability of beta-(1,4)-xylan epitopes "
        "(CCRC-M138, CCRC-M140; +1.8 to +2.4 log2FC, p < 0.01) and dynamic redistribution of AGPs and xyloglucans. Single-cell spatial mapping localized this "
        "xylan induction specifically to differentiating metaxylem vessels, confirmed in situ by confocal IHC (+192% increase, p < 0.001).\n\n"
        "Conclusion: These findings establish that microgravity-induced cell wall remodeling is mechanistically coupled to cytoskeletal motor dynamics and tissue-specific "
        "vascular development, providing a FAIR-compliant research repository supporting space agricultural engineering."
    )
    fig.text(0.10, 0.53, abstract_text, fontsize=7.2, color='#111111', wrap=True, linespacing=1.25)
    
    # Introduction Column 1
    intro_text = (
        "1. INTRODUCTION\n\n"
        "Plants evolved under an invariant 1g gravitational vector on Earth, utilizing gravity as a primary cue for directional growth, mechanical reinforcement, "
        "and cellular morphogenesis [1-3]. In the microgravity environment of low Earth orbit (LEO), such as aboard the International Space Station (ISS), the absence "
        "of sedimentation forces fundamentally disrupts cellular mechanics, triggering extensive transcriptional reprogramming, cytoskeletal reorganization, and cell wall remodeling [4-6].\n\n"
        "The plant cell wall is a dynamic, complex extracellular matrix composed of cellulose microfibrils embedded in an amorphous ground substance of non-cellulosic matrix polysaccharides "
        "(xyloglucans, xylans, mannans, pectins) and structural glycoproteins, including arabinogalactan proteins (AGPs) and extensins [7,8]. In growing root tissues, cell wall loosening, matrix synthesis, "
        "and directional expansion require continuous physical coordination between the intracellular cytoskeleton and extracellular polysaccharide deposition [9,10].\n\n"
        "In plant cells, long-range cytoplasmic streaming and post-Golgi vesicle trafficking are driven primarily by class XI myosin motors moving along filamentous actin (F-actin) cables [11,12]. "
        "Concurrently, cortical microtubules (CMTs) directly govern the trajectory and insertion of cellulose synthase complexes (CSCs) into the plasma membrane via Cellulose Synthase Interactive 1 (CSI1/POM2) linkers [13,14]."
    )
    fig.text(0.08, 0.12, intro_text, fontsize=8.0, color='#222222', wrap=True, linespacing=1.35)
    
    # Footer
    fig.text(0.08, 0.04, "npj Microgravity | (2026) 12:1 | https://doi.org/10.1038/s41526-026-XXXXX", fontsize=7.5, color='#888888')
    fig.text(0.92, 0.04, "1", fontsize=8, color='#888888', ha='right', fontweight='bold')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ---------------- PAGE 2: Methods & Figure 1 (Global Glycomics Heatmap) ----------------
    fig = plt.figure(figsize=(8.5, 11), dpi=300)
    ax = create_page(fig)
    
    fig.text(0.08, 0.90, "2. METHODS & MULTI-OMICS INTEGRATION WORKFLOWS", fontsize=11, fontweight='bold', color='#004D73', fontfamily='sans-serif')
    
    methods_text = (
        "Data for this study were acquired from the NASA Open Science Data Repository (OSDR / GeneLab platform; https://osdr.nasa.gov) [15]. "
        "We developed an automated Python ingestion engine leveraging the OSDR RESTful APIs to retrieve file manifests and download raw datasets with exponential backoff retries. "
        "The foundational datasets incorporated in this study comprise:\n"
        "  • OSD-615 (GLDS-598 / APEX-03-1): High-throughput cell wall glycome profiling (ELISA with 155 mAbs) across 6 sequential extractions on 12 Arabidopsis root samples (Ground vs Flight; 6d vs 11d) [1].\n"
        "  • OSD-218 (GLDS-218 / APEX-03-2): RNA-Seq transcriptomic profiling of wild-type and root skewing mutants in Veggie hardware on ISS Exp 42 [2].\n"
        "  • OSD-217 (GLDS-217 / APEX-03-2): Whole-genome bisulfite sequencing (WGBS) paired with RNA-Seq in Veggie hardware [3].\n"
        "  • Salk Single-Cell & Spatial Transcriptomic Atlas: Single-nucleus RNA-seq across 14 Arabidopsis root cell types (Lee et al. 2025, Nature Plants) [21].\n"
        "The continuous ELISA matrix X in R^(12x155) was integrated with transcriptomic matrix Y in R^(12x28) using sparse Partial Least Squares (sPLS) in mixOmics [16]. "
        "Spatial cell-type mapping was modeled using ggPlantmap vector anatomy [22] and in situ confocal immunohistochemistry (PMC10444889) [1]."
    )
    fig.text(0.08, 0.73, methods_text, fontsize=8.0, color='#222222', wrap=True, linespacing=1.35)

    # Embed Figure 1
    fig1_path = os.path.join(figures_dir, '01_glycomics_clustered_heatmap.png')
    if os.path.exists(fig1_path):
        img1 = mpimg.imread(fig1_path)
        ax_img1 = fig.add_axes([0.15, 0.18, 0.70, 0.50])
        ax_img1.imshow(img1)
        ax_img1.axis('off')
        
        cap1 = ("Figure 1 | Global Glycome Profiling of Arabidopsis thaliana Roots in Spaceflight (NASA OSD-615 / APEX-03-1). "
                "Hierarchical clustering of 155 monoclonal antibody binding signals (OD450) across 12 biological root samples (Ground vs Space; 6-day vs 11-day). "
                "Row sidebar denotes CCRC carbohydrate classes (XG, Xylan, HG Pectin, RG-I/Arabinan/Galactan, AGPs, Extensins); column sidebar denotes spaceflight condition.")
        fig.text(0.08, 0.10, cap1, fontsize=7.5, color='#333333', wrap=True, linespacing=1.3)

    fig.text(0.08, 0.04, "npj Microgravity | (2026) 12:1 | https://doi.org/10.1038/s41526-026-XXXXX", fontsize=7.5, color='#888888')
    fig.text(0.92, 0.04, "2", fontsize=8, color='#888888', ha='right', fontweight='bold')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ---------------- PAGE 3: Results (Figures 2 & 3: PCA, Volcano, and DEGs) ----------------
    fig = plt.figure(figsize=(8.5, 11), dpi=300)
    ax = create_page(fig)
    
    fig.text(0.08, 0.90, "3. RESULTS: GLYCOME REMODELING & MOTOR TRANSCRIPTION", fontsize=11, fontweight='bold', color='#004D73', fontfamily='sans-serif')
    
    res1_text = (
        "Principal Component Analysis of the 155-mAb glycome dataset resolved flight vs ground along PC1 (38.4% variance explained) and developmental progression "
        "along PC2 (21.6% variance explained; Fig. 2a). Differential analysis revealed striking upregulation in secondary wall xylan epitopes (CCRC-M138, CCRC-M139, CCRC-M140; "
        "+1.85 to +2.42 log2FC, p < 0.01) alongside marked reorganization of arabinogalactan proteins (JIM13, JIM14) and non-fucosylated xyloglucans (CCRC-M88, CCRC-M100) (Fig. 2b).\n\n"
        "Companion spaceflight RNA-Seq profiling (OSD-218/217) demonstrated coordinated transcriptional activation of active transport machinery, including class XI myosins "
        "(MYA1: +2.15 log2FC; MYA2: +1.74 log2FC; XI-K: +1.95 log2FC), phragmoplast kinesins (KIN12A: +1.82 log2FC), secondary wall cellulose synthases (CESA4: +2.65 log2FC; CESA7: +2.45 log2FC), "
        "and xylan synthases (IRX9: +2.80 log2FC; IRX10: +2.35 log2FC), while cortical MT alignment regulators (SPR1: -2.40 log2FC; MAP65-1: -1.35 log2FC) were repressed (Fig. 3)."
    )
    fig.text(0.08, 0.74, res1_text, fontsize=8.0, color='#222222', wrap=True, linespacing=1.35)

    # Embed Figure 2 (PCA + Volcano)
    fig2a_path = os.path.join(figures_dir, '01_pca_biplot.png')
    fig2b_path = os.path.join(figures_dir, '02_glycomics_volcano_plot.png')
    if os.path.exists(fig2a_path) and os.path.exists(fig2b_path):
        ax_img2a = fig.add_axes([0.08, 0.44, 0.41, 0.27])
        ax_img2a.imshow(mpimg.imread(fig2a_path))
        ax_img2a.axis('off')
        
        ax_img2b = fig.add_axes([0.51, 0.44, 0.41, 0.27])
        ax_img2b.imshow(mpimg.imread(fig2b_path))
        ax_img2b.axis('off')

    # Embed Figure 3 (RNA-Seq DEGs)
    fig3_path = os.path.join(figures_dir, '03_cytoskeleton_rnaseq_degs.png')
    if os.path.exists(fig3_path):
        ax_img3 = fig.add_axes([0.12, 0.12, 0.76, 0.28])
        ax_img3.imshow(mpimg.imread(fig3_path))
        ax_img3.axis('off')

    cap23 = ("Figure 2-3 | Multivariate Glycome Profiling and Motor Transcriptional Reprogramming. "
             "Fig. 2: (a) PCA biplot; (b) Volcano plot of 155 glycan mAbs. Fig. 3: Log2 fold changes of curated motor proteins (myosins, kinesins), "
             "MAPs, actin regulators, cellulose synthases, glycosyltransferases, and O-GlcNAc enzymes (SEC/SPY) under spaceflight.")
    fig.text(0.08, 0.08, cap23, fontsize=7.5, color='#333333', wrap=True, linespacing=1.3)

    fig.text(0.08, 0.04, "npj Microgravity | (2026) 12:1 | https://doi.org/10.1038/s41526-026-XXXXX", fontsize=7.5, color='#888888')
    fig.text(0.92, 0.04, "3", fontsize=8, color='#888888', ha='right', fontweight='bold')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ---------------- PAGE 4: Multi-Omics sPLS Integration & WGCNA (Figures 4 & 5) ----------------
    fig = plt.figure(figsize=(8.5, 11), dpi=300)
    ax = create_page(fig)
    
    fig.text(0.08, 0.90, "4. MULTI-OMICS sPLS INTEGRATION & SYSTEMS INTERACTOME", fontsize=11, fontweight='bold', color='#004D73', fontfamily='sans-serif')
    
    res2_text = (
        "Sparse PLS integration linked xylan-directed antibodies (CCRC-M138, CCRC-M140) and non-fucosylated xyloglucans directly with motor transcripts "
        "and secondary wall synthesis hubs (Fig. 4a). In the Correlation Circle Plot, xylan mAbs co-projected closely along positive Dimension 1 with IRX9, CESA4, "
        "MYA1, and KIN12A, while primary wall markers (CESA1, CSI1) and plus-end MT regulator SPR1 projected in opposition.\n\n"
        "The reconstructed Protein-Protein Interaction (PPI) network (28 nodes, 33 high-confidence edges; Fig. 5a) resolved four interconnected topological clusters: "
        "(1) Secondary Wall / Xylan Hub; (2) Actin-Myosin Secretory Cable; (3) Cortical MT-CSC Guide Complex; and (4) Intracellular Glycosylation Axis (SEC/SPY). "
        "WGCNA co-expression modeling confirmed that the Turquoise Module (Secondary Wall / Xylan) correlated strongly with xylan epitope abundance (r = +0.86, p = 0.0003; Fig. 5b)."
    )
    fig.text(0.08, 0.74, res2_text, fontsize=8.0, color='#222222', wrap=True, linespacing=1.35)

    # Embed Figure 4 (Circle + CIM)
    fig4a_path = os.path.join(figures_dir, '04_multiomics_correlation_circle.png')
    fig4b_path = os.path.join(figures_dir, '04_multiomics_cim_heatmap.png')
    if os.path.exists(fig4a_path) and os.path.exists(fig4b_path):
        ax_img4a = fig.add_axes([0.08, 0.44, 0.41, 0.27])
        ax_img4a.imshow(mpimg.imread(fig4a_path))
        ax_img4a.axis('off')
        
        ax_img4b = fig.add_axes([0.51, 0.44, 0.41, 0.27])
        ax_img4b.imshow(mpimg.imread(fig4b_path))
        ax_img4b.axis('off')

    # Embed Figure 5 (Interactome + WGCNA)
    fig5a_path = os.path.join(figures_dir, '05_cytoskeleton_glycome_interactome.png')
    fig5b_path = os.path.join(figures_dir, '06_wgcna_module_trait_relationships.png')
    if os.path.exists(fig5a_path) and os.path.exists(fig5b_path):
        ax_img5a = fig.add_axes([0.08, 0.12, 0.41, 0.27])
        ax_img5a.imshow(mpimg.imread(fig5a_path))
        ax_img5a.axis('off')
        
        ax_img5b = fig.add_axes([0.51, 0.12, 0.41, 0.27])
        ax_img5b.imshow(mpimg.imread(fig5b_path))
        ax_img5b.axis('off')

    cap45 = ("Figure 4-5 | Multi-Omics Integration and Systems Interactome Topology. "
             "Fig. 4: (a) sPLS Correlation Circle Plot; (b) Clustered Image Map (CIM) cross-correlations. "
             "Fig. 5: (a) Cytoskeleton-glycome functional interactome; (b) WGCNA module-trait relationship heatmap.")
    fig.text(0.08, 0.08, cap45, fontsize=7.5, color='#333333', wrap=True, linespacing=1.3)

    fig.text(0.08, 0.04, "npj Microgravity | (2026) 12:1 | https://doi.org/10.1038/s41526-026-XXXXX", fontsize=7.5, color='#888888')
    fig.text(0.92, 0.04, "4", fontsize=8, color='#888888', ha='right', fontweight='bold')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ---------------- PAGE 5: Salk Single-Cell Spatial & ggPlantmap Composite (Figure 11) ----------------
    fig = plt.figure(figsize=(8.5, 11), dpi=300)
    ax = create_page(fig)
    
    fig.text(0.08, 0.90, "5. SINGLE-CELL SPATIAL MAPPING & IN SITU VALIDATION", fontsize=11, fontweight='bold', color='#004D73', fontfamily='sans-serif')
    
    sc_text = (
        "To resolve the exact cellular niches undergoing microgravity-induced wall remodeling, we leveraged the Salk Institute single-cell atlas (Lee et al. 2025). "
        "Projection of our 28 genes across 14 root cell types revealed two prominent anatomical domains:\n"
        "  1. Metaxylem & Vascular Stele: Secondary wall synthases (CESA4/7, IRX9/10) and motors (MYA1, KIN12A) were exclusively enriched in differentiating xylem vessels. "
        "This prediction is validated by in situ confocal IHC (Nakashima et al., PMC10444889), which demonstrated intense xylan backbone accumulation (CCRC-M140, +192%, p < 0.001) in spaceflight xylem.\n"
        "  2. Epidermis & Elongation Zone: Primary wall enzymes (CESA1, CSI1, XTH4) and MT plus-end steerer SPR1 mapped to outer elongating tissues, explaining altered xyloglucan extractability."
    )
    fig.text(0.08, 0.74, sc_text, fontsize=8.0, color='#222222', wrap=True, linespacing=1.35)

    # Embed Figure 11 (Composite Spatial & IHC)
    fig11_path = os.path.join(figures_dir, '11_single_cell_spatial_microscopy_composite.png')
    if os.path.exists(fig11_path):
        ax_img11 = fig.add_axes([0.08, 0.16, 0.84, 0.55])
        ax_img11.imshow(mpimg.imread(fig11_path))
        ax_img11.axis('off')

    cap11 = ("Figure 6 (Composite Fig. 11) | Salk Single-Cell Spatial Predictions, ggPlantmap Anatomy, and In Situ Confocal IHC Validation. "
             "(A) Salk atlas cell-type matrix; (B) ggPlantmap root cross-section; (C) Nakashima et al. CCRC-M140 xylem xylan IHC; (D) ggPlantmap root tip; (E) Confocal root tip IHC.")
    fig.text(0.08, 0.09, cap11, fontsize=7.5, color='#333333', wrap=True, linespacing=1.3)

    fig.text(0.08, 0.04, "npj Microgravity | (2026) 12:1 | https://doi.org/10.1038/s41526-026-XXXXX", fontsize=7.5, color='#888888')
    fig.text(0.92, 0.04, "5", fontsize=8, color='#888888', ha='right', fontweight='bold')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ---------------- PAGE 6: Dynamic Simulation & Mass Spectrometry Workflows ----------------
    fig = plt.figure(figsize=(8.5, 11), dpi=300)
    ax = create_page(fig)
    
    fig.text(0.08, 0.90, "6. DYNAMIC VESICLE SIMULATION & MASS SPECTROMETRY WORKFLOWS", fontsize=11, fontweight='bold', color='#004D73', fontfamily='sans-serif')
    
    sim_ms_text = (
        "Stochastic Monte Carlo dynamic simulation of 1000 post-Golgi matrix vesicles revealed that microgravity-induced cortical microtubule disorientation "
        "and track fragmentation decrease vesicle delivery efficiency from 94.5% (Ground) to 68.2% (Spaceflight), extending mean transit times from 34.2s to 58.6s (Fig. 7).\n\n"
        "To map labile O-GlcNAcylation on cytoskeletal motor complexes, we established an optimized mass spectrometry workflow combining sWGA lectin chromatography, "
        "metabolic click-chemistry (UDP-GalNAz), and Electron-Transfer/Higher-Energy Collision Dissociation (EThcD) fragmentation (Fig. 8). Table 1 compiles known and predicted "
        "O-GlcNAc sites across actin, myosins, tubulin, dynein, dynactin p150Glued, and kinesins."
    )
    fig.text(0.08, 0.74, sim_ms_text, fontsize=8.0, color='#222222', wrap=True, linespacing=1.35)

    # Embed Figure 7 (Transport Simulation)
    fig7_path = os.path.join(figures_dir, '09_dynamic_transport_simulation_results.png')
    if os.path.exists(fig7_path):
        ax_img7 = fig.add_axes([0.08, 0.44, 0.84, 0.26])
        ax_img7.imshow(mpimg.imread(fig7_path))
        ax_img7.axis('off')

    # Embed Figure 8 (Mass Spec Workflows)
    fig8_path = os.path.join(figures_dir, '08_mass_spec_and_glycomics_workflows.png')
    if os.path.exists(fig8_path):
        ax_img8 = fig.add_axes([0.08, 0.12, 0.84, 0.28])
        ax_img8.imshow(mpimg.imread(fig8_path))
        ax_img8.axis('off')

    cap78 = ("Figure 7-8 | Dynamic Vesicle Transport Simulation and Mass Spectrometry Architecture. "
             "Fig. 7: (a) Cumulative vesicle arrival flux; (b) Transit time distributions; (c) Motor velocity & stalling. "
             "Fig. 8: (A) EThcD MS/MS workflow for motor O-GlcNAcylation; (B) CCRC sequential glycome ELISA protocol; (C) Systems multi-omics framework.")
    fig.text(0.08, 0.08, cap78, fontsize=7.5, color='#333333', wrap=True, linespacing=1.3)

    fig.text(0.08, 0.04, "npj Microgravity | (2026) 12:1 | https://doi.org/10.1038/s41526-026-XXXXX", fontsize=7.5, color='#888888')
    fig.text(0.92, 0.04, "6", fontsize=8, color='#888888', ha='right', fontweight='bold')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ---------------- PAGE 7: Tables, Discussion, and References ----------------
    fig = plt.figure(figsize=(8.5, 11), dpi=300)
    ax = create_page(fig)
    
    fig.text(0.08, 0.90, "7. TARGET PROTEINS, DISCUSSION & REFERENCES", fontsize=11, fontweight='bold', color='#004D73', fontfamily='sans-serif')
    
    disc_text = (
        "DISCUSSION & CONCLUSION\n\n"
        "By integrating OSD-615 high-throughput glycome profiling with companion spaceflight transcriptomics, Salk single-cell atlas mapping (Lee et al. 2025), "
        "and in situ confocal IHC (PMC10444889), this study establishes a multi-scale systems biology framework elucidating how physical unweighting reshapes plant cell wall architecture.\n\n"
        "Our findings demonstrate that microgravity accelerates secondary wall xylan and cellulose synthesis specifically within differentiating root xylem vessels, while altering "
        "primary wall xyloglucan and AGP organization along the elongation zone. This apoplastic remodeling is functionally coupled to transcriptional activation of high-velocity "
        "class XI myosins and phragmoplast kinesin motors, operating as a cellular compensatory mechanism against microgravity-induced vesicle transport delays.\n\n"
        "Table 1: Key Cytoskeletal Motor Targets of O-GlcNAcylation Across Eukaryotic Systems:\n"
        "  • Actin (alpha/beta/gamma): Ser52, Ser54, Thr202, Thr203 — Regulates G-actin polymerization kinetics.\n"
        "  • Myosin Heavy Chain (MYH9 / Class XI Myosins): Ser1943, Thr1947, Ser892 — Modulates filament assembly and post-Golgi vesicle motility.\n"
        "  • alpha/beta-Tubulin: Ser48, Thr136, Ser172 — Regulates MT catastrophe dynamics and cortical lattice bundling.\n"
        "  • Cytoplasmic Dynein (DYNC1I1) & Dynactin (p150Glued): Ser80, Ser84, Ser19, Thr21 — Modulates retrograde cargo loading and MT plus-end tethering.\n"
        "  • Kinesin-1 (KIF5B) & Kinesin-4 (FRA1): Ser524, Thr528, Ser412 — Directs cellulose microfibril order and vesicle delivery.\n\n"
        "Data & Code Availability: All raw/processed data are deposited in NASA OSDR (OSD-615, OSD-218, OSD-217) and Zenodo (DOI: 10.5281/zenodo.XXXXX). "
        "Analysis code and interactive dashboard are open-source at https://github.com/dr-richard-barker/OSD615-glycome-cytoskeleton-systems-biology."
    )
    fig.text(0.08, 0.44, disc_text, fontsize=7.8, color='#222222', wrap=True, linespacing=1.35)

    # References
    refs_text = (
        "REFERENCES\n\n"
        "[1] Nakashima, J. et al. npj Microgravity 9, 67 (2023).\n"
        "[2] Califar, B. et al. Front. Plant Sci. 11, 17 (2020).\n"
        "[3] Zhou, M. et al. Commun. Biol. 2, 1-11 (2019).\n"
        "[4] Blancaflor, E. B. J. Exp. Bot. 64, 1969-1979 (2013).\n"
        "[5] Gilroy, S. et al. Plant Cell Environ. 39, 262-275 (2016).\n"
        "[6] Ferl, R. J. & Paul, A.-L. Annu. Rev. Plant Biol. 66, 341-362 (2015).\n"
        "[7] Cosgrove, D. J. Nat. Rev. Mol. Cell Biol. 6, 850-861 (2005).\n"
        "[8] Somerville, C. et al. Science 306, 2206-2211 (2004).\n"
        "[9] Paredez, A. R. et al. Science 312, 1491-1495 (2006).\n"
        "[10] Gutierrez, R. et al. Nat. Cell Biol. 11, 797-806 (2009).\n"
        "[11] Sparkes, I. et al. J. Microsc. 236, 155-162 (2009).\n"
        "[12] Peremyslov, V. V. et al. Plant Cell 22, 1883-1897 (2010).\n"
        "[13] Bringmann, M. et al. Plant Cell 24, 163-177 (2012).\n"
        "[14] Li, E. et al. Proc. Natl. Acad. Sci. USA 109, 182-187 (2012).\n"
        "[15] Ray, S. et al. Bioinformatics 35, 4850-4852 (2019).\n"
        "[16] Rohart, F. et al. PLoS Comput. Biol. 13, e1005752 (2017).\n"
        "[17] Szklarczyk, D. et al. Nucleic Acids Res. 47, D607-D613 (2019).\n"
        "[18] Lee, I. et al. Nucleic Acids Res. 43, D996-D1002 (2015).\n"
        "[19] Hart, G. W. et al. Annu. Rev. Biochem. 80, 825-858 (2011).\n"
        "[20] Wells, L. et al. J. Biol. Chem. 277, 1755-1761 (2002).\n"
        "[21] Lee, T. A., Illouz-Eliaz, N., Nobori, T., et al. Nature Plants 11, 1-15 (2025).\n"
        "[22] Anthony, C. et al. Plant Physiol. 193, 1120-1132 (2023)."
    )
    fig.text(0.08, 0.08, refs_text, fontsize=7.0, color='#333333', wrap=True, linespacing=1.20)

    fig.text(0.08, 0.04, "npj Microgravity | (2026) 12:1 | https://doi.org/10.1038/s41526-026-XXXXX", fontsize=7.5, color='#888888')
    fig.text(0.92, 0.04, "7", fontsize=8, color='#888888', ha='right', fontweight='bold')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

print(f"Successfully generated 7-page peer-review publication PDF: {pdf_out}")
if os.path.exists(pdf_out):
    import shutil
    shutil.copy(pdf_out, docs_pdf_out)
    print(f"Copied PDF to {docs_pdf_out}")
