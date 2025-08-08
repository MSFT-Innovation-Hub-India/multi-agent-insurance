"""
Browser and page management for automation.
"""

import time
from playwright.sync_api import sync_playwright
from config.settings import settings

class BrowserManager:
    """Manages browser lifecycle and page operations."""
    
    def __init__(self):
        """Initialize the browser manager."""
        self.playwright = None
        self.browser = None
        self.page = None
        self._context_manager = None
    
    def __enter__(self):
        """Context manager entry."""
        self.start_browser()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_browser()
    
    def start_browser(self):
        """Start the browser with configured settings."""
        self._context_manager = sync_playwright()
        self.playwright = self._context_manager.__enter__()
        
        self.browser = self.playwright.chromium.launch(
            headless=settings.BROWSER_HEADLESS,
            chromium_sandbox=True,
            env={},
            args=settings.BROWSER_ARGS
        )
        
        self.page = self.browser.new_page()
        self.page.set_viewport_size({
            "width": settings.BROWSER_WIDTH, 
            "height": settings.BROWSER_HEIGHT
        })
    
    def close_browser(self):
        """Close the browser and cleanup resources."""
        if self.browser:
            self.browser.close()
        if self._context_manager:
            self._context_manager.__exit__(None, None, None)
    
    def navigate_to(self, url: str, wait_until: str = "domcontentloaded"):
        """Navigate to a URL."""
        if not self.page:
            raise RuntimeError("Browser page not initialized")
        
        self.page.goto(url, wait_until=wait_until)
        time.sleep(settings.DEFAULT_WAIT_TIME)
    
    def get_current_page(self):
        """Get the current active page, switching if necessary."""
        if not self.browser:
            return self.page
        
        all_pages = self.browser.contexts[0].pages
        if len(all_pages) > 1 and all_pages[-1] != self.page:
            self.page = all_pages[-1]
            print("Switched to new page/tab")
        
        return self.page
    
    def take_screenshot(self) -> bytes:
        """Take a screenshot of the current page."""
        if not self.page:
            raise RuntimeError("Browser page not initialized")
        
        return self.page.screenshot()
    
    def wait(self, seconds: int = None):
        """Wait for a specified number of seconds."""
        wait_time = seconds if seconds is not None else settings.DEFAULT_WAIT_TIME
        time.sleep(wait_time)
