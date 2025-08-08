// Rules Page JavaScript with Indian Insurance Context
document.addEventListener('DOMContentLoaded', function() {
    console.log('Rules page loading...');
    
    // Initialize rules functionality
    initializeRules();
    setupSearchAndFilter();
    setupAccordion();
    loadRulesData();
    
    console.log('Rules page initialized successfully');
});

// Indian insurance rules data
const rulesDatabase = {
    health: [
        {
            id: 'HLT-001',
            description: 'Claims above ₹50,000 require pre-authorization from network hospitals as per IRDAI guidelines',
            severity: 'high',
            category: 'Authorization'
        },
        {
            id: 'HLT-002', 
            description: 'Waiting period of 30 days for illnesses and 48 months for pre-existing diseases (PED)',
            severity: 'high',
            category: 'Waiting Period'
        },
        {
            id: 'HLT-003',
            description: 'Room rent capped at 1% of sum insured or ₹5,000 per day, whichever is lower',
            severity: 'medium',
            category: 'Coverage Limits'
        },
        {
            id: 'HLT-004',
            description: 'Maternity claims require 9-month waiting period from policy inception date',
            severity: 'medium',
            category: 'Maternity'
        },
        {
            id: 'HLT-005',
            description: 'Alternative medicine (AYUSH) treatments covered up to ₹25,000 per policy year',
            severity: 'low',
            category: 'Alternative Medicine'
        },
        {
            id: 'HLT-006',
            description: 'Domiciliary treatment covered only for illness/injury requiring 3+ days bed rest',
            severity: 'medium',
            category: 'Home Treatment'
        },
        {
            id: 'HLT-007',
            description: 'Mental health conditions covered as per Mental Healthcare Act 2017 guidelines',
            severity: 'medium',
            category: 'Mental Health'
        },
        {
            id: 'HLT-008',
            description: 'COVID-19 related expenses covered as per IRDAI circular dated 21/04/2020',
            severity: 'high',
            category: 'Pandemic Coverage'
        }
    ],
    motor: [
        {
            id: 'MOT-001',
            description: 'Third party claims processed as per Motor Vehicles Act 1988 and latest amendments',
            severity: 'high',
            category: 'Third Party'
        },
        {
            id: 'MOT-002',
            description: 'Own damage claims require FIR for theft cases and accidents involving third party',
            severity: 'high',
            category: 'Documentation'
        },
        {
            id: 'MOT-003',
            description: 'Zero depreciation available only for vehicles less than 5 years old',
            severity: 'medium',
            category: 'Depreciation'
        },
        {
            id: 'MOT-004',
            description: 'Cashless repair facility available at network garages across India',
            severity: 'low',
            category: 'Repair'
        },
        {
            id: 'MOT-005',
            description: 'Claim settlement within 30 days as mandated by IRDAI guidelines',
            severity: 'high',
            category: 'Timeline'
        },
        {
            id: 'MOT-006',
            description: 'Commercial vehicle claims require valid fitness certificate and permit',
            severity: 'medium',
            category: 'Commercial'
        },
        {
            id: 'MOT-007',
            description: 'Two-wheeler claims for vehicles above 150cc require helmet wearing proof',
            severity: 'medium',
            category: 'Safety Equipment'
        },
        {
            id: 'MOT-008',
            description: 'Geographic coverage extends to entire India including Jammu & Kashmir, Ladakh',
            severity: 'low',
            category: 'Geographic Coverage'
        }
    ],
    life: [
        {
            id: 'LIF-001',
            description: 'Nomination mandatory as per Section 39 of Insurance Act 1938',
            severity: 'high',
            category: 'Nomination'
        },
        {
            id: 'LIF-002',
            description: 'Suicide exclusion period of 12 months from policy commencement date',
            severity: 'high',
            category: 'Exclusions'
        },
        {
            id: 'LIF-003',
            description: 'Medical examination required for sum assured above ₹25 lakhs',
            severity: 'medium',
            category: 'Medical Requirements'
        },
        {
            id: 'LIF-004',
            description: 'Grace period of 30 days for premium payment (15 days for monthly mode)',
            severity: 'medium',
            category: 'Premium Payment'
        },
        {
            id: 'LIF-005',
            description: 'Free look period of 15 days for offline policies, 30 days for online policies',
            severity: 'low',
            category: 'Free Look'
        },
        {
            id: 'LIF-006',
            description: 'Term insurance claims require death certificate from competent authority',
            severity: 'high',
            category: 'Documentation'
        },
        {
            id: 'LIF-007',
            description: 'Unit Linked plans subject to market risk and SEBI regulations',
            severity: 'medium',
            category: 'Investment Risk'
        },
        {
            id: 'LIF-008',
            description: 'Senior citizen policies available up to age 75 with medical examination',
            severity: 'low',
            category: 'Age Limits'
        }
    ]
};

