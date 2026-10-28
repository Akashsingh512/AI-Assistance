from app.database.database_manager import DatabaseManager
from app.automation.app_launcher import AppLauncher
from app.automation.browser_manager import BrowserManager
from app.automation.clipboard_manager import ClipboardManager
from app.automation.screenshot_manager import ScreenshotManager

class ActionExecutor:
    def __init__(self, db: DatabaseManager):
        self.app_launcher = AppLauncher(db)
        
    def execute(self, action_dict: dict) -> str:
        """
        Executes a safe desktop action based on the parsed dictionary.
        action_dict format: {"action": "...", "parameters": {"target": "..."}}
        """
        action = action_dict.get("action")
        params = action_dict.get("parameters", {})
        target = params.get("target", "")

        if action == "application_launch":
            return self.app_launcher.launch_app(target)
            
        elif action == "website_open":
            return BrowserManager.open_website(target)
            
        elif action == "desktop_automation":
            if "screenshot" in target.lower():
                return ScreenshotManager.take_screenshot()
            elif "copy" in target.lower():
                extra_text = params.get("extra", "")
                if extra_text:
                    return ClipboardManager.copy_text(extra_text)
                return "No text provided to copy."
            else:
                return f"Unsupported desktop automation task: {target}"
                
        else:
            return f"Action '{action}' is not supported by the executor directly."
