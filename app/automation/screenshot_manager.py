import pyautogui
import os
from datetime import datetime

class ScreenshotManager:
    @staticmethod
    def take_screenshot(save_dir: str = None) -> str:
        try:
            if not save_dir:
                # Default to user's Pictures folder
                save_dir = os.path.join(os.path.expanduser("~"), "Pictures", "AI Assistant Screenshots")
            
            os.makedirs(save_dir, exist_ok=True)
            
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(save_dir, filename)
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            return f"Screenshot saved to {filepath}"
        except Exception as e:
            return f"Failed to take screenshot: {e}"
