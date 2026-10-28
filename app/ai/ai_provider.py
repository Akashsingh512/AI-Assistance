from abc import ABC, abstractmethod

class AIProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, context: list = None) -> str:
        """Generates a text response and appends to the conversation history."""
        pass

    @abstractmethod
    def generate_stateless_response(self, prompt: str) -> str:
        """Generates a text response without affecting conversation history."""
        pass
