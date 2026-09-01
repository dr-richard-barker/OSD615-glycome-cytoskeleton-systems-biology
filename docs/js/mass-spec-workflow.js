// Mass Spectrometry Workflows Module

export function initMassSpecWorkflow() {
    fetch('data/mass_spec_workflow.json')
        .then(r => r.json())
        .then(data => {
            const workflows = data.workflows;
            renderWorkflow(workflows[0]);
            setupWorkflowTabs(workflows);
        })
        .catch(err => console.error('Error loading mass spec workflow:', err));
}

function renderWorkflow(wf) {
    const titleEl = document.getElementById('ms-workflow-title');
    const container = document.getElementById('ms-step-container');
    if (!titleEl || !container || !wf) return;

    titleEl.innerText = wf.title;
    let html = '';
    wf.steps.forEach(s => {
        html += `<div class="step-card">
            <div class="step-number">Step ${s.step}</div>
            <div class="step-title">${s.name}</div>
            <div class="step-desc">${s.details}</div>
        </div>`;
    });
    container.innerHTML = html;
}

function setupWorkflowTabs(workflows) {
    const b1 = document.getElementById('ms-tab-1');
    const b2 = document.getElementById('ms-tab-2');
    const b3 = document.getElementById('ms-tab-3');

    if (b1) {
        b1.addEventListener('click', () => {
            renderWorkflow(workflows[0]);
            b1.className = 'btn-primary';
            if (b2) b2.className = 'btn-secondary';
            if (b3) b3.className = 'btn-secondary';
        });
    }
    if (b2) {
        b2.addEventListener('click', () => {
            renderWorkflow(workflows[1]);
            if (b1) b1.className = 'btn-secondary';
            b2.className = 'btn-primary';
            if (b3) b3.className = 'btn-secondary';
        });
    }
    if (b3) {
        b3.addEventListener('click', () => {
            renderWorkflow(workflows[2]);
            if (b1) b1.className = 'btn-secondary';
            if (b2) b2.className = 'btn-secondary';
            b3.className = 'btn-primary';
        });
    }
}

// Auto init
initMassSpecWorkflow();
