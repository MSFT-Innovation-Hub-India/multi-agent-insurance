"""
Configuration settings for the browser automation system.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application configuration settings."""
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "Fl4K9mHabFAqqaeEgbpziq4pSK98eXiQm6PMs3r2hKA8YWMcV4WJJQQJ99BDACHYHv6XJ3w3AAAAACOGFNlv")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://ai-ronakofficial14141992ai537166517119.openai.azure.com")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")
    AZURE_OPENAI_MODEL = "computer-use-preview"
    
    # Browser Configuration
    BROWSER_WIDTH = int(os.getenv("BROWSER_WIDTH", "1024"))
    BROWSER_HEIGHT = int(os.getenv("BROWSER_HEIGHT", "768"))
    BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
    
    # Computer Use Tool Configuration
    COMPUTER_USE_TOOLS = [{
        "type": "computer_use_preview",
        "display_width": BROWSER_WIDTH,
        "display_height": BROWSER_HEIGHT,
        "environment": "browser",
    }]
    
    # Application Settings
    MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "50"))
    DEFAULT_WAIT_TIME = int(os.getenv("DEFAULT_WAIT_TIME", "2"))
    BASE_RETRY_DELAY = int(os.getenv("BASE_RETRY_DELAY", "2"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))
    
    # CRM System
    DEFAULT_CRM_URL = os.getenv("DEFAULT_CRM_URL", "http://localhost:8000/login.html")
    
    # Browser Launch Args
    BROWSER_ARGS = [
        "--disable-extensions", 
        "--disable-file-system"
    ]
    
    @classmethod
    def validate_settings(cls):
        """Validate that required settings are present."""
        required_settings = [
            'AZURE_OPENAI_API_KEY',
            'AZURE_OPENAI_ENDPOINT'
        ]
        
        missing_settings = []
        for setting in required_settings:
            if not getattr(cls, setting):
                missing_settings.append(setting)
        
        if missing_settings:
            raise ValueError(f"Missing required settings: {', '.join(missing_settings)}")
        
        return True

# Create a global settings instance
settings = Settings()
