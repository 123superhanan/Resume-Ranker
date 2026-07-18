import fitz

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text


text = extract_text("resumes/resume1.pdf")

print(text)