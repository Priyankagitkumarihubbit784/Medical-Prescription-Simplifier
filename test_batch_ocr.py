
from pathlib import Path

from src.document_upload import process_uploaded_document
from src.extraction import extract_medical_information
from src.advanced_verification import assess_extraction_quality

file_path = Path(
    r"C:\Users\priya\Downloads\sample_prescription_image.png"
)

result = process_uploaded_document(
    file_path.name,
    file_path.read_bytes()
)

medical_text = result["text"]

print("\n1. OCR TEXT")
print("=" * 40)
print(medical_text)

extracted = extract_medical_information(medical_text)

print("\n2. EXTRACTED INFORMATION")
print("=" * 40)

for key, value in extracted.items():
    print(f"{key}: {value}")

quality = assess_extraction_quality(
    extracted,
    source_type=result["method"]
)

print("\n3. EXTRACTION QUALITY")
print("=" * 40)
print(quality)
