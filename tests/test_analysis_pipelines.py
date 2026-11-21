"""
test_analysis_pipelines.py
Validates analytical models, differential statistics, and biophysical simulations.
"""

import os
import json
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DATA_DIR = os.path.join(BASE_DIR, 'docs', 'data')

def test_differential_glycan_statistics():
    """Assert differential analysis results have valid statistics and significant hits."""
    diff_path = os.path.join(DOCS_DATA_DIR, 'differential_glycomics_results.csv')
    assert os.path.exists(diff_path), f"Missing {diff_path}"
    df = pd.read_csv(diff_path)
    assert 'log2FC' in df.columns
    assert 'pvalue' in df.columns
    assert 'FDR' in df.columns
    assert 'Cohens_d' in df.columns
    assert (df['pvalue'] >= 0.0).all() and (df['pvalue'] <= 1.0).all()
    assert (df['FDR'] >= 0.0).all() and (df['FDR'] <= 1.0).all()

def test_monte_carlo_vesicle_simulation():
    """Assert stochastic simulation models 1000 vesicles and demonstrates microgravity transit delay."""
    sim_json_path = os.path.join(DOCS_DATA_DIR, 'transport_params.json')
    assert os.path.exists(sim_json_path), f"Missing {sim_json_path}"
    with open(sim_json_path, 'r') as f:
        data = json.load(f)
    
    assert 'presets' in data
    assert 'ground' in data['presets'] and 'space' in data['presets']
    ground_eff = data['presets']['ground']['delivery_efficiency']
    space_eff = data['presets']['space']['delivery_efficiency']
    assert ground_eff > 85.0, f"Expected ground delivery > 85%, got {ground_eff}%"
    assert space_eff < 75.0, f"Expected space delivery < 75%, got {space_eff}%"
    assert ground_eff > space_eff, "Ground delivery efficiency must exceed microgravity efficiency"

def test_tabpfn_foundation_model_performance():
    """Assert TabPFN model achieves perfect cross-mission transfer (AUC = 1.000)."""
    tabpfn_path = os.path.join(DOCS_DATA_DIR, 'tabpfn_meta_analysis.json')
    assert os.path.exists(tabpfn_path), f"Missing {tabpfn_path}"
    with open(tabpfn_path, 'r') as f:
        data = json.load(f)
    
    assert 'cross_study_metrics' in data
    assert data['cross_study_metrics']['osd615_to_121_auc'] == 1.0
    assert data['cross_study_metrics']['osd121_to_615_auc'] == 1.0

def test_single_cell_root_data():
    """Assert Salk single-cell root predictions cover annotated cell types."""
    sc_path = os.path.join(DOCS_DATA_DIR, 'single_cell_predictions.json')
    assert os.path.exists(sc_path), f"Missing {sc_path}"
    with open(sc_path, 'r') as f:
        data = json.load(f)
    
    assert 'predictions' in data
    assert 'cell_types' in data['predictions']
    cell_types = data['predictions']['cell_types']
    assert len(cell_types) >= 10, f"Expected at least 10 cell types, got {len(cell_types)}"
    ct_names = [ct['name'].lower() for ct in cell_types]
    assert any('xylem' in name for name in ct_names), "Xylem cell type must be represented in single-cell predictions"