let currentRules = [];
let filteredRules = [];

function initializeRules() {
    // Add event listeners
    const addRuleBtn = document.getElementById('addRuleBtn');
    const searchInput = document.getElementById('rulesSearch');
    const filterSelect = document.getElementById('rulesFilter');

    if (addRuleBtn) {
        addRuleBtn.addEventListener('click', openAddRuleModal);
    }

    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }

    if (filterSelect) {
        filterSelect.addEventListener('change', handleFilter);
    }

    // Update rules summary
    updateRulesSummary();
}

function setupSearchAndFilter() {
    // Initialize search functionality
    const searchInput = document.getElementById('rulesSearch');
    if (searchInput) {
        searchInput.placeholder = 'Search rules by ID, description, or category...';
    }
}

function setupAccordion() {
    // Add click handlers for accordion headers
    document.addEventListener('click', function(e) {
        if (e.target.closest('.accordion-header')) {
            const header = e.target.closest('.accordion-header');
            const item = header.closest('.accordion-item');
            const content = item.querySelector('.accordion-content');
            const toggle = header.querySelector('.accordion-toggle');

            // Toggle active state
            const isActive = item.classList.contains('active');
            
            if (isActive) {
                item.classList.remove('active');
                header.classList.remove('active');
                content.classList.remove('active');
                toggle.classList.remove('active');
            } else {
                item.classList.add('active');
                header.classList.add('active');
                content.classList.add('active');
                toggle.classList.add('active');
            }
        }
    });
}

function loadRulesData() {
    console.log('Loading rules data...');
    
    // Populate accordion with rules data
    const accordion = document.querySelector('.rules-accordion');
    if (!accordion) {
        console.error('Rules accordion container not found');
        return;
    }

    const categories = [
        {
            key: 'health',
            title: 'Health Insurance Rules',
            icon: '🏥',
            description: 'IRDAI compliant health insurance claim processing rules'
        },
        {
            key: 'motor',
            title: 'Motor Insurance Rules', 
            icon: '🚗',
            description: 'Motor Vehicle Act 1988 compliant motor insurance rules'
        },
        {
            key: 'life',
            title: 'Life Insurance Rules',
            icon: '💰',
            description: 'Life insurance claim processing as per Insurance Act 1938'
        }
    ];

    accordion.innerHTML = categories.map(category => {
        const rules = rulesDatabase[category.key];
        console.log(`Loading ${rules.length} rules for ${category.title}`);
        return createAccordionItem(category, rules);
    }).join('');
    
    console.log('Rules data loaded successfully');
}

function createAccordionItem(category, rules) {
    return `
        <div class="accordion-item" data-category="${category.key}">
            <div class="accordion-header">
                <div class="accordion-title">
                    <span class="accordion-icon">${category.icon}</span>
                    <div>
                        <div>${category.title}</div>
                        <div style="font-size: 0.8rem; font-weight: 400; color: var(--text-secondary); margin-top: 0.25rem;">
                            ${category.description}
                        </div>
                    </div>
                </div>
                <div class="accordion-meta">
                    <span class="rule-count">${rules.length} rules</span>
                    <span class="accordion-toggle">▼</span>
                </div>
            </div>
            <div class="accordion-content">
                <div class="accordion-body">
                    ${createRulesTable(rules)}
                </div>
            </div>
        </div>
    `;
}

