
import pymupdf

pdf = pymupdf.open()
page = pdf.new_page()

text = """
DEMO PRESCRIPTION

Medicine: DemoMed-A 250 mg

Instructions: Take one tablet twice daily for 5 days.

Warning: Avoid driving if drowsy.

Possible side effects: nausea and dizziness.
"""

page.insert_textbox(
    pymupdf.Rect(50, 50, 550, 400),
    text,
    fontsize=14
)

pdf.save("test_prescription.pdf")
pdf.close()

print("Test PDF created successfully!")
