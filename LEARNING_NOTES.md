Phase 1 Notes — PDF Text Extraction

What we did: Used the pypdf library's PdfReader to open a PDF and loop through every page, extracting raw text with .extract_text(), building it into one combined string.

Why it matters: This is the entry point of any document-AI system — before an AI can answer questions from a document, the document has to be converted from a formatted file into plain, usable text. Every RAG pipeline starts here.

Key concept: pypdf only works on text-based PDFs. Scanned/image PDFs would return empty text and need OCR instead (different tool, not used here).

Gotcha hit: Running with python -m 01_read_pdf.py failed — -m expects a module name without .py. Fix: python 01_read_pdf.py (no -m flag).


Phase 2 Notes — Chunking

Split extracted PDF text into fixed-size pieces using a loop and string slicing
chunk_size=500 → 61 chunks; chunk_size=1000 → 31 chunks
Chunks can cut sentences mid-way — a known trade-off of fixed-size chunking
Chose chunk_size=[your final choice] because [your reason]

Phase 3 Notes — Embeddings + Vector Database

Embeddings convert text into numbers representing meaning, not exact words
ChromaDB automatically generates embeddings when .add() is called (using a downloaded model, all-MiniLM-L6-v2)
Chunks and their embeddings get stored together in a named "collection"
Later, a search query gets embedded the same way, and ChromaDB finds the closest matches

Phase 4 Notes — Vector Search

A query gets converted into an embedding the same way chunks were
ChromaDB compares the query's embedding against all stored chunk embeddings, returns closest matches
Works even when the query's wording differs completely from the document's wording (tested: "What is HTML?" vs "Define Hyper Text Markup Language" — same top result)

Phase 5 Notes — RAG Assembly with Ollama

Installed Ollama app + pulled Llama 3.2 model locally
Used ollama Python library to send prompts to the local model
Built a prompt combining retrieved chunks (context) + question + instruction to only answer from context
Confirmed grounding: in-scope question answered accurately from PDF content
Confirmed hallucination control: out-of-scope question correctly triggered "I don't know" instead of the model using its own knowledge

Phase 6 Notes — Streamlit UI + Deployment

- Restructured the pipeline into a Streamlit web app with file upload and text input
- Added error handling for pages with no extractable text, and for Ollama being unreachable
- Set up Git and GitHub: .gitignore, README, organized learning_steps/ folder
- Deployment consideration: Ollama can't run on Streamlit Community Cloud's servers, so public deployment needs either a local-only demo, a fallback message, or swapping to a cloud LLM API for the hosted version
