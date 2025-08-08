// Global Secure Shield - Main JavaScript Utilities

// Authentication utilities
const Auth = {
    login: (username, password) => {
        // Dummy authentication - in real app, this would make API call
        if (username && password) {
            localStorage.setItem('gss_user', JSON.stringify({
                username: username,
                loginTime: new Date().toISOString(),
                role: 'Claims Officer'
            }));
            return true;
        }
        return false;
    },

    logout: () => {
        localStorage.removeItem('gss_user');
        window.location.href = 'login.html';
    },

    isLoggedIn: () => {
        return localStorage.getItem('gss_user') !== null;
    },

    getUser: () => {
        const user = localStorage.getItem('gss_user');
        return user ? JSON.parse(user) : null;
    },

    requireAuth: () => {
        if (!Auth.isLoggedIn()) {
            window.location.href = 'login.html';
        }
    }
};

// Utility functions
const Utils = {
    // Generate random numbers for mock data
    randomBetween: (min, max) => Math.floor(Math.random() * (max - min + 1)) + min,

    // Format currency
    formatCurrency: (amount) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            minimumFractionDigits: 0
        }).format(amount);
    },

    // Format date
    formatDate: (date) => {
        return new Intl.DateTimeFormat('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(new Date(date));
    },

    // Show notification
    showNotification: (message, type = 'success') => {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
                <span class="notification-message">${message}</span>
            </div>
        `;
        
        // Add notification styles if not already added
        if (!document.querySelector('#notification-styles')) {
            const styles = document.createElement('style');
            styles.id = 'notification-styles';
            styles.textContent = `
                .notification {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    padding: 1rem 1.5rem;
                    border-radius: 12px;
                    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                    z-index: 3000;
                    animation: slideInFromRight 0.3s ease;
                    max-width: 400px;
                }
                .notification-success { background: #dcfce7; color: #166534; border-left: 4px solid #10b981; }
                .notification-error { background: #fee2e2; color: #991b1b; border-left: 4px solid #ef4444; }
                .notification-info { background: #dbeafe; color: #1e40af; border-left: 4px solid #3b82f6; }
                .notification-content { display: flex; align-items: center; gap: 0.75rem; }
                @keyframes slideInFromRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(styles);
        }

        document.body.appendChild(notification);
        setTimeout(() => {
            notification.style.animation = 'slideInFromRight 0.3s ease reverse';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    },

    // Animate counter
    animateCounter: (element, target, duration = 2000) => {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current).toLocaleString();
        }, 16);
    },

    // Create progress bar animation
    animateProgressBar: (element, percentage, duration = 1000) => {
        element.style.width = '0%';
        setTimeout(() => {
            element.style.transition = `width ${duration}ms ease`;
            element.style.width = percentage + '%';
        }, 100);
    },

    // Validate form fields
    validateForm: (formData) => {
        const errors = [];
        
        for (const [key, value] of Object.entries(formData)) {
            if (!value || value.trim() === '') {
                errors.push(`${key.replace(/([A-Z])/g, ' $1').toLowerCase()} is required`);
            }
        }

        return {
            isValid: errors.length === 0,
            errors: errors
        };
    },

    // Calculate risk score (mock algorithm)
    calculateRiskScore: (claimData) => {
        let score = 0;
        let factors = [];

        // Amount factor
        const amount = parseFloat(claimData.claimAmount);
        if (amount > 500000) {
            score += 30;
            factors.push('High claim amount');
        } else if (amount > 100000) {
            score += 15;
            factors.push('Medium claim amount');
        }

        // Claim type factor
        if (claimData.claimType === 'motor') {
            score += 10;
            factors.push('Motor claims have higher fraud risk');
        } else if (claimData.claimType === 'health') {
            score += 5;
            factors.push('Health claim verification required');
        }

        // Recent incident factor
        const incidentDate = new Date(claimData.incidentDate);
        const daysSince = (new Date() - incidentDate) / (1000 * 60 * 60 * 24);
        if (daysSince < 7) {
            score += 20;
            factors.push('Very recent incident');
        }

        // Random factor for demonstration
        score += Utils.randomBetween(0, 15);

        let level, color;
        if (score < 25) {
            level = 'Low';
            color = 'success';
        } else if (score < 50) {
            level = 'Medium';
            color = 'warning';
        } else {
            level = 'High';
            color = 'danger';
        }

        return {
            score: Math.min(score, 100),
            level: level,
            color: color,
            factors: factors
        };
    }
};

// DOM utilities
const DOM = {
    // Create element with attributes
    createElement: (tag, attributes = {}, children = []) => {
        const element = document.createElement(tag);
        
        Object.entries(attributes).forEach(([key, value]) => {
            if (key === 'className') {
                element.className = value;
            } else if (key === 'innerHTML') {
                element.innerHTML = value;
            } else {
                element.setAttribute(key, value);
            }
        });

        children.forEach(child => {
            if (typeof child === 'string') {
                element.appendChild(document.createTextNode(child));
            } else {
                element.appendChild(child);
            }
        });

        return element;
    },

    // Show/hide loading spinner
    showLoading: (element) => {
        element.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <span>Processing...</span>
            </div>
        `;
        
        // Add spinner styles if not already added
        if (!document.querySelector('#spinner-styles')) {
            const styles = document.createElement('style');
            styles.id = 'spinner-styles';
            styles.textContent = `
                .loading-spinner {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 1rem;
                    padding: 2rem;
                }
                .spinner {
                    width: 40px;
                    height: 40px;
                    border: 4px solid #e5e7eb;
                    border-top: 4px solid #3b82f6;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(styles);
        }
    },

    // Mobile menu toggle
    initMobileMenu: () => {
        const toggle = document.querySelector('.mobile-menu-toggle');
        const navLinks = document.querySelector('.nav-links');
        
        if (toggle && navLinks) {
            toggle.addEventListener('click', () => {
                navLinks.classList.toggle('mobile-open');
            });
        }
    },

    // Initialize tooltips
    initTooltips: () => {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                const tooltip = document.createElement('div');
                tooltip.className = 'tooltip';
                tooltip.textContent = e.target.getAttribute('data-tooltip');
                
                // Add tooltip styles if not already added
                if (!document.querySelector('#tooltip-styles')) {
                    const styles = document.createElement('style');
                    styles.id = 'tooltip-styles';
                    styles.textContent = `
                        .tooltip {
                            position: absolute;
                            background: #1f2937;
                            color: white;
                            padding: 0.5rem 0.75rem;
                            border-radius: 6px;
                            font-size: 0.875rem;
                            z-index: 1000;
                            pointer-events: none;
                            white-space: nowrap;
                            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                        }
                        .tooltip::before {
                            content: '';
                            position: absolute;
                            top: 100%;
                            left: 50%;
                            transform: translateX(-50%);
                            border-left: 5px solid transparent;
                            border-right: 5px solid transparent;
                            border-top: 5px solid #1f2937;
                        }
                    `;
                    document.head.appendChild(styles);
                }

                document.body.appendChild(tooltip);
                
                const rect = e.target.getBoundingClientRect();
                tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
                tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            });

            element.addEventListener('mouseleave', () => {
                const tooltip = document.querySelector('.tooltip');
                if (tooltip) tooltip.remove();
            });
        });
    }
};

