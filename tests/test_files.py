import os
import pytest
from app.files.file_search import FileSearch
from app.files.document_reader import DocumentReader

@pytest.fixture
def temp_workspace(tmp_path):
    d = tmp_path / "workspace"
    d.mkdir()
    
    file1 = d / "test1.txt"
    file1.write_text("Hello, this is a text file.")
    
    file2 = d / "report.md"
    file2.write_text("Markdown report content.")
    
    return d

def test_file_search(temp_workspace):
    results = FileSearch.search_files(str(temp_workspace), keyword="test", extension=".txt")
    assert len(results) == 1
    assert "test1.txt" in results[0]
    
def test_document_reader_txt(temp_workspace):
    target = os.path.join(str(temp_workspace), "test1.txt")
    content = DocumentReader.read_text(target)
    assert "Hello" in content
    
def test_document_reader_unsupported(temp_workspace):
    target = os.path.join(str(temp_workspace), "fake.xyz")
    # create fake file
    with open(target, "w") as f:
        f.write("data")
        
    content = DocumentReader.read_text(target)
    assert "Error: Unsupported file format" in content
