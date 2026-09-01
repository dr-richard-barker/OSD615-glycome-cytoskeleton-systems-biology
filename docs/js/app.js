// Main Dashboard Application Controller
import './glycomics-heatmap.js';
import './charts.js';
import './multiomics-integration.js';
import './network-viewer.js';
import './pathway-diagram.js';
import './transport-simulator.js';
import './mass-spec-workflow.js';
import './veggie-study-explorer.js';
import './ggplantmap-viewer.js';
import './microscopy-database.js';

// Navigation & Tab Switching
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', e => {
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
        
        e.currentTarget.classList.add('active');
        const tabId = e.currentTarget.getAttribute('data-tab');
        const targetTab = document.getElementById(tabId);
        if (targetTab) {
            targetTab.classList.add('active');
        }

        // Trigger Plotly / Cytoscape / Canvas resizes
        window.dispatchEvent(new Event('resize'));
    });
});

// Dark / Light Theme Toggle with LocalStorage Persistence
const themeToggle = document.getElementById('theme-toggle');
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const html = document.documentElement;
        const nextTheme = html.dataset.theme === 'dark' ? 'light' : 'dark';
        html.dataset.theme = nextTheme;
        localStorage.setItem('theme', nextTheme);
        window.dispatchEvent(new Event('resize'));
    });
}

// Restore saved theme on startup
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    document.documentElement.dataset.theme = savedTheme;
}