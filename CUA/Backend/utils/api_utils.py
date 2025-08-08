"""
API utilities and retry logic for robust API calls.
"""

import time
from config.settings import settings

def safe_api_call(func, max_retries=None, base_delay=None):
    """
    Safely call OpenAI API with exponential backoff retry logic.
    
    Args:
        func: Function to call
        max_retries: Maximum number of retries (default from settings)
        base_delay: Base delay in seconds (default from settings)
        
    Returns:
        Result of function call or None if all retries failed
    """
    max_retries = max_retries or settings.MAX_RETRIES
    base_delay = base_delay or settings.BASE_RETRY_DELAY
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            error_str = str(e)
            print(f"API call failed (attempt {attempt + 1}/{max_retries}): {error_str}")
            
            if attempt == max_retries - 1:
                print("Max retries reached. Raising exception.")
                raise e
            
            delay = _calculate_delay(error_str, base_delay, attempt)
            print(f"Waiting {delay} seconds before retry...")
            time.sleep(delay)
    
    return None

def _calculate_delay(error_str: str, base_delay: int, attempt: int) -> int:
    """
    Calculate delay based on error type and attempt number.
    
    Args:
        error_str: Error message string
        base_delay: Base delay in seconds
        attempt: Current attempt number
        
    Returns:
        Delay in seconds
    """
    if "503" in error_str or "InternalServerError" in error_str:
        # Server overload - exponential backoff
        return base_delay * (2 ** attempt)
    elif "429" in error_str or "rate" in error_str.lower():
        # Rate limit - longer exponential backoff
        return base_delay * (3 ** attempt)
    else:
        # Other errors - constant delay
        return base_delay

def is_rate_limit_error(error_str: str) -> bool:
    """Check if error is a rate limit error."""
    return "429" in error_str or "rate" in error_str.lower()

def is_server_error(error_str: str) -> bool:
    """Check if error is a server error."""
    return "503" in error_str or "InternalServerError" in error_str
