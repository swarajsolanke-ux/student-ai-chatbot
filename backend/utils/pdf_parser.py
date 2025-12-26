# pdf_parser.py - Part of utils module
import pdfplumber

def extract_text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(p.page.extract_text() for p in pdf.pages)
