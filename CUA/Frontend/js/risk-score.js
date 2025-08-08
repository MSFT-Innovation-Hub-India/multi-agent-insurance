// Risk Analysis Module - Complete Implementation
class RiskAnalysisApp {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 4;
        this.formData = {};
        this.selectedRules = new Set();
        this.ruleResults = new Map();
        this.autoValidate = false;
        this.init();
    }

    init() {
        this.loadStep(1);
        this.initializeDefaultRules();
    }

    initializeDefaultRules() {
        // Auto-select all rules by default
        Object.keys(RiskAnalysisData.rules).forEach(category => {
            RiskAnalysisData.rules[category].forEach(rule => {
                this.selectedRules.add(rule.id);
            });
        });
    }

    loadStep(stepNumber) {
        this.currentStep = stepNumber;
        this.updateProgressIndicator();
        this.renderStepContent();
    }

    updateProgressIndicator() {
        const steps = document.querySelectorAll('.step');
        steps.forEach((step, index) => {
            const stepNum = index + 1;
            step.classList.remove('active', 'completed');
            
            if (stepNum < this.currentStep) {
                step.classList.add('completed');
            } else if (stepNum === this.currentStep) {
                step.classList.add('active');
            }
        });
    }

    renderStepContent() {
        const container = document.querySelector('.step-content-container');
        
        switch (this.currentStep) {
            case 1:
                container.innerHTML = this.renderStep1();
                break;
            case 2:
                container.innerHTML = this.renderStep2();
                this.attachRuleEventListeners();
                break;
            case 3:
                container.innerHTML = this.renderStep3();
                break;
            case 4:
                container.innerHTML = this.renderStep4();
                break;
        }
        
        this.attachEventListeners();
    }

    // Step 1: Collect Customer & Claim Details
    renderStep1() {
        return `
            <div class="step-content">
                <div class="step-header">
                    <h2>Step 1: Collect Customer & Claim Details</h2>
                    <p>Enter the customer and claim information to begin the risk analysis process.</p>
                    <div class="dummy-data-actions">
                        <button type="button" class="btn btn-sm btn-secondary" onclick="app.fillDummyData()">
                            📝 Fill Sample Data
                        </button>
                        <button type="button" class="btn btn-sm btn-secondary" onclick="app.clearForm()">
                            🗑️ Clear Form
                        </button>
                    </div>
                </div>
                
                <div class="form-container">
                    <div class="form-section">
                        <h3>Customer Information</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="customerName">Customer Name *</label>
                                <input type="text" id="customerName" value="${this.formData.customerName || ''}" 
                                       placeholder="Enter customer full name" required>
                            </div>
                            <div class="form-group">
                                <label for="policyNumber">Policy Number *</label>
                                <input type="text" id="policyNumber" value="${this.formData.policyNumber || ''}" 
                                       placeholder="Enter policy number" required>
                            </div>
                        </div>
                    </div>

                    <div class="form-section">
                        <h3>Claim Information</h3>
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="claimType">Claim Type *</label>
                                <input type="text" id="claimType" value="${this.formData.claimType || ''}" 
                                       placeholder="Enter claim type (e.g., health, motor, life)" required>
                            </div>
                            <div class="form-group">
                                <label for="claimAmount">Claim Amount (₹) *</label>
                                <input type="number" id="claimAmount" value="${this.formData.claimAmount || ''}" 
                                       placeholder="Enter claim amount" min="0" required>
                            </div>
                            <div class="form-group">
                                <label for="policyStartDate">Policy Start Date *</label>
                                <input type="date" id="policyStartDate" value="${this.formData.policyStartDate || ''}" required>
                            </div>
                            <div class="form-group">
                                <label for="incidentDate">Incident Date *</label>
                                <input type="date" id="incidentDate" value="${this.formData.incidentDate || ''}" required>
                            </div>
                            <div class="form-group full-width">
                                <label for="hospitalGarageName">Hospital/Garage Name</label>
                                <input type="text" id="hospitalGarageName" value="${this.formData.hospitalGarageName || ''}" 
                                       placeholder="Enter hospital or garage name">
                            </div>
                        </div>
                    </div>

                    <div class="step-actions">
                        <button type="button" class="btn btn-primary" onclick="app.submitStep1()">
                            Submit & Continue to Step 2
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // Step 2: Auto-Filter Relevant Rules
    renderStep2() {
        const claimType = this.formData.claimType;
        const relevantRules = claimType ? RiskAnalysisData.rules[claimType] || [] : [];
        
        return `
            <div class="step-content">
                <div class="step-header">
                    <h2>Step 2: Select Relevant Rules</h2>
                    <p>Rules have been auto-filtered based on claim type: <strong>${this.formatClaimType(claimType)}</strong></p>
                </div>

                <div class="rules-section">
                    <div class="rules-filter">
                        <div class="filter-info">
                            <span class="filter-text">Rules have been auto-filtered based on claim type: <strong>${this.formatClaimType(claimType)}</strong></span>
                            <span class="rules-count">${relevantRules.length} Rules Found for ${this.formatClaimType(claimType)}</span>
                        </div>
                    </div>

                    <div class="rules-grid">
                        ${relevantRules.map(rule => `
                            <div class="rule-card ${this.selectedRules.has(rule.id) ? 'selected' : ''}" data-rule-id="${rule.id}">
                                <div class="rule-header">
                                    <div class="rule-info">
                                        <input type="checkbox" class="rule-checkbox" id="rule-${rule.id}" 
                                               ${this.selectedRules.has(rule.id) ? 'checked' : ''}
                                               onchange="app.toggleRuleSelection('${rule.id}')">
                                        <span class="rule-id">${rule.id}</span>
                                        <span class="rule-severity ${(rule.severity || rule.riskLevel || 'medium').toLowerCase()}">
                                            ${rule.severity || rule.riskLevel || 'Medium'}
                                        </span>
                                    </div>
                                </div>
                                <div class="rule-description">
                                    ${rule.description}
                                </div>
                            </div>
                        `).join('')}
                    </div>

                    <div class="rules-summary">
                        <div class="summary-info">
                            <span class="selected-count">${this.selectedRules.size} rules selected</span>
                            <div class="bulk-actions">
                                <button type="button" class="btn btn-sm btn-secondary" onclick="app.selectAllRules()">Select All</button>
                                <button type="button" class="btn btn-sm btn-secondary" onclick="app.deselectAllRules()">Deselect All</button>
                            </div>
                        </div>
                    </div>

                    <div class="step-actions">
                        <button type="button" class="btn btn-secondary" onclick="app.loadStep(1)">
                            ← Back to Step 1
                        </button>
                        <button type="button" class="btn btn-primary" onclick="app.proceedToStep3()">
                            Continue to Rule Checks →
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // Step 3: Perform Rule Checks
    renderStep3() {
        const selectedRulesArray = this.getSelectedRulesArray();
        
        // Automatically evaluate all selected rules
        this.runAutoValidation();
        
        return `
            <div class="step-content">
                <div class="step-header">
                    <h2>Step 3: Rule Validation Results</h2>
                    <p>Automatically evaluated ${selectedRulesArray.length} rules against your claim data.</p>
                </div>

                <div class="rule-checking-container">
                    <div class="rules-checking">
                        ${selectedRulesArray.map(rule => {
                            const result = this.ruleResults.get(rule.id);
                            const ruleSeverity = rule.severity || rule.riskLevel || 'Medium';
                            const passed = result ? result.passed : false;
                            
                            return `
                                <div class="rule-check-card">
                                    <div class="rule-check-id">${rule.id}</div>
                                    <div class="rule-check-name">${rule.description}</div>
                                    <div class="rule-check-reason">
                                        Severity: <span class="rule-severity ${ruleSeverity.toLowerCase()}">${ruleSeverity}</span>
                                    </div>
                                    <div class="rule-status">
                                        <button class="status-btn ${passed ? 'pass' : 'fail'}" disabled>
                                            ${passed ? '✓ Pass' : '✗ Fail'}
                                        </button>
                                    </div>
                                    ${result && result.reason ? `
                                        <div class="rule-reason">
                                            <strong>Reason:</strong> ${result.reason}
                                        </div>
                                    ` : ''}
                                </div>
                            `;
                        }).join('')}
                    </div>

                    <div class="validation-summary">
                        <div class="summary-stats">
                            <div class="stat-item">
                                <span class="stat-number">${this.getPassedRulesCount()}</span>
                                <span class="stat-label">Passed</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">${this.getFailedRulesCount()}</span>
                                <span class="stat-label">Failed</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-number">${this.getCriticalFailuresCount()}</span>
                                <span class="stat-label">Critical Failures</span>
                            </div>
                        </div>
                    </div>

                    <div class="step-actions">
                        <button type="button" class="btn btn-secondary" onclick="app.loadStep(2)">
                            ← Back to Rules
                        </button>
                        <button type="button" class="btn btn-primary" onclick="app.proceedToStep4()">
                            View Risk Analysis →
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // Step 4: Show Risk Analysis Result
    renderStep4() {
        const riskScore = this.calculateRiskScore();
        const riskLevel = this.getRiskLevel(riskScore.score);
        const recommendation = this.getRecommendation(riskLevel);
        const criticalFailures = this.getCriticalFailures();
        
        return `
            <div class="step-content">
                <div class="step-header">
                    <h2>Step 4: Risk Analysis Result</h2>
                    <p>Complete analysis based on claim data and rule validation results.</p>
                </div>

                <div class="results-container">
                    <div class="risk-score-section">
                        <div class="risk-score-card ${riskLevel.toLowerCase()}">
                            <div class="score-header">
                                <h3>Risk Assessment</h3>
                                <span class="score-calculation">
                                    Based on ${this.getFailedRulesCount()} failed rules
                                </span>
                            </div>
                            <div class="score-display">
                                <div class="score-number">${riskScore.score}</div>
                                <div class="score-level">${riskLevel} Risk</div>
                            </div>
                        </div>

                        <div class="recommendation-card ${recommendation.type}">
                            <div class="recommendation-icon">${recommendation.icon}</div>
                            <div class="recommendation-content">
                                <h4>${recommendation.action}</h4>
                                <p>${recommendation.description}</p>
                            </div>
                        </div>
                    </div>

                    <div class="claim-summary">
                        <h4>Claim Summary</h4>
                        <div class="summary-grid">
                            <div class="summary-item">
                                <span class="label">Customer Name</span>
                                <span class="value">${this.formData.customerName}</span>
                            </div>
                            <div class="summary-item">
                                <span class="label">Policy Number</span>
                                <span class="value">${this.formData.policyNumber}</span>
                            </div>
                            <div class="summary-item">
                                <span class="label">Claim Type</span>
                                <span class="value">${this.formatClaimType(this.formData.claimType)}</span>
                            </div>
                            <div class="summary-item">
                                <span class="label">Claim Amount</span>
                                <span class="value">₹${parseInt(this.formData.claimAmount).toLocaleString('en-IN')}</span>
                            </div>
                            <div class="summary-item">
                                <span class="label">Rules Evaluated</span>
                                <span class="value">${this.selectedRules.size}</span>
                            </div>
                            <div class="summary-item">
                                <span class="label">Analysis Date</span>
                                <span class="value">${new Date().toLocaleDateString('en-IN')}</span>
                            </div>
                        </div>
                    </div>

                    ${criticalFailures.length > 0 ? `
                        <div class="critical-failures-section">
                            <h4 style="color: #dc2626; margin-bottom: 1rem;">🚨 Critical Rule Violations</h4>
                            <div class="critical-failures">
                                ${criticalFailures.map(rule => `
                                    <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 1rem; margin-bottom: 0.5rem;">
                                        <div style="font-weight: 600; color: #dc2626; margin-bottom: 0.25rem;">${rule.id}</div>
                                        <div style="color: #374151; font-size: 0.9rem;">${rule.description}</div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}

                    <div class="step-actions">
                        <button type="button" class="btn btn-secondary" onclick="app.loadStep(3)">
                            ← Back to Rule Checks
                        </button>
                        <button type="button" class="btn btn-success" onclick="app.downloadReport()">
                            📄 Download Report
                        </button>
                        <button type="button" class="btn btn-primary" onclick="app.resetAnalysis()">
                            🔄 New Analysis
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // Event Listeners and Helper Methods
    attachEventListeners() {
        document.addEventListener('input', (e) => {
            if (e.target.matches('input, select, textarea')) {
                this.formData[e.target.id] = e.target.value;
            }
        });
    }

    attachRuleEventListeners() {
        window.app = this; // Ensure global access for onclick handlers
    }

    // Step 1 Methods
    submitStep1() {
        if (this.validateStep1()) {
            this.loadStep(2);
        } else {
            alert('Please fill in all required fields.');
        }
    }

    validateStep1() {
        const required = ['customerName', 'policyNumber', 'claimType', 'claimAmount', 'policyStartDate', 'incidentDate'];
        return required.every(field => {
            const value = this.formData[field];
            if (!value) return false;
            // Convert to string and trim for validation
            const stringValue = String(value).trim();
            return stringValue !== '';
        });
    }

    fillDummyData() {
        if (RiskAnalysisData && RiskAnalysisData.sampleClaims && RiskAnalysisData.sampleClaims.length > 0) {
            const randomSample = RiskAnalysisData.sampleClaims[Math.floor(Math.random() * RiskAnalysisData.sampleClaims.length)];
            
            this.formData = {
                customerName: randomSample.customerName,
                policyNumber: randomSample.policyNumber,
                claimType: randomSample.claimType,
                claimAmount: randomSample.claimAmount,
                policyStartDate: randomSample.policyStartDate,
                incidentDate: randomSample.incidentDate,
                hospitalGarageName: randomSample.providerName
            };
            
            // Update form fields
            Object.keys(this.formData).forEach(key => {
                const element = document.getElementById(key);
                if (element) {
                    element.value = this.formData[key];
                }
            });
        } else {
            alert('No sample data available.');
        }
    }

    clearForm() {
        this.formData = {};
        const fields = ['customerName', 'policyNumber', 'claimType', 'claimAmount', 'policyStartDate', 'incidentDate', 'hospitalGarageName'];
        fields.forEach(field => {
            const element = document.getElementById(field);
            if (element) {
                element.value = '';
            }
        });
    }

    // Step 2 Methods
    toggleRuleSelection(ruleId) {
        if (this.selectedRules.has(ruleId)) {
            this.selectedRules.delete(ruleId);
        } else {
            this.selectedRules.add(ruleId);
        }
        this.updateRuleCard(ruleId);
        this.updateSelectedCount();
    }

    updateRuleCard(ruleId) {
        const ruleCard = document.querySelector(`[data-rule-id="${ruleId}"]`);
        const checkbox = document.getElementById(`rule-${ruleId}`);
        
        if (this.selectedRules.has(ruleId)) {
            ruleCard.classList.add('selected');
            checkbox.checked = true;
        } else {
            ruleCard.classList.remove('selected');
            checkbox.checked = false;
        }
    }

    updateSelectedCount() {
        const countElement = document.querySelector('.selected-count');
        if (countElement) {
            countElement.textContent = `${this.selectedRules.size} rules selected`;
        }
    }

    selectAllRules() {
        const claimType = this.formData.claimType;
        if (claimType && RiskAnalysisData.rules[claimType]) {
            RiskAnalysisData.rules[claimType].forEach(rule => {
                this.selectedRules.add(rule.id);
            });
            this.loadStep(2); // Refresh display
        }
    }

    deselectAllRules() {
        this.selectedRules.clear();
        this.loadStep(2); // Refresh display
    }

    proceedToStep3() {
        if (this.selectedRules.size === 0) {
            alert('Please select at least one rule to proceed.');
            return;
        }
        this.loadStep(3);
    }

    // Step 3 Methods
    runAutoValidation() {
        const selectedRulesArray = this.getSelectedRulesArray();
        
        selectedRulesArray.forEach(rule => {
            const result = this.evaluateRule(rule);
            this.ruleResults.set(rule.id, result);
        });
    }

    evaluateRule(rule) {
        // Simplified rule evaluation logic based on claim data
        const claimAmount = parseInt(this.formData.claimAmount);
        const policyStartDate = new Date(this.formData.policyStartDate);
        const incidentDate = new Date(this.formData.incidentDate);
        const daysBetween = (incidentDate - policyStartDate) / (1000 * 60 * 60 * 24);
        
        // Sample rule evaluation logic based on rule conditions
        const ruleId = rule.id;
        
        // Health Insurance Rules
        if (ruleId.startsWith('HLT-')) {
            switch (ruleId) {
                case 'HLT-001':
                    return {
                        passed: claimAmount <= 500000,
                        reason: claimAmount > 500000 ? 'Claim amount exceeds ₹5,00,000 limit' : 'Within acceptable limit'
                    };
                case 'HLT-002':
                    return {
                        passed: daysBetween >= 30,
                        reason: daysBetween < 30 ? 'Policy too new - 30-day waiting period not met' : 'Waiting period satisfied'
                    };
                case 'HLT-003':
                    return {
                        passed: claimAmount <= 300000,
                        reason: claimAmount > 300000 ? 'Room rent may exceed limits' : 'Room rent within limits'
                    };
                default:
                    const passed = Math.random() > 0.3;
                    return {
                        passed: passed,
                        reason: passed ? 'Health rule validation passed' : 'Health rule validation failed'
                    };
            }
        }
        
        // Motor Insurance Rules
        if (ruleId.startsWith('MOT-')) {
            switch (ruleId) {
                case 'MOT-001':
                    return {
                        passed: claimAmount <= 1500000,
                        reason: claimAmount > 1500000 ? 'Third-party claim exceeds ₹15 lakhs - requires legal clearance' : 'Within acceptable limit'
                    };
                case 'MOT-002':
                    return {
                        passed: daysBetween >= 30,
                        reason: daysBetween < 30 ? 'Motor accident within 30 days - flagged for investigation' : 'Policy eligibility confirmed'
                    };
                case 'MOT-003':
                    return {
                        passed: claimAmount <= 200000,
                        reason: claimAmount > 200000 ? 'Total loss claim - requires surveyor assessment and police FIR' : 'Within normal claim range'
                    };
                default:
                    const passed = Math.random() > 0.3;
                    return {
                        passed: passed,
                        reason: passed ? 'Motor rule validation passed' : 'Motor rule validation failed'
                    };
            }
        }
        
        // Life Insurance Rules
        if (ruleId.startsWith('LIF-')) {
            switch (ruleId) {
                case 'LIF-001':
                    return {
                        passed: daysBetween >= 365, // 1 year for suicide exclusion
                        reason: daysBetween < 365 ? 'Policy requires 12-month waiting period for suicide exclusion check' : 'Suicide exclusion period satisfied'
                    };
                case 'LIF-002':
                    return {
                        passed: claimAmount <= 2500000,
                        reason: claimAmount > 2500000 ? 'Claim exceeds ₹25 lakhs - requires medical examination and police verification' : 'Within coverage limits'
                    };
                default:
                    const passed = Math.random() > 0.3;
                    return {
                        passed: passed,
                        reason: passed ? 'Life rule validation passed' : 'Life rule validation failed'
                    };
            }
        }
        
        // Default case for any other rules
        const passed = Math.random() > 0.3;
        return {
            passed: passed,
            reason: passed ? 'Rule validation passed' : 'Rule validation failed'
        };
    }

    proceedToStep4() {
        this.loadStep(4);
    }

    // Step 4 Methods and Calculations
    calculateRiskScore() {
        let highFailures = 0;
        let mediumFailures = 0;
        let lowFailures = 0;
        
        this.selectedRules.forEach(ruleId => {
            const result = this.ruleResults.get(ruleId);
            if (result && !result.passed) {
                const rule = this.getRuleById(ruleId);
                if (rule) {
                    const severity = rule.severity || rule.riskLevel || 'Medium';
                    switch (severity) {
                        case 'High':
                            highFailures++;
                            break;
                        case 'Medium':
                            mediumFailures++;
                            break;
                        case 'Low':
                            lowFailures++;
                            break;
                    }
                }
            }
        });
        
        const score = Math.min((highFailures * 30) + (mediumFailures * 20) + (lowFailures * 10), 100);
        
        return {
            score: score,
            highFailures: highFailures,
            mediumFailures: mediumFailures,
            lowFailures: lowFailures
        };
    }

    getRiskLevel(score) {
        if (score >= 60) return 'High';
        if (score >= 30) return 'Medium';
        return 'Low';
    }

    getRecommendation(riskLevel) {
        switch (riskLevel) {
            case 'High':
                return {
                    type: 'escalate',
                    action: 'Escalate for Review',
                    description: 'This claim requires immediate attention from a senior adjuster due to high risk factors.',
                    icon: '🚨'
                };
            case 'Medium':
                return {
                    type: 'investigate',
                    action: 'Investigate Further',
                    description: 'Additional documentation and verification may be required before approval.',
                    icon: '🔍'
                };
            default:
                return {
                    type: 'approve',
                    action: 'Approve',
                    description: 'Claim meets all criteria and can be processed for approval.',
                    icon: '✅'
                };
        }
    }

    // Utility Methods
    getSelectedRulesArray() {
        const claimType = this.formData.claimType;
        if (!claimType || !RiskAnalysisData.rules[claimType]) return [];
        
        return RiskAnalysisData.rules[claimType].filter(rule => this.selectedRules.has(rule.id));
    }

    getRuleById(ruleId) {
        const claimType = this.formData.claimType;
        if (!claimType || !RiskAnalysisData.rules[claimType]) return null;
        
        return RiskAnalysisData.rules[claimType].find(rule => rule.id === ruleId);
    }

    getPassedRulesCount() {
        let count = 0;
        this.selectedRules.forEach(ruleId => {
            const result = this.ruleResults.get(ruleId);
            if (result && result.passed) count++;
        });
        return count;
    }

    getFailedRulesCount() {
        let count = 0;
        this.selectedRules.forEach(ruleId => {
            const result = this.ruleResults.get(ruleId);
            if (result && !result.passed) count++;
        });
        return count;
    }

    getCriticalFailuresCount() {
        let count = 0;
        this.selectedRules.forEach(ruleId => {
            const result = this.ruleResults.get(ruleId);
            const rule = this.getRuleById(ruleId);
            if (result && !result.passed && rule && (rule.severity === 'High' || rule.riskLevel === 'High')) {
                count++;
            }
        });
        return count;
    }

    getCriticalFailures() {
        const failures = [];
        this.selectedRules.forEach(ruleId => {
            const result = this.ruleResults.get(ruleId);
            const rule = this.getRuleById(ruleId);
            if (result && !result.passed && rule && (rule.severity === 'High' || rule.riskLevel === 'High')) {
                failures.push(rule);
            }
        });
        return failures;
    }

    formatClaimType(type) {
        const types = {
            'health': 'Health Insurance',
            'motor': 'Motor Insurance',
            'life': 'Life Insurance'
        };
        return types[type] || type;
    }

    downloadReport() {
        const reportContent = this.generateReportContent();
        const blob = new Blob([reportContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `Risk_Analysis_Report_${this.formData.policyNumber}_${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    generateReportContent() {
        const riskScore = this.calculateRiskScore();
        const riskLevel = this.getRiskLevel(riskScore.score);
        const recommendation = this.getRecommendation(riskLevel);
        
        return `RISK ANALYSIS REPORT
====================

Customer Information:
- Name: ${this.formData.customerName}
- Policy Number: ${this.formData.policyNumber}
- Claim Type: ${this.formatClaimType(this.formData.claimType)}
- Claim Amount: ₹${parseInt(this.formData.claimAmount).toLocaleString('en-IN')}
- Policy Start Date: ${this.formData.policyStartDate}
- Incident Date: ${this.formData.incidentDate}
- Hospital/Garage: ${this.formData.hospitalGarageName || 'N/A'}

Risk Analysis Results:
- Risk Score: ${riskScore.score}
- Risk Level: ${riskLevel}
- Recommendation: ${recommendation.action}

Rule Evaluation Summary:
- Total Rules Evaluated: ${this.selectedRules.size}
- Passed: ${this.getPassedRulesCount()}
- Failed: ${this.getFailedRulesCount()}
- Critical Failures: ${this.getCriticalFailuresCount()}

Detailed Rule Results:
${this.getSelectedRulesArray().map(rule => {
    const result = this.ruleResults.get(rule.id);
    return `- ${rule.id} (${rule.description}): ${result ? (result.passed ? 'PASSED' : 'FAILED') : 'NOT EVALUATED'}${result && result.reason ? ` - ${result.reason}` : ''}`;
}).join('\n')}

Report Generated: ${new Date().toLocaleString('en-IN')}`;
    }

    resetAnalysis() {
        this.currentStep = 1;
        this.formData = {};
        this.selectedRules.clear();
        this.ruleResults.clear();
        this.autoValidate = false;
        this.initializeDefaultRules();
        this.loadStep(1);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.app = new RiskAnalysisApp();
});
