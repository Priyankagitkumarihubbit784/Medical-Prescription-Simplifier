
import base64

from flask import Flask, render_template, request

from src.extraction import extract_medical_information
from src.simplification import simplify_text
from src.verification import verify_simplification
from src.document_upload import process_uploaded_document
from src.advanced_verification import assess_extraction_quality
from src.batch_processor import process_batch, create_batch_csv

from evaluation.evaluate import calculate_readability


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

DISCLAIMER = (
    "This tool does not replace medical advice. "
    "Consult your doctor or pharmacist."
)


# FILE SIZE ERROR HANDLER
@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        result=None,
        error="The uploaded files exceed the 50 MB total limit.",
        original_text="",
        disclaimer=DISCLAIMER,
        ocr_info=None,
        batch_results=None,
        batch_csv_base64=None
    ), 413


# HOME PAGE: MANUAL TEXT AND DOCUMENT EXTRACTION
@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error = None
    original_text = ""
    ocr_info = None

    if request.method == "POST":

        action = request.form.get("action", "analyze")

        if action == "extract":

            uploaded_file = request.files.get("document")

            if not uploaded_file or not uploaded_file.filename:
                error = "Please select a PDF or prescription image."

            else:
                try:

                    file_bytes = uploaded_file.read()

                    ocr_info = process_uploaded_document(
                        uploaded_file.filename,
                        file_bytes
                    )

                    original_text = ocr_info["text"]

                    if not original_text.strip():
                        error = (
                            "No text could be extracted. "
                            "Try a clearer image or enter the text manually."
                        )

                except Exception as e:

                    error = str(e)
                    print("OCR error:", e)

        elif action == "analyze":

            original_text = request.form.get(
                "medical_text", ""
            ).strip()

            previous_ocr_method = request.form.get(
                "ocr_method", ""
            ).strip()

            previous_ocr_pages = request.form.get(
                "ocr_pages", ""
            ).strip()

            if previous_ocr_method:

                ocr_info = {
                    "method": previous_ocr_method,
                    "pages": previous_ocr_pages
                }

            if not original_text:

                error = "Please enter or extract medical text."

            elif len(original_text) > 10000:

                error = (
                    "Please enter text containing fewer than "
                    "10,000 characters."
                )

            else:

                try:

                    # 1. Extract medical information
                    extracted_info = extract_medical_information(
                        original_text
                    )

                    # 2. Assess extraction completeness
                    source_type = (
                        ocr_info["method"]
                        if ocr_info and ocr_info.get("method")
                        else "manual"
                    )

                    extraction_quality = assess_extraction_quality(
                        extracted_info,
                        source_type=source_type
                    )

                    # 3. Simplify medical text
                    simplified_text = simplify_text(
                        original_text
                    )

                    # 4. Verify simplification
                    verification = verify_simplification(
                        original_text,
                        simplified_text
                    )

                    safe_output = verification["safe_output"]

                    # 5. Calculate readability
                    original_readability = calculate_readability(
                        original_text
                    )

                    simplified_readability = calculate_readability(
                        safe_output
                    )

                    # 6. Calculate readability improvement
                    readability_improvement = round(
                        simplified_readability["flesch_reading_ease"]
                        - original_readability["flesch_reading_ease"],
                        2
                    )

                    result = {
                        "extracted": extracted_info,
                        "extraction_quality": extraction_quality,
                        "simplified": safe_output,
                        "verification": verification,
                        "original_readability": original_readability,
                        "simplified_readability": simplified_readability,
                        "readability_improvement": readability_improvement,
                        "disclaimer": DISCLAIMER,
                        "ocr_info": ocr_info
                    }

                except Exception as e:

                    error = (
                        "An error occurred during processing. "
                        "Please check your input and try again."
                    )

                    print("Application error:", e)

    return render_template(
        "index.html",
        result=result,
        error=error,
        original_text=original_text,
        disclaimer=DISCLAIMER,
        ocr_info=ocr_info,
        batch_results=None,
        batch_csv_base64=None
    )


# BATCH DOCUMENT PROCESSING
@app.route("/batch", methods=["POST"])
def batch_upload():

    batch_results = None
    batch_csv_base64 = None
    error = None

    try:

        uploaded_files = request.files.getlist("documents")

        files = [
            (file.filename, file.read())
            for file in uploaded_files
            if file and file.filename
        ]

        if not files:
            raise ValueError(
                "Please select at least one document."
            )

        if len(files) > 5:
            raise ValueError(
                "Maximum 5 documents can be uploaded."
            )

        batch_results = process_batch(files)

        csv_bytes = create_batch_csv(batch_results)

        batch_csv_base64 = base64.b64encode(
            csv_bytes
        ).decode("utf-8")

    except Exception as e:

        error = str(e)
        print("Batch processing error:", e)

    return render_template(
        "index.html",
        result=None,
        error=error,
        original_text="",
        disclaimer=DISCLAIMER,
        ocr_info=None,
        batch_results=batch_results,
        batch_csv_base64=batch_csv_base64
    )


# START FLASK APPLICATION
if __name__ == "__main__":

    print("=" * 50)
    print("MEDICAL PRESCRIPTION SIMPLIFIER")
    print("Starting Flask application...")
    print("Open http://127.0.0.1:5000")
    print("=" * 50)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
