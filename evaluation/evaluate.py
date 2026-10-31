
import csv
import re
import math
import os
import sys

# Make the main project folder accessible
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.extraction import extract_medical_information
from src.simplification import simplify_text
from src.verification import verify_simplification


DATA_FILE = os.path.join(
    ROOT, "data", "raw", "medical_dataset.csv"
)

RESULTS_DIR = os.path.join(ROOT, "results")
CHART_DIR = os.path.join(RESULTS_DIR, "charts")

os.makedirs(CHART_DIR, exist_ok=True)


# -------------------------------------------------
# 1. OPTIONAL TEXTSTAT LIBRARY
# -------------------------------------------------

try:
    import textstat
    TEXTSTAT_AVAILABLE = True
except Exception:
    TEXTSTAT_AVAILABLE = False


# -------------------------------------------------
# 2. TEXT NORMALIZATION
# -------------------------------------------------

def normalize(value):

    if isinstance(value, list):
        value = " ".join(value)

    value = str(value).lower().strip()

    value = re.sub(r"^warning:\s*", "", value)
    value = value.replace("for ", "")

    value = re.sub(r"[^\w\s.]", "", value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def normalize_frequency(value):

    value = normalize(value)

    replacements = {
        "twice daily": "two times a day",
        "twice a day": "two times a day",
        "once daily": "one time a day",
        "once a day": "one time a day",
        "three times daily": "three times a day",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    return value


def field_matches(field, predicted, actual):

    if field == "frequency":
        return (
            normalize_frequency(predicted)
            == normalize_frequency(actual)
        )

    return normalize(predicted) == normalize(actual)


# -------------------------------------------------
# 3. PRECISION, RECALL AND F1
# -------------------------------------------------

def calculate_metrics(tp, fp, fn):

    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    return {
        "precision": round(precision * 100, 2),
        "recall": round(recall * 100, 2),
        "f1_score": round(f1 * 100, 2)
    }


# -------------------------------------------------
# 4. READABILITY FALLBACK
# -------------------------------------------------

def count_syllables(word):

    word = word.lower()
    word = re.sub(r"[^a-z]", "", word)

    if not word:
        return 0

    groups = re.findall(r"[aeiouy]+", word)

    count = len(groups)

    if word.endswith("e") and count > 1:
        count -= 1

    return max(1, count)


def fallback_readability(text):

    words = re.findall(r"\b[a-zA-Z]+\b", text)

    sentences = re.split(r"[.!?]+", text)
    sentences = [s for s in sentences if s.strip()]

    word_count = len(words)
    sentence_count = max(1, len(sentences))

    if word_count == 0:
        return {
            "flesch_reading_ease": 0,
            "fk_grade": 0,
            "gunning_fog": 0,
            "smog": 0
        }

    syllables = [count_syllables(w) for w in words]

    total_syllables = sum(syllables)

    complex_words = sum(s >= 3 for s in syllables)

    avg_sentence_length = word_count / sentence_count
    avg_syllables = total_syllables / word_count
    complex_percentage = complex_words / word_count

    flesch = (
        206.835
        - 1.015 * avg_sentence_length
        - 84.6 * avg_syllables
    )

    fk_grade = (
        0.39 * avg_sentence_length
        + 11.8 * avg_syllables
        - 15.59
    )

    fog = 0.4 * (
        avg_sentence_length
        + 100 * complex_percentage
    )

    smog = (
        1.043 * math.sqrt(
            complex_words * 30 / sentence_count
        ) + 3.1291
    )

    return {
        "flesch_reading_ease": round(flesch, 2),
        "fk_grade": round(fk_grade, 2),
        "gunning_fog": round(fog, 2),
        "smog": round(smog, 2)
    }


# -------------------------------------------------
# 5. READABILITY CALCULATION
# -------------------------------------------------

def calculate_readability(text):

    if TEXTSTAT_AVAILABLE:

        try:
            return {
                "flesch_reading_ease":
                    round(textstat.flesch_reading_ease(text), 2),

                "fk_grade":
                    round(textstat.flesch_kincaid_grade(text), 2),

                "gunning_fog":
                    round(textstat.gunning_fog(text), 2),

                "smog":
                    round(textstat.smog_index(text), 2)
            }

        except Exception:
            pass

    return fallback_readability(text)


# -------------------------------------------------
# 6. SAVE CSV
# -------------------------------------------------

def save_csv(filename, rows):

    if not rows:
        return

    path = os.path.join(RESULTS_DIR, filename)

    with open(path, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)

    print("Saved:", path)


# -------------------------------------------------
# 7. CREATE SVG READABILITY CHART
# -------------------------------------------------

def create_readability_chart(summary):

    labels = ["Original", "Unverified", "Verified"]

    values = [
        summary["original"]["flesch_reading_ease"],
        summary["unverified"]["flesch_reading_ease"],
        summary["verified"]["flesch_reading_ease"]
    ]

    width = 650
    height = 380

    max_value = max(100, max(values) + 10)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',

        '<rect width="100%" height="100%" fill="white"/>',

        '<text x="325" y="35" text-anchor="middle" '
        'font-size="20" font-weight="bold">'
        'Readability Comparison</text>'
    ]

    bar_width = 110
    positions = [90, 270, 450]

    for label, value, x in zip(labels, values, positions):

        bar_height = max(0, value / max_value * 230)
        y = 300 - bar_height

        svg.append(
            f'<rect x="{x}" y="{y}" '
            f'width="{bar_width}" height="{bar_height}" '
            f'fill="#4385C5" rx="5"/>'
        )

        svg.append(
            f'<text x="{x + bar_width/2}" y="{y - 10}" '
            f'text-anchor="middle" font-size="15">'
            f'{value}</text>'
        )

        svg.append(
            f'<text x="{x + bar_width/2}" y="325" '
            f'text-anchor="middle" font-size="14">'
            f'{label}</text>'
        )

    svg.append(
        '<text x="325" y="365" text-anchor="middle" '
        'font-size="13">Higher score generally means easier reading</text>'
    )

    svg.append('</svg>')

    path = os.path.join(
        CHART_DIR, "readability_chart.svg"
    )

    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(svg))

    print("Chart saved:", path)


