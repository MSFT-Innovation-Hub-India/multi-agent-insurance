"""
User interaction utilities for input/output operations.
"""

from config.system_instructions import SystemInstructions

class UserInteraction:
    """Handles user input and output interactions."""
    
    @staticmethod
    def print_header(header_text: str, width: int = 50):
        """Print a formatted header."""
        print("="*width)
        print(header_text)
        print("="*width)
    
    @staticmethod
    def print_agent_message(message: str):
        """Print an agent message with formatting."""
        UserInteraction.print_header(
            SystemInstructions.USER_INTERACTION_MESSAGES['agent_prompt'],
            60
        )
        print(message)
        print("="*60)
        print(SystemInstructions.USER_INTERACTION_MESSAGES['tip'])
        print("-" * 60)
    
    @staticmethod
    def get_user_response() -> str:
        """Get user response with proper prompt."""
        return input(
            SystemInstructions.USER_INTERACTION_MESSAGES['user_response_prompt']
        ).strip()
    
    @staticmethod
    def get_customer_id() -> str:
        """Get customer ID from user."""
        return input(
            SystemInstructions.USER_INTERACTION_MESSAGES['customer_id_prompt']
        ).strip()
    
    @staticmethod
    def get_username() -> str:
        """Get username from user."""
        return input(
            SystemInstructions.USER_INTERACTION_MESSAGES['username_prompt']
        ).strip()
    
    @staticmethod
    def get_password() -> str:
        """Get password from user."""
        return input(
            SystemInstructions.USER_INTERACTION_MESSAGES['password_prompt']
        ).strip()
    
    @staticmethod
    def confirm_action(prompt: str) -> bool:
        """Get user confirmation for an action."""
        response = input(f"{prompt} (yes/no): ").strip().lower()
        return response in ['yes', 'y']
    
    @staticmethod
    def print_error(error_message: str):
        """Print an error message with formatting."""
        print(f"❌ ERROR: {error_message}")
    
    @staticmethod
    def print_success(success_message: str):
        """Print a success message with formatting."""
        print(f"✅ SUCCESS: {success_message}")
    
    @staticmethod
    def print_warning(warning_message: str):
        """Print a warning message with formatting."""
        print(f"⚠️  WARNING: {warning_message}")
    
    @staticmethod
    def print_info(info_message: str):
        """Print an info message with formatting."""
        print(f"ℹ️  INFO: {info_message}")
    
    @staticmethod
    def validate_input(value: str, field_name: str) -> bool:
        """Validate that input is not empty."""
        if not value:
            UserInteraction.print_error(f"No {field_name} provided.")
            return False
        return True
    
    @staticmethod
    def get_validated_input(prompt: str, field_name: str) -> str:
        """Get validated input that cannot be empty."""
        while True:
            value = input(prompt).strip()
            if UserInteraction.validate_input(value, field_name):
                return value
            print(f"Please provide a valid {field_name}.")

def get_user_credentials():
    """Get all user credentials with validation."""
    # Return default values without any user interaction
    return "default", "demo", "123"
