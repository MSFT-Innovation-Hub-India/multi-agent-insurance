
# Browser Automation System - Modular Version
# This script uses a modular architecture with separated concerns

from core.automation_engine import AutomationEngine
from utils.user_interaction import UserInteraction
from config.settings import settings

def main():
    """Main function to run the automation system using modular structure."""
    try:
        # Validate settings
        settings.validate_settings()
        
        # Print header
        UserInteraction.print_header("RISK SCORE ANALYSIS")
        
        # Use default values - no user input required
        customer_id = "default"
        username = "demo"  
        password = "123"
        
        # Create and run automation engine
        engine = AutomationEngine()
        engine.run_automation(customer_id, username, password)
        
    except KeyboardInterrupt:
        UserInteraction.print_warning("Process interrupted by user")
    except Exception as e:
        UserInteraction.print_error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
