from PIL import Image, ImageDraw
from src.document_upload import process_uploaded_document

image = Image.new("RGB", (1200, 500), "white")
draw = ImageDraw.Draw(image)

text = """
DEMO PRESCRIPTION

DemoMed-A 250 mg

Take one tablet twice daily for 5 days.

Warning: Avoid driving if drowsy.

Side effects include nausea and dizziness.
"""

draw.multiline_text(
    (50, 50),
    text,
    fill="black",
    spacing=18
)

image.save("test_prescription.png")

with open("test_prescription.png", "rb") as file:
    file_bytes = file.read()

result = process_uploaded_document(
    "test_prescription.png",
    file_bytes
)

print("\nOCR METHOD:", result["method"])
print("\nEXTRACTED TEXT:")
print(result["text"])