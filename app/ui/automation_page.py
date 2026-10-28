from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QGroupBox, QLineEdit, QFormLayout
)
from PySide6.QtCore import Qt
from app.database.database_manager import DatabaseManager
from app.automation.action_executor import ActionExecutor

class AutomationPage(QWidget):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.executor = ActionExecutor(self.db)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("Desktop Automation")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Quick Actions
        quick_actions_group = QGroupBox("Quick Actions")
        quick_actions_group.setStyleSheet("color: white; font-size: 14px;")
        qa_layout = QHBoxLayout(quick_actions_group)
        
        btn_screenshot = QPushButton("Take Screenshot")
        btn_screenshot.clicked.connect(lambda: self.log_action(self.executor.execute({
            "action": "desktop_automation", "parameters": {"target": "screenshot"}
        })))
        
        btn_calc = QPushButton("Open Calculator")
        btn_calc.clicked.connect(lambda: self.log_action(self.executor.execute({
            "action": "application_launch", "parameters": {"target": "calculator"}
        })))
        
        for btn in [btn_screenshot, btn_calc]:
            btn.setStyleSheet("""
                QPushButton { background-color: #3A3B3C; color: white; padding: 10px; border-radius: 5px; }
                QPushButton:hover { background-color: #4A4B4C; }
            """)
            qa_layout.addWidget(btn)
            
        layout.addWidget(quick_actions_group)

        # Custom App Registry
        app_group = QGroupBox("Custom Application Registry")
        app_group.setStyleSheet("color: white; font-size: 14px;")
        app_layout = QVBoxLayout(app_group)
        
        form_layout = QFormLayout()
        self.app_name_input = QLineEdit()
        self.app_path_input = QLineEdit()
        
        for widget in [self.app_name_input, self.app_path_input]:
            widget.setStyleSheet("background-color: #3A3B3C; color: white; padding: 5px;")
            
        form_layout.addRow("App Name:", self.app_name_input)
        form_layout.addRow("Executable Path:", self.app_path_input)
        
        add_app_btn = QPushButton("Add Custom App")
        add_app_btn.setStyleSheet("background-color: #2D88FF; color: white; padding: 5px; border-radius: 5px;")
        add_app_btn.clicked.connect(self.add_custom_app)
        
        app_layout.addLayout(form_layout)
        app_layout.addWidget(add_app_btn, alignment=Qt.AlignRight)
        layout.addWidget(app_group)

        # Execution History Log
        history_group = QGroupBox("Execution Log")
        history_group.setStyleSheet("color: white; font-size: 14px;")
        history_layout = QVBoxLayout(history_group)
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("background-color: #242526; color: #E4E6EB; border: 1px solid #3A3B3C;")
        history_layout.addWidget(self.history_list)
        
        layout.addWidget(history_group)

    def log_action(self, result: str):
        self.history_list.insertItem(0, result)

    def add_custom_app(self):
        name = self.app_name_input.text().strip()
        path = self.app_path_input.text().strip()
        if name and path:
            self.db.add_custom_app(name, path)
            self.log_action(f"Added custom app '{name}' mapped to '{path}'")
            self.app_name_input.clear()
            self.app_path_input.clear()
