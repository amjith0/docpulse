from pypdf import PdfReader

# Phase 1 - extract text from PDF
reader = PdfReader("my_notes.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# Phase 2 - chunk the text
def chunk_text(text, chunk_size=1000):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

chunks = chunk_text(text)
print(f"Total chunks: {len(chunks)}")
print(chunks[1])