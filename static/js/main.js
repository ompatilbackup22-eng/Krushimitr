// Main JavaScript for KrishiMitra: Agriband

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Mobile number formatting
    const mobileInputs = document.querySelectorAll('input[type="tel"]');
    mobileInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 10) {
                value = value.substring(0, 10);
            }
            e.target.value = value;
        });
    });

    // Pincode formatting
    const pincodeInputs = document.querySelectorAll('input[name="pincode"]');
    pincodeInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 6) {
                value = value.substring(0, 6);
            }
            e.target.value = value;
        });
    });

    // Password confirmation validation
    const passwordInputs = document.querySelectorAll('input[name="password"], input[name="confirm_password"]');
    if (passwordInputs.length === 2) {
        const password = passwordInputs[0];
        const confirmPassword = passwordInputs[1];
        
        confirmPassword.addEventListener('input', function() {
            if (password.value !== confirmPassword.value) {
                confirmPassword.setCustomValidity('Passwords do not match');
            } else {
                confirmPassword.setCustomValidity('');
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Dashboard auto-refresh for alerts
    if (window.location.pathname.includes('/dashboard')) {
        setInterval(function() {
            // Check for new alerts every 30 seconds
            fetch('/alerts/upcoming')
                .then(response => response.text())
                .then(data => {
                    // Simple check for new alerts by counting pending alerts
                    const alertCount = (data.match(/alert-card/g) || []).length;
                    if (alertCount > 0) {
                        showNotification(`You have ${alertCount} upcoming alerts!`, 'info');
                    }
                })
                .catch(error => console.log('Alert check failed:', error));
        }, 30000);
    }

    // Chart initialization (if Chart.js is loaded)
    if (typeof Chart !== 'undefined') {
        initializeCharts();
    }

    // Weather data auto-refresh
    if (window.location.pathname.includes('/weather')) {
        setInterval(function() {
            refreshWeatherData();
        }, 300000); // Refresh every 5 minutes
    }
});

// Utility functions
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, 5000);
    }
}

function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Soil analysis functions
function analyzeSoilData(soilData) {
    const analysis = {
        ph_status: 'Optimal',
        moisture_status: 'Adequate',
        nitrogen_status: 'Sufficient',
        phosphorus_status: 'Sufficient',
        potassium_status: 'Sufficient',
        recommendations: []
    };

    // pH analysis
    if (soilData.ph < 6.0) {
        analysis.ph_status = 'Acidic';
        analysis.recommendations.push('Add lime to increase pH');
    } else if (soilData.ph > 7.5) {
        analysis.ph_status = 'Alkaline';
        analysis.recommendations.push('Add sulfur to decrease pH');
    }

    // Moisture analysis
    if (soilData.moisture < 50) {
        analysis.moisture_status = 'Low';
        analysis.recommendations.push('Increase irrigation frequency');
    } else if (soilData.moisture > 80) {
        analysis.moisture_status = 'High';
        analysis.recommendations.push('Improve drainage');
    }

    // Nutrient analysis
    if (soilData.nitrogen < 20) {
        analysis.nitrogen_status = 'Deficient';
        analysis.recommendations.push('Apply nitrogen-rich fertilizer');
    }

    if (soilData.phosphorus < 15) {
        analysis.phosphorus_status = 'Deficient';
        analysis.recommendations.push('Apply phosphorus-rich fertilizer');
    }

    if (soilData.potassium < 20) {
        analysis.potassium_status = 'Deficient';
        analysis.recommendations.push('Apply potassium-rich fertilizer');
    }

    return analysis;
}

// Weather functions
function refreshWeatherData() {
    const refreshBtn = document.querySelector('#refresh-weather');
    if (refreshBtn) {
        refreshBtn.innerHTML = '<span class="loading"></span> Refreshing...';
        refreshBtn.disabled = true;
        
        fetch('/weather/fetch')
            .then(response => {
                if (response.ok) {
                    showNotification('Weather data updated successfully!', 'success');
                    location.reload();
                } else {
                    showNotification('Failed to update weather data', 'error');
                }
            })
            .catch(error => {
                showNotification('Error updating weather data', 'error');
            })
            .finally(() => {
                refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh';
                refreshBtn.disabled = false;
            });
    }
}

// Chart initialization
function initializeCharts() {
    // Soil data chart
    const soilCtx = document.getElementById('soilChart');
    if (soilCtx) {
        new Chart(soilCtx, {
            type: 'radar',
            data: {
                labels: ['pH', 'Moisture', 'Nitrogen', 'Phosphorus', 'Potassium'],
                datasets: [{
                    label: 'Current Values',
                    data: [7.0, 60, 25, 18, 22],
                    borderColor: 'rgb(40, 167, 69)',
                    backgroundColor: 'rgba(40, 167, 69, 0.2)',
                    pointBackgroundColor: 'rgb(40, 167, 69)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(40, 167, 69)'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    // Weather data chart
    const weatherCtx = document.getElementById('weatherChart');
    if (weatherCtx) {
        new Chart(weatherCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Temperature (°C)',
                    data: [28, 30, 32, 29, 31, 33, 30],
                    borderColor: 'rgb(255, 193, 7)',
                    backgroundColor: 'rgba(255, 193, 7, 0.2)',
                    tension: 0.4
                }, {
                    label: 'Humidity (%)',
                    data: [65, 60, 55, 70, 68, 62, 58],
                    borderColor: 'rgb(23, 162, 184)',
                    backgroundColor: 'rgba(23, 162, 184, 0.2)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// Export functions for use in other scripts
window.KrishiMitra = {
    showNotification,
    formatNumber,
    formatDate,
    formatDateTime,
    analyzeSoilData,
    refreshWeatherData
};
