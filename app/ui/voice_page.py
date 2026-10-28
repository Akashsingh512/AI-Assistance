from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit
)
from PySide6.QtCore import Qt, QThread, Signal
from app.voice.speech_to_text import SpeechToText
from app.voice.text_to_speech import TextToSpeech
from app.ai.conversation_manager import ConversationManager
from app.ai.task_router import TaskRouter
from app.automation.action_executor import ActionExecutor
from app.database.database_manager import DatabaseManager

class ListeningWorker(QThread):
    finished = Signal(str)
    
    def __init__(self, stt: SpeechToText):
        super().__init__()
        self.stt = stt
        
    def run(self):
        text = self.stt.listen()
        self.finished.emit(text)

class ProcessingWorker(QThread):
    finished = Signal(str)
    
    def __init__(self, cm: ConversationManager, router: TaskRouter, executor: ActionExecutor, text: str):
        super().__init__()
        self.cm = cm
        self.router = router
        self.executor = executor
        self.text = text
        
    def run(self):
        # 1. Route task
        route = self.router.route_task(self.text)
        action = route.get("action", "general_ai_question")
        
        # 2. Execute or Chat
        if action == "general_ai_question" or action == "unsupported_action":
            response = self.cm.send_message(self.text)
        else:
            response = self.executor.execute(route)
            
        self.finished.emit(response)

class VoicePage(QWidget):
    def __init__(self, db: DatabaseManager, cm: ConversationManager):
        super().__init__()
        self.db = db
        self.cm = cm
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.router = TaskRouter(cm)
        self.executor = ActionExecutor(db)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        title = QLabel("Voice Assistant")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.status_label = QLabel("Click the microphone to start listening")
        self.status_label.setStyleSheet("color: #B0B3B8; font-size: 16px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.mic_btn = QPushButton("🎤")
        self.mic_btn.setFixedSize(100, 100)
        self.mic_btn.setCursor(Qt.PointingHandCursor)
        self.mic_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D88FF;
                color: white;
                font-size: 40px;
                border-radius: 50px;
            }
            QPushButton:hover { background-color: #1a74e5; }
        """)
        self.mic_btn.clicked.connect(self.toggle_listening)
        layout.addWidget(self.mic_btn, alignment=Qt.AlignCenter)

        self.transcript_box = QTextEdit()
        self.transcript_box.setReadOnly(True)
        self.transcript_box.setFixedHeight(200)
        self.transcript_box.setStyleSheet("background-color: #242526; color: white; border: 1px solid #3A3B3C; padding: 10px;")
        layout.addWidget(self.transcript_box)
        
        self.is_listening = False

    def toggle_listening(self):
        voice_input_enabled = self.db.get_setting("voice_input", "Enabled")
        if voice_input_enabled != "Enabled":
            self.transcript_box.append("Error: Voice input is disabled in Settings.")
            return
            
        if not self.is_listening:
            self.start_listening()

    def start_listening(self):
        self.is_listening = True
        self.mic_btn.setStyleSheet("""
            QPushButton { background-color: #E02424; color: white; font-size: 40px; border-radius: 50px; }
        """)
        self.status_label.setText("Listening...")
        self.mic_btn.setEnabled(False)
        
        self.listen_worker = ListeningWorker(self.stt)
        self.listen_worker.finished.connect(self.on_listen_finished)
        self.listen_worker.start()

    def on_listen_finished(self, text):
        self.is_listening = False
        self.mic_btn.setStyleSheet("""
            QPushButton { background-color: #2D88FF; color: white; font-size: 40px; border-radius: 50px; }
            QPushButton:hover { background-color: #1a74e5; }
        """)
        self.mic_btn.setEnabled(True)
        
        if not text or "error" in text.lower() or "sorry" in text.lower():
            self.status_label.setText("Assistant Ready")
            self.transcript_box.append(f"User (Voice): {text}")
            return
            
        self.transcript_box.append(f"User (Voice): {text}")
        self.status_label.setText("Processing...")
        self.mic_btn.setEnabled(False)
        
        self.process_worker = ProcessingWorker(self.cm, self.router, self.executor, text)
        self.process_worker.finished.connect(self.on_process_finished)
        self.process_worker.start()

    def on_process_finished(self, response):
        self.transcript_box.append(f"Assistant: {response}\n")
        self.status_label.setText("Assistant Ready")
        self.mic_btn.setEnabled(True)
        
        voice_output_enabled = self.db.get_setting("voice_output", "Enabled")
        if voice_output_enabled == "Enabled":
            self.tts.speak(response)
