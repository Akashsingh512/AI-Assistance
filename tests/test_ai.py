import pytest
from app.ai.conversation_manager import ConversationManager
from app.database.database_manager import DatabaseManager

class MockDatabaseManager(DatabaseManager):
    def __init__(self):
        self.settings = {"ai_provider": "Mock"}
        self.keys = {}
        
    def get_setting(self, key, default=None):
        return self.settings.get(key, default)
        
    def get_api_key(self, provider):
        return self.keys.get(provider)

def test_conversation_manager_no_provider():
    db = MockDatabaseManager()
    cm = ConversationManager(db)
    response = cm.send_message("Hello")
    assert "Error" in response
    assert "not configured properly" in response
