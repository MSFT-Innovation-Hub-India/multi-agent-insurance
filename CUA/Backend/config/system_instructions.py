"""
System instructions and prompts for the automation system.
"""

class SystemInstructions:
    """Container for system instructions and prompts."""
    
    LOGIN_AND_NAVIGATION_PROMPT = """
Navigate to the page and handle any login if required. 
If you need login credentials, use 'demo' and '123' for the System and then 

go to the Risk Analysis page.
On that page, enter the following customer details:

{
  "customerName": "Rajesh Kumar Sharma",
  "policyNumber": "GSS-2025-123456",
  "claimType": "health",
  "claimAmount": 185000,
  "policyStartDate": "2023-05-15",
  "incidentDate": "2025-08-01",
  "providerName": "Apollo Hospital, Delhi"
}

Click the Submit button.
After the page updates, scroll down and click the Continue button.
Then click the View Risk Analysis button.

Once the Risk Analysis report is visible, extract only the Risk Assessment score, which appears as a number (e.g., 60) in the report section titled "Risk Assessment".

Return only the score in this format:
"The Risk Assessment score is '60'."

Do not return any other text or offer further assistance.
"""
    
    CUSTOMER_SEARCH_PROMPT_TEMPLATE = """
Go to the customers tab and find the CRM Ref for the Customer ID {customer_id}.
If you need login credentials, use {username} and {password} for the CRM System.
"""
    
    SAFETY_WARNING_MESSAGE = """
⚠️ SAFETY WARNING DETECTED!
The system has flagged potential safety concerns with the current action.
Please review the warning details below and confirm if you want to proceed.
"""
    
    SESSION_END_COMMANDS = ['quit', 'bye', 'exit', 'stop']
    
    USER_INTERACTION_MESSAGES = {
        'agent_prompt': "🤖 AGENT MESSAGE:",
        'tip': "💡 Tip: Type 'quit', 'bye', 'exit', or 'stop' to end the session",
        'user_response_prompt': "Your response: ",
        'acknowledge_safety': "Acknowledge safety warning? (yes/no): ",
        'customer_id_prompt': "Enter the Customer ID you want to search for: ",
        'username_prompt': "Enter the Username of the CRM System: ",
        'password_prompt': "Enter the Password of the CRM System: ",
        'system_header': "CUSTOMER LOOKUP SYSTEM",
        'login_header': "EXECUTING FIRST HALF: LOGIN AND NAVIGATION",
        'search_header': "EXECUTING SECOND HALF: FIND CUSTOMER {customer_id}",
        'final_result_header': "FINAL RESULT:",
        'safety_acknowledged': "✅ Safety checks acknowledged. Proceeding...",
        'user_declined': "🛑 User declined to proceed. Ending session...",
        'user_stop_request': "🛑 User requested to stop the session. Ending...",
        'sending_response': "✅ Sending to agent: {response}"
    }
    
    @staticmethod
    def get_customer_search_prompt(customer_id: str, username: str, password: str) -> str:
        """Generate customer search prompt with provided credentials."""
        return SystemInstructions.CUSTOMER_SEARCH_PROMPT_TEMPLATE.format(
            customer_id=customer_id,
            username=username,
            password=password
        )
    
    @staticmethod
    def is_quit_command(command: str) -> bool:
        """Check if the command is a quit command."""
        return command.lower().strip() in SystemInstructions.SESSION_END_COMMANDS
    
    @staticmethod
    def is_agent_requesting_input(message: str) -> bool:
        """Check if the agent is requesting user input."""
        if not message:
            return False
        
        indicators = [
            '?',
            'provide',
            'need',
            "we've detected instructions that may cause your application to perform malicious or unauthorized actions",
            "please acknowledge this warning"
        ]
        
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in indicators)
