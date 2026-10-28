import pyperclip

class ClipboardManager:
    @staticmethod
    def copy_text(text: str) -> str:
        try:
            pyperclip.copy(text)
            return "Successfully copied text to clipboard."
        except Exception as e:
            return f"Failed to copy to clipboard: {e}"

    @staticmethod
    def get_text() -> str:
        try:
            return pyperclip.paste()
        except Exception as e:
            return f"Failed to read from clipboard: {e}"
