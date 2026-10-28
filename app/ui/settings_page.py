from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QFormLayout, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from app.database.database_manager import DatabaseManager

class SettingsPage(QWidget):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # AI Provider Settings
        ai_group = QGroupBox("AI Configuration")
        ai_group.setStyleSheet("color: white; font-size: 14px;")
        ai_layout = QFormLayout(ai_group)
        ai_layout.setSpacing(15)

        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["Gemini", "OpenAI"])
        self.provider_combo.setStyleSheet("background-color: #3A3B3C; color: white; padding: 5px;")
        
        current_provider = self.db.get_setting("ai_provider", "Gemini")
        self.provider_combo.setCurrentText(current_provider)
        ai_layout.addRow("Primary AI Provider:", self.provider_combo)

        self.gemini_key_input = QLineEdit()
        self.gemini_key_input.setEchoMode(QLineEdit.Password)
        self.gemini_key_input.setStyleSheet("background-color: #3A3B3C; color: white; padding: 5px;")
        gemini_key = self.db.get_api_key("gemini")
        if gemini_key:
            self.gemini_key_input.setText(gemini_key)
        ai_layout.addRow("Google Gemini API Key:", self.gemini_key_input)

        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(QLineEdit.Password)
        self.openai_key_input.setStyleSheet("background-color: #3A3B3C; color: white; padding: 5px;")
        openai_key = self.db.get_api_key("openai")
        if openai_key:
            self.openai_key_input.setText(openai_key)
        ai_layout.addRow("OpenAI API Key:", self.openai_key_input)

        layout.addWidget(ai_group)

        # General Settings
        general_group = QGroupBox("General Settings")
        general_group.setStyleSheet("color: white; font-size: 14px;")
        general_layout = QFormLayout(general_group)
        general_layout.setSpacing(15)

        self.voice_input_combo = QComboBox()
        self.voice_input_combo.addItems(["Enabled", "Disabled"])
        self.voice_input_combo.setStyleSheet("background-color: #3A3B3C; color: white; padding: 5px;")
        self.voice_input_combo.setCurrentText(self.db.get_setting("voice_input", "Enabled"))
        general_layout.addRow("Voice Input:", self.voice_input_combo)
        
        self.voice_output_combo = QComboBox()
        self.voice_output_combo.addItems(["Enabled", "Disabled"])
        self.voice_output_combo.setStyleSheet("background-color: #3A3B3C; color: white; padding: 5px;")
        self.voice_output_combo.setCurrentText(self.db.get_setting("voice_output", "Enabled"))
        general_layout.addRow("Voice Output (TTS):", self.voice_output_combo)

        layout.addWidget(general_group)

        # Save Button
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D88FF;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a74e5;
            }
        """)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn, alignment=Qt.AlignRight)

        layout.addStretch()

    def save_settings(self):
        # Save general settings
        self.db.set_setting("ai_provider", self.provider_combo.currentText())
        self.db.set_setting("voice_input", self.voice_input_combo.currentText())
        self.db.set_setting("voice_output", self.voice_output_combo.currentText())

        # Save API keys securely
        self.db.set_api_key("gemini", self.gemini_key_input.text())
        self.db.set_api_key("openai", self.openai_key_input.text())

        QMessageBox.information(self, "Success", "Settings saved successfully.")
