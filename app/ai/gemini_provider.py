import google.generativeai as genai
from app.ai.ai_provider import AIProvider

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Gemini API key is required.")
        genai.configure(api_key=api_key)
        # Using a reliable conversational model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = self.model.start_chat(history=[])

    def generate_response(self, prompt: str, context: list = None) -> str:
        """
        Sends message to Gemini and returns the text response.
        Relies on the chat object to maintain history.
        """
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {str(e)}"

    def generate_stateless_response(self, prompt: str) -> str:
        """
        Sends message to Gemini using the model directly, not the chat object.
        Does not pollute the chat history.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini (stateless): {str(e)}"
