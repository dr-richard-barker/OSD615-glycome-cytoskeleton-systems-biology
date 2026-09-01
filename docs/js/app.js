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

// Global Tab Switching Function
export function switchTab(tabId) {
    if (!tabId) return;
    
    // Update active state on nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('data-tab') === tabId) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Update active state on tab panes
    document.querySelectorAll('.tab-pane, .tab-content').forEach(pane => {
        if (pane.id === tabId) {
            pane.classList.add('active');
        } else {
            pane.classList.remove('active');
        }
    });

    // Scroll to top of main container smoothly
    const mainContainer = document.querySelector('main.container');
    if (mainContainer && window.scrollY > 300) {
        window.scrollTo({ top: 320, behavior: 'smooth' });
    }

    // Trigger window resize for Plotly, Cytoscape, and HTML5 Canvas redraws
    setTimeout(() => {
        window.dispatchEvent(new Event('resize'));
    }, 50);
}

// Navigation Event Listeners
document.querySelectorAll('.nav-link, .nav-trigger').forEach(el => {
    el.addEventListener('click', e => {
        e.preventDefault();
        const tabId = el.getAttribute('data-tab') || el.getAttribute('href')?.replace('#', '');
        if (tabId) {
            switchTab(tabId);
            // Update hash in URL
            history.pushState(null, '', `#${tabId}`);
        }
    });
});

// Deep linking on load from URL hash
window.addEventListener('DOMContentLoaded', () => {
    const hash = window.location.hash.replace('#', '');
    if (hash && document.getElementById(hash)) {
        switchTab(hash);
    }
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