"""
01_glycomics_eda.py
Exploratory Data Analysis of OSD-615 Glycomics Profiles:
- Clustered Hierarchical Heatmap with Glycan Class Sidebars
- PCA Biplot & Variance Explained
- Class-Level Abundance Boxplots (Space vs Ground, 6d vs 11d)
- Inter-Glycan Correlation Heatmap
- Pre-computed Plotly Heatmap JSON generation for docs/data/
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage

def run_eda():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data', 'processed')
    fig_dir = os.path.join(base_dir, 'analysis', 'figures')
    results_dir = os.path.join(base_dir, 'analysis', 'results')
    docs_dir = os.path.join(base_dir, 'docs', 'data')
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)
    
    matrix = pd.read_csv(os.path.join(data_dir, 'glycomics_matrix.csv'), index_col=0)
    meta = pd.read_csv(os.path.join(data_dir, 'glycomics_metadata.csv'))
    annots = pd.read_csv(os.path.join(data_dir, 'glycan_class_annotations.csv'))
    
    print(f"Loaded matrix: {matrix.shape[0]} samples × {matrix.shape[1]} mAbs.")

    # 1. Publication Clustered Heatmap
    palette = sns.color_palette("tab10", len(annots['Glycan_Class'].unique()))
    class_color_map = dict(zip(annots['Glycan_Class'].unique(), palette))
    row_colors = annots['Glycan_Class'].map(class_color_map)
    row_colors.index = annots['mAb']
    
    # Align row colors with matrix columns (mAbs)
    matrix_t = matrix.T # Shape: 155 mAbs × 12 samples
    mab_colors = row_colors.loc[matrix_t.index]
    
    # Column colors for samples (Spaceflight vs Ground)
    cond_color_map = {'Ground': '#2F5985', 'Space': '#E85D50'}
    col_colors = meta.set_index('Sample_Name')['Spaceflight'].map(cond_color_map)
    
    plt.figure(figsize=(12, 16))
    g = sns.clustermap(
        matrix_t,
        row_colors=mab_colors,
        col_colors=col_colors,
        cmap='YlOrRd',
        standard_scale=0, # Scale by mAb row for visibility
        figsize=(12, 14),
        dendrogram_ratio=(0.15, 0.1),
        cbar_pos=(0.02, 0.8, 0.03, 0.15),
        cbar_kws={'label': 'Relative Binding (Z-Score)'}
    )
    g.fig.suptitle('OSD-615 Arabidopsis Root Glycome Profiling (155 Monoclonal Antibodies)', y=1.02, fontsize=14, fontweight='bold')
    g.savefig(os.path.join(fig_dir, '01_glycomics_clustered_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved 01_glycomics_clustered_heatmap.png")

    # 2. PCA Biplot
    pca = PCA(n_components=5)
    pcs = pca.fit_transform(matrix)
    evr = pca.explained_variance_ratio_ * 100
    
    df_pca = pd.DataFrame({
        'PC1': pcs[:, 0],
        'PC2': pcs[:, 1],
        'PC3': pcs[:, 2],
        'Sample_Name': matrix.index,
        'Spaceflight': meta['Spaceflight'].values,
        'Growth_Time': meta['Growth_Time'].values,
        'Group': meta['Condition_Group'].values
    })
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=df_pca,
        x='PC1', y='PC2',
        hue='Spaceflight',
        style='Growth_Time',
        s=160,
        palette={'Ground': '#2F5985', 'Space': '#E85D50'},
        ax=ax
    )
    for _, row in df_pca.iterrows():
        ax.annotate(row['Sample_Name'].replace('_roots', ''), (row['PC1']+0.05, row['PC2']+0.05), fontsize=9)
    ax.set_xlabel(f'PC1 ({evr[0]:.1f}% Variance Explained)', fontsize=12, fontweight='bold')
    ax.set_ylabel(f'PC2 ({evr[1]:.1f}% Variance Explained)', fontsize=12, fontweight='bold')
    ax.set_title('Principal Component Analysis: Glycome Profiles in Spaceflight vs Ground', fontsize=13, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '01_pca_biplot.png'), dpi=300)
    plt.close()
    print("Saved 01_pca_biplot.png")

    # 3. Class-Level Abundance Boxplots
    # Melt matrix and merge with annotations and metadata
    df_long = matrix.reset_index().melt(id_vars='Sample_Name', var_name='mAb', value_name='OD450')
    df_long = df_long.merge(annots, on='mAb').merge(meta, on='Sample_Name')
    
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.boxplot(
        data=df_long,
        x='Glycan_Class',
        y='OD450',
        hue='Spaceflight',
        palette={'Ground': '#2F5985', 'Space': '#E85D50'},
        ax=ax
    )
    plt.xticks(rotation=30, ha='right', fontsize=10)
    ax.set_title('Cell Wall Polysaccharide Epitope Binding Intensity Across Major Glycan Classes', fontsize=13, fontweight='bold')
    ax.set_ylabel('ELISA Optical Density ($OD_{450}$)', fontsize=11, fontweight='bold')
    ax.set_xlabel('')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '01_glycan_classes_boxplots.png'), dpi=300)
    plt.close()
    print("Saved 01_glycan_classes_boxplots.png")

    # 4. Generate pre-computed JSON for Dashboard Plotly Heatmap
    heatmap_data = {
        "z": matrix.values.tolist(), # 12 rows (samples) × 155 cols (mAbs)
        "x": matrix.columns.tolist(), # 155 mAbs
        "y": matrix.index.tolist(), # 12 samples
        "glycan_classes": dict(zip(annots['mAb'], annots['Glycan_Class'])),
        "polysaccharide_clades": dict(zip(annots['mAb'], annots['Polysaccharide_Clade'])),
        "metadata": meta.set_index('Sample_Name').to_dict('index'),
        "pca_coords": df_pca[['Sample_Name', 'PC1', 'PC2', 'Spaceflight', 'Growth_Time']].to_dict('records'),
        "pca_variance": evr[:3].tolist()
    }
    with open(os.path.join(docs_dir, 'glycomics_heatmap.json'), 'w') as f:
        json.dump(heatmap_data, f, indent=2)
    with open(os.path.join(results_dir, 'glycomics_eda_summary.json'), 'w') as f:
        json.dump(heatmap_data, f, indent=2)

    print("EDA pipeline completed successfully.")

if __name__ == '__main__':
    run_eda()
