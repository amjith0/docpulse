from pypdf import PdfReader
import chromadb

# Phase 1 - extract text from PDF
reader = PdfReader("my_notes.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# Phase 2 - chunk the text
def chunk_text(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

chunks = chunk_text(text)

# Phase 3 - store chunks in a vector database
client = chromadb.Client()
collection = client.create_collection("study_docs")

collection.add(
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

print("Chunks stored:", collection.count())

results = collection.query(
    query_texts=["What is HTML?"],
    n_results=3
)

for doc in results["documents"][0]:
    print(doc)
    print("---")