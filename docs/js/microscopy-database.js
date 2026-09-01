// Interactive Microscopy & IHC Image Database Module
// Connects in situ microscopy images from PMC10444889 (Nakashima et al. 2023 / 41526_2023_312_MOESM2_ESM.pdf)
// with side-by-side ggPlantmap spatial predictions

let microscopyData = [];
let currentCategory = 'all';

export function initMicroscopyDatabase() {
    fetch('data/microscopy_database.json')
        .then(r => r.json())
        .then(res => {
            microscopyData = res.images || [];
            renderGallery(microscopyData);
            setupFilters();
        })
        .catch(err => console.error('Error loading microscopy database:', err));
}

function renderGallery(images) {
    const galleryEl = document.getElementById('microscopy-gallery');
    if (!galleryEl) return;

    if (!images || images.length === 0) {
        galleryEl.innerHTML = '<div style="padding:20px; text-align:center; color:#94a3b8;">No matching microscopy panels found.</div>';
        return;
    }

    let html = '';
    images.forEach(img => {
        const isSuppl = img.category === 'Supplementary';
        const badgeColor = isSuppl ? '#8B5CF6' : 'var(--navy)';
        
        html += `
            <div class="card microscopy-card" style="display:flex; flex-direction:column; gap:12px; margin-bottom:20px; border-left: 4px solid ${isSuppl ? '#8B5CF6' : 'var(--teal)'};">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:8px;">
                    <div>
                        <span class="badge" style="background:${badgeColor}; color:#fff; font-size:0.75rem; padding:3px 8px; border-radius:4px;">${img.figure}</span>
                        <strong style="margin-left:8px; font-size:1.05rem; color:var(--text);">${img.title}</strong>
                    </div>
                    <span style="font-size:0.8rem; color:#64748b;">${img.modality}</span>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:15px; align-items:center;">
                    <div style="text-align:center; background:#070d18; padding:10px; border-radius:6px; border:1px solid rgba(255,255,255,0.05);">
                        <img src="microscopy_images/${img.filename}" alt="${img.title}" style="max-width:100%; height:auto; max-height:360px; border-radius:4px; object-fit:contain; cursor:pointer;" onclick="window.open('microscopy_images/${img.filename}', '_blank')">
                        <div style="font-size:0.75rem; color:#94a3b8; margin-top:6px;">🔍 Click image to open full high-resolution view</div>
                    </div>

                    <div style="font-size:0.9rem; line-height:1.5;">
                        <p><strong>Tissue & Stage:</strong> ${img.tissue} (${img.stage})</p>
                        ${img.antibodies ? `<p><strong>Target Antibodies:</strong> <span style="color:var(--coral); font-weight:bold;">${img.antibodies.join(', ')}</span></p>` : ''}
                        ${img.findings ? `<p><strong>Key In Situ Finding:</strong> ${img.findings}</p>` : `<p><strong>Description:</strong> ${img.description || ''}</p>`}
                        
                        <div style="background:rgba(63, 182, 168, 0.08); border-left:3px solid var(--teal); padding:8px 12px; border-radius:4px; margin-top:10px; font-size:0.85rem; color:#cbd5e1;">
                            <strong>Multi-Omics Context:</strong> Validates spaceflight remodeling of secondary cell wall xylan and motor transport complexes (<em>IRX9</em>, <em>CESA4</em>, <em>MYA1</em>) in xylem and root tissues.
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    galleryEl.innerHTML = html;
}

function setupFilters() {
    const filterInput = document.getElementById('microscopy-search');
    const categorySelect = document.getElementById('microscopy-category');

    function applyFilters() {
        const q = filterInput ? filterInput.value.toLowerCase().trim() : '';
        const cat = categorySelect ? categorySelect.value : 'all';

        const filtered = microscopyData.filter(img => {
            const matchesCat = cat === 'all' || 
                               (cat === 'main' && img.category === 'Main') || 
                               (cat === 'suppl' && img.category === 'Supplementary') ||
                               (cat === 'ihc' && img.modality.includes('Confocal')) ||
                               (cat === 'histology' && (img.modality.includes('Histology') || img.modality.includes('Stereomicroscopy') || img.modality.includes('Morphometric')));
            
            const matchesQuery = !q || 
                                 img.title.toLowerCase().includes(q) || 
                                 img.figure.toLowerCase().includes(q) || 
                                 (img.findings && img.findings.toLowerCase().includes(q)) || 
                                 (img.antibodies && img.antibodies.some(a => a.toLowerCase().includes(q)));
            
            return matchesCat && matchesQuery;
        });

        renderGallery(filtered);
    }

    if (filterInput) {
        filterInput.addEventListener('input', applyFilters);
    }
    if (categorySelect) {
        categorySelect.addEventListener('change', applyFilters);
    }
}

// Safe DOM initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMicroscopyDatabase);
} else {
    initMicroscopyDatabase();
}
