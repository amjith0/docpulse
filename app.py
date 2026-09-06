import streamlit as st
from pypdf import PdfReader
import chromadb
import ollama

st.title("DocPulse - Smart Study Assistant")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    # Extract text from the uploaded PDF
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    # Split text into chunks for embedding
    def chunk_text(text, chunk_size=1000):
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i+chunk_size])
        return chunks

    chunks = chunk_text(text)

    # Store chunks in the vector database
    client = chromadb.Client()
    collection = client.get_or_create_collection("study_docs")
    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    st.success(f"PDF processed into {len(chunks)} chunks. Ask a question below.")

    question = st.text_input("Ask a question about your document:")

    if question:
        # Retrieve the most relevant chunks for the question
        results = collection.query(query_texts=[question], n_results=5)
        retrieved_chunks = results["documents"][0]

        # Build the prompt and query the local LLM
        context = "\n\n".join(retrieved_chunks)
        prompt = f"""Answer the question in detail using only the context below. Explain thoroughly and include relevant examples if present. If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {question}"""

        try:
            response = ollama.chat(
                model="llama3.2",
                messages=[{"role": "user", "content": prompt}]
            )
            st.write(response["message"]["content"])
        except Exception as e:
            st.error("Couldn't reach the local Ollama model. Make sure Ollama is running.")