# DocPulse - Smart Study Assistant

A local, privacy-first RAG (Retrieval-Augmented Generation) application that lets you upload a PDF and ask natural-language questions about its content — answered using a locally-hosted open-source LLM, with zero reliance on paid APIs.

## How It Works

1. Upload a PDF document
2. The text is extracted and split into chunks
3. Each chunk is converted into an embedding and stored in a vector database (ChromaDB)
4. When you ask a question, the most relevant chunks are retrieved using semantic search
5. Those chunks are passed to a locally-running Llama 3.2 model (via Ollama), which generates a grounded answer — strictly based on the document's content

## Tech Stack

- **Python** - core logic
- **pypdf** - PDF text extraction
- **ChromaDB** - vector database for semantic search
- **Ollama + Llama 3.2** - local LLM inference (no API costs, fully offline capable)
- **Streamlit** - web interface

## Running Locally

1. Clone this repo
   \`\`\`bash
   git clone <your-repo-url>
   cd docpulse
   \`\`\`

2. Create a virtual environment and install dependencies
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate
   pip install pypdf chromadb ollama streamlit
   \`\`\`

3. Install [Ollama](https://ollama.com) and pull the model
   \`\`\`bash
   ollama run llama3.2
   \`\`\`

4. Run the app
   \`\`\`bash
   streamlit run app.py
   \`\`\`

5. Open the local URL shown in your terminal, upload a PDF, and start asking questions

## Learning Process

The `learning_steps/` folder contains the step-by-step scripts used to build this project incrementally — from PDF extraction through to the full RAG pipeline — documented in `LEARNING_NOTES.md`.

## Possible Future Improvements

- Sentence-aware/recursive chunking instead of fixed-size
- Persistent vector storage across sessions
- Source chunk citations shown alongside answers
- Multi-document support