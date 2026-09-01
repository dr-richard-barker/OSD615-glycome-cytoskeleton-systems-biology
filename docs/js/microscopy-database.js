// Interactive Microscopy & IHC Image Database Module
// Connects in situ microscopy images from PMC10444889 (Nakashima et al. 2023)
// with side-by-side ggPlantmap spatial predictions

let microscopyData = [];

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

    let html = '';
    images.forEach(img => {
        html += `
            <div class="card microscopy-card" style="display:flex; flex-direction:column; gap:12px; margin-bottom:20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border); padding-bottom:8px;">
                    <div>
                        <span class="badge" style="background:var(--navy); color:#fff; font-size:0.75rem; padding:3px 8px; border-radius:4px;">${img.figure}</span>
                        <strong style="margin-left:8px; font-size:1.05rem; color:var(--text);">${img.title}</strong>
                    </div>
                    <span style="font-size:0.8rem; color:#64748b;">${img.modality}</span>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:15px; align-items:center;">
                    <div style="text-align:center; background:#0a0f1d; padding:10px; border-radius:6px;">
                        <img src="microscopy_images/${img.filename}" alt="${img.title}" style="max-width:100%; height:auto; max-height:360px; border-radius:4px; object-fit:contain;" onclick="window.open('microscopy_images/${img.filename}', '_blank')">
                        <div style="font-size:0.75rem; color:#94a3b8; margin-top:4px;">🔍 Click image to open high-resolution view</div>
                    </div>

                    <div style="font-size:0.9rem; line-height:1.5;">
                        <p><strong>Tissue & Stage:</strong> ${img.tissue} (${img.stage})</p>
                        ${img.antibodies ? `<p><strong>Target Antibodies:</strong> <span style="color:var(--coral); font-weight:bold;">${img.antibodies.join(', ')}</span></p>` : ''}
                        ${img.findings ? `<p><strong>Key In Situ Finding:</strong> ${img.findings}</p>` : `<p><strong>Description:</strong> ${img.description}</p>`}
                        
                        <div style="background:rgba(63, 182, 168, 0.1); border-left:3px solid var(--teal); padding:8px 12px; border-radius:4px; margin-top:10px; font-size:0.85rem;">
                            <strong>Multi-Omics Context:</strong> Validates spaceflight upregulation of secondary cell wall xylan and motor transport complexes (*IRX9*, *CESA4*, *MYA1*) in xylem tissues.
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
    if (!filterInput) return;

    filterInput.addEventListener('input', e => {
        const q = e.target.value.toLowerCase().trim();
        if (!q) {
            renderGallery(microscopyData);
            return;
        }

        const filtered = microscopyData.filter(img => {
            return img.title.toLowerCase().includes(q) ||
                   img.figure.toLowerCase().includes(q) ||
                   img.tissue.toLowerCase().includes(q) ||
                   (img.antibodies && img.antibodies.some(a => a.toLowerCase().includes(q))) ||
                   (img.findings && img.findings.toLowerCase().includes(q));
        });
        renderGallery(filtered);
    });
}

// Auto init
initMicroscopyDatabase();
