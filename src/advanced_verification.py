
REQUIRED_FIELDS = {
    "drug_name": "Drug Name",
    "strength": "Strength",
    "dosage": "Dosage",
    "frequency": "Frequency",
    "duration": "Duration",
    "warnings": "Warnings",
    "side_effects": "Side Effects"
}

CRITICAL_FIELDS = [
    "drug_name",
    "strength",
    "dosage",
    "frequency",
    "duration"
]


def is_missing(value):
    """Check whether an extracted field is missing."""

    if value is None:
        return True

    if isinstance(value, str):
        return (
            not value.strip()
            or value.strip().lower() == "not identified"
        )

    if isinstance(value, list):
        return (
            len(value) == 0
            or all(
                str(item).strip().lower() == "not identified"
                for item in value
            )
        )

    return False


def assess_extraction_quality(extracted_info, source_type="manual"):
    """
    Assess extraction completeness and identify fields
    that require human review.

    This is a rule-based completeness assessment,
    not a medical accuracy or confidence score.
    """

    detected_fields = []
    missing_fields = []
    review_fields = []

    for field, label in REQUIRED_FIELDS.items():

        value = extracted_info.get(field)

        if is_missing(value):
            missing_fields.append(label)

        else:
            detected_fields.append(label)

    # Important medication fields always require review
    for field in CRITICAL_FIELDS:

        if is_missing(extracted_info.get(field)):
            label = REQUIRED_FIELDS[field]

            review_fields.append(
                f"{label} could not be identified. "
                "Please check the original prescription."
            )

    # OCR may incorrectly recognize important information
    if source_type in ["ocr", "Tesseract OCR", "Scanned PDF OCR"]:

        review_fields.append(
            "OCR-extracted text must be compared with the original "
            "document, especially medicine names, strengths and dosage."
        )

    if missing_fields:
        status = "Review Required"

    elif source_type in ["ocr", "Tesseract OCR", "Scanned PDF OCR"]:
        status = "Manual Review Required"

    else:
        status = "Fields Detected - Human Review Recommended"

    total_fields = len(REQUIRED_FIELDS)
    detected_count = len(detected_fields)

    completeness_percentage = round(
        (detected_count / total_fields) * 100,
        2
    )

    return {
        "detected_fields": detected_fields,
        "missing_fields": missing_fields,
        "review_fields": review_fields,
        "detected_count": detected_count,
        "total_fields": total_fields,
        "completeness_percentage": completeness_percentage,
        "status": status,
        "assessment_type": "Rule-based completeness assessment"
    }
