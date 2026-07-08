import pytesseract
from PIL import Image

# Change this only if Tesseract is installed elsewhere
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\rajva\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
def extract_image_text(path):

    image = Image.open(path)

    text = pytesseract.image_to_string(image)

    return text