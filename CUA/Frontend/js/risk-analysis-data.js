// Risk Analysis Data - Indian Insurance Context
// Contains rules, sample data, and validation logic

const RiskAnalysisData = {
    // Sample Indian claims data for testing
    sampleClaims: [
        {
            customerName: "Rajesh Kumar Sharma",
            policyNumber: "GSS-2025-123456",
            claimType: "health",
            claimAmount: 185000,
            policyStartDate: "2023-05-15",
            incidentDate: "2025-08-01",
            providerName: "Apollo Hospital, Delhi"
        },
        {
            customerName: "Priya Singh Chauhan",
            policyNumber: "GSS-2024-987654",
            claimType: "motor",
            claimAmount: 45000,
            policyStartDate: "2024-01-10",
            incidentDate: "2025-07-28",
            providerName: "Maruti Service Center, Mumbai"
        },
        {
            customerName: "Amit Patel",
            policyNumber: "GSS-2023-456789",
            claimType: "life",
            claimAmount: 2500000,
            policyStartDate: "2020-12-05",
            incidentDate: "2025-07-30",
            providerName: "LIC Branch Office, Ahmedabad"
        },
        {
            customerName: "Sunita Sharma Gupta",
            policyNumber: "GSS-2025-111222",
            claimType: "health",
            claimAmount: 320000,
            policyStartDate: "2024-03-20",
            incidentDate: "2025-08-02",
            providerName: "Max Healthcare, Gurgaon"
        },
        {
            customerName: "Vikram Reddy",
            policyNumber: "GSS-2024-333444",
            claimType: "motor",
            claimAmount: 75000,
            policyStartDate: "2023-08-12",
            incidentDate: "2025-08-03",
            providerName: "Hyundai Service Center, Hyderabad"
        },
        {
            customerName: "Anita Joshi",
            policyNumber: "GSS-2024-555666",
            claimType: "health",
            claimAmount: 250000,
            policyStartDate: "2023-11-25",
            incidentDate: "2025-07-25",
            providerName: "Fortis Hospital, Bangalore"
        },
        {
            customerName: "Mohammed Ali Khan",
            policyNumber: "GSS-2025-777888",
            claimType: "motor",
            claimAmount: 120000,
            policyStartDate: "2024-06-18",
            incidentDate: "2025-08-04",
            providerName: "Honda Service Center, Chennai"
        },
        {
            customerName: "Deepika Iyer",
            policyNumber: "GSS-2024-999000",
            claimType: "health",
            claimAmount: 95000,
            policyStartDate: "2023-09-10",
            incidentDate: "2025-07-29",
            providerName: "Manipal Hospital, Kolkata"
        },
        {
            customerName: "Ravi Agarwal",
            policyNumber: "GSS-2023-112233",
            claimType: "life",
            claimAmount: 1500000,
            policyStartDate: "2019-04-15",
            incidentDate: "2025-08-01",
            providerName: "HDFC Life Branch, Pune"
        },
        {
            customerName: "Kavita Nair",
            policyNumber: "GSS-2025-445566",
            claimType: "health",
            claimAmount: 85000,
            policyStartDate: "2024-12-01",
            incidentDate: "2025-08-05",
            providerName: "AIIMS Hospital, Delhi"
        }
    ],

    // Insurance rules database with Indian context
    rules: {
        health: [
            {
                id: "HLT-001",
                description: "Claims above ₹5,00,000 require pre-authorization from network hospitals as per IRDAI guidelines",
                type: "health",
                severity: "High",
                condition: "claimAmount > 500000",
                weight: 25
            },
            {
                id: "HLT-002",
                description: "Waiting period of 30 days for illnesses and 48 months for pre-existing diseases (PED)",
                type: "health",
                severity: "High",
                condition: "daysSincePolicyStart < 30",
                weight: 30
            },
            {
                id: "HLT-003",
                description: "Room rent capped at 1% of sum insured or ₹5,000 per day, whichever is lower",
                type: "health",
                severity: "Medium",
                condition: "claimAmount > 300000",
                weight: 15
            },
            {
                id: "HLT-004",
                description: "Maternity claims require 9-month waiting period from policy inception date",
                type: "health",
                severity: "Medium",
                condition: "daysSincePolicyStart < 270",
                weight: 20
            },
            {
                id: "HLT-005",
                description: "Alternative medicine (AYUSH) treatments covered up to ₹25,000 per policy year",
                type: "health",
                severity: "Low",
                condition: "claimAmount > 25000",
                weight: 10
            },
            {
                id: "HLT-006",
                description: "Domiciliary treatment covered only for illness/injury requiring 3+ days bed rest",
                type: "health",
                severity: "Medium",
                condition: "claimAmount < 10000",
                weight: 12
            },
            {
                id: "HLT-007",
                description: "Claims within 15 days of policy purchase require enhanced verification",
                type: "health",
                severity: "High",
                condition: "daysSincePolicyStart < 15",
                weight: 35
            }
        ],
        motor: [
            {
                id: "MOT-001",
                description: "Third-party claims exceeding ₹15 lakhs require legal clearance as per Motor Vehicle Act",
                type: "motor",
                severity: "High",
                condition: "claimAmount > 1500000",
                weight: 30
            },
            {
                id: "MOT-002",
                description: "Motor accidents within 30 days of policy purchase flagged for investigation",
                type: "motor",
                severity: "High",
                condition: "daysSincePolicyStart < 30",
                weight: 25
            },
            {
                id: "MOT-003",
                description: "Total loss claims require surveyor assessment and police FIR",
                type: "motor",
                severity: "High",
                condition: "claimAmount > 200000",
                weight: 20
            },
            {
                id: "MOT-004",
                description: "Own damage claims above ₹50,000 require cashless garage approval",
                type: "motor",
                severity: "Medium",
                condition: "claimAmount > 50000",
                weight: 15
            },
            {
                id: "MOT-005",
                description: "Theft claims require police complaint and RC book submission",
                type: "motor",
                severity: "High",
                condition: "claimAmount > 100000",
                weight: 25
            },
            {
                id: "MOT-006",
                description: "Natural calamity claims require meteorological department confirmation",
                type: "motor",
                severity: "Medium",
                condition: "claimAmount > 75000",
                weight: 18
            },
            {
                id: "MOT-007",
                description: "Claims within 7 days of incident date require immediate documentation",
                type: "motor",
                severity: "Low",
                condition: "daysSinceIncident > 7",
                weight: 10
            }
        ],
        life: [
            {
                id: "LIF-001",
                description: "Life insurance claims within 12 months require suicide exclusion check",
                type: "life",
                severity: "High",
                condition: "daysSincePolicyStart < 365",
                weight: 40
            },
            {
                id: "LIF-002",
                description: "Claims above ₹25 lakhs require medical examination and police verification",
                type: "life",
                severity: "High",
                condition: "claimAmount > 2500000",
                weight: 30
            },
            {
                id: "LIF-003",
                description: "Death claims require death certificate and nominee verification",
                type: "life",
                severity: "Medium",
                condition: "claimAmount > 1000000",
                weight: 20
            },
            {
                id: "LIF-004",
                description: "Accidental death claims require police investigation report",
                type: "life",
                severity: "High",
                condition: "claimAmount > 500000",
                weight: 35
            },
            {
                id: "LIF-005",
                description: "Premium payment verification required for claims during grace period",
                type: "life",
                severity: "Medium",
                condition: "daysSincePolicyStart > 1095",
                weight: 15
            },
            {
                id: "LIF-006",
                description: "Multiple policies from same insured require aggregation check",
                type: "life",
                severity: "Medium",
                condition: "claimAmount > 1500000",
                weight: 18
            }
        ]
    },

    // Risk scoring thresholds
    riskThresholds: {
        low: { min: 0, max: 30 },
        medium: { min: 31, max: 60 },
        high: { min: 61, max: 100 }
    },

    // Fraud indicators
    fraudIndicators: [
        "Multiple claims from same provider",
        "Recent policy inception",
        "High claim amount relative to premium",
        "Previous fraudulent activities",
        "Suspicious provider history"
    ],

    // Common Indian hospitals and garages for validation
    providerDatabase: {
        hospitals: [
            "Apollo Hospital", "Fortis Healthcare", "Max Healthcare", "Manipal Hospital",
            "Narayana Health", "Medanta", "BLK Hospital", "Sir Ganga Ram Hospital",
            "Kokilaben Hospital", "Lilavati Hospital", "Ruby Hospital", "Wockhardt Hospital",
            "AIIMS", "Safdarjung Hospital", "King George Medical College", "PGIMER Chandigarh"
        ],
        garages: [
            "Maruti Service Center", "Hyundai Service Center", "Tata Motors Service",
            "Honda Service Center", "Toyota Service Center", "Mahindra Service",
            "Ford Service Center", "Skoda Service Center", "Volkswagen Service",
            "Renault Service Center", "Nissan Service Center", "BMW Service Center"
        ]
    }
};

