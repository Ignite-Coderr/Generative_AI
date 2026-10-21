from app.indexer import index_pdf
import os

if __name__ == "__main__":
    pdf_path = os.path.join("data", "nodejs.pdf")
    if os.path.exists(pdf_path):
        print(f"Indexing {pdf_path}...")
        index_pdf(pdf_path)
    else:
        print(f"PDF not found at {pdf_path}")
