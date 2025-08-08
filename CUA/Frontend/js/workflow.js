// Workflow Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize workflow functionality
    initializeWorkflow();
    initializeControls();
    initializeModal();
});

let workflowSimulation = null;
let isSimulationRunning = false;

function initializeWorkflow() {
    // Add event listeners for workflow buttons
    const simulateBtn = document.getElementById('simulateWorkflow');
    const downloadBtn = document.getElementById('downloadGuide');
    const resetBtn = document.getElementById('resetWorkflow');
    const pauseBtn = document.getElementById('pauseWorkflow');

    if (simulateBtn) {
        simulateBtn.addEventListener('click', startWorkflowSimulation);
    }

    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadGuide);
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', resetWorkflow);
    }

    if (pauseBtn) {
        pauseBtn.addEventListener('click', togglePauseWorkflow);
    }
}

function initializeControls() {
    // Add event listeners for range controls
    const speedControl = document.getElementById('simulationSpeed');
    const thresholdControl = document.getElementById('autoApproveThreshold');

    if (speedControl) {
        speedControl.addEventListener('input', updateSimulationSpeed);
    }

    if (thresholdControl) {
        thresholdControl.addEventListener('input', updateAutoApproveThreshold);
    }
}

function initializeModal() {
    const modal = document.getElementById('stepModal');
    const closeBtn = document.getElementById('closeStepModal');

    if (closeBtn) {
        closeBtn.addEventListener('click', closeStepModal);
    }

    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeStepModal();
            }
        });
    }
}

function startWorkflowSimulation() {
    if (isSimulationRunning) {
        return;
    }

    isSimulationRunning = true;
    const simulateBtn = document.getElementById('simulateWorkflow');
    const pauseBtn = document.getElementById('pauseWorkflow');

    if (simulateBtn) {
        simulateBtn.textContent = 'Running...';
        simulateBtn.disabled = true;
    }

    if (pauseBtn) {
        pauseBtn.disabled = false;
    }

    resetWorkflow();
    
    const steps = document.querySelectorAll('.workflow-step');
    const speed = document.getElementById('simulationSpeed')?.value || 5;
    const delay = 3000 - (speed * 250); // Speed affects delay

    let currentStep = 0;

    workflowSimulation = setInterval(() => {
        if (currentStep < steps.length) {
            simulateStep(currentStep + 1);
            currentStep++;
        } else {
            stopWorkflowSimulation();
        }
    }, delay);
}

function simulateStep(stepNumber) {
    const step = document.querySelector(`[data-step="${stepNumber}"]`);
    const status = document.getElementById(`status-${stepNumber}`);
    const marker = step?.querySelector('.step-marker');

    if (!step || !status) return;

    // Add processing animation
    step.classList.add('active');
    marker?.classList.add('processing');
    status.textContent = 'Processing...';
    status.className = 'step-status processing';

    // Simulate processing time
    setTimeout(() => {
        // Complete the step
        step.classList.remove('active');
        step.classList.add('completed');
        marker?.classList.remove('processing');
        status.textContent = 'Completed';
        status.className = 'step-status completed';

        // Show completion notification
        showStepCompletion(stepNumber);
    }, 1500);
}

function showStepCompletion(stepNumber) {
    const stepTitles = [
        '', 'Document Upload', 'Policy Verification', 'Risk Assessment', 
        'Fraud Detection', 'Manual Review', 'Final Decision'
    ];

    showNotification(`✅ ${stepTitles[stepNumber]} completed successfully`, 'success');
}

function stopWorkflowSimulation() {
    if (workflowSimulation) {
        clearInterval(workflowSimulation);
        workflowSimulation = null;
    }

    isSimulationRunning = false;
    
    const simulateBtn = document.getElementById('simulateWorkflow');
    const pauseBtn = document.getElementById('pauseWorkflow');

    if (simulateBtn) {
        simulateBtn.innerHTML = '<span class="btn-icon">▶️</span> Simulate Workflow';
        simulateBtn.disabled = false;
    }

    if (pauseBtn) {
        pauseBtn.innerHTML = '<span class="btn-icon">⏸️</span> Pause';
        pauseBtn.disabled = true;
    }

    showNotification('🎉 Workflow simulation completed!', 'success');
}

function togglePauseWorkflow() {
    const pauseBtn = document.getElementById('pauseWorkflow');
    
    if (workflowSimulation) {
        // Pause
        clearInterval(workflowSimulation);
        workflowSimulation = null;
        if (pauseBtn) {
            pauseBtn.innerHTML = '<span class="btn-icon">▶️</span> Resume';
        }
        showNotification('⏸️ Workflow simulation paused', 'info');
    } else if (isSimulationRunning) {
        // Resume
        startWorkflowSimulation();
        if (pauseBtn) {
            pauseBtn.innerHTML = '<span class="btn-icon">⏸️</span> Pause';
        }
        showNotification('▶️ Workflow simulation resumed', 'info');
    }
}

