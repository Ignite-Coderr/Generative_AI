import pdfplumber

def extract_resume_text(file):
    with pdfplumber.open(file.file) as pdf:
        return " ".join(page.extract_text() for page in pdf.pages)
