from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QLineEdit, QPushButton, QLabel, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QTextCursor
from app.ai.conversation_manager import ConversationManager

class AIWorker(QThread):
    finished = Signal(str)
    
    def __init__(self, conversation_manager, message):
        super().__init__()
        self.conversation_manager = conversation_manager
        self.message = message
        
    def run(self):
        response = self.conversation_manager.send_message(self.message)
        self.finished.emit(response)

class ChatMessage(QFrame):
    def __init__(self, text, is_user=True):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        
        if is_user:
            self.setStyleSheet("""
                QFrame {
                    background-color: #2D88FF;
                    color: white;
                    border-radius: 10px;
                    margin-left: 50px;
                }
            """)
            layout.addWidget(self.label, alignment=Qt.AlignRight)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #3A3B3C;
                    color: #E4E6EB;
                    border-radius: 10px;
                    margin-right: 50px;
                }
            """)
            layout.addWidget(self.label, alignment=Qt.AlignLeft)

class ChatPage(QWidget):
    def __init__(self, conversation_manager: ConversationManager):
        super().__init__()
        self.cm = conversation_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Status Label
        self.status_label = QLabel("Assistant Ready")
        self.status_label.setStyleSheet("color: #B0B3B8; font-style: italic;")
        layout.addWidget(self.status_label)

        # Chat History Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)
        
        layout.addWidget(self.scroll_area)

        # Input Area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask me anything...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #3A3B3C;
                color: white;
                padding: 12px;
                border-radius: 20px;
                font-size: 14px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D88FF;
                color: white;
                padding: 12px 20px;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a74e5;
            }
        """)
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #3A3B3C;
                color: white;
                padding: 12px 20px;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A4B4C;
            }
        """)
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_chat)
        input_layout.addWidget(self.clear_btn)

        layout.addLayout(input_layout)

    def send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self.input_field.clear()
        self.add_message_ui(text, is_user=True)
        self.status_label.setText("Processing...")
        self.input_field.setEnabled(False)
        self.send_btn.setEnabled(False)

        self.worker = AIWorker(self.cm, text)
        self.worker.finished.connect(self.handle_response)
        self.worker.start()

    def handle_response(self, response):
        self.add_message_ui(response, is_user=False)
        self.status_label.setText("Assistant Ready")
        self.input_field.setEnabled(True)
        self.send_btn.setEnabled(True)
        self.input_field.setFocus()

    def add_message_ui(self, text, is_user):
        msg_widget = ChatMessage(text, is_user)
        self.scroll_layout.addWidget(msg_widget)
        
        # Scroll to bottom
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def clear_chat(self):
        for i in reversed(range(self.scroll_layout.count())): 
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None: 
                widget.setParent(None)
        
        # Re-initialize conversation manager provider to clear history
        self.cm._initialize_provider()
        self.status_label.setText("Assistant Ready (Chat Cleared)")
