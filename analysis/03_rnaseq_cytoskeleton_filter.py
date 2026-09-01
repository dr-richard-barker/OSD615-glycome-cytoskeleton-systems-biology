"""
03_rnaseq_cytoskeleton_filter.py
Filters and annotates spaceflight RNA-Seq differential expression datasets
(companion APEX-03-2 OSD-218/OSD-217 studies) for cytoskeletal transport machinery,
motor proteins, cellulose synthases, and matrix glycosyltransferases.
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def filter_and_plot_rnaseq():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proc_dir = os.path.join(base_dir, 'data', 'processed')
    fig_dir = os.path.join(base_dir, 'analysis', 'figures')
    results_dir = os.path.join(base_dir, 'analysis', 'results')
    docs_dir = os.path.join(base_dir, 'docs', 'data')
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)

    degs_path = os.path.join(proc_dir, 'rnaseq_cytoskeleton_degs.csv')
    df_degs = pd.read_csv(degs_path)
    print(f"Loaded {len(df_degs)} curated cytoskeletal and cell wall remodeling transcripts.")

    # 1. Publication Figure: Grouped Bar Chart by Gene Family
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Sort by pathway / gene family and log2FC
    df_sorted = df_degs.sort_values(by=['Pathway', 'log2FC'], ascending=[True, True])
    
    palette = {'Microtubule Motor Transport': '#2F5985', 'Actin-Driven Vesicle Motility': '#E85D50',
               'Microtubule Organization': '#3FB6A8', 'Microtubule Directionality': '#F4A261',
               'Microtubule Polymerization': '#457B9D', 'Actin Nucleation': '#E76F51',
               'Actin Polymerization': '#6A4C93', 'Actin Bundling': '#8338EC',
               'Membrane-Actin Nucleation': '#3A86FF', 'Cell Wall Biosynthesis': '#2A9D8F',
               'Vascular Secondary Wall': '#D62828', 'CSC-Microtubule Alignment': '#0077B6',
               'Xylan Biosynthesis': '#9B5DE5', 'Xyloglucan Remodeling': '#F15BB5',
               'Wall Loosening': '#00BBF9', 'Pectin De-esterification': '#00F5D4',
               'Intracellular O-GlcNAcylation': '#FFB703', 'Intracellular Glycosylation': '#FB8500',
               'Cell Wall Secretory Machinery': '#1D3557'}
    
    colors = [palette.get(p, '#888888') for p in df_sorted['Pathway']]
    
    y_pos = np.arange(len(df_sorted))
    bars = ax.barh(y_pos, df_sorted['log2FC'], color=colors, edgecolor='black', linewidth=0.5)
    
    ax.set_yticks(y_pos)
    labels = [f"{row['Gene_Symbol']} ({row['Gene_ID']})" for _, row in df_sorted.iterrows()]
    ax.set_yticklabels(labels, fontsize=9)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlabel('$\log_2$ Fold Change in Microgravity (Spaceflight / Ground Control)', fontsize=11, fontweight='bold')
    ax.set_title('Transcriptional Reprogramming of Cytoskeletal Motors & Cell Wall Machinery\nCompanion Spaceflight Studies (APEX-03-2 / Veggie Hardware)', fontsize=12, fontweight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    # Custom legend for major functional groups
    major_groups = ['Microtubule Motor Transport', 'Actin-Driven Vesicle Motility', 'Vascular Secondary Wall', 'Xylan Biosynthesis', 'CSC-Microtubule Alignment', 'Intracellular O-GlcNAcylation']
    handles = [plt.Rectangle((0,0),1,1, color=palette[g]) for g in major_groups]
    ax.legend(handles, major_groups, loc='lower right', fontsize=8, title='Functional Category', framealpha=0.9)

    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '03_cytoskeleton_rnaseq_degs.png'), dpi=300)
    plt.close()
    print("Saved 03_cytoskeleton_rnaseq_degs.png")

    # 2. Export JSON summary
    out_json = {
        "transcripts": df_degs.to_dict('records'),
        "summary": {
            "total_genes": len(df_degs),
            "upregulated": int(sum(df_degs['log2FC'] > 0)),
            "downregulated": int(sum(df_degs['log2FC'] < 0)),
            "pathways": df_degs['Pathway'].unique().tolist()
        }
    }
    with open(os.path.join(docs_dir, 'cytoskeleton_rnaseq_summary.json'), 'w') as f:
        json.dump(out_json, f, indent=2)
    with open(os.path.join(results_dir, 'cytoskeleton_rnaseq_summary.json'), 'w') as f:
        json.dump(out_json, f, indent=2)

    print("RNA-Seq cytoskeleton filtering complete.")

if __name__ == '__main__':
    filter_and_plot_rnaseq()
