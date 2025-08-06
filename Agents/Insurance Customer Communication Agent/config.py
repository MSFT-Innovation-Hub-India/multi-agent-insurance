"""
Configuration module for the Insurance Customer Communication Agent

This module contains all configuration settings, connection strings, and constants
used throughout the insurance agent application.
"""

# Azure AI Project Configuration
AZURE_PROJECT_CONNECTION_STRING = "eastus2.api.azureml.ms;aee23923-3bba-468d-8dcd-7c4bc1ce218f;rg-ronakofficial1414-9323_ai;ronakofficial1414-8644"
AZURE_AGENT_ID = "asst_eo3eOzKI2Sk7NlezVZU35rL8"

# Logic App Configuration
INSURANCE_LOGIC_APP_URL = "https://demoinsurance.azurewebsites.net:443/api/Insurance/triggers/When_a_HTTP_request_is_received/invoke?api-version=2022-05-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=SnPAbyaqajdIX8V-V4MHttI0DFq0yF5wrk_dWzXE1VI"

# Insurance Stages Configuration
INSURANCE_STAGES = {
    1: {
        "name": "Policy Number Generation",
        "description": "for customers receiving their policy number",
        "tool_function": "send_insurance_policy_number"
    },
    2: {
        "name": "Claim In Progress", 
        "description": "for customers with claims being processed",
        "tool_function": "send_insurance_claim_in_progress"
    },
    3: {
        "name": "Claim Approved",
        "description": "for customers with approved claims", 
        "tool_function": "send_insurance_claim_approved"
    },
    4: {
        "name": "Claim Rejected",
        "description": "for customers with rejected claims",
        "tool_function": "send_insurance_claim_rejected"
    }
}

# Agent Configuration
AGENT_COMPANY_NAME = "Global Secure Shield"
AGENT_NAME = "Insurance Customer Communication Agent"
AGENT_EMOJI = "🏥"

# UI Configuration
SEPARATOR_LENGTH = 70
SEPARATOR_CHAR = "="

# Tool Response Configuration
TOOL_SUCCESS_MESSAGE = "Thank you for using our insurance services. You will be notified via email about your {service_type}."
TOOL_ERROR_MESSAGE = "There was an issue processing your request. Please try again later or contact customer support."

# Run Monitoring Configuration
RUN_CHECK_INTERVAL = 1  # seconds
COMPLETED_STATUSES = ["completed", "requires_action", "failed", "cancelled", "expired"]