function createRulesTable(rules) {
    if (rules.length === 0) {
        return `
            <div class="no-results">
                <div class="no-results-icon">📋</div>
                <p>No rules found for this category.</p>
            </div>
        `;
    }

    return `
        <table class="rules-table">
            <thead>
                <tr>
                    <th>Rule ID</th>
                    <th>Description</th>
                    <th>Category</th>
                    <th>Severity</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${rules.map(rule => createRuleRow(rule)).join('')}
            </tbody>
        </table>
    `;
}

function createRuleRow(rule) {
    const severityClass = `severity-${rule.severity}`;
    const severityIcon = rule.severity === 'high' ? '🔴' : rule.severity === 'medium' ? '🟡' : '🟢';

    return `
        <tr data-rule-id="${rule.id}">
            <td>
                <span class="rule-id">${rule.id}</span>
            </td>
            <td>
                <div class="rule-description">${rule.description}</div>
            </td>
            <td>
                <span class="rule-category">${rule.category}</span>
            </td>
            <td>
                <span class="rule-severity ${severityClass}">
                    ${severityIcon} ${rule.severity.toUpperCase()}
                </span>
            </td>
            <td>
                <div class="rule-actions">
                    <button class="action-btn view" onclick="viewRuleDetails('${rule.id}')">
                        👁️ View
                    </button>
                    <button class="action-btn edit" onclick="editRule('${rule.id}')">
                        ✏️ Edit
                    </button>
                </div>
            </td>
        </tr>
    `;
}

function updateRulesSummary() {
    // Calculate summary statistics
    const totalRules = Object.values(rulesDatabase).flat().length;
    const highSeverity = Object.values(rulesDatabase).flat().filter(r => r.severity === 'high').length;
    const categories = Object.keys(rulesDatabase).length;
    const lastUpdated = 'August 2025'; // Current month

    // Update summary cards
    const summaryCards = document.querySelector('.summary-cards');
    if (summaryCards) {
        summaryCards.innerHTML = `
            <div class="summary-card">
                <span class="summary-icon">📊</span>
                <div class="summary-value">${totalRules}</div>
                <div class="summary-label">Total Rules</div>
            </div>
            <div class="summary-card">
                <span class="summary-icon">🔴</span>
                <div class="summary-value">${highSeverity}</div>
                <div class="summary-label">High Priority</div>
            </div>
            <div class="summary-card">
                <span class="summary-icon">📋</span>
                <div class="summary-value">${categories}</div>
                <div class="summary-label">Categories</div>
            </div>
            <div class="summary-card">
                <span class="summary-icon">🔄</span>
                <div class="summary-value">${lastUpdated}</div>
                <div class="summary-label">Last Updated</div>
            </div>
        `;
    }
}

function handleSearch() {
    const searchInput = document.getElementById('rulesSearch');
    const searchTerm = searchInput?.value.toLowerCase() || '';
    
    // Search through all rules
    const allRules = Object.values(rulesDatabase).flat();
    filteredRules = allRules.filter(rule => 
        rule.id.toLowerCase().includes(searchTerm) ||
        rule.description.toLowerCase().includes(searchTerm) ||
        rule.category.toLowerCase().includes(searchTerm)
    );

    // Update display
    updateRulesDisplay(searchTerm);
}

function handleFilter() {
    const filterSelect = document.getElementById('rulesFilter');
    const selectedSeverity = filterSelect?.value || 'all';
    
    // Get current search term
    const searchInput = document.getElementById('rulesSearch');
    const searchTerm = searchInput?.value.toLowerCase() || '';
    
    // Apply both search and filter
    let rules = Object.values(rulesDatabase).flat();
    
    if (searchTerm) {
        rules = rules.filter(rule => 
            rule.id.toLowerCase().includes(searchTerm) ||
            rule.description.toLowerCase().includes(searchTerm) ||
            rule.category.toLowerCase().includes(searchTerm)
        );
    }
    
    if (selectedSeverity !== 'all') {
        rules = rules.filter(rule => rule.severity === selectedSeverity);
    }
    
    filteredRules = rules;
    updateRulesDisplay(searchTerm, selectedSeverity);
}

