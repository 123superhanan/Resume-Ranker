# import fitz
# from pathlib import Path

# PROJECT_ROOT = Path(__file__).resolve().parent.parent

# def  extract_text(pdf_path: Path) -> str:
#     """Extracts all text from a single PDF file."""
#     try:
#         doc = fitz.open(str(pdf_path))
#         text = ""
#         for page in doc:
#             text += page.get_text()
#         return text
#     except Exception as e:
#         print(f"Error reading {pdf_path.name}: {e}")
#         return ""
    


import fitz

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text