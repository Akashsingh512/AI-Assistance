import pytest
from app.automation.clipboard_manager import ClipboardManager

def test_clipboard_manager():
    text_to_copy = "TestClipboard123"
    result = ClipboardManager.copy_text(text_to_copy)
    assert "Successfully" in result
    
    pasted_text = ClipboardManager.get_text()
    assert pasted_text == text_to_copy
