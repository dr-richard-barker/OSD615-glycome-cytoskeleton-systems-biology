import os
import json
import requests

def search_veggie():
    url = "https://osdr.nasa.gov/osdr/data/search?term=veggie&ffield=organism&fvalue=Arabidopsis thaliana&type=cgene&size=100"
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir_proc = os.path.join(base_dir, 'data', 'processed')
    out_dir_docs = os.path.join(base_dir, 'docs', 'data')
    os.makedirs(out_dir_proc, exist_ok=True)
    os.makedirs(out_dir_docs, exist_ok=True)
    
    fallback_data = [
        {"Accession": "OSD-615", "Study Title": "Veggie-3", "organism": "Arabidopsis thaliana"},
        {"Accession": "OSD-218", "Study Title": "APEX-03-2", "organism": "Arabidopsis thaliana"},
        {"Accession": "OSD-217", "Study Title": "APEX-03-1", "organism": "Arabidopsis thaliana"}
    ]
    
    try:
        print("Querying OSDR...")
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        print("Success.")
    except Exception as e:
        print(f"Failed to fetch: {e}. Using fallback.")
        data = {"hits": {"hits": [{"_source": item} for item in fallback_data]}}
    
    registry = []
    for hit in data.get("hits", {}).get("hits", []):
        source = hit.get("_source", {})
        registry.append({
            "Accession": source.get("Accession", ""),
            "Study Title": source.get("Study Title", ""),
            "organism": source.get("organism", ""),
            "Study Assay Technology Type": source.get("Study Assay Technology Type", ""),
            "Mission": source.get("Mission", ""),
            "Experiment Platform": source.get("Experiment Platform", "")
        })
        
    for out in [os.path.join(out_dir_proc, 'veggie_study_registry.json'), os.path.join(out_dir_docs, 'veggie_studies.json')]:
        with open(out, 'w') as f:
            json.dump(registry, f, indent=4)
    print("Registry saved.")

if __name__ == '__main__':
    search_veggie()
