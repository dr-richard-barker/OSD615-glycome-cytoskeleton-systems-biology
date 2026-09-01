# 🧬 Glycome–Cytoskeleton Systems Biology: OSD-615 Follow-Up

**Linking glycomics data to actin and kinesin/myosin cytoskeletal machinery in *Arabidopsis thaliana* under microgravity via multi-omics integration and dynamic systems modeling.**

[![GitHub Pages](https://img.shields.io/badge/Dashboard-Live-brightgreen?logo=github)](https://dr-richard-barker.github.io/OSD615-glycome-cytoskeleton-systems-biology/)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.XXXXX-blue)](https://doi.org/10.5281/zenodo.XXXXX)
[![License: MIT](https://img.shields.io/badge/Code-MIT-yellow.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0)
[![FAIR](https://img.shields.io/badge/FAIR-Compliant-orange)](fair_deposit/)

---

## Overview

This repository is a follow-up research project to NASA OSD-615 (Advanced Plant EXperiment 03-1), which demonstrated that microgravity profoundly remodels *Arabidopsis thaliana* root cell walls using glycome profiling with ~155 monoclonal antibodies (Nakashima et al. 2023, *npj Microgravity* 9:67).

**This project extends the original study by:**

1. **Multi-omics integration** of OSD-615 glycomics ELISA data with companion RNA-Seq from OSDR VEGGIE hardware studies (OSD-218, OSD-217)
2. **Network modeling** of how cytoskeletal transport machinery (kinesins, myosins, MAPs) connects to cell wall glycan deposition
3. **Dynamic simulation** of motor-driven vesicle transport under normal vs. microgravity conditions
4. **Comprehensive review** of O-GlcNAcylation of motor protein complexes across kingdoms
5. **Interactive dashboard** with live data exploration and transport simulator

## Key Question

> How does microgravity-induced disruption of the cytoskeletal network alter Golgi-to-cell-wall secretory vesicle delivery, and can systems biology modeling predict the resulting cell wall glycan remodeling observed in spaceflight roots?

## Data Sources

| Study | Accession | Data Type | Hardware | Reference |
|-------|-----------|-----------|----------|-----------|
| APEX-03-1 | [OSD-615](https://osdr.nasa.gov/bio/repo/data/studies/OSD-615) | Glycome profiling (ELISA, 155 mAbs) | ISS Veggie | Nakashima et al. 2023 |
| APEX-03-2 | [OSD-218](https://osdr.nasa.gov/bio/repo/data/studies/OSD-218) | RNA-Seq (Col-0, Ws, spr1, sku5) | ISS Veggie | Califar et al. 2020 |
| APEX-03-2 | [OSD-217](https://osdr.nasa.gov/bio/repo/data/studies/OSD-217) | WGBS + RNA-Seq (Ws) | ISS Veggie | Zhou et al. 2019 |
| Additional VEGGIE studies | Multiple | RNA-Seq | ISS Veggie | Various |

## Project Structure

```
├── data/                  # Data acquisition and curation
├── analysis/              # Python analysis pipeline (9 scripts)
├── manuscript/            # LaTeX manuscript (npj format) + Word doc
├── docs/                  # Interactive GitHub Pages dashboard
└── fair_deposit/          # FAIR metadata (RO-Crate, Zenodo, CITATION.cff)
```

## Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/dr-richard-barker/OSD615-glycome-cytoskeleton-systems-biology.git
cd OSD615-glycome-cytoskeleton-systems-biology
python -m venv .venv && source .venv/bin/activate
pip install -r analysis/requirements.txt

# 2. Fetch data from NASA OSDR
python data/fetch_osdr_data.py
python data/search_veggie_studies.py
python data/curate_data.py

# 3. Run analysis pipeline
for script in analysis/0*.py; do python "$script"; done

# 4. Build manuscript
cd manuscript && make all
```

## Interactive Dashboard

Visit the [live dashboard](https://dr-richard-barker.github.io/OSD615-glycome-cytoskeleton-systems-biology/) to explore:

- 🔥 **Glycomics Heatmap** — Interactive 155 mAb × 12 sample clustered heatmap
- 🌋 **Differential Analysis** — Volcano plots and effect size comparisons
- 🔗 **Network Viewer** — Cytoscape.js protein–protein interaction network
- 🚀 **Transport Simulator** — Interactive motor-vesicle transport simulation
- 🔬 **MS Workflow** — Step-through mass spectrometry protocol diagrams
- 📊 **Multi-Omics Integration** — sPLS correlation circles and CIM heatmaps

## Citation

```bibtex
@software{barker2026glycome_cytoskeleton,
  author = {Barker, Richard},
  title = {Glycome-Cytoskeleton Systems Biology: Follow-Up to OSD-615},
  year = {2026},
  url = {https://github.com/dr-richard-barker/OSD615-glycome-cytoskeleton-systems-biology}
}
```

## Acknowledgments

This work builds on data from NASA's Open Science Data Repository (OSDR) and the GeneLab program. We thank the APEX-03 investigation team (Blancaflor, Gilroy, Nakashima, Pattathil, Hahn) for generating the foundational glycomics dataset.

## License

- **Code**: [MIT License](LICENSE)
- **Data & Manuscript**: [CC BY 4.0](LICENSE-CC-BY-4.0)