// Mock data for the application
const MockData = {
    dashboardStats: {
        totalClaims: Utils.randomBetween(145, 275),
        inReview: Utils.randomBetween(35, 65),
        highRisk: Utils.randomBetween(8, 18),
        avgProcessingTime: Utils.randomBetween(2.1, 4.8)
    },

    recentClaims: [
        { id: 'CLM001', customer: 'Rajesh Kumar Sharma', type: 'Health', amount: '₹1,85,000', status: 'In Review', risk: 'Medium', hospital: 'Apollo Hospital, Delhi' },
        { id: 'CLM002', customer: 'Priya Singh Chauhan', type: 'Motor', amount: '₹45,000', status: 'Approved', risk: 'Low', garage: 'Maruti Service Center, Mumbai' },
        { id: 'CLM003', customer: 'Amit Patel', type: 'Life', amount: '₹25,00,000', status: 'Under Investigation', risk: 'High', reason: 'High sum assured claim' },
        { id: 'CLM004', customer: 'Sunita Sharma Gupta', type: 'Health', amount: '₹3,20,000', status: 'Pending Documents', risk: 'Medium', hospital: 'Max Healthcare, Gurgaon' },
        { id: 'CLM005', customer: 'Vikram Reddy', type: 'Motor', amount: '₹75,000', status: 'Rejected', risk: 'High', reason: 'Policy lapsed' },
        { id: 'CLM006', customer: 'Anita Joshi', type: 'Health', amount: '₹2,50,000', status: 'Approved', risk: 'Low', hospital: 'Fortis Hospital, Bangalore' },
        { id: 'CLM007', customer: 'Mohammed Ali Khan', type: 'Motor', amount: '₹1,20,000', status: 'In Review', risk: 'Medium', garage: 'Hyundai Service, Hyderabad' },
        { id: 'CLM008', customer: 'Deepika Iyer', type: 'Health', amount: '₹95,000', status: 'Approved', risk: 'Low', hospital: 'Manipal Hospital, Chennai' }
    ],

    riskRules: [
        { id: 'HLT-001', description: 'Claims above ₹5 lakhs require pre-authorization as per IRDAI guidelines', type: 'Health', severity: 'High' },
        { id: 'MOT-001', description: 'Motor accidents within 30 days of policy purchase flagged for investigation', type: 'Motor', severity: 'High' },
        { id: 'HLT-002', description: 'Multiple claims from same hospital in 90-day period require review', type: 'Health', severity: 'Medium' },
        { id: 'ALL-001', description: 'Claims during grace period subject to premium payment verification', type: 'All', severity: 'High' },
        { id: 'HLT-003', description: 'Pre-existing disease claims within 48-month waiting period', type: 'Health', severity: 'Medium' },
        { id: 'MOT-002', description: 'Third-party claims exceeding ₹15 lakhs require legal clearance', type: 'Motor', severity: 'High' },
        { id: 'LIF-001', description: 'Life insurance claims within 12 months require suicide exclusion check', type: 'Life', severity: 'High' }
    ],

    fraudWatchlist: [
        { name: 'Krishna Medical Center, Noida', type: 'Hospital', reason: 'Inflated bills and fake procedures', risk: 'High', reportedBy: 'Claims Team Delhi' },
        { name: 'Quick Fix Garage, Pune', type: 'Garage', reason: 'False damage assessment reports', risk: 'High', reportedBy: 'Motor Claims Team' },
        { name: 'Ramesh Mishra', type: 'Customer', reason: 'Multiple fraudulent health claims', risk: 'High', reportedBy: 'Fraud Detection AI' },
        { name: 'City Care Clinic, Lucknow', type: 'Hospital', reason: 'Unnecessary diagnostic tests', risk: 'Medium', reportedBy: 'Medical Auditor' },
        { name: 'Singh Auto Repair', type: 'Garage', reason: 'Overcharging for parts', risk: 'Medium', reportedBy: 'Customer Complaint' }
    ],

    indianCities: [
        'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 
        'Surat', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Bhopal', 'Visakhapatnam',
        'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana', 'Coimbatore', 'Agra', 'Madurai', 'Nashik'
    ],

    indianHospitals: [
        'Apollo Hospital', 'Fortis Healthcare', 'Max Healthcare', 'Manipal Hospital', 
        'Narayana Health', 'Medanta', 'BLK Hospital', 'Sir Ganga Ram Hospital',
        'Kokilaben Hospital', 'Lilavati Hospital', 'Ruby Hospital', 'Wockhardt Hospital'
    ],

    claimTypes: {
        health: ['Hospitalization', 'Surgery', 'Emergency Treatment', 'Maternity', 'Dental', 'Day Care'],
        motor: ['Accident Damage', 'Theft', 'Third Party', 'Fire', 'Natural Calamity', 'Vandalism'],
        life: ['Death Claim', 'Maturity', 'Surrender', 'Partial Withdrawal', 'Loan Against Policy']
    }
};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    // Initialize mobile menu
    DOM.initMobileMenu();
    
    // Initialize tooltips
    DOM.initTooltips();
    
    // Set active nav link based on current page
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage || (currentPage === '' && href === 'dashboard.html')) {
            link.classList.add('nav-active');
        } else {
            link.classList.remove('nav-active');
        }
    });
    
    // Add fade-in animation to main content
    const mainContent = document.querySelector('main') || document.querySelector('.container');
    if (mainContent) {
        mainContent.classList.add('fade-in-up');
    }

    // Add logout functionality to logout buttons
    const logoutBtns = document.querySelectorAll('.logout-btn');
    logoutBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            if (confirm('Are you sure you want to logout?')) {
                Auth.logout();
            }
        });
    });
});

// Export for use in other files
window.Auth = Auth;
window.Utils = Utils;
window.DOM = DOM;
window.MockData = MockData;
