# DocPulse - Smart Study Assistant

**Live demo:** [docpulse.streamlit.app](https://docpulse.streamlit.app)

A RAG (Retrieval-Augmented Generation) application that lets you upload a PDF and ask natural-language questions about its content. Answers are strictly grounded in the document itself, with no hallucinated content outside what's provided.

DocPulse runs on a **dual-provider architecture**: locally, it uses a self-hosted, fully offline Llama 3.2 model via Ollama — no API costs, no internet dependency, no data leaving your machine. The live deployed version above uses Groq's free-tier cloud API instead, since Ollama can't run on Streamlit's servers. Both paths share the exact same retrieval and prompting logic.

## How It Works

1. Upload a PDF document
2. The text is extracted and split into chunks
3. Each chunk is converted into an embedding and stored in a vector database (ChromaDB)
4. When you ask a question, the most relevant chunks are retrieved using semantic search
5. Those chunks are passed to an LLM — Llama 3.2 via Ollama locally, or `gpt-oss-20b` via Groq's cloud API when deployed — which generates a grounded answer based strictly on the retrieved content

## Tech Stack

- **Python** - core logic
- **pypdf** - PDF text extraction
- **ChromaDB** - vector database for semantic search
- **Ollama + Llama 3.2** - local, self-hosted LLM inference (no API costs, fully offline capable)
- **Groq (`gpt-oss-20b`)** - free-tier cloud LLM inference, used only for the deployed version
- **python-dotenv** - loads local environment variables from `.env`
- **Streamlit** - web interface

## Running Locally

1. Clone this repo
   ```bash
   git clone <your-repo-url>
   cd docpulse
   ```

2. Create a virtual environment and install dependencies
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Install [Ollama](https://ollama.com) and pull the model
   ```bash
   ollama run llama3.2
   ```

4. Run the app
   ```bash
   streamlit run app.py
   ```

5. Open the local URL shown in your terminal, upload a PDF, and start asking questions

Running locally with no `.env` file (default) uses Ollama automatically. No API key needed.

## Optional: Using Groq Instead of Ollama Locally

To test the cloud path locally (useful before deploying):

1. Get a free API key at [console.groq.com](https://console.groq.com)
2. Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_key_here
   ```
3. Run the app as usual — it will detect the key and use Groq instead of Ollama

`.env` is gitignored and never committed.

## Deploying Your Own Copy

1. Push this repo to your own GitHub account
2. Create an app on [share.streamlit.io](https://share.streamlit.io), pointing to `app.py`
3. In the app's **Advanced settings → Secrets**, add (TOML format, quotes required):
   ```
   GROQ_API_KEY = "your_key_here"
   ```
4. Deploy — the app will automatically use Groq since no local Ollama instance is reachable

## Learning Process

The `learning_steps/` folder contains the step-by-step scripts used to build this project incrementally — from PDF extraction through to the full RAG pipeline — documented in `LEARNING_NOTES.md`. Design decisions and trade-offs considered along the way are logged in `modifications.md`.

## Possible Future Improvements

- Sentence-aware/recursive chunking instead of fixed-size
- Persistent vector storage across sessions
- Source chunk citations shown alongside answers
- Multi-document support
- Fully self-hosted deployment (Ollama running on a rented cloud server) instead of relying on Groq's free tier for the public demo