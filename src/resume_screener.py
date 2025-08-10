from docx import Document

def read_resume(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

if __name__ == "_main_":
    sample_resume = 'sample_resumes/sample1.docx'  # adjust path if needed
    text = read_resume(sample_resume)
    if text:
        print("Resume Text:\n")
        print(text)
    else:
        print("No text extracted.")