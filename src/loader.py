# src/loader.py
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def load_balanced_resumes(
    root_dir: str | Path = "data",
    glob_pattern: str = "**/*.pdf",
    files_per_folder: int = 5,
) -> List[Document]:
    """
    Scans the data root, collects exactly files_per_folder PDFs from each subfolder,
    and returns a list of raw LangChain Documents.
    """
    root = Path(root_dir)
    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {root.resolve()}")

    # 1. Group files by subfolder name
    grouped_files = {}
    for pdf_path in root.glob(glob_pattern):
        folder_name = pdf_path.parent.name
        if folder_name not in grouped_files:
            grouped_files[folder_name] = []
        grouped_files[folder_name].append(pdf_path)

    # 2. Slice up to files_per_folder from each group
    balanced_pdf_files = []
    print("--- Loader Configuration Breakdown ---")
    for folder, files in grouped_files.items():
        limited_files = files[:files_per_folder]
        balanced_pdf_files.extend(limited_files)
        print(f"📁 {folder}: Selected {len(limited_files)} out of {len(files)} total files.")

    # 3. Load files into raw Document arrays
    all_raw_docs: List[Document] = []
    for pdf_path in balanced_pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_path))
            pages = loader.load()

            # Append tracking metadata to raw pages
            for page in pages:
                page.metadata["career"] = pdf_path.parent.name
                page.metadata["filename"] = pdf_path.name

            all_raw_docs.extend(pages)
        except Exception as e:
            print(f"❌ Failed to load {pdf_path.name}: {e}")

    print(f"\nSuccessfully loaded {len(all_raw_docs)} total raw pages from disk.")
    return all_raw_docs

if __name__ == "__main__":
    # Test loader alone
    raw_docs = load_balanced_resumes("../data", files_per_folder=5)
