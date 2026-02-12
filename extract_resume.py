
from pypdf import PdfReader

reader = PdfReader("d:/agentic-ai/resume/VaranSinghRohila_Resume.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"

with open("d:/agentic-ai/resume/resume_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Resume text extracted successfully.")
