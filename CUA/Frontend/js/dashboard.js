// Dashboard JavaScript with Indian Insurance Context

document.addEventListener('DOMContentLoaded', function() {
    // Ensure user is logged in
    Auth.requireAuth();

    // Initialize dashboard
    initDashboard();
    loadDashboardData();
    setupEventListeners();
    initCharts();
});

function initDashboard() {
    // Set current date in Indian format
    const currentDateElement = document.getElementById('currentDate');
    if (currentDateElement) {
        currentDateElement.textContent = new Intl.DateTimeFormat('en-IN', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date());
    }

    // Set user name with Indian context
    const user = Auth.getUser();
    const userNameElement = document.getElementById('userFullName');
    if (userNameElement && user) {
        userNameElement.textContent = user.username.charAt(0).toUpperCase() + user.username.slice(1);
    }

    // Set greeting based on time (Indian context)
    setIndianGreeting();
}

function setIndianGreeting() {
    const hour = new Date().getHours();
    let greeting = '';
    
    if (hour < 12) {
        greeting = 'Good Morning! Ready to process claims efficiently.';
    } else if (hour < 17) {
        greeting = 'Good Afternoon! IRDAI compliance checks ongoing.';
    } else {
        greeting = 'Good Evening! Wrapping up today\'s claim assessments.';
    }
    
    const greetingElement = document.querySelector('.page-subtitle');
    if (greetingElement) {
        greetingElement.textContent = greeting;
    }
}

function loadDashboardData() {
    // Animate stats counters with Indian insurance data
    animateStatsCounters();
    
    // Load recent claims table with Indian claims
    loadRecentClaims();
    
    // Auto-refresh data every 30 seconds
    setInterval(() => {
        updateStatsSubtly();
    }, 30000);
}

function animateStatsCounters() {
    const stats = MockData.dashboardStats;
    
    // Animate each counter with error handling
    setTimeout(() => {
        const element = document.getElementById('totalClaims');
        if (element) {
            Utils.animateCounter(element, stats.totalClaims, 2000);
        }
    }, 200);
    
    setTimeout(() => {
        const element = document.getElementById('inReviewClaims');
        if (element) {
            Utils.animateCounter(element, stats.inReview, 2000);
        }
    }, 400);
    
    setTimeout(() => {
        const element = document.getElementById('highRiskClaims');
        if (element) {
            Utils.animateCounter(element, stats.highRisk, 2000);
        }
    }, 600);
    
    setTimeout(() => {
        const element = document.getElementById('avgProcessingTime');
        if (element) {
            Utils.animateCounter(element, stats.avgProcessingTime, 2000, 1); // 1 decimal place
        }
    }, 800);
}

function updateStatsSubtly() {
    // Update stats with slight variations
    const stats = MockData.dashboardStats;
    
    const elements = [
        { id: 'totalClaims', value: stats.totalClaims + Utils.randomBetween(-2, 3) },
        { id: 'inReviewClaims', value: Math.max(0, stats.inReview + Utils.randomBetween(-2, 2)) },
        { id: 'highRiskClaims', value: Math.max(0, stats.highRisk + Utils.randomBetween(-1, 1)) },
        { id: 'avgProcessingTime', value: Math.max(1, stats.avgProcessingTime + Utils.randomBetween(-2, 2)) }
    ];

    elements.forEach(({ id, value }) => {
        const element = document.getElementById(id);
        if (element) {
            const currentValue = parseInt(element.textContent);
            if (currentValue !== value) {
                element.style.transform = 'scale(1.1)';
                element.style.color = 'var(--light-blue)';
                
                setTimeout(() => {
                    element.textContent = value.toLocaleString();
                    setTimeout(() => {
                        element.style.transform = '';
                        element.style.color = '';
                    }, 200);
                }, 100);
            }
        }
    });
}

function loadRecentClaims() {
    const tableBody = document.getElementById('claimsTableBody');
    if (!tableBody) return;

    const claims = MockData.recentClaims;
    
    tableBody.innerHTML = claims.map(claim => `
        <tr class="claim-row" data-claim-id="${claim.id}">
            <td class="claim-id">${claim.id}</td>
            <td class="customer-name">${claim.customer}</td>
            <td>
                <span class="claim-type-badge ${claim.type.toLowerCase()}">
                    ${getClaimTypeIcon(claim.type)} ${claim.type}
                </span>
            </td>
            <td class="claim-amount">${Utils.formatCurrency(claim.amount)}</td>
            <td>
                <span class="status-badge status-${claim.status.toLowerCase().replace(' ', '-')}">
                    ${claim.status}
                </span>
            </td>
            <td>
                <span class="badge badge-${claim.risk.toLowerCase()}">
                    ${claim.risk} Risk
                </span>
            </td>
            <td>
                <button class="action-btn view" onclick="viewClaimDetails('${claim.id}')">
                    👁️ View
                </button>
            </td>
        </tr>
    `).join('');

    // Add row hover effects
    const rows = tableBody.querySelectorAll('.claim-row');
    rows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
            this.style.backgroundColor = 'var(--gray-50)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.backgroundColor = '';
        });
    });
}