function resetWorkflow() {
    // Stop any running simulation
    if (workflowSimulation) {
        clearInterval(workflowSimulation);
        workflowSimulation = null;
    }

    isSimulationRunning = false;

    // Reset all steps
    const steps = document.querySelectorAll('.workflow-step');
    steps.forEach((step, index) => {
        const status = document.getElementById(`status-${index + 1}`);
        const marker = step.querySelector('.step-marker');

        step.classList.remove('active', 'completed');
        marker?.classList.remove('processing');
        
        if (status) {
            status.textContent = 'Pending';
            status.className = 'step-status';
        }
    });

    // Reset buttons
    const simulateBtn = document.getElementById('simulateWorkflow');
    const pauseBtn = document.getElementById('pauseWorkflow');

    if (simulateBtn) {
        simulateBtn.innerHTML = '<span class="btn-icon">▶️</span> Simulate Workflow';
        simulateBtn.disabled = false;
    }

    if (pauseBtn) {
        pauseBtn.innerHTML = '<span class="btn-icon">⏸️</span> Pause';
        pauseBtn.disabled = true;
    }

    showNotification('🔄 Workflow reset successfully', 'info');
}

function updateSimulationSpeed() {
    const speed = document.getElementById('simulationSpeed')?.value;
    showNotification(`⚡ Simulation speed updated to ${speed}/10`, 'info');
}

function updateAutoApproveThreshold() {
    const threshold = document.getElementById('autoApproveThreshold')?.value;
    showNotification(`🎯 Auto-approve threshold set to ${threshold}%`, 'info');
}

function downloadGuide() {
    // Simulate file download
    showNotification('📄 Workflow guide download started...', 'info');
    
    setTimeout(() => {
        showNotification('✅ Workflow guide downloaded successfully!', 'success');
    }, 2000);
}

