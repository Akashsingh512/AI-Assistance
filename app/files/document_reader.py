import os
import PyPDF2
from docx import Document as DocxDocument

class DocumentReader:
    @staticmethod
    def read_text(file_path: str) -> str:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
            
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == ".txt" or ext == ".md" or ext == ".log":
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read()
            elif ext == ".pdf":
                return DocumentReader._read_pdf(file_path)
            elif ext == ".docx":
                return DocumentReader._read_docx(file_path)
            else:
                return f"Error: Unsupported file format '{ext}'."
        except Exception as e:
            return f"Error reading file '{file_path}': {e}"

    @staticmethod
    def _read_pdf(file_path: str) -> str:
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text

    @staticmethod
    def _read_docx(file_path: str) -> str:
        doc = DocxDocument(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
