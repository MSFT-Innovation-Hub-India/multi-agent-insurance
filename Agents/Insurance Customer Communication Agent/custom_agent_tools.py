"""
Custom Agent Tools Module for Insurance Customer Communication

This module contains tool definitions that can be used by the AI agent to perform
specific operations related to insurance customer communication through Logic Apps.

Each tool has:
1. A clear schema definition that describes required parameters
2. Instructions for the agent on when and how to use the tool
3. A reference to the actual function implementation that performs the work
"""

from azure.ai.projects.models import ToolDefinition
from typing import Dict, Any, List
from custom_agent_functions import send_insurance_policy_number, send_insurance_claim_in_progress, send_insurance_claim_approved, send_insurance_claim_rejected

def create_send_insurance_policy_number_tool() -> Dict[str, Any]:
    """
    Create a tool definition for sending policy number generation email.
    
    This tool should be used when a customer provides customer ID and requests Stage 1 (Policy Number Generation).
    
    Returns:
        Dict[str, Any]: The tool definition in the format expected by the Azure AI Projects SDK
    """
    
    tool_definition = {
        "type": "function",
        "function": {
            "name": "send_insurance_policy_number",
            "description": """Send policy number generation email to insurance customers.
            ONLY use this tool when:
            1. Customer provides a valid customer ID
            2. Customer requests Stage 1 or mentions policy number generation
            You MUST have the customer_id before calling this tool.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The unique ID of the insurance customer (required)"
                    }
                },
                "required": ["customer_id"]
            }
        }
    }
    
    return tool_definition


def create_send_insurance_claim_in_progress_tool() -> Dict[str, Any]:
    """
    Create a tool definition for sending claim in progress email.
    
    This tool should be used when a customer provides customer ID and requests Stage 2 (Claim In Progress).
    
    Returns:
        Dict[str, Any]: The tool definition in the format expected by the Azure AI Projects SDK
    """
    
    tool_definition = {
        "type": "function",
        "function": {
            "name": "send_insurance_claim_in_progress",
            "description": """Send claim processing status email to insurance customers.
            ONLY use this tool when:
            1. Customer provides a valid customer ID
            2. Customer requests Stage 2 or mentions claim in progress
            You MUST have the customer_id before calling this tool.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The unique ID of the insurance customer (required)"
                    }
                },
                "required": ["customer_id"]
            }
        }
    }
    
    return tool_definition


def create_send_insurance_claim_approved_tool() -> Dict[str, Any]:
    """
    Create a tool definition for sending claim approved email.
    
    This tool should be used when a customer provides customer ID and requests Stage 3 (Claim Approved).
    
    Returns:
        Dict[str, Any]: The tool definition in the format expected by the Azure AI Projects SDK
    """
    
    tool_definition = {
        "type": "function",
        "function": {
            "name": "send_insurance_claim_approved",
            "description": """Send claim approval notification email to insurance customers.
            ONLY use this tool when:
            1. Customer provides a valid customer ID
            2. Customer requests Stage 3 or mentions claim approved
            You MUST have the customer_id before calling this tool.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The unique ID of the insurance customer (required)"
                    }
                },
                "required": ["customer_id"]
            }
        }
    }
    
    return tool_definition


def create_send_insurance_claim_rejected_tool() -> Dict[str, Any]:
    """
    Create a tool definition for sending claim rejected email.
    
    This tool should be used when a customer provides customer ID and requests Stage 4 (Claim Rejected).
    
    Returns:
        Dict[str, Any]: The tool definition in the format expected by the Azure AI Projects SDK
    """
    
    tool_definition = {
        "type": "function",
        "function": {
            "name": "send_insurance_claim_rejected",
            "description": """Send claim rejection notification email to insurance customers.
            ONLY use this tool when:
            1. Customer provides a valid customer ID
            2. Customer requests Stage 4 or mentions claim rejected
            You MUST have the customer_id before calling this tool.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The unique ID of the insurance customer (required)"
                    }
                },
                "required": ["customer_id"]
            }
        }
    }
    
    return tool_definition


def get_all_custom_agent_tools() -> List[Dict[str, Any]]:
    """
    Get all custom insurance agent tools.
    
    Returns a list of all available insurance communication tools that can be
    used by the AI agent for customer communication.
    
    Returns:
        List[Dict[str, Any]]: List of all insurance communication tool definitions
    """
    
    # List of all insurance communication tools
    tools = [
        create_send_insurance_policy_number_tool(),
        create_send_insurance_claim_in_progress_tool(),
        create_send_insurance_claim_approved_tool(),
        create_send_insurance_claim_rejected_tool()
    ]
    
    return tools


def get_tool_function_map() -> Dict[str, callable]:
    """
    Get a mapping of tool names to their corresponding function implementations.
    
    This mapping is used by the agent to call the correct function when a tool is invoked.
    
    Returns:
        Dict[str, callable]: Dictionary mapping tool names to function implementations
    """
    
    return {
        "send_insurance_policy_number": send_insurance_policy_number,
        "send_insurance_claim_in_progress": send_insurance_claim_in_progress,
        "send_insurance_claim_approved": send_insurance_claim_approved,
        "send_insurance_claim_rejected": send_insurance_claim_rejected
    }


# For backward compatibility, create individual tool getter functions
def get_send_insurance_policy_number_tool() -> Dict[str, Any]:
    return create_send_insurance_policy_number_tool()

def get_send_insurance_claim_in_progress_tool() -> Dict[str, Any]:
    return create_send_insurance_claim_in_progress_tool()

def get_send_insurance_claim_approved_tool() -> Dict[str, Any]:
    return create_send_insurance_claim_approved_tool()

def get_send_insurance_claim_rejected_tool() -> Dict[str, Any]:
    return create_send_insurance_claim_rejected_tool()
