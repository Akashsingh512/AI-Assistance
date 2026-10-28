import sqlite3
import os
import keyring

DB_PATH = "config/app.db"
KEYRING_SERVICE_NAME = "ai_desktop_assistant"

class DatabaseManager:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_apps (
                name TEXT PRIMARY KEY,
                path TEXT
            )
        ''')
        self.conn.commit()

    def get_setting(self, key: str, default=None):
        self.cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return default

    def set_setting(self, key: str, value: str):
        self.cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, str(value)))
        self.conn.commit()

    def get_api_key(self, provider: str):
        try:
            return keyring.get_password(KEYRING_SERVICE_NAME, f"{provider}_api_key")
        except Exception:
            return None

    def set_api_key(self, provider: str, api_key: str):
        try:
            if api_key:
                keyring.set_password(KEYRING_SERVICE_NAME, f"{provider}_api_key", api_key)
            else:
                try:
                    keyring.delete_password(KEYRING_SERVICE_NAME, f"{provider}_api_key")
                except keyring.errors.PasswordDeleteError:
                    pass
        except Exception as e:
            print(f"Error saving API key to keyring: {e}")

    def add_custom_app(self, name: str, path: str):
        self.cursor.execute("INSERT OR REPLACE INTO custom_apps (name, path) VALUES (?, ?)", (name, path))
        self.conn.commit()

    def remove_custom_app(self, name: str):
        self.cursor.execute("DELETE FROM custom_apps WHERE name=?", (name,))
        self.conn.commit()

    def get_custom_apps(self):
        self.cursor.execute("SELECT name, path FROM custom_apps")
        return dict(self.cursor.fetchall())
