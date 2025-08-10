import os
from docx import Document

file_path = '../sample_resumes/sample1.docx'

print("Current working directory:", os.getcwd())

if os.path.exists(file_path):
    print(f"File found at '{file_path}'. Trying to open...")
    doc = Document(file_path)
    print(f"Document has {len(doc.paragraphs)} paragraphs.")
else:
    print(f"File not found at '{file_path}'. Please check path.")