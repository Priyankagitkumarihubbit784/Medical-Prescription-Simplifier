import os

from src.ocr_engine import extract_document_text

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def process_uploaded_document(filename, file_bytes):

    if not filename:
        raise ValueError("No file was selected.")

    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only PDF, JPG, JPEG and PNG files are supported."
        )

    if not file_bytes:
        raise ValueError("The uploaded file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError("File size must not exceed 10 MB.")

    signatures = {
        ".pdf": file_bytes.startswith(b"%PDF"),
        ".jpg": file_bytes.startswith(b"\xff\xd8\xff"),
        ".jpeg": file_bytes.startswith(b"\xff\xd8\xff"),
        ".png": file_bytes.startswith(b"\x89PNG\r\n\x1a\n")
    }

    if not signatures[extension]:
        raise ValueError("The file content does not match its extension.")

    return extract_document_text(filename, file_bytes)