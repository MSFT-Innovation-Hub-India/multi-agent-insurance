"""
Core automation engine that orchestrates the automation workflow.
"""

from core.azure_client import azure_client
from core.browser_manager import BrowserManager
from handlers.action_handler import ActionHandler
from handlers.safety_handler import SafetyHandler
from utils.api_utils import safe_api_call
from utils.screenshot_utils import encode_screenshot
from utils.user_interaction import UserInteraction
from config.settings import settings
from config.system_instructions import SystemInstructions

class AutomationEngine:
    """Main automation engine that orchestrates the entire workflow."""
    
    def __init__(self):
        """Initialize the automation engine."""
        self.browser_manager = None
        self.action_handler = None
        self.safety_handler = SafetyHandler()
        self.user_interaction = UserInteraction()
    
    def run_automation(self, customer_id: str, username: str, password: str):
        """Run the complete automation workflow."""
        # Start automation without extra output
        
        with BrowserManager() as browser_manager:
            self.browser_manager = browser_manager
            self.action_handler = ActionHandler(browser_manager)
            
            # Navigate to initial URL
            browser_manager.navigate_to(settings.DEFAULT_CRM_URL)
            
            # Execute the automation workflow
            self._execute_login_and_navigation()
    
    def _execute_login_and_navigation(self):
        """Execute the login and navigation phase."""
        self.user_interaction.print_header(
            SystemInstructions.USER_INTERACTION_MESSAGES['login_header']
        )
        
        def create_response():
            return azure_client.create_initial_response(
                SystemInstructions.LOGIN_AND_NAVIGATION_PROMPT
            )
        
        response = safe_api_call(create_response)
        if response:
            print("First half response:", response.output)
            self._computer_use_loop(response)
        else:
            print("Failed to get initial response for first half")
    
    def _computer_use_loop(self, response):
        """
        Main computer use loop with safety checks and user interaction.
        """
        iteration_count = 0
        
        while iteration_count < settings.MAX_ITERATIONS:
            try:
                computer_calls = [item for item in response.output if item.type == "computer_call"]
                
                if not computer_calls:
                    # Check if agent is requesting user input
                    agent_message = self._extract_agent_message(response)
                    
                    if agent_message and SystemInstructions.is_agent_requesting_input(agent_message):
                        response = self._handle_user_interaction(response, agent_message)
                        if response is None:
                            break
                        continue
                    
                    print("No more computer calls. Task completed.")
                    for item in response.output:
                        print(item)
                    break
                
                computer_call = computer_calls[0]
                action = computer_call.action
                
                # Handle safety checks
                if hasattr(computer_call, 'pending_safety_checks') and computer_call.pending_safety_checks:
                    response = self.safety_handler.handle_safety_checks(
                        computer_call, response, self.action_handler, azure_client
                    )
                    if response is None:
                        break
                else:
                    # Normal action execution
                    response = self._execute_normal_action(computer_call, response, iteration_count)
                    if response is None:
                        break
                
                print(f"Response {iteration_count + 1}: {response.output}")
                iteration_count += 1
                
            except Exception as e:
                print(f"Error in computer use loop iteration {iteration_count + 1}: {e}")
                break
        
        print(f"Computer use loop completed after {iteration_count} iterations")
        return response
    
    def _extract_agent_message(self, response) -> str:
        """Extract agent message from response."""
        agent_message = ""
        for item in response.output:
            if hasattr(item, 'content') and item.content:
                for content_item in item.content:
                    if hasattr(content_item, 'text'):
                        agent_message += content_item.text + " "
            elif hasattr(item, 'text'):
                agent_message += item.text + " "
        
        return agent_message.strip()
    
    def _handle_user_interaction(self, response, agent_message):
        """Handle user interaction when agent requests input."""
        self.user_interaction.print_agent_message(agent_message)
        user_response = self.user_interaction.get_user_response()
        
        if SystemInstructions.is_quit_command(user_response):
            print(SystemInstructions.USER_INTERACTION_MESSAGES['user_stop_request'])
            return None
        
        if user_response:
            print(SystemInstructions.USER_INTERACTION_MESSAGES['sending_response'].format(
                response=user_response
            ))
            
            def create_user_response():
                return azure_client.create_followup_response(
                    response.id,
                    [{"role": "user", "content": user_response}]
                )
            
            return safe_api_call(create_user_response)
        
        return response
    
    def _execute_normal_action(self, computer_call, response, iteration_count):
        """Execute a normal action without safety checks."""
        action = computer_call.action
        call_id = computer_call.call_id
        
        print(f"Iteration {iteration_count + 1}: {action}")
        
        # Execute the action
        self.action_handler.execute_action(action)
        self.browser_manager.wait(1)
        
        # Take screenshot and create response
        screenshot_bytes = self.browser_manager.take_screenshot()
        screenshot_base64 = encode_screenshot(screenshot_bytes)
        
        def make_api_call():
            return azure_client.create_followup_response(
                response.id,
                [{
                    "call_id": call_id,
                    "type": "computer_call_output",
                    "output": {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{screenshot_base64}"
                    }
                }]
            )
        
        return safe_api_call(make_api_call)
