import pdfplumber
from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\rajva\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\poppler-26.02.0\Library\bin"


def extract_pdf_text(filepath):

    text = ""

    with pdfplumber.open(filepath) as pdf:
        total_pages = len(pdf.pages)

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    if text.strip() == "":
        print("Running OCR...")
        print("PDF:", filepath)
        print("Poppler:", POPPLER_PATH)

        images = convert_from_path(
            filepath,
            poppler_path=POPPLER_PATH
        )

        for image in images:
            text += pytesseract.image_to_string(image)

    return text, total_pages