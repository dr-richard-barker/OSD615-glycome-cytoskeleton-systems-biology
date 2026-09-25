"""
build_dashboard.py
Synchronizes genuine analytical results, precomputed models, and publication figures
from analysis/results/ and analysis/figures/ to the static web dashboard directory docs/.
Does NOT overwrite customized HTML, CSS, or JS application controllers.
"""

import os
import shutil

root_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(root_dir, 'docs')
data_dir = os.path.join(docs_dir, 'data')
figures_dir = os.path.join(docs_dir, 'figures')
cose_dir = os.path.join(docs_dir, 'cose')

os.makedirs(data_dir, exist_ok=True)
os.makedirs(figures_dir, exist_ok=True)
os.makedirs(cose_dir, exist_ok=True)

# Copy branding assets if present
branding_sources = [
    ('/Users/drb_laptop/Documents/AIRI_to_AIR/docs/cose/cose-logo.png', os.path.join(cose_dir, 'cose-logo.png')),
    ('/Users/drb_laptop/Documents/AIRI_to_AIR/docs/cose/regolith-logo.png', os.path.join(cose_dir, 'regolith-logo.png'))
]
for src, dst in branding_sources:
    if os.path.exists(src):
        shutil.copy(src, dst)

# Synchronize analytical results to docs/data/
results_dir = os.path.join(root_dir, 'analysis', 'results')
if os.path.exists(results_dir):
    for fn in os.listdir(results_dir):
        if fn.endswith('.json') or fn.endswith('.csv'):
            src_fp = os.path.join(results_dir, fn)
            dst_fp = os.path.join(data_dir, fn)
            shutil.copy(src_fp, dst_fp)
    print("Synchronized empirical analysis results to docs/data/.")

# Synchronize publication figures to docs/figures/
analysis_figs = os.path.join(root_dir, 'analysis', 'figures')
if os.path.exists(analysis_figs):
    for fn in os.listdir(analysis_figs):
        if fn.endswith('.png') or fn.endswith('.svg') or fn.endswith('.pdf'):
            src_fp = os.path.join(analysis_figs, fn)
            dst_fp = os.path.join(figures_dir, fn)
            shutil.copy(src_fp, dst_fp)
    print("Synchronized figures to docs/figures/.")

print("Dashboard asset synchronization complete (safe mode - no layout clobbering).")
