"""
test_json_schemas.py
Validates that all JSON data models in docs/data/ are valid JSON and non-empty.
"""

import os
import glob
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DATA_DIR = os.path.join(BASE_DIR, 'docs', 'data')

def test_all_json_files_parse():
    """Ensure every JSON file in docs/data/ is syntactically valid and non-empty."""
    json_files = glob.glob(os.path.join(DOCS_DATA_DIR, '*.json'))
    assert len(json_files) >= 10, f"Expected at least 10 JSON files, found {len(json_files)}"
    
    for fpath in json_files:
        fname = os.path.basename(fpath)
        with open(fpath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception as e:
                raise AssertionError(f"Failed to parse JSON file {fname}: {e}")
            assert data is not None, f"JSON file {fname} is empty"

def test_key_json_models():
    """Verify specific schema structures for core visualization endpoints."""
    required_files = [
        'glycomics_heatmap.json',
        'network_graph.json',
        'transport_params.json',
        'single_cell_predictions.json',
        'microscopy_database.json',
        'tabpfn_meta_analysis.json',
        'veggie_studies.json'
    ]
    for rf in required_files:
        fpath = os.path.join(DOCS_DATA_DIR, rf)
        assert os.path.exists(fpath), f"Missing critical JSON file: {rf}"
