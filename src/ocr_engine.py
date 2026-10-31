
import os
import io
import re

import pytesseract
import pymupdf

from PIL import (
    Image,
    ImageOps,
    ImageEnhance,
    ImageFilter,
    ImageChops
)
from pypdf import PdfReader


# Tesseract configuration
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# OCR settings
MAX_PDF_PAGES = 10


def preprocess_image(image):
    """Improve image quality before OCR."""

    image = image.convert("RGB")

    # Convert to grayscale
    image = ImageOps.grayscale(image)

    # Improve contrast
    image = ImageOps.autocontrast(image)

    # Remove unnecessary white borders
    background = Image.new("L", image.size, 255)
    difference = ImageChops.difference(image, background)
    bounding_box = difference.point(
        lambda pixel: 255 if pixel > 20 else 0
    ).getbbox()

    if bounding_box:
        image = image.crop(bounding_box)

    # Add a small white border
    image = ImageOps.expand(image, border=30, fill=255)

    # Enlarge image
    image = image.resize(
        (image.width * 3, image.height * 3),
        Image.Resampling.LANCZOS
    )

    # Improve contrast and sharpness
    image = ImageEnhance.Contrast(image).enhance(2.0)
    image = ImageEnhance.Sharpness(image).enhance(2.0)

    return image


def clean_ocr_text(text):
    """Clean unnecessary OCR spacing."""

    text = text.replace("\x0c", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def perform_ocr(image):
    """Try multiple Tesseract page segmentation modes."""

    processed_image = preprocess_image(image)

    configurations = [
        "--oem 3 --psm 6",
        "--oem 3 --psm 11",
        "--oem 3 --psm 4"
    ]

    best_text = ""

    for config in configurations:
        try:
            text = pytesseract.image_to_string(
                processed_image,
                config=config
            )

            text = clean_ocr_text(text)

            if len(text) > len(best_text):
                best_text = text

        except Exception:
            continue

    return best_text


def extract_image_text(file_bytes):
    """Extract text from an image."""

    image = Image.open(io.BytesIO(file_bytes))
    text = perform_ocr(image)

    return {
        "text": text,
        "method": "Tesseract OCR",
        "pages": 1
    }


def extract_pdf_text(file_bytes):
    """Extract text from digital or scanned PDFs."""

    pdf_stream = io.BytesIO(file_bytes)

    # First try normal PDF text extraction
    try:
        reader = PdfReader(pdf_stream)

        extracted_pages = []

        for page in reader.pages[:MAX_PDF_PAGES]:
            extracted_pages.append(page.extract_text() or "")

        digital_text = "\n".join(extracted_pages).strip()

        if len(digital_text) >= 30:
            return {
                "text": digital_text,
                "method": "PDF Text Extraction",
                "pages": len(extracted_pages)
            }

    except Exception:
        pass

    # If PDF has no readable text, use OCR
    document = pymupdf.open(stream=file_bytes, filetype="pdf")

    pages = min(len(document), MAX_PDF_PAGES)
    ocr_results = []

    for page_number in range(pages):
        page = document.load_page(page_number)

        pixmap = page.get_pixmap(
            matrix=pymupdf.Matrix(3, 3),
            alpha=False
        )

        image = Image.open(
            io.BytesIO(pixmap.tobytes("png"))
        )

        ocr_results.append(perform_ocr(image))

    document.close()

    return {
        "text": "\n\n".join(ocr_results).strip(),
        "method": "Scanned PDF OCR",
        "pages": pages
    }


def extract_document_text(filename, file_bytes):
    """Main function used by the Flask application."""

    extension = os.path.splitext(filename)[1].lower()

    if extension in [".jpg", ".jpeg", ".png"]:
        return extract_image_text(file_bytes)

    elif extension == ".pdf":
        return extract_pdf_text(file_bytes)

    else:
        raise ValueError("Unsupported document format.")
