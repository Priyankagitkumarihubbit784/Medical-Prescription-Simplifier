from src.extraction import extract_medical_information
from src.advanced_verification import assess_extraction_quality


sample_text = """
DemoMed-A 250 mg.
Take one tablet twice daily for 5 days.
Warning: Avoid driving if drowsy.
Side effects include nausea and dizziness.
"""

extracted = extract_medical_information(sample_text)

quality = assess_extraction_quality(
    extracted,
    source_type="manual"
)

print("\nEXTRACTION QUALITY REPORT")
print("=" * 45)

print("Status:", quality["status"])

print(
    "Completeness:",
    quality["completeness_percentage"],
    "%"
)

print("\nDetected Fields:")
for field in quality["detected_fields"]:
    print("✓", field)

print("\nMissing Fields:")
for field in quality["missing_fields"]:
    print("!", field)

print("\nManual Review:")
for warning in quality["review_fields"]:
    print("⚠", warning)