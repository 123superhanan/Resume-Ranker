# src/chunker.py
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(
    documents: List[Document], 
    chunk_size: int = 500, 
    chunk_overlap: int = 50
) -> List[Document]:
    """
    Takes an incoming list of LangChain Document objects and breaks their text 
    down into optimized chunks while retaining all metadata.
    """
    if not documents:
        print("⚠️ Warning: Received empty document list to chunk.")
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"✂️ Chunker: Successfully split {len(documents)} pages into {len(chunks)} fragments.")
    return chunks

# --- Orchestrate both files together ---
if __name__ == "__main__":
    # Import the execution function from your loader file
    from loader import load_balanced_resumes
    
    print("🚀 Running complete pipeline step...")
    
    # 1. Fetch the files safely
    raw_pages = load_balanced_resumes("../data", files_per_folder=5)
    
    # 2. Split them up using the standalone chunker script
    processed_chunks = split_documents(raw_pages, chunk_size=500, chunk_overlap=50)
    
    # Preview a sample chunk structure to confirm layout
    if processed_chunks:
        print("\n--- Processed Sample Chunk ---")
        print(f"Filename: {processed_chunks[0].metadata['filename']}")
        print(f"Field:    {processed_chunks[0].metadata['career']}")
        print(f"Snippet:  {processed_chunks[0].page_content[:100]}...")
