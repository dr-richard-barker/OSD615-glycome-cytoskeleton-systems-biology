// NASA OSDR VEGGIE Hardware Study Explorer Module
let allStudies = [];

export function initVeggieExplorer() {
    fetch('data/veggie_studies.json')
        .then(r => r.json())
        .then(data => {
            allStudies = data;
            renderTable(allStudies);
            setupSearch();
        })
        .catch(err => console.error('Error loading VEGGIE studies:', err));
}

function renderTable(studies) {
    const tbody = document.querySelector('#veggie-table tbody');
    if (!tbody) return;

    let html = '';
    studies.forEach(s => {
        const osdrUrl = `https://osdr.nasa.gov/bio/repo/data/studies/${s.Accession}`;
        const doiUrl = s.DOI ? `https://doi.org/${s.DOI}` : '#';

        html += `<tr>
            <td><a href="${osdrUrl}" target="_blank" style="color:var(--teal); font-weight:bold; text-decoration:none;">${s.Accession} ↗</a></td>
            <td><strong>${s.Title}</strong></td>
            <td><em>${s.Organism}</em></td>
            <td><span style="font-size:0.85rem; color:#64748b;">${s.Hardware}<br>${s.Mission}</span></td>
            <td>${s.Assay}</td>
            <td>${s.DOI ? `<a href="${doiUrl}" target="_blank" style="color:var(--coral); font-size:0.85rem;">${s.DOI} ↗</a>` : '—'}</td>
        </tr>`;
    });
    tbody.innerHTML = html;
}

function setupSearch() {
    const searchInput = document.getElementById('veggie-search');
    if (!searchInput) return;

    searchInput.addEventListener('input', e => {
        const q = e.target.value.toLowerCase().trim();
        if (!q) {
            renderTable(allStudies);
            return;
        }

        const filtered = allStudies.filter(s => {
            return s.Accession.toLowerCase().includes(q) ||
                   s.Title.toLowerCase().includes(q) ||
                   s.Organism.toLowerCase().includes(q) ||
                   s.Assay.toLowerCase().includes(q) ||
                   s.Mission.toLowerCase().includes(q);
        });
        renderTable(filtered);
    });
}

// Auto init
initVeggieExplorer();