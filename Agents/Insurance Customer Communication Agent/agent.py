"""
Insurance Customer Communication Agent

This is the main agent module that handles insurance customer communication
by integrating with Azure AI Projects and Logic Apps to send appropriate
email notifications based on customer ID and insurance stage.
"""

# pip install azure-ai-projects~=1.0.0b7
# pip install requests
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import time
import json
import sys

# Import our modular components
from custom_agent_functions import (
    send_insurance_policy_number, 
    send_insurance_claim_in_progress, 
    send_insurance_claim_approved, 
    send_insurance_claim_rejected
)
from custom_agent_tools import get_all_custom_agent_tools
from config import AZURE_PROJECT_CONNECTION_STRING, AZURE_AGENT_ID
from utils import (
    print_welcome_message, 
    display_latest_message, 
    monitor_run_status,
    is_exit_command
)
from tool_handler import InsuranceToolHandler
from system_instructions import get_system_instructions


# Initialize the Azure AI Project client
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=AZURE_PROJECT_CONNECTION_STRING
)

# Get the agent
agent = project_client.agents.get_agent(AZURE_AGENT_ID)


def create_new_thread():
    """Create a new thread for the conversation"""
    return project_client.agents.create_thread()


def interact_with_insurance_agent():
    """Main function to handle insurance customer communication"""
    # Print welcome message using utility function
    print_welcome_message()
    
    # Create a new thread for this conversation
    thread = create_new_thread()
    print(f"\n🔄 Starting a new conversation thread (ID: {thread.id})")
    
    # Initialize tool handler
    tool_handler = InsuranceToolHandler()
    
    # Get all custom agent tools
    agent_tools = get_all_custom_agent_tools()
    
    # Get system instructions
    system_instruction = get_system_instructions()
    
    # Send an initial greeting message to start the conversation
    initial_message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Hello, I need help with communication during my insurance process."
    )
    
    print("\n⏳ Agent is thinking...")
    
    # Process the initial message with system instructions but no tools yet
    run = project_client.agents.create_and_process_run(
        thread_id=thread.id,
        agent_id=agent.id,
        instructions=system_instruction
    )
    
    # Display the agent's initial response
    display_latest_message(project_client, thread.id)
    
    # Start the conversation loop
    while True:
        # Get user input
        user_message = input("👤 You: ")
        
        if is_exit_command(user_message):
            print("\n👋 Thank you for using our insurance services. Goodbye!")
            break
        
        # Send message to the agent
        message = project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=user_message
        )
        
        print("\n⏳ Agent is processing your request...")
        
        # Create run with all custom tools and system instructions
        run = project_client.agents.create_run(
            thread_id=thread.id,
            agent_id=agent.id,
            tools=agent_tools,
            instructions=system_instruction
        )
        
        # Monitor the run using utility function
        run = monitor_run_status(project_client, run, thread.id)
        
        # Check if the run requires action (tool use)
        if run.status == "requires_action" and hasattr(run, "required_action"):
            # Handle tool calls using the tool handler
            tool_outputs = tool_handler.handle_tool_calls(
                run.required_action.submit_tool_outputs.tool_calls
            )
            
            # Submit tool outputs back to the agent if we have any
            if tool_outputs:
                run = project_client.agents.submit_tool_outputs_to_run(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                
                # Monitor the run again after submitting tool outputs
                run = monitor_run_status(project_client, run, thread.id)
        
        # Display the latest message from the agent
        display_latest_message(project_client, thread.id)


# Start the interactive Insurance Customer Communication Agent
if __name__ == "__main__":
    try:
        interact_with_insurance_agent()
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please contact support for assistance.")
        sys.exit(1)