function updateRulesDisplay(searchTerm = '', severityFilter = 'all') {
    const accordion = document.querySelector('.rules-accordion');
    if (!accordion) return;

    // Group filtered rules by type
    const groupedRules = {
        health: filteredRules.filter(rule => rule.id.startsWith('HLT')),
        motor: filteredRules.filter(rule => rule.id.startsWith('MOT')),
        life: filteredRules.filter(rule => rule.id.startsWith('LIF'))
    };

    // Update each accordion section
    Object.keys(groupedRules).forEach(type => {
        const accordionItem = accordion.querySelector(`[data-category="${type}"]`);
        if (accordionItem) {
            const content = accordionItem.querySelector('.accordion-body');
            const rules = groupedRules[type];
            
            if (rules.length === 0 && (searchTerm || severityFilter !== 'all')) {
                accordionItem.style.display = 'none';
            } else {
                accordionItem.style.display = 'block';
                content.innerHTML = createRulesTable(rules);
                
                // Update rule count
                const countElement = accordionItem.querySelector('.rule-count');
                if (countElement) {
                    countElement.textContent = `${rules.length} rules`;
                }
            }
        }
    });

    // Show no results message if no rules found
    if (filteredRules.length === 0 && (searchTerm || severityFilter !== 'all')) {
        showNoResultsMessage();
    }
}

function showNoResultsMessage() {
    const accordion = document.querySelector('.rules-accordion');
    if (accordion) {
        accordion.innerHTML = `
            <div class="no-results">
                <div class="no-results-icon">🔍</div>
                <h3>No rules found</h3>
                <p>Try adjusting your search criteria or filter settings.</p>
                <button class="btn btn-primary" onclick="clearFilters()">Clear Filters</button>
            </div>
        `;
    }
}

function clearFilters() {
    // Clear search and filter
    const searchInput = document.getElementById('rulesSearch');
    const filterSelect = document.getElementById('rulesFilter');
    
    if (searchInput) searchInput.value = '';
    if (filterSelect) filterSelect.value = 'all';
    
    // Reload original data
    loadRulesData();
}

function viewRuleDetails(ruleId) {
    // Find rule details
    const allRules = Object.values(rulesDatabase).flat();
    const rule = allRules.find(r => r.id === ruleId);
    
    if (rule) {
        // Create and show modal with rule details
        showRuleModal(rule, 'view');
    }
}

function editRule(ruleId) {
    // Find rule details
    const allRules = Object.values(rulesDatabase).flat();
    const rule = allRules.find(r => r.id === ruleId);
    
    if (rule) {
        // Create and show modal with editable form
        showRuleModal(rule, 'edit');
    }
}