function getClaimTypeIcon(type) {
    const icons = {
        'Health': '🏥',
        'Motor': '🚗',
        'Life': '👤'
    };
    return icons[type] || '📋';
}

function setupEventListeners() {
    // Refresh data button
    const refreshBtn = document.getElementById('refreshData');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            showLoadingModal();
            
            // Simulate API call
            setTimeout(() => {
                hideLoadingModal();
                updateStatsSubtly();
                Utils.showNotification('Dashboard data refreshed successfully!', 'success');
            }, 2000);
        });
    }

    // Export claims button
    const exportBtn = document.getElementById('exportClaims');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            Utils.showNotification('Claims data exported to CSV', 'info');
            // In real app, this would trigger actual export
        });
    }

    // Claims search
    const searchInput = document.getElementById('claimsSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            filterClaims(this.value);
        });
    }

    // Chart period selector
    const chartPeriodSelect = document.querySelector('.chart-period');
    if (chartPeriodSelect) {
        chartPeriodSelect.addEventListener('change', function() {
            updateClaimsChart(this.value);
        });
    }
}

function showLoadingModal() {
    const modal = document.getElementById('loadingModal');
    if (modal) {
        modal.classList.add('active');
    }
}

function hideLoadingModal() {
    const modal = document.getElementById('loadingModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

function filterClaims(searchTerm) {
    const rows = document.querySelectorAll('.claim-row');
    const term = searchTerm.toLowerCase();

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const shouldShow = text.includes(term);
        
        row.style.display = shouldShow ? '' : 'none';
        
        if (shouldShow && term) {
            row.style.backgroundColor = 'rgba(59, 130, 246, 0.05)';
        } else {
            row.style.backgroundColor = '';
        }
    });
}

function viewClaimDetails(claimId) {
    Utils.showNotification(`Opening details for claim ${claimId}`, 'info');
    // In real app, this would navigate to claim details page
    window.location.href = `claim-details.html?id=${claimId}`;
}

// Chart initialization and updates
function initCharts() {
    drawClaimsTypeChart();
    drawRiskDistributionChart();
}

function drawClaimsTypeChart() {
    const canvas = document.getElementById('claimsTypeChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const data = [
        { label: 'Health', value: 45, color: '#3b82f6' },
        { label: 'Motor', value: 30, color: '#10b981' },
        { label: 'Life', value: 25, color: '#f59e0b' }
    ];

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw bar chart
    const barWidth = 80;
    const barSpacing = 50;
    const maxValue = Math.max(...data.map(d => d.value));
    const chartHeight = 150;
    const startY = 180;

    data.forEach((item, index) => {
        const x = 60 + index * (barWidth + barSpacing);
        const barHeight = (item.value / maxValue) * chartHeight;
        const y = startY - barHeight;

        // Draw bar with gradient
        const gradient = ctx.createLinearGradient(0, y, 0, startY);
        gradient.addColorStop(0, item.color);
        gradient.addColorStop(1, item.color + '80');

        ctx.fillStyle = gradient;
        ctx.fillRect(x, y, barWidth, barHeight);

        // Draw value label
        ctx.fillStyle = '#374151';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(item.value + '%', x + barWidth/2, y - 10);

        // Draw category label
        ctx.fillStyle = '#6b7280';
        ctx.font = '12px Arial';
        ctx.fillText(item.label, x + barWidth/2, startY + 20);
    });
}

function drawRiskDistributionChart() {
    const canvas = document.getElementById('riskDistributionChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const data = [
        { label: 'Low Risk', value: 60, color: '#10b981' },
        { label: 'Medium Risk', value: 30, color: '#f59e0b' },
        { label: 'High Risk', value: 10, color: '#ef4444' }
    ];

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw pie chart
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 80;
    let currentAngle = -Math.PI / 2;

    data.forEach((item, index) => {
        const sliceAngle = (item.value / 100) * 2 * Math.PI;

        // Draw slice
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
        ctx.closePath();

        // Create gradient
        const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
        gradient.addColorStop(0, item.color);
        gradient.addColorStop(1, item.color + '80');

        ctx.fillStyle = gradient;
        ctx.fill();

        // Draw percentage in center of slice
        const textAngle = currentAngle + sliceAngle / 2;
        const textX = centerX + Math.cos(textAngle) * (radius / 2);
        const textY = centerY + Math.sin(textAngle) * (radius / 2);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(item.value + '%', textX, textY + 5);

        currentAngle += sliceAngle;
    });
}

function updateClaimsChart(period) {
    // Simulate data change based on period
    const periodData = {
        'today': [45, 30, 25],
        'week': [40, 35, 25],
        'month': [50, 28, 22]
    };

    // Update chart with animation
    Utils.showNotification(`Chart updated for ${period}`, 'info');
    drawClaimsTypeChart(); // In real app, would pass new data
}

// CSS for claim type badges
const additionalStyles = document.createElement('style');
additionalStyles.textContent = `
    .claim-type-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    .claim-type-badge.health {
        background: #dcfce7;
        color: #166534;
    }
    .claim-type-badge.motor {
        background: #dbeafe;
        color: #1e40af;
    }
    .claim-type-badge.life {
        background: #fef3c7;
        color: #92400e;
    }
`;
document.head.appendChild(additionalStyles);