# -------------------------------------------------
# 8. MAIN EVALUATION
# -------------------------------------------------

def run_evaluation():

    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(
            "Dataset not found: " + DATA_FILE
        )

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = list(csv.DictReader(file))

    if not records:
        raise ValueError("Dataset is empty.")

    fields = [
        "drug_name",
        "strength",
        "dosage",
        "frequency",
        "duration",
        "warnings",
        "side_effects"
    ]

    counts = {
        field: {"tp": 0, "fp": 0, "fn": 0}
        for field in fields
    }

    readability_rows = []
    faithfulness_rows = []

    original_scores = []
    unverified_scores = []
    verified_scores = []

    interventions = 0

    # Process every dataset record
    for index, record in enumerate(records, start=1):

        original = record["original_text"]

        # Extraction
        extracted = extract_medical_information(original)

        # Extraction evaluation
        for field in fields:

            actual = record[field]
            predicted = extracted[field]

            correct = field_matches(
                field, predicted, actual
            )

            if correct:
                counts[field]["tp"] += 1
            else:
                if normalize(predicted) != "not identified":
                    counts[field]["fp"] += 1

                counts[field]["fn"] += 1

        # Baseline B: Simplification without verification
        unverified = simplify_text(original)

        # Baseline C: Full pipeline with verification
        verification = verify_simplification(
            original, unverified
        )

        verified = verification["safe_output"]

        if not verification["verification_passed"]:
            interventions += 1

        # Evaluate readability
        original_readability = calculate_readability(original)

        unverified_readability = calculate_readability(
            unverified
        )

        verified_readability = calculate_readability(
            verified
        )

        original_scores.append(original_readability)
        unverified_scores.append(unverified_readability)
        verified_scores.append(verified_readability)

        readability_rows.append({
            "record_id": index,
            "original_flesch":
                original_readability["flesch_reading_ease"],
            "unverified_flesch":
                unverified_readability["flesch_reading_ease"],
            "verified_flesch":
                verified_readability["flesch_reading_ease"],
            "original_fk_grade":
                original_readability["fk_grade"],
            "verified_fk_grade":
                verified_readability["fk_grade"],
            "original_fog":
                original_readability["gunning_fog"],
            "verified_fog":
                verified_readability["gunning_fog"],
            "original_smog":
                original_readability["smog"],
            "verified_smog":
                verified_readability["smog"]
        })

        # Faithfulness evaluation
        baseline_faithful = verification["verification_passed"]

        final_check = verify_simplification(
            original, verified
        )

        pipeline_faithful = final_check["verification_passed"]

        faithfulness_rows.append({
            "record_id": index,
            "unverified_faithful": baseline_faithful,
            "verified_pipeline_faithful": pipeline_faithful
        })

    # -------------------------------------------------
    # 9. FIELD-WISE EXTRACTION METRICS
    # -------------------------------------------------

    extraction_results = []

    for field in fields:

        result = calculate_metrics(
            counts[field]["tp"],
            counts[field]["fp"],
            counts[field]["fn"]
        )

        extraction_results.append({
            "field": field,
            **result
        })

    # -------------------------------------------------
    # 10. AVERAGE READABILITY
    # -------------------------------------------------

    def average_scores(score_list):

        keys = [
            "flesch_reading_ease",
            "fk_grade",
            "gunning_fog",
            "smog"
        ]

        return {
            key: round(
                sum(item[key] for item in score_list)
                / len(score_list), 2
            )
            for key in keys
        }

    readability_summary = {
        "original": average_scores(original_scores),
        "unverified": average_scores(unverified_scores),
        "verified": average_scores(verified_scores)
    }

    readability_results = []

    for baseline, scores in readability_summary.items():

        readability_results.append({
            "baseline": baseline,
            **scores
        })

    # -------------------------------------------------
    # 11. FAITHFULNESS PERCENTAGE
    # -------------------------------------------------

    total = len(faithfulness_rows)

    baseline_pass = sum(
        row["unverified_faithful"]
        for row in faithfulness_rows
    )

    pipeline_pass = sum(
        row["verified_pipeline_faithful"]
        for row in faithfulness_rows
    )

    faithfulness_summary = {
        "unverified_percentage":
            round(baseline_pass / total * 100, 2),

        "verified_pipeline_percentage":
            round(pipeline_pass / total * 100, 2),

        "verification_interventions": interventions
    }

    # -------------------------------------------------
    # 12. SAVE ALL RESULTS
    # -------------------------------------------------

    save_csv("extraction_metrics.csv", extraction_results)

    save_csv("readability_comparison.csv", readability_rows)

    save_csv("readability_summary.csv", readability_results)

    save_csv("faithfulness_metrics.csv", faithfulness_rows)

    save_csv("evaluation_summary.csv", [
        {
            "metric": key,
            "value": value
        }
        for key, value in faithfulness_summary.items()
    ])

    create_readability_chart(readability_summary)

    # -------------------------------------------------
    # 13. PRINT RESULTS
    # -------------------------------------------------

    print("\n" + "=" * 55)
    print("MEDICAL PRESCRIPTION SIMPLIFIER - EVALUATION")
    print("=" * 55)

    print("\nTOTAL TEST RECORDS:", total)

    print("\nEXTRACTION METRICS")

    for result in extraction_results:
        print(result)

    print("\nREADABILITY SUMMARY")

    for baseline, scores in readability_summary.items():
        print(baseline, ":", scores)

    print("\nFAITHFULNESS SUMMARY")

    print(faithfulness_summary)

    print("\nREADABILITY ENGINE:",
          "textstat" if TEXTSTAT_AVAILABLE else "Built-in fallback")

    print("\nALL EVALUATION FILES GENERATED SUCCESSFULLY!")


if __name__ == "__main__":
    run_evaluation()
