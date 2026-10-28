import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon

from app.database.database_manager import DatabaseManager
from app.ai.conversation_manager import ConversationManager
from app.ui.chat_page import ChatPage
from app.ui.settings_page import SettingsPage
from app.ui.automation_page import AutomationPage
from app.ui.files_page import FilesPage
from app.ui.voice_page import VoicePage
from app.ui.system_page import SystemPage

class SidebarButton(QPushButton):
    def __init__(self, text, icon_path=None):
        super().__init__(text)
        self.setCheckable(True)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.setFont(font)
        
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 20px;
                border: none;
                border-radius: 8px;
                color: #B0B3B8;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #3A3B3C;
                color: #FFFFFF;
            }
            QPushButton:checked {
                background-color: #2D88FF;
                color: #FFFFFF;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Personal Desktop Assistant")
        self.setMinimumSize(1000, 700)
        
        self.db = DatabaseManager()
        self.cm = ConversationManager(self.db)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #18191A; }
            QWidget { color: #E4E6EB; font-family: 'Segoe UI', Arial, sans-serif; }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("QFrame { background-color: #242526; border-right: 1px solid #3A3B3C; }")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 30, 15, 30)
        sidebar_layout.setSpacing(10)
        
        title_label = QLabel("AI Assistant")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #FFFFFF; padding-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title_label)
        
        self.btn_chat = SidebarButton("Chat")
        self.btn_voice = SidebarButton("Voice Assistant")
        self.btn_automation = SidebarButton("Desktop Automation")
        self.btn_files = SidebarButton("File Assistant")
        self.btn_system = SidebarButton("System Monitor")
        self.btn_settings = SidebarButton("Settings")
        
        self.nav_buttons = [
            self.btn_chat, self.btn_voice, self.btn_automation, 
            self.btn_files, self.btn_system, self.btn_settings
        ]
        
        for i, btn in enumerate(self.nav_buttons):
            sidebar_layout.addWidget(btn)
            btn.clicked.connect(lambda checked, idx=i: self.switch_page(idx))
            
        sidebar_layout.addStretch()
        
        # Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("QStackedWidget { background-color: #18191A; }")
        
        self.page_chat = ChatPage(self.cm)
        self.page_voice = VoicePage(self.db, self.cm)
        self.page_automation = AutomationPage(self.db)
        self.page_files = FilesPage(self.cm)
        self.page_system = SystemPage()
        self.page_settings = SettingsPage(self.db)
        
        self.stacked_widget.addWidget(self.page_chat)
        self.stacked_widget.addWidget(self.page_voice)
        self.stacked_widget.addWidget(self.page_automation)
        self.stacked_widget.addWidget(self.page_files)
        self.stacked_widget.addWidget(self.page_system)
        self.stacked_widget.addWidget(self.page_settings)
        
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)
        
        self.btn_chat.setChecked(True)
        self.switch_page(0)

    def switch_page(self, index):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        self.stacked_widget.setCurrentIndex(index)
