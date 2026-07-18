# import fitz
# from pathlib import Path
# from parser import extract_text

# PROJECT_ROOT = Path(__file__).resolve().parent.parent

# def load_all_resumes(data_subdir: str = "data") -> list[dict]:
#     """
#     Scans the data directory, extracts text, and preserves the job category
#     based on the folder name (e.g., ACCOUNTANT).
#     """
#     data_dir = PROJECT_ROOT / data_subdir
#     documents = []
    
#     # Recursively find all PDF files under the data folder
#     for pdf_path in data_dir.rglob("*.pdf"):
#         # The immediate parent directory name acts as the candidate's category label
#         category = pdf_path.parent.name 
        
#         text = extract_text(pdf_path)
#         if text.strip():
#             documents.append({
#                 "text": text,
#                 "metadata": {
#                     "source": str(pdf_path.relative_to(PROJECT_ROOT)),
#                     "category": category,
#                     "filename": pdf_path.name
#                 }
#             })
            
#     print(f"Loaded {len(documents)} resumes successfully.")
#     return documents