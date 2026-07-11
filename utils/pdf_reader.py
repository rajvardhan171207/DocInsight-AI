import os
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\rajva\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    POPPLER_PATH = r"C:\poppler-26.02.0\Library\bin"
else:
    POPPLER_PATH = None


def extract_pdf_text(filepath):

    text = ""

    with pdfplumber.open(filepath) as pdf:

        total_pages = len(pdf.pages)

        MAX_PAGES = min(total_pages, 30)

        for page in pdf.pages[:MAX_PAGES]:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    # OCR only if no text found
    if text.strip() == "":

        print("Running OCR...")

        if POPPLER_PATH:
            images = convert_from_path(
                filepath,
                poppler_path=POPPLER_PATH
            )
        else:
            images = convert_from_path(filepath)

        for image in images:
            text += pytesseract.image_to_string(image)

    return text, total_pages