// Utility functions for risk analysis
const RiskAnalysisUtils = {
    // Calculate days between two dates
    daysBetween: (startDate, endDate) => {
        const start = new Date(startDate);
        const end = new Date(endDate);
        const timeDiff = end.getTime() - start.getTime();
        return Math.ceil(timeDiff / (1000 * 3600 * 24));
    },

    // Evaluate a rule condition
    evaluateRule: (rule, claimData) => {
        const daysSincePolicyStart = RiskAnalysisUtils.daysBetween(
            claimData.policyStartDate, 
            new Date().toISOString().split('T')[0]
        );
        const daysSinceIncident = RiskAnalysisUtils.daysBetween(
            claimData.incidentDate, 
            new Date().toISOString().split('T')[0]
        );

        const context = {
            claimAmount: parseFloat(claimData.claimAmount),
            daysSincePolicyStart: daysSincePolicyStart,
            daysSinceIncident: daysSinceIncident
        };

        try {
            // Replace variables in condition with actual values
            let condition = rule.condition;
            Object.keys(context).forEach(key => {
                condition = condition.replace(new RegExp(key, 'g'), context[key]);
            });

            // Evaluate the condition (simple evaluation)
            return eval(condition);
        } catch (error) {
            console.error('Error evaluating rule:', rule.id, error);
            return false;
        }
    },

    // Calculate risk score based on failed rules
    calculateRiskScore: (failedRules) => {
        let totalScore = 0;
        let criticalCount = 0;

        failedRules.forEach(rule => {
            totalScore += rule.weight || 10;
            if (rule.severity === 'High') {
                criticalCount++;
            }
        });

        // Add bonus penalty for critical rules
        totalScore += criticalCount * 10;

        // Cap at 100
        return Math.min(totalScore, 100);
    },

    // Get risk level based on score
    getRiskLevel: (score) => {
        const thresholds = RiskAnalysisData.riskThresholds;
        if (score <= thresholds.low.max) return 'Low';
        if (score <= thresholds.medium.max) return 'Medium';
        return 'High';
    },

    // Get recommendation based on risk level and failed rules
    getRecommendation: (riskLevel, failedRules) => {
        const criticalRules = failedRules.filter(rule => rule.severity === 'High');
        
        if (criticalRules.length > 0) {
            return 'Investigate - Critical violations detected';
        }
        
        switch (riskLevel) {
            case 'Low':
                return 'Approve - Low risk claim';
            case 'Medium':
                return 'Review - Moderate risk requires verification';
            case 'High':
                return 'Escalate - High risk requires senior approval';
            default:
                return 'Review Required';
        }
    },

    // Generate detailed report
    generateReport: (claimData, riskResult) => {
        const reportDate = new Date().toLocaleDateString('en-IN');
        const reportTime = new Date().toLocaleTimeString('en-IN');

        return `
GLOBAL SECURE SHIELD - RISK ANALYSIS REPORT
==========================================

Report Generated: ${reportDate} at ${reportTime}

CLAIM DETAILS:
--------------
Customer Name: ${claimData.customerName}
Policy Number: ${claimData.policyNumber}
Claim Type: ${claimData.claimType.toUpperCase()}
Claim Amount: ₹${parseFloat(claimData.claimAmount).toLocaleString('en-IN')}
Policy Start Date: ${claimData.policyStartDate}
Incident Date: ${claimData.incidentDate}
Provider: ${claimData.providerName}

RISK ASSESSMENT:
---------------
Risk Score: ${riskResult.score}/100
Risk Level: ${riskResult.level}
Recommendation: ${riskResult.recommendation}

RULE VIOLATIONS:
---------------
${riskResult.failedRules.length > 0 ? 
    riskResult.failedRules.map(rule => 
        `[${rule.severity.toUpperCase()}] ${rule.id}: ${rule.description}`
    ).join('\n') : 
    'No rule violations detected.'
}

CRITICAL ISSUES:
---------------
${riskResult.criticalRules.length > 0 ? 
    riskResult.criticalRules.map(rule => 
        `🚨 ${rule.id}: ${rule.description}`
    ).join('\n') : 
    'No critical issues identified.'
}

NEXT STEPS:
----------
${riskResult.recommendation}

---
This report is generated by Global Secure Shield's automated risk analysis system.
For queries, contact: claims@globalsecureshield.com
        `.trim();
    }
};
