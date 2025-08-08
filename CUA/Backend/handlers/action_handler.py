"""
Action handler for executing browser actions.
"""

import time

class ActionHandler:
    """Handles execution of different types of browser actions."""
    
    def __init__(self, browser_manager):
        """Initialize the action handler with browser manager."""
        self.browser_manager = browser_manager
    
    def execute_action(self, action):
        """Execute a browser action based on its type."""
        action_type = action.type
        page = self.browser_manager.get_current_page()
        
        try:
            match action_type:
                case "click":
                    self._handle_click(page, action)
                case "scroll":
                    self._handle_scroll(page, action)
                case "keypress":
                    self._handle_keypress(page, action)
                case "type":
                    self._handle_type(page, action)
                case "wait":
                    self._handle_wait()
                case "screenshot":
                    self._handle_screenshot()
                case _:
                    print(f"Unrecognized action: {action}")
        
        except Exception as e:
            print(f"Error handling action {action}: {e}")
    
    def _handle_click(self, page, action):
        """Handle click actions."""
        x, y = action.x, action.y
        button = action.button
        print(f"Clicking at ({x}, {y}) with button {button}")
        page.mouse.click(x, y, button=button)
    
    def _handle_scroll(self, page, action):
        """Handle scroll actions."""
        x, y = action.x, action.y
        scroll_x, scroll_y = action.scroll_x, action.scroll_y
        print(f"Scrolling at ({x}, {y}) with offsets (scroll_x={scroll_x}, scroll_y={scroll_y})")
        page.mouse.move(x, y)
        page.evaluate(f"window.scrollBy({scroll_x}, {scroll_y})")
    
    def _handle_keypress(self, page, action):
        """Handle keypress actions."""
        keys = action.keys
        for k in keys:
            print(f"Keypress: '{k}'")
            if k.lower() == "enter":
                page.keyboard.press("Enter")
            elif k.lower() == "space":
                page.keyboard.press(" ")
            else:
                page.keyboard.press(k)
    
    def _handle_type(self, page, action):
        """Handle typing actions."""
        text = action.text
        print(f"Typing: {text}")
        page.keyboard.type(text)
    
    def _handle_wait(self):
        """Handle wait actions."""
        print("Waiting...")
        time.sleep(2)
    
    def _handle_screenshot(self):
        """Handle screenshot actions."""
        print("Taking screenshot...")
        # Screenshot is automatically handled after action execution
