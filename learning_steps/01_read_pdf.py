from pypdf import PdfReader
reader=PdfReader("my_notes.pdf")
text=""
for page in reader.pages:
    text+= page.extract_text()
print(text[:500])