function showRuleModal(rule, mode) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'flex';
    
    const isViewMode = mode === 'view';
    const title = isViewMode ? 'Rule Details' : 'Edit Rule';
    
    modal.innerHTML = `
        <div class="modal-content">
            <button class="modal-close">✕</button>
            <div class="modal-header">
                <h2 class="modal-title">${title}</h2>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Rule ID</label>
                    <input type="text" class="form-input" value="${rule.id}" ${isViewMode ? 'readonly' : ''}>
                </div>
                <div class="form-group">
                    <label class="form-label">Description</label>
                    <textarea class="form-textarea" ${isViewMode ? 'readonly' : ''}>${rule.description}</textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">Category</label>
                    <input type="text" class="form-input" value="${rule.category}" ${isViewMode ? 'readonly' : ''}>
                </div>
                <div class="form-group">
                    <label class="form-label">Severity</label>
                    <select class="form-select" ${isViewMode ? 'disabled' : ''}>
                        <option value="low" ${rule.severity === 'low' ? 'selected' : ''}>Low</option>
                        <option value="medium" ${rule.severity === 'medium' ? 'selected' : ''}>Medium</option>
                        <option value="high" ${rule.severity === 'high' ? 'selected' : ''}>High</option>
                    </select>
                </div>
                ${!isViewMode ? `
                <div class="form-actions">
                    <button class="btn btn-secondary" onclick="closeModal(this)">Cancel</button>
                    <button class="btn btn-primary" onclick="saveRule('${rule.id}', this)">Save Changes</button>
                </div>
                ` : ''}
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
    
    // Add close functionality
    modal.querySelector('.modal-close').addEventListener('click', () => {
        document.body.removeChild(modal);
        document.body.style.overflow = 'auto';
    });
}

function closeModal(button) {
    const modal = button.closest('.modal');
    document.body.removeChild(modal);
    document.body.style.overflow = 'auto';
}

function saveRule(ruleId, button) {
    // Simulate saving changes
    showNotification('✅ Rule updated successfully!', 'success');
    closeModal(button);
    
    // Reload rules data
    setTimeout(() => {
        loadRulesData();
    }, 500);
}

function openAddRuleModal() {
    // Create add rule modal
    const modal = document.createElement('div');
    modal.className = 'modal add-rule-modal';
    modal.style.display = 'flex';
    
    modal.innerHTML = `
        <div class="modal-content">
            <button class="modal-close">✕</button>
            <div class="modal-header">
                <h2 class="modal-title">Add New Rule</h2>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label class="form-label">Rule Type</label>
                    <select class="form-select" id="newRuleType">
                        <option value="health">Health Insurance</option>
                        <option value="motor">Motor Insurance</option>
                        <option value="life">Life Insurance</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Description</label>
                    <textarea class="form-textarea" id="newRuleDescription" placeholder="Enter detailed rule description..."></textarea>
                </div>
                <div class="form-group">
                    <label class="form-label">Category</label>
                    <input type="text" class="form-input" id="newRuleCategory" placeholder="e.g., Authorization, Waiting Period">
                </div>
                <div class="form-group">
                    <label class="form-label">Severity</label>
                    <select class="form-select" id="newRuleSeverity">
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                    </select>
                </div>
                <div class="form-actions">
                    <button class="btn btn-secondary" onclick="closeModal(this)">Cancel</button>
                    <button class="btn btn-primary" onclick="addNewRule(this)">Add Rule</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
    
    // Add close functionality
    modal.querySelector('.modal-close').addEventListener('click', () => {
        document.body.removeChild(modal);
        document.body.style.overflow = 'auto';
    });
}

function addNewRule(button) {
    // Get form data
    const type = document.getElementById('newRuleType').value;
    const description = document.getElementById('newRuleDescription').value;
    const category = document.getElementById('newRuleCategory').value;
    const severity = document.getElementById('newRuleSeverity').value;
    
    // Validate required fields
    if (!description.trim() || !category.trim()) {
        showNotification('❌ Please fill in all required fields', 'error');
        return;
    }
    
    // Generate new rule ID
    const prefix = type === 'health' ? 'HLT' : type === 'motor' ? 'MOT' : 'LIF';
    const existingRules = rulesDatabase[type];
    const nextNumber = String(existingRules.length + 1).padStart(3, '0');
    const newId = `${prefix}-${nextNumber}`;
    
    // Add rule to database
    const newRule = {
        id: newId,
        description: description.trim(),
        category: category.trim(),
        severity: severity
    };
    
    rulesDatabase[type].push(newRule);
    
    // Show success message and close modal
    showNotification('✅ New rule added successfully!', 'success');
    closeModal(button);
    
    // Reload rules data
    setTimeout(() => {
        loadRulesData();
        updateRulesSummary();
    }, 500);
}

// Utility function for notifications (reused from other pages)
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '12px 20px',
        backgroundColor: type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6',
        color: 'white',
        borderRadius: '8px',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
        zIndex: '10000',
        fontSize: '14px',
        fontWeight: '500',
        maxWidth: '400px',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}
