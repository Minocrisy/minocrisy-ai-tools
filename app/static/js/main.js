/**
 * Minocrisy AI Tools - Main JavaScript
 * Contains common functionality used across the application.
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add active class to current nav item
    highlightCurrentNavItem();
    
    // Initialize tooltips if Bootstrap is available
    initializeTooltips();
    
    // Check API status on pages that need it
    checkApiStatus();
});

/**
 * Highlight the current navigation item based on the current URL path.
 */
function highlightCurrentNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        
        // Check if the current path starts with the link's href
        // This handles both exact matches and subpaths
        if (currentPath === href || 
            (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Initialize Bootstrap tooltips if Bootstrap is available.
 */
function initializeTooltips() {
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

/**
 * Check API status on pages that need it.
 */
function checkApiStatus() {
    const apiStatusElement = document.getElementById('api-status');
    
    // Only proceed if the element exists
    if (!apiStatusElement) return;
    
    // If the API status is already being loaded by a page-specific script, don't duplicate
    if (apiStatusElement.getAttribute('data-loading') === 'true') return;
    
    apiStatusElement.setAttribute('data-loading', 'true');
    
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            let statusHtml = '<ul class="list-group">';
            
            for (const [api, status] of Object.entries(data)) {
                const statusClass = status ? 'text-success' : 'text-danger';
                const statusText = status ? 'Connected' : 'Not Configured';
                const icon = status ? '✅' : '❌';
                
                statusHtml += `
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        ${api.charAt(0).toUpperCase() + api.slice(1)} API
                        <span class="${statusClass}">${icon} ${statusText}</span>
                    </li>
                `;
            }
            
            statusHtml += '</ul>';
            apiStatusElement.innerHTML = statusHtml;
        })
        .catch(error => {
            console.error('Error fetching API status:', error);
            apiStatusElement.innerHTML = '<p class="text-danger">Error loading API status</p>';
        });
}

/**
 * Show an error message to the user.
 * 
 * @param {string} message - The error message to display
 * @param {string} containerId - The ID of the container to show the error in
 */
function showError(message, containerId = 'error-container') {
    const container = document.getElementById(containerId);
    
    if (container) {
        container.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        container.style.display = 'block';
    } else {
        // Fallback to alert if container doesn't exist
        alert(message);
    }
}

/**
 * Format a date string to a more readable format.
 * 
 * @param {string} dateString - The date string to format
 * @returns {string} The formatted date string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}
