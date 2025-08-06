"""
Utilities module for the Insurance Customer Communication Agent

This module contains utility functions and helper methods used throughout
the insurance agent application.
"""

import time
from typing import Dict, Any, Optional
from config import (
    SEPARATOR_LENGTH, 
    SEPARATOR_CHAR, 
    AGENT_NAME, 
    AGENT_EMOJI, 
    INSURANCE_STAGES,
    RUN_CHECK_INTERVAL,
    COMPLETED_STATUSES
)


def print_welcome_message():
    """Print the welcome message and instructions for the insurance agent"""
    print(SEPARATOR_CHAR * SEPARATOR_LENGTH)
    print(f"{AGENT_EMOJI} {AGENT_NAME} {AGENT_EMOJI}")
    print("This agent helps customers with communication during their insurance process.")
    print("Please provide your customer ID and select the appropriate insurance stage:")
    print("INSURANCE SERVICES:")
    
    for stage_num, stage_info in INSURANCE_STAGES.items():
        print(f"  Stage {stage_num}: {stage_info['name']} - {stage_info['description']}")
    
    print("Type 'exit' or 'quit' to end the conversation")
    print(SEPARATOR_CHAR * SEPARATOR_LENGTH)


def extract_message_content(text_message) -> str:
    """
    Extract the text content from a message object
    
    Args:
        text_message: The message object to extract content from
        
    Returns:
        str: The extracted text content
    """
    try:
        if hasattr(text_message, 'text') and hasattr(text_message.text, 'value'):
            return text_message.text.value
        elif isinstance(text_message, dict) and 'text' in text_message and 'value' in text_message['text']:
            return text_message['text']['value']
        else:
            # Try to access as dictionary
            message_dict = text_message.as_dict() if hasattr(text_message, 'as_dict') else text_message
            if isinstance(message_dict, dict) and 'text' in message_dict and 'value' in message_dict['text']:
                return message_dict['text']['value']
    except Exception:
        pass
    
    # Fallback: return the string representation
    return str(text_message)


def display_latest_message(project_client, thread_id: str):
    """
    Display only the most recent assistant message from the thread
    
    Args:
        project_client: The Azure AI Project client
        thread_id (str): The thread ID to get messages from
    """
    messages = project_client.agents.list_messages(thread_id=thread_id)
    
    # Find the most recent assistant message
    latest_message = None
    for message in messages.text_messages:
        message_content = extract_message_content(message)
        latest_message = message_content
        break  # Only get the most recent message (first in the list)
    
    if latest_message:
        print(f"\n🤖 Agent: {latest_message}\n")
    else:
        print("\n🤖 Agent: No response received.\n")


def monitor_run_status(project_client, run, thread_id: str):
    """
    Monitor a run until it reaches a completed status
    
    Args:
        project_client: The Azure AI Project client
        run: The run object to monitor
        thread_id (str): The thread ID
        
    Returns:
        The final run object with completed status
    """
    run_status = None
    while run_status not in COMPLETED_STATUSES:
        # Get the current run status
        run = project_client.agents.get_run(run_id=run.id, thread_id=thread_id)
        run_status = run.status
        
        # If still in progress, wait a bit before checking again
        if run_status == "in_progress":
            time.sleep(RUN_CHECK_INTERVAL)
    
    return run


def get_stage_info(stage_number: int) -> Optional[Dict[str, str]]:
    """
    Get information about a specific insurance stage
    
    Args:
        stage_number (int): The stage number (1-4)
        
    Returns:
        Optional[Dict[str, str]]: Stage information or None if invalid stage
    """
    return INSURANCE_STAGES.get(stage_number)


def validate_customer_id(customer_id: str) -> bool:
    """
    Validate if a customer ID is in the correct format
    
    Args:
        customer_id (str): The customer ID to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not customer_id or not isinstance(customer_id, str):
        return False
    
    # Remove whitespace and check if it's not empty
    customer_id = customer_id.strip()
    return len(customer_id) > 0


def format_tool_success_message(service_type: str) -> str:
    """
    Format a success message for tool execution
    
    Args:
        service_type (str): The type of service (policy, claim status, etc.)
        
    Returns:
        str: Formatted success message
    """
    from config import TOOL_SUCCESS_MESSAGE
    return TOOL_SUCCESS_MESSAGE.format(service_type=service_type)


def is_exit_command(user_input: str) -> bool:
    """
    Check if the user input is an exit command
    
    Args:
        user_input (str): The user's input
        
    Returns:
        bool: True if it's an exit command, False otherwise
    """
    return user_input.lower().strip() in ['exit', 'quit', 'bye', 'goodbye']
