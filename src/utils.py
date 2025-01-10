import os

def load_pdfs(pdf_folder):
    return [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
