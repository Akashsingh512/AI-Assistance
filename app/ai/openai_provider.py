from openai import OpenAI
from app.ai.ai_provider import AIProvider

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"
        self.history = [
            {"role": "system", "content": "You are a helpful desktop AI assistant."}
        ]

    def generate_response(self, prompt: str, context: list = None) -> str:
        """
        Sends message to OpenAI and returns the text response.
        Maintains local history list.
        """
        try:
            self.history.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history
            )
            
            ai_message = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": ai_message})
            
            return ai_message
        except Exception as e:
            return f"Error communicating with OpenAI: {str(e)}"

    def generate_stateless_response(self, prompt: str) -> str:
        """
        Sends message to OpenAI without using or updating the internal history.
        """
        try:
            temp_history = [
                {"role": "system", "content": "You are a helpful desktop AI assistant."},
                {"role": "user", "content": prompt}
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=temp_history
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with OpenAI (stateless): {str(e)}"
