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
            themeIcon.className = 'fas fa-moon';
            themeText.innerText = 'Dark Mode';
        } else {
            themeIcon.className = 'fas fa-sun';
            themeText.innerText = 'Light Mode';
        }
    }
    // Sync CoSE chrome rails if present
    document.querySelectorAll('.topbar, .sitebar').forEach(el => {
        el.classList.remove('cose-dark', 'cose-light');
        el.classList.add(theme === 'dark' ? 'cose-dark' : 'cose-light');
    });
}

let activeTheme = localStorage.getItem('theme') || localStorage.getItem('barker.theme') || 'light';

export function applyHardTheme(theme) {
    activeTheme = theme;
    document.documentElement.dataset.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    if (document.body) {
        document.body.dataset.theme = theme;
        document.body.setAttribute('data-theme', theme);
    }
    try {
        localStorage.setItem('theme', theme);
        localStorage.setItem('barker.theme', theme);
    } catch (e) {}
    updateThemeUI(theme);

    // Broadcast custom event for all charts and canvases to re-theme
    window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: theme } }));
    setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
}

// Dark / Light Hard Theme Toggle with LocalStorage Persistence
const themeToggle = document.getElementById('theme-toggle');
if (themeToggle) {
    themeToggle.addEventListener('click', (e) => {
        e.preventDefault();
        const current = document.documentElement.getAttribute('data-theme') || activeTheme;
        const nextTheme = current === 'dark' ? 'light' : 'dark';
        applyHardTheme(nextTheme);
    });
}

// Observe external CoSE theme button changes
const themeObserver = new MutationObserver((mutations) => {
    mutations.forEach((m) => {
        if (m.type === 'attributes' && m.attributeName === 'data-theme') {
            const newTheme = document.documentElement.getAttribute('data-theme');
            if (newTheme && newTheme !== activeTheme) {
                applyHardTheme(newTheme);
            }
        }
    });
});
themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

// Restore or initialize theme on startup
applyHardTheme(activeTheme);