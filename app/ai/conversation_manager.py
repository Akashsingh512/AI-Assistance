from app.ai.ai_provider import AIProvider
from app.ai.gemini_provider import GeminiProvider
from app.ai.openai_provider import OpenAIProvider
from app.database.database_manager import DatabaseManager

class ConversationManager:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.provider: AIProvider = None
        self._initialize_provider()

    def _initialize_provider(self):
        provider_name = self.db.get_setting("ai_provider", "Gemini")
        try:
            if provider_name == "Gemini":
                api_key = self.db.get_api_key("gemini")
                if api_key:
                    self.provider = GeminiProvider(api_key)
            elif provider_name == "OpenAI":
                api_key = self.db.get_api_key("openai")
                if api_key:
                    self.provider = OpenAIProvider(api_key)
        except Exception as e:
            print(f"Failed to initialize AI Provider: {e}")
            self.provider = None

    def send_message(self, message: str) -> str:
        if not self.provider:
            self._initialize_provider()
            
        if not self.provider:
            return "Error: AI Provider not configured properly. Please check your API keys in Settings."
            
        return self.provider.generate_response(message)

    def send_stateless_message(self, message: str) -> str:
        if not self.provider:
            self._initialize_provider()
            
        if not self.provider:
            return "Error: AI Provider not configured properly. Please check your API keys in Settings."
            
        return self.provider.generate_stateless_response(message)
