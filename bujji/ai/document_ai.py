"""
Document AI — PDF & Image Analysis Module
=========================================
Extracts text from PDF documents and performs image/screenshot analysis.
"""

from pathlib import Path

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


def extract_pdf_text(pdf_path, max_pages=15):
    """Extract readable text from a PDF file."""
    if not PDF_AVAILABLE:
        return "PyPDF2 is not installed. Run `pip install PyPDF2` to enable PDF text extraction."

    path = Path(pdf_path)
    if not path.exists():
        return f"File not found: {pdf_path}"

    try:
        reader = PyPDF2.PdfReader(str(path))
        text_parts = []
        num_pages = min(len(reader.pages), max_pages)

        for i in range(num_pages):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text_parts.append(f"--- Page {i + 1} ---\n{page_text}")

        if not text_parts:
            return "No extractable text found in this PDF (it may contain scanned images)."

        combined = "\n\n".join(text_parts)
        return combined
    except Exception as e:
        return f"Error reading PDF file: {e}"
