"""
Screenshot utilities for encoding and processing screenshots.
"""

import base64
from PIL import Image
from io import BytesIO

def encode_screenshot(screenshot_bytes: bytes) -> str:
    """
    Encode screenshot bytes to base64 string.
    
    Args:
        screenshot_bytes: Raw screenshot bytes
        
    Returns:
        Base64 encoded screenshot string
    """
    return base64.b64encode(screenshot_bytes).decode("utf-8")

def decode_screenshot(screenshot_base64: str) -> bytes:
    """
    Decode base64 screenshot string to bytes.
    
    Args:
        screenshot_base64: Base64 encoded screenshot string
        
    Returns:
        Raw screenshot bytes
    """
    return base64.b64decode(screenshot_base64)

def save_screenshot(screenshot_bytes: bytes, filepath: str):
    """
    Save screenshot bytes to file.
    
    Args:
        screenshot_bytes: Raw screenshot bytes
        filepath: Path to save the screenshot
    """
    image = Image.open(BytesIO(screenshot_bytes))
    image.save(filepath)

def get_screenshot_info(screenshot_bytes: bytes) -> dict:
    """
    Get information about the screenshot.
    
    Args:
        screenshot_bytes: Raw screenshot bytes
        
    Returns:
        Dictionary with screenshot information
    """
    image = Image.open(BytesIO(screenshot_bytes))
    return {
        "size": image.size,
        "mode": image.mode,
        "format": image.format,
        "width": image.width,
        "height": image.height
    }

def resize_screenshot(screenshot_bytes: bytes, max_width: int = None, max_height: int = None) -> bytes:
    """
    Resize screenshot while maintaining aspect ratio.
    
    Args:
        screenshot_bytes: Raw screenshot bytes
        max_width: Maximum width (optional)
        max_height: Maximum height (optional)
        
    Returns:
        Resized screenshot bytes
    """
    image = Image.open(BytesIO(screenshot_bytes))
    
    if max_width or max_height:
        # Calculate new size maintaining aspect ratio
        original_width, original_height = image.size
        
        if max_width and max_height:
            ratio = min(max_width / original_width, max_height / original_height)
        elif max_width:
            ratio = max_width / original_width
        else:
            ratio = max_height / original_height
        
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Convert back to bytes
    output = BytesIO()
    image.save(output, format='PNG')
    return output.getvalue()
