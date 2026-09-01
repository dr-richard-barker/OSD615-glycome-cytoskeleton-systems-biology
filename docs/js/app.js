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
import './tabpfn-viewer.js';

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

    // Trigger window resize and Plotly chart recalculation
    setTimeout(() => {
        window.dispatchEvent(new Event('resize'));
        ['heatmap', 'volcano', 'bar-chart', 'circle-plot', 'cim-heatmap', 'tabpfn-roc-plot', 'tabpfn-importance-plot'].forEach(id => {
            const el = document.getElementById(id);
            if (el && window.Plotly && el.data) {
                try {
                    window.Plotly.Plots.resize(el);
                } catch (e) {}
            }
        });
    }, 60);
}

// Navigation Event Listeners
document.querySelectorAll('.nav-link, .nav-trigger').forEach(el => {
    el.addEventListener('click', e => {
        e.preventDefault();
        const tabId = el.getAttribute('data-tab') || el.getAttribute('href')?.replace('#', '');
        if (tabId) {
            switchTab(tabId);
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

function updateThemeUI(theme) {
    const themeIcon = document.getElementById('theme-icon');
    const themeText = document.getElementById('theme-text');
    if (themeIcon && themeText) {
        if (theme === 'light') {
            themeIcon.className = 'fas fa-sun';
            themeText.innerText = 'Light Mode';
        } else {
            themeIcon.className = 'fas fa-moon';
            themeText.innerText = 'Dark Mode';
        }
    }
}

// Dark / Light Theme Toggle with LocalStorage Persistence
const themeToggle = document.getElementById('theme-toggle');
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const html = document.documentElement;
        const nextTheme = html.dataset.theme === 'dark' ? 'light' : 'dark';
        html.dataset.theme = nextTheme;
        localStorage.setItem('theme', nextTheme);
        updateThemeUI(nextTheme);
        
        // Broadcast custom event for all charts to re-theme
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: nextTheme } }));
        window.dispatchEvent(new Event('resize'));
    });
}

// Restore saved theme on startup
const savedTheme = localStorage.getItem('theme') || 'dark';
document.documentElement.dataset.theme = savedTheme;
updateThemeUI(savedTheme);