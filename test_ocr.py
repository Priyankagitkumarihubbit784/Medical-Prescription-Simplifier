from src.ocr_engine import check_ocr_engine

try:
    version = check_ocr_engine()
    print("OCR ENGINE WORKING!")
    print("Tesseract version:", version)

except Exception as error:
    print("OCR ERROR:", error)