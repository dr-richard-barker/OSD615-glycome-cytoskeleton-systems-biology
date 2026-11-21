"""
test_fair_compliance.py
Validates FAIR deposit schemas (RO-Crate 1.1 and Zenodo).
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAIR_DIR = os.path.join(BASE_DIR, 'fair_deposit')

def test_ro_crate_metadata_structure():
    """Assert RO-Crate metadata conforms to W3C RO-Crate 1.1 schema."""
    crate_path = os.path.join(FAIR_DIR, 'ro-crate-metadata.json')
    assert os.path.exists(crate_path), f"Missing {crate_path}"
    with open(crate_path, 'r', encoding='utf-8') as f:
        crate = json.load(f)
    
    assert "@context" in crate
    assert "https://w3id.org/ro/crate/1.1/context" in str(crate["@context"])
    assert "@graph" in crate
    
    # Root dataset node
    root_nodes = [n for n in crate["@graph"] if n.get("@id") == "./"]
    assert len(root_nodes) == 1, "Must contain exactly one root dataset node with @id './'"
    root = root_nodes[0]
    assert "name" in root
    assert "description" in root
    assert "license" in root
    assert "isBasedOn" in root
    assert "hasPart" in root

def test_zenodo_metadata_structure():
    """Assert Zenodo metadata contains required deposit keys."""
    zenodo_path = os.path.join(FAIR_DIR, 'zenodo.json')
    assert os.path.exists(zenodo_path), f"Missing {zenodo_path}"
    with open(zenodo_path, 'r', encoding='utf-8') as f:
        z = json.load(f)
    
    assert "title" in z
    assert "description" in z
    assert "creators" in z and len(z["creators"]) > 0
    assert "keywords" in z and len(z["keywords"]) >= 5
    assert "license" in z
    assert "related_identifiers" in z
