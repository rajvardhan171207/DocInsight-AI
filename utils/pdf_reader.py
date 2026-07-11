import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
import os

# Windows only
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\rajva\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    POPPLER_PATH = r"C:\poppler-26.02.0\Library\bin"
else:
    POPPLER_PATH = None

MAX_PAGES = 30


def extract_pdf_text(filepath):

    text = ""

    doc = fitz.open(filepath)

    total_pages = len(doc)

    pages_to_process = min(total_pages, MAX_PAGES)

    for page_no in range(pages_to_process):

        try:

            page = doc.load_page(page_no)

            page_text = page.get_text()

            if page_text:
                text += page_text + "\n"

        except Exception:
            continue

    doc.close()

    # OCR only if PDF has no selectable text
    if text.strip() == "":

        print("Running OCR...")

        if POPPLER_PATH:

            images = convert_from_path(
                filepath,
                poppler_path=POPPLER_PATH,
                first_page=1,
                last_page=pages_to_process
            )

        else:

            images = convert_from_path(
                filepath,
                first_page=1,
                last_page=pages_to_process
            )

        for image in images:

            text += pytesseract.image_to_string(image)

    return text, total_pages, pages_to_process