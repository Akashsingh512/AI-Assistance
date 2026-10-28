from app.ai.conversation_manager import ConversationManager
from app.files.document_reader import DocumentReader

class DocumentSummarizer:
    def __init__(self, cm: ConversationManager):
        self.cm = cm

    def summarize(self, file_path: str) -> str:
        content = DocumentReader.read_text(file_path)
        if content.startswith("Error"):
            return content

        if len(content.strip()) == 0:
            return "The document appears to be empty."
            
        prompt = (
            "Please provide a concise summary of the following document content. "
            "Extract the key information and present it clearly.\n\n"
            f"Document Content:\n{content[:15000]}" # Limit to roughly fit context windows
        )

        return self.cm.send_stateless_message(prompt)
