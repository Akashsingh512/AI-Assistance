import sys
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # If run in test mode, close immediately
    if "--test" in sys.argv:
        print("Test mode: UI initialized successfully.")
        sys.exit(0)
        
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
