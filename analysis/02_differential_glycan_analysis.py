"""
02_differential_glycan_analysis.py
Statistical Analysis of OSD-615 Cell Wall Glycomics:
- Two-way ANOVA (Spaceflight × Growth Time) & Welch t-tests
- Log2 Fold-Changes (Space vs Ground) at 6-day, 11-day, and combined
- Benjamini-Hochberg False Discovery Rate (FDR) correction
- Cohen's d effect size calculation per glycan epitope
- Volcano plot & Significant hits bar chart
- Pre-computed JSON export for dashboard
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def run_differential_analysis():
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
    annots = pd.read_csv(os.path.join(data_dir, 'glycan_class_annotations.csv')).set_index('mAb')

    # Merge metadata
    df_all = matrix.join(meta.set_index('Sample_Name'))

    space_samples = df_all[df_all['Spaceflight'] == 'Space']
    ground_samples = df_all[df_all['Spaceflight'] == 'Ground']

    diff_results = []
    mabs = matrix.columns.tolist()

    for m in mabs:
        s_vals = space_samples[m].values
        g_vals = ground_samples[m].values

        mean_space = float(np.mean(s_vals))
        mean_ground = float(np.mean(g_vals))
        
        # Avoid log of 0 by adding small epsilon
        eps = 1e-4
        fc = (mean_space + eps) / (mean_ground + eps)
        log2fc = float(np.log2(fc))

        # Welch t-test (Space vs Ground)
        t_stat, p_val = stats.ttest_ind(s_vals, g_vals, equal_var=False)
        if np.isnan(p_val): p_val = 1.0

        # Sub-analysis at 6d and 11d
        s_6d = df_all[(df_all['Spaceflight'] == 'Space') & (df_all['Growth_Time'] == 6)][m].values
        g_6d = df_all[(df_all['Spaceflight'] == 'Ground') & (df_all['Growth_Time'] == 6)][m].values
        s_11d = df_all[(df_all['Spaceflight'] == 'Space') & (df_all['Growth_Time'] == 11)][m].values
        g_11d = df_all[(df_all['Spaceflight'] == 'Ground') & (df_all['Growth_Time'] == 11)][m].values

        log2fc_6d = float(np.log2((np.mean(s_6d)+eps) / (np.mean(g_6d)+eps)))
        log2fc_11d = float(np.log2((np.mean(s_11d)+eps) / (np.mean(g_11d)+eps)))
        
        _, p_6d = stats.ttest_ind(s_6d, g_6d, equal_var=False)
        _, p_11d = stats.ttest_ind(s_11d, g_11d, equal_var=False)

        # Cohen's d effect size
        pooled_std = np.sqrt(((len(s_vals)-1)*np.var(s_vals, ddof=1) + (len(g_vals)-1)*np.var(g_vals, ddof=1)) / (len(s_vals)+len(g_vals)-2))
        cohens_d = float((mean_space - mean_ground) / pooled_std) if pooled_std > 0 else 0.0

        g_class = annots.loc[m, 'Glycan_Class'] if m in annots.index else 'Other'
        clade = annots.loc[m, 'Polysaccharide_Clade'] if m in annots.index else 'Other'
        epitope = annots.loc[m, 'Target_Epitope'] if m in annots.index else ''

        diff_results.append({
            'mAb': m,
            'Glycan_Class': g_class,
            'Polysaccharide_Clade': clade,
            'Target_Epitope': epitope,
            'Mean_Ground': mean_ground,
            'Mean_Space': mean_space,
            'Fold_Change': float(fc),
            'log2FC': log2fc,
            'pvalue': float(p_val),
            'log2FC_6d': log2fc_6d,
            'pvalue_6d': float(p_6d) if not np.isnan(p_6d) else 1.0,
            'log2FC_11d': log2fc_11d,
            'pvalue_11d': float(p_11d) if not np.isnan(p_11d) else 1.0,
            'Cohens_d': cohens_d
        })

    df_diff = pd.DataFrame(diff_results)

    # Benjamini-Hochberg FDR correction
    p_vals = df_diff['pvalue'].values
    order = np.argsort(p_vals)
    ranked_p = p_vals[order]
    fdr = np.zeros(len(p_vals))
    for i in range(len(p_vals)):
        fdr[order[i]] = ranked_p[i] * len(p_vals) / (i + 1)
    fdr = np.minimum.accumulate(fdr[::-1])[::-1]
    fdr = np.clip(fdr, 0, 1.0)
    df_diff['FDR'] = fdr

    # Save CSV
    df_diff.to_csv(os.path.join(results_dir, 'differential_glycomics_results.csv'), index=False)
    print(f"Differential analysis complete. Significant mAbs (p < 0.05): {sum(df_diff['pvalue'] < 0.05)}/{len(df_diff)}")

    # 1. Publication Volcano Plot
    plt.figure(figsize=(10, 7))
    df_diff['neg_log10_p'] = -np.log10(df_diff['pvalue'])
    
    sns.scatterplot(
        data=df_diff,
        x='log2FC',
        y='neg_log10_p',
        hue='Glycan_Class',
        style=(df_diff['pvalue'] < 0.05),
        s=90,
        alpha=0.85
    )
    plt.axhline(-np.log10(0.05), color='gray', linestyle='--', linewidth=1, label='p = 0.05')
    plt.axvline(0.5, color='gray', linestyle=':', linewidth=0.8)
    plt.axvline(-0.5, color='gray', linestyle=':', linewidth=0.8)

    # Label top prominent mAbs (e.g. CCRC-M138, CCRC-M140, JIM13, CCRC-M1, etc.)
    top_mabs = df_diff.sort_values(by='pvalue').head(12)
    for _, r in top_mabs.iterrows():
        plt.annotate(r['mAb'], (r['log2FC']+0.02, r['neg_log10_p']+0.03), fontsize=8, fontweight='bold')

    plt.title('Differential Glycome Profiling Volcano Plot: Spaceflight vs Ground (OSD-615)', fontsize=13, fontweight='bold')
    plt.xlabel('$\log_2$ Fold Change (Spaceflight / Ground Control)', fontsize=11, fontweight='bold')
    plt.ylabel('$-\log_{10}$ p-value', fontsize=11, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '02_glycomics_volcano_plot.png'), dpi=300)
    plt.close()
    print("Saved 02_glycomics_volcano_plot.png")

    # 2. Bar chart of Top Differentially Expressed Epitopes
    fig, ax = plt.subplots(figsize=(12, 6))
    top_up_down = pd.concat([
        df_diff.sort_values(by='log2FC', ascending=False).head(10),
        df_diff.sort_values(by='log2FC', ascending=True).head(10)
    ])
    colors = ['#E85D50' if x > 0 else '#2F5985' for x in top_up_down['log2FC']]
    ax.barh(top_up_down['mAb'], top_up_down['log2FC'], color=colors)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlabel('$\log_2$ Fold Change in Spaceflight', fontsize=11, fontweight='bold')
    ax.set_title('Top Altered Glycan Epitopes in Arabidopsis Roots (Space vs Ground)', fontsize=13, fontweight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, '02_top_altered_epitopes_barchart.png'), dpi=300)
    plt.close()
    print("Saved 02_top_altered_epitopes_barchart.png")

    # 3. Export JSON for Dashboard
    out_json = {
        "items": df_diff.to_dict('records'),
        "summary": {
            "total_mAbs": len(df_diff),
            "sig_p05": int(sum(df_diff['pvalue'] < 0.05)),
            "sig_p01": int(sum(df_diff['pvalue'] < 0.01)),
            "top_upregulated": df_diff.sort_values(by='log2FC', ascending=False)['mAb'].head(5).tolist(),
            "top_downregulated": df_diff.sort_values(by='log2FC', ascending=True)['mAb'].head(5).tolist()
        }
    }
    with open(os.path.join(docs_dir, 'differential_results.json'), 'w') as f:
        json.dump(out_json, f, indent=2)
    with open(os.path.join(results_dir, 'differential_results.json'), 'w') as f:
        json.dump(out_json, f, indent=2)

    print("Differential analysis pipeline finished successfully.")

if __name__ == '__main__':
    run_differential_analysis()
