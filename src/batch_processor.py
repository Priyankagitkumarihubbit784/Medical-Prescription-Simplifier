
import csv
import io

from src.document_upload import process_uploaded_document
from src.extraction import extract_medical_information
from src.simplification import simplify_text
from src.verification import verify_simplification
from src.advanced_verification import assess_extraction_quality
from evaluation.evaluate import calculate_readability


MAX_BATCH_FILES = 5


def process_batch(files):
    """
    Process multiple uploaded prescription documents.

    Each item in files must contain:
    (filename, file_bytes)
    """

    if not files:
        raise ValueError("Please upload at least one document.")

    if len(files) > MAX_BATCH_FILES:
        raise ValueError(
            f"You can upload a maximum of {MAX_BATCH_FILES} documents."
        )

    results = []

    for filename, file_bytes in files:

        record = {
            "filename": filename,
            "status": "Failed",
            "error": "",
            "extracted": {},
            "simplified": "",
            "verification_passed": False,
            "completeness": 0
        }

        try:

            # 1. Extract text from document
            document = process_uploaded_document(
                filename,
                file_bytes
            )

            original_text = document["text"]

            if not original_text.strip():
                raise ValueError("No readable text found.")

            # 2. Extract medical information
            extracted = extract_medical_information(
                original_text
            )

            # 3. Check extraction completeness
            quality = assess_extraction_quality(
                extracted,
                source_type=document["method"]
            )

            # 4. Simplify text
            simplified = simplify_text(original_text)

            # 5. Verify simplification
            verification = verify_simplification(
                original_text,
                simplified
            )

            # 6. Readability analysis
            readability = calculate_readability(
                original_text
            )

            record.update({
                "status": "Processed",
                "method": document["method"],
                "pages": document["pages"],
                "extracted": extracted,
                "simplified": verification["safe_output"],
                "verification_passed": verification[
                    "verification_passed"
                ],
                "completeness": quality[
                    "completeness_percentage"
                ],
                "readability": readability
            })

        except Exception as error:

            record["error"] = str(error)

        results.append(record)

    return results


def create_batch_csv(results):
    """
    Convert batch processing results into CSV bytes.
    """

    output = io.StringIO()

    fieldnames = [
        "filename",
        "status",
        "drug_name",
        "strength",
        "dosage",
        "frequency",
        "duration",
        "warnings",
        "side_effects",
        "verification_passed",
        "completeness",
        "error"
    ]

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames
    )

    writer.writeheader()

    for result in results:

        extracted = result.get("extracted", {})

        writer.writerow({
            "filename": result.get("filename", ""),
            "status": result.get("status", ""),
            "drug_name": extracted.get("drug_name", ""),
            "strength": extracted.get("strength", ""),
            "dosage": extracted.get("dosage", ""),
            "frequency": extracted.get("frequency", ""),
            "duration": extracted.get("duration", ""),
            "warnings": "; ".join(
                extracted.get("warnings", [])
            ) if isinstance(
                extracted.get("warnings", []), list
            ) else extracted.get("warnings", ""),
            "side_effects": extracted.get("side_effects", ""),
            "verification_passed": result.get(
                "verification_passed", False
            ),
            "completeness": result.get("completeness", 0),
            "error": result.get("error", "")
        })

    return output.getvalue().encode("utf-8-sig")
