from pypdf import PdfReader
import chromadb
import ollama

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

# Phase 3 - store chunks in a vector database
client = chromadb.Client()
collection = client.create_collection("study_docs")
collection.add(
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

# Phase 4 - search for relevant chunks
question = "What is HTML?"
results = collection.query(query_texts=[question], n_results=5)
retrieved_chunks = results["documents"][0]

# Phase 5 - build the prompt and ask Llama
context = "\n\n".join(retrieved_chunks)

prompt = f"""Answer the question in detail using only the context below. Explain thoroughly and include relevant examples if present. If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {question}"""

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": prompt}]
)

print(response["message"]["content"])