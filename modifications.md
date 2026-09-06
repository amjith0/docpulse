# Possible Improvements & Design Trade-offs

This log documents scenarios identified while building DocPulse, along with fixes considered and their trade-offs. Some have been implemented; others are noted as future improvements.

## Phase 1 — PDF Reading

**Scenario:** PDF has scanned/image pages, extraction returns blank text
- **Fix:** Add OCR (`pytesseract` + `pdf2image`) as a fallback when `extract_text()` returns empty
- **Trade-off:** OCR is slower and less accurate than native text extraction — only use when needed

**Scenario:** Multiple documents need to be compared
- **Fix:** Allow multiple file uploads (`st.file_uploader(..., accept_multiple_files=True)`), tag each chunk with its source filename
- **Trade-off:** Adds complexity to chunk IDs and requires tracking which document each answer came from

## Phase 2 — Chunking

**Scenario:** Chunks cut off mid-sentence, hurting answer quality
- **Fix:** Switch to sentence-aware or recursive chunking — split on paragraph/sentence boundaries first, only force-cut if still too long
- **Trade-off:** More complex logic than fixed-size slicing, but noticeably better chunk quality

**Scenario:** Chunks have no overlap, so context at boundaries gets lost
- **Fix:** Add overlapping chunks — each chunk shares the last 50-100 characters with the next one
- **Trade-off:** More total chunks stored, but prevents losing meaning that spans a chunk boundary

## Phase 3 — Embeddings + Vector Database

**Scenario:** Vector database rebuilds from scratch every run
- **Fix:** Use `chromadb.PersistentClient(path="./chroma_db")` instead of `chromadb.Client()` to save to disk
- **Trade-off:** Faster repeat use, but needs logic to avoid duplicate entries

**Scenario:** Default embedding model isn't accurate enough for a specialized domain
- **Fix:** Swap to a different embedding model from Hugging Face, better suited to that domain
- **Trade-off:** Domain-specific models can be larger/slower; the default (`all-MiniLM-L6-v2`) is a solid general-purpose choice

## Phase 4 — Vector Search

**Scenario:** Search retrieves loosely-related, unhelpful chunks
- **Fix:** Add a similarity threshold — discard weak matches instead of always returning top-N
- **Trade-off:** May return fewer (or zero) results, needing graceful "no relevant info found" handling

**Scenario:** Meaning-based search misses exact-term queries
- **Fix:** Hybrid search — combine vector search with traditional keyword search
- **Trade-off:** More complex to implement, but a recognized production RAG upgrade

## Phase 5 — RAG + Local LLM

**Scenario:** Answers feel shallow (encountered during development)
- **Fix implemented:** Increased chunk size (500 → 1000), increased `n_results` (3 → 5), and updated the prompt to explicitly request detail and examples
- **Result:** Noticeably more thorough, well-structured answers

**Scenario:** Model is slow on limited hardware
- **Fix:** Try a smaller model (`llama3.2:1b`) for faster responses, or compare with Mistral
- **Trade-off:** Smaller models respond faster but may be less detailed

**Scenario:** No memory of previous questions in a session
- **Fix:** Maintain a conversation history list, append each Q&A pair, include recent history in the prompt
- **Trade-off:** Longer prompts mean slower responses; needs a history length limit

**Scenario:** No visibility into which chunks informed an answer
- **Fix:** Display retrieved chunks alongside the answer (`st.expander("Sources")`)
- **Trade-off:** None significant — also a strong source-attribution talking point

## Phase 6 — Streamlit UI

**Scenario:** Every question reprocesses the whole PDF from scratch
- **Fix:** Use `st.session_state` to store chunks/collection so re-asking questions doesn't require reprocessing
- **Trade-off:** More Streamlit-specific state management, but meaningfully better UX

**Scenario:** No feedback during long processing steps
- **Fix:** Add `st.spinner("Processing...")` around chunking/embedding steps
- **Trade-off:** None — pure UX improvement