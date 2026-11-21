"""
test_data_integrity.py
Validates empirical data matrices, metadata schemas, and absence of missing values.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def test_glycomics_matrix_dimensions():
    """Assert OSD-615 matrix has exactly 12 samples and 155 monoclonal antibodies."""
    matrix_path = os.path.join(DATA_DIR, 'glycomics_matrix.csv')
    assert os.path.exists(matrix_path), f"Missing {matrix_path}"
    df = pd.read_csv(matrix_path, index_col=0)
    assert df.shape == (12, 155), f"Expected (12, 155), got {df.shape}"
    assert not df.isna().any().any(), "Matrix contains NaN values"
    assert not np.isinf(df.values).any(), "Matrix contains infinite values"
    assert (df.values >= 0).all(), "Glycomics ELISA OD450 values must be non-negative"

def test_glycomics_metadata_completeness():
    """Assert metadata covers all 12 biological replicates with balanced factors."""
    meta_path = os.path.join(DATA_DIR, 'glycomics_metadata.csv')
    assert os.path.exists(meta_path), f"Missing {meta_path}"
    df = pd.read_csv(meta_path)
    assert len(df) == 12, f"Expected 12 metadata rows, got {len(df)}"
    assert set(df['Spaceflight'].unique()) == {'Ground', 'Space'}
    assert set(df['Growth_Time'].astype(str).unique()) == {'6', '11'}
    assert set(df['Condition_Group'].unique()) == {'Ground_6d', 'Ground_11d', 'Space_6d', 'Space_11d'}
    
    # 3 replicates per condition group
    group_counts = df['Condition_Group'].value_counts()
    for group, count in group_counts.items():
        assert count == 3, f"Group {group} has {count} replicates, expected 3"

def test_glycan_annotations():
    """Assert all 155 antibodies are annotated with valid CCRC glycan classes."""
    annots_path = os.path.join(DATA_DIR, 'glycan_class_annotations.csv')
    assert os.path.exists(annots_path), f"Missing {annots_path}"
    df = pd.read_csv(annots_path)
    assert len(df) == 155, f"Expected 155 annotated mAbs, got {len(df)}"
    assert 'mAb' in df.columns and 'Glycan_Class' in df.columns
    classes = df['Glycan_Class'].unique()
    assert len(classes) >= 5, f"Expected at least 5 glycan classes, found {len(classes)}"

def test_rnaseq_degs():
    """Assert RNA-Seq dataset contains key cytoskeletal and cell wall targets."""
    rnaseq_path = os.path.join(DATA_DIR, 'rnaseq_cytoskeleton_degs.csv')
    assert os.path.exists(rnaseq_path), f"Missing {rnaseq_path}"
    df = pd.read_csv(rnaseq_path)
    assert len(df) >= 20, f"Expected at least 20 genes, got {len(df)}"
    gene_symbols = set(df['Gene_Symbol'].values)
    must_include = {'MYA1', 'CESA4', 'CESA7', 'IRX9', 'IRX10', 'SPR1', 'SEC', 'SPY'}
    for gene in must_include:
        assert gene in gene_symbols, f"Missing critical gene {gene} in RNA-Seq DEG table"