function showStepDetails(stepNumber) {
    const modal = document.getElementById('stepModal');
    const title = document.getElementById('stepModalTitle');
    const body = document.getElementById('stepModalBody');

    const stepDetails = {
        1: {
            title: 'Document Upload - Detailed Process',
            content: `
                <div class="step-detail-content">
                    <h3>📄 Document Collection Process</h3>
                    <p>This step involves the initial collection and validation of all required documents from the customer or agent.</p>
                    
                    <h4>Required Documents by Insurance Type:</h4>
                    <ul>
                        <li><strong>Health Insurance:</strong> Claim form, Hospital bills, Discharge summary, Doctor's prescription, ID proof, Policy copy</li>
                        <li><strong>Motor Insurance:</strong> Claim form, FIR copy, RC book, Driving license, Repair estimates, Photos</li>
                        <li><strong>Life Insurance:</strong> Claim form, Death certificate, Medical records, Nominee ID proof, Policy documents</li>
                    </ul>
                    
                    <h4>Validation Checks:</h4>
                    <ul>
                        <li>Document format verification (PDF, JPG, PNG)</li>
                        <li>File size limits (Max 5MB per document)</li>
                        <li>Completeness check against policy requirements</li>
                        <li>Digital signature validation</li>
                    </ul>
                    
                    <h4>Indian Compliance:</h4>
                    <p>All documents are verified against IRDAI guidelines and Indian regulatory requirements.</p>
                </div>
            `
        },
        2: {
            title: 'Policy Verification - System Integration',
            content: `
                <div class="step-detail-content">
                    <h3>🔍 Comprehensive Policy Validation</h3>
                    <p>Automated verification process that cross-checks policy details with our core systems.</p>
                    
                    <h4>Verification Parameters:</h4>
                    <ul>
                        <li><strong>Policy Status:</strong> Active, Lapsed, Cancelled verification</li>
                        <li><strong>Premium Status:</strong> Up-to-date payment verification</li>
                        <li><strong>Coverage Limits:</strong> Sum insured vs claim amount</li>
                        <li><strong>Waiting Period:</strong> Policy maturation checks</li>
                        <li><strong>Exclusions:</strong> Coverage limitation verification</li>
                    </ul>
                    
                    <h4>System Integration:</h4>
                    <ul>
                        <li>Policy Management System (PMS) integration</li>
                        <li>Premium collection system linkage</li>
                        <li>Agent portal synchronization</li>
                        <li>Customer portal updates</li>
                    </ul>
                    
                    <h4>IRDAI Compliance:</h4>
                    <p>All verifications follow IRDAI guidelines for claim processing timelines and requirements.</p>
                </div>
            `
        },
        3: {
            title: 'AI Risk Assessment - Advanced Analytics',
            content: `
                <div class="step-detail-content">
                    <h3>🎯 Machine Learning Risk Scoring</h3>
                    <p>Our advanced AI engine analyzes multiple data points to generate accurate risk scores.</p>
                    
                    <h4>Risk Factors Analyzed:</h4>
                    <ul>
                        <li><strong>Customer Profile:</strong> Age, history, claim frequency</li>
                        <li><strong>Claim Details:</strong> Amount, type, timing patterns</li>
                        <li><strong>Medical Data:</strong> Treatment history, hospital reputation</li>
                        <li><strong>Geographic:</strong> Location risk factors, regional patterns</li>
                        <li><strong>Behavioral:</strong> Submission patterns, document quality</li>
                    </ul>
                    
                    <h4>AI Model Features:</h4>
                    <ul>
                        <li>Deep learning neural networks</li>
                        <li>Pattern recognition algorithms</li>
                        <li>Predictive analytics</li>
                        <li>Real-time scoring engine</li>
                        <li>Continuous model improvement</li>
                    </ul>
                    
                    <h4>Indian Market Adaptations:</h4>
                    <p>Model trained on Indian healthcare patterns, regional variations, and local risk factors.</p>
                </div>
            `
        },
        4: {
            title: 'Fraud Detection - Security Framework',
            content: `
                <div class="step-detail-content">
                    <h3>🛡️ Multi-layered Fraud Prevention</h3>
                    <p>Comprehensive fraud detection system protecting against various types of insurance fraud.</p>
                    
                    <h4>Detection Mechanisms:</h4>
                    <ul>
                        <li><strong>Blacklist Screening:</strong> Customer, hospital, agent verification</li>
                        <li><strong>Pattern Analysis:</strong> Unusual claim patterns detection</li>
                        <li><strong>Network Analysis:</strong> Connected fraud ring identification</li>
                        <li><strong>Document Analysis:</strong> Forgery and tampering detection</li>
                        <li><strong>Behavioral Analysis:</strong> Suspicious activity patterns</li>
                    </ul>
                    
                    <h4>Indian Fraud Types:</h4>
                    <ul>
                        <li>Fake medical bills and prescriptions</li>
                        <li>Inflated repair estimates</li>
                        <li>Pre-existing condition concealment</li>
                        <li>Agent collaboration fraud</li>
                        <li>Documentation fraud</li>
                    </ul>
                    
                    <h4>Regulatory Compliance:</h4>
                    <p>Fraud detection aligned with IRDAI anti-fraud guidelines and IRDA regulations.</p>
                </div>
            `
        },
        5: {
            title: 'Manual Review - Expert Assessment',
            content: `
                <div class="step-detail-content">
                    <h3>👤 Senior Claims Officer Review</h3>
                    <p>Human expertise combined with AI insights for accurate claim assessment.</p>
                    
                    <h4>Review Triggers:</h4>
                    <ul>
                        <li><strong>High Risk Score:</strong> AI score above threshold</li>
                        <li><strong>Fraud Alerts:</strong> Suspicious activity detected</li>
                        <li><strong>High Value Claims:</strong> Above ₹1 lakh threshold</li>
                        <li><strong>Complex Cases:</strong> Multiple complications</li>
                        <li><strong>Customer Disputes:</strong> Contested assessments</li>
                    </ul>
                    
                    <h4>Review Process:</h4>
                    <ul>
                        <li>Document authenticity verification</li>
                        <li>Medical necessity assessment</li>
                        <li>Policy terms interpretation</li>
                        <li>Claim amount validation</li>
                        <li>Final approval decision</li>
                    </ul>
                    
                    <h4>Officer Qualifications:</h4>
                    <p>Senior Claims Officers with minimum 5 years experience and IRDAI certification.</p>
                </div>
            `
        },
        6: {
            title: 'Final Decision - Customer Communication',
            content: `
                <div class="step-detail-content">
                    <h3>✅ Decision Processing & Communication</h3>
                    <p>Final claim decision processing with comprehensive customer communication.</p>
                    
                    <h4>Decision Outcomes:</h4>
                    <ul>
                        <li><strong>Approved:</strong> Full or partial claim settlement</li>
                        <li><strong>Rejected:</strong> Claim denied with detailed reasons</li>
                        <li><strong>More Information:</strong> Additional documents required</li>
                        <li><strong>Investigation:</strong> Detailed investigation needed</li>
                    </ul>
                    
                    <h4>Communication Channels:</h4>
                    <ul>
                        <li>Email notification with detailed report</li>
                        <li>SMS updates for quick notifications</li>
                        <li>Customer portal updates</li>
                        <li>Phone call for high-value claims</li>
                        <li>Physical letter for regulatory compliance</li>
                    </ul>
                    
                    <h4>Settlement Process:</h4>
                    <ul>
                        <li>NEFT/RTGS bank transfer (approved claims)</li>
                        <li>Cashless settlement (pre-approved cases)</li>
                        <li>Reimbursement processing</li>
                        <li>TDS calculation and deduction</li>
                    </ul>
                    
                    <h4>Appeals Process:</h4>
                    <p>30-day appeal window with Insurance Ombudsman escalation option as per IRDAI guidelines.</p>
                </div>
            `
        }
    };

    const details = stepDetails[stepNumber];
    if (details && title && body && modal) {
        title.textContent = details.title;
        body.innerHTML = details.content;
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeStepModal() {
    const modal = document.getElementById('stepModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Utility function for notifications
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
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
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}
