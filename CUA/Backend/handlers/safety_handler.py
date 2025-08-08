"""
Safety handler for managing safety checks and user confirmations.
"""

from utils.screenshot_utils import encode_screenshot
from utils.api_utils import safe_api_call
from utils.user_interaction import UserInteraction
from config.system_instructions import SystemInstructions

class SafetyHandler:
    """Handles safety checks and user confirmations."""
    
    def __init__(self):
        """Initialize the safety handler."""
        self.user_interaction = UserInteraction()
    
    def handle_safety_checks(self, computer_call, response, action_handler, azure_client):
        """
        Handle safety checks with user confirmation.
        
        Args:
            computer_call: The computer call with safety checks
            response: The current response object
            action_handler: Action handler instance
            azure_client: Azure OpenAI client instance
            
        Returns:
            Updated response object or None if user declines
        """
        pending_safety_checks = computer_call.pending_safety_checks
        
        self._display_safety_warning(pending_safety_checks)
        
        if not self._get_user_acknowledgment():
            print(SystemInstructions.USER_INTERACTION_MESSAGES['user_declined'])
            return None
        
        print(SystemInstructions.USER_INTERACTION_MESSAGES['safety_acknowledged'])
        
        # Execute the action
        action_handler.execute_action(computer_call.action)
        action_handler.browser_manager.wait(1)
        
        # Get screenshot
        screenshot_bytes = action_handler.browser_manager.take_screenshot()
        screenshot_base64 = encode_screenshot(screenshot_bytes)
        
        # Create input with acknowledged safety checks
        api_input = {
            "type": "computer_call_output",
            "call_id": computer_call.call_id,
            "acknowledged_safety_checks": [
                {
                    "id": getattr(safety_check, 'id', ''),
                    "code": getattr(safety_check, 'code', ''),
                    "message": getattr(safety_check, 'message', '')
                }
                for safety_check in pending_safety_checks
            ],
            "output": {
                "type": "input_image",
                "image_url": f"data:image/png;base64,{screenshot_base64}"
            }
        }
        
        # Make API call with acknowledged safety checks
        def make_api_call_with_acknowledgment():
            return azure_client.create_followup_response(
                response.id,
                [api_input]
            )
        
        return safe_api_call(make_api_call_with_acknowledgment)
    
    def _display_safety_warning(self, pending_safety_checks):
        """Display safety warning information to the user."""
        print("\n" + "⚠️" + "="*60)
        print("SAFETY WARNING DETECTED!")
        print("="*60)
        
        for safety_check in pending_safety_checks:
            print(f"Safety Check ID: {getattr(safety_check, 'id', 'N/A')}")
            print(f"Code: {getattr(safety_check, 'code', 'N/A')}")
            print(f"Message: {getattr(safety_check, 'message', 'N/A')}")
            print("-" * 60)
    
    def _get_user_acknowledgment(self) -> bool:
        """Get user acknowledgment for safety warnings."""
        print("💡 Type 'yes' to acknowledge and proceed, or 'no' to stop")
        user_acknowledgment = input(
            SystemInstructions.USER_INTERACTION_MESSAGES['acknowledge_safety']
        ).strip().lower()
        
        return user_acknowledgment in ['yes', 'y']
