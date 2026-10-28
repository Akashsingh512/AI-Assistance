import os
import subprocess
from app.database.database_manager import DatabaseManager

class AppLauncher:
    def __init__(self, db: DatabaseManager):
        self.db = db
        # A basic mapping of common apps to their executable names/paths on Windows
        self.common_apps = {
            "chrome": "chrome.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "vs code": "code",
            "explorer": "explorer.exe",
            "edge": "msedge.exe",
            "task manager": "taskmgr.exe"
        }

    def launch_app(self, app_name: str) -> str:
        app_name_lower = app_name.lower()
        
        # Check custom apps in DB first
        custom_apps = self.db.get_custom_apps()
        for name, path in custom_apps.items():
            if name.lower() in app_name_lower:
                return self._execute(path, name)

        # Check predefined apps
        for key, exe_name in self.common_apps.items():
            if key in app_name_lower:
                return self._execute(exe_name, key)

        return f"Could not find application: {app_name}. Please add it in settings."

    def _execute(self, command: str, name: str) -> str:
        try:
            # os.startfile is Windows only. Using subprocess for cross-platform fallback
            if os.name == 'nt':
                os.startfile(command)
            else:
                subprocess.Popen([command])
            return f"Successfully opened {name}."
        except Exception as e:
            return f"Failed to open {name}: {str(e)}"
