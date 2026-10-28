import json
from app.ai.conversation_manager import ConversationManager

class TaskRouter:
    def __init__(self, conversation_manager: ConversationManager):
        self.cm = conversation_manager

    def route_task(self, user_input: str) -> dict:
        """
        Uses the AI provider to classify the intent of the user input.
        Returns a dictionary with 'action' and 'parameters'.
        """
        system_prompt = """
        You are a task router for a desktop assistant.
        Classify the user's input into one of the following action categories:
        - general_ai_question (for chat, coding, general questions)
        - application_launch (e.g., "Open Chrome", "Launch Notepad")
        - website_open (e.g., "Open YouTube", "Go to google.com")
        - file_search (e.g., "Find my report", "Search for invoices")
        - document_summarization (e.g., "Summarize this PDF")
        - desktop_automation (e.g., "Take a screenshot", "Copy to clipboard")
        - system_information (e.g., "How much RAM is free?", "CPU usage")
        - unsupported_action (if none match)

        Respond ONLY with a valid JSON object in the following format:
        {
            "action": "category_name",
            "parameters": {
                "target": "target_app_or_website_or_topic",
                "extra": "any_other_relevant_info"
            }
        }
        """

        prompt = f"{system_prompt}\n\nUser Input: '{user_input}'"
        
        try:
            # Use stateless response to avoid poisoning chat history
            response_text = self.cm.send_stateless_message(prompt).strip()
            # Clean up the response if it has markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            elif response_text.startswith("```"):
                response_text = response_text[3:]
                
            if response_text.endswith("```"):
                response_text = response_text[:-3]
                
            return json.loads(response_text.strip())
        except Exception as e:
            print(f"Routing failed: {e}")
            return {"action": "general_ai_question", "parameters": {"target": user_input}}
