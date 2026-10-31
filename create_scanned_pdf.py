
import pymupdf
from PIL import Image

# Open the existing prescription image
image = Image.open("test_prescription.png").convert("RGB")

# Save it temporarily as an image
image.save("temp_prescription.jpg")

# Create a PDF containing only the image
pdf = pymupdf.open()
page = pdf.new_page(width=595, height=842)

page.insert_image(
    pymupdf.Rect(40, 40, 555, 800),
    filename="temp_prescription.jpg"
)

pdf.save("test_scanned_prescription.pdf")
pdf.close()

print("Scanned PDF created successfully!")
