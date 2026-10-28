import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QListWidget, QGroupBox, QTextEdit, QFileDialog,
    QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from app.files.file_search import FileSearch
from app.files.document_reader import DocumentReader
from app.files.document_summarizer import DocumentSummarizer
from app.ai.conversation_manager import ConversationManager

class SummarizeWorker(QThread):
    finished = Signal(str)
    
    def __init__(self, summarizer, filepath):
        super().__init__()
        self.summarizer = summarizer
        self.filepath = filepath
        
    def run(self):
        summary = self.summarizer.summarize(self.filepath)
        self.finished.emit(summary)

class FilesPage(QWidget):
    def __init__(self, cm: ConversationManager):
        super().__init__()
        self.summarizer = DocumentSummarizer(cm)
        self.current_directory = os.path.expanduser("~")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("File Assistant")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Search Controls
        search_layout = QHBoxLayout()
        
        self.dir_input = QLineEdit()
        self.dir_input.setText(self.current_directory)
        self.dir_input.setStyleSheet("background-color: #3A3B3C; color: white; padding: 5px;")
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setStyleSheet("background-color: #3A3B3C; color: white; padding: 5px;")
        browse_btn.clicked.connect(self.browse_directory)
        
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Search keyword...")
        self.keyword_input.setStyleSheet("background-color: #3A3B3C; color: white; padding: 5px;")
        
        self.ext_input = QLineEdit()
        self.ext_input.setPlaceholderText("Ext (e.g., .txt)")
        self.ext_input.setFixedWidth(100)
        self.ext_input.setStyleSheet("background-color: #3A3B3C; color: white; padding: 5px;")
        
        search_btn = QPushButton("Search")
        search_btn.setStyleSheet("background-color: #2D88FF; color: white; padding: 5px 15px; font-weight:bold;")
        search_btn.clicked.connect(self.perform_search)
        
        search_layout.addWidget(QLabel("Dir:"))
        search_layout.addWidget(self.dir_input)
        search_layout.addWidget(browse_btn)
        search_layout.addWidget(self.keyword_input)
        search_layout.addWidget(self.ext_input)
        search_layout.addWidget(search_btn)
        
        layout.addLayout(search_layout)

        # Main Area (List and Detail View)
        main_hlayout = QHBoxLayout()
        
        # Results List
        list_group = QGroupBox("Search Results")
        list_group.setStyleSheet("color: white;")
        list_layout = QVBoxLayout(list_group)
        self.result_list = QListWidget()
        self.result_list.setStyleSheet("background-color: #242526; color: white; border: 1px solid #3A3B3C;")
        self.result_list.itemClicked.connect(self.load_file_details)
        list_layout.addWidget(self.result_list)
        main_hlayout.addWidget(list_group, 1)

        # File Details
        detail_group = QGroupBox("File Actions & Preview")
        detail_group.setStyleSheet("color: white;")
        detail_layout = QVBoxLayout(detail_group)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setStyleSheet("background-color: #242526; color: white; border: 1px solid #3A3B3C;")
        detail_layout.addWidget(self.preview_text)
        
        btn_layout = QHBoxLayout()
        self.read_btn = QPushButton("Read File")
        self.read_btn.clicked.connect(self.read_current_file)
        self.read_btn.setEnabled(False)
        
        self.summarize_btn = QPushButton("AI Summarize")
        self.summarize_btn.clicked.connect(self.summarize_current_file)
        self.summarize_btn.setEnabled(False)
        
        for btn in [self.read_btn, self.summarize_btn]:
            btn.setStyleSheet("""
                QPushButton { background-color: #2D88FF; color: white; padding: 8px; border-radius: 4px; }
                QPushButton:disabled { background-color: #555; color: #888; }
            """)
            btn_layout.addWidget(btn)
            
        detail_layout.addLayout(btn_layout)
        main_hlayout.addWidget(detail_group, 2)
        
        layout.addLayout(main_hlayout)
        
        self.current_selected_file = None

    def browse_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", self.dir_input.text())
        if dir_path:
            self.dir_input.setText(dir_path)

    def perform_search(self):
        directory = self.dir_input.text()
        keyword = self.keyword_input.text()
        ext = self.ext_input.text()
        
        self.result_list.clear()
        results = FileSearch.search_files(directory, keyword, ext)
        
        if not results:
            self.result_list.addItem("No files found.")
            return
            
        for r in results:
            self.result_list.addItem(r)

    def load_file_details(self, item):
        path = item.text()
        if path == "No files found.":
            return
            
        self.current_selected_file = path
        self.preview_text.setText(f"Selected: {os.path.basename(path)}\nPath: {path}\n\nClick 'Read File' to load content.")
        
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.txt', '.md', '.log', '.pdf', '.docx']:
            self.read_btn.setEnabled(True)
            self.summarize_btn.setEnabled(True)
        else:
            self.read_btn.setEnabled(False)
            self.summarize_btn.setEnabled(False)

    def read_current_file(self):
        if self.current_selected_file:
            content = DocumentReader.read_text(self.current_selected_file)
            self.preview_text.setText(content)

    def summarize_current_file(self):
        if self.current_selected_file:
            self.preview_text.setText("Requesting AI summary, please wait...")
            self.summarize_btn.setEnabled(False)
            
            self.worker = SummarizeWorker(self.summarizer, self.current_selected_file)
            self.worker.finished.connect(self.handle_summary_result)
            self.worker.start()

    def handle_summary_result(self, summary):
        self.preview_text.setText(f"--- AI Summary ---\n\n{summary}")
        self.summarize_btn.setEnabled(True)
