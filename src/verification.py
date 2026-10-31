
import re

from src.extraction import extract_medical_information


def normalize(value):
    """Normalize text for comparison."""
    return re.sub(r"\s+", " ", str(value).lower()).strip()


def normalize_frequency(value):
    """Treat common equivalent frequency phrases consistently."""

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


def extract_numeric_units(text):
    """Extract numerical values together with their units."""

    pattern = (
        r"\b\d+(?:\.\d+)?\s*"
        r"(?:mg|mcg|g|ml|iu|days?|weeks?|months?|hours?)?\b"
    )

    matches = re.findall(pattern, text, re.IGNORECASE)

    return [normalize(item) for item in matches]


def check_warning_preservation(original_warning, simplified_text):
    """
    Check whether important warning concepts are retained.
    This is a keyword-based check, not clinical validation.
    """

    warning = normalize(original_warning)
    output = normalize(simplified_text)

    warning_groups = [
        ["alcohol"],
        ["driving", "drive"],
        ["drowsy", "sleepy", "sleepiness"],
        ["children", "child"],
        ["exceed", "more than"],
        ["expiry", "expired"],
        ["sunlight"],
        ["dry place"],
        ["share"],
    ]

    for group in warning_groups:
        source_has_concept = any(word in warning for word in group)

        if source_has_concept:
            output_has_concept = any(
                word in output for word in group
            )

            if not output_has_concept:
                return False

    return True


def check_side_effect_preservation(original_effects, simplified_text):
    """
    Check whether the listed side-effect terms remain present.
    """

    effects = normalize(original_effects)
    output = normalize(simplified_text)

    synonym_groups = [
        ["nausea"],
        ["dizziness", "dizzy"],
        ["headache"],
        ["sleepiness", "drowsiness", "sleepy"],
        ["vomiting", "vomit"],
        ["rash"],
    ]

    for group in synonym_groups:
        source_has_effect = any(word in effects for word in group)

        if source_has_effect:
            output_has_effect = any(
                word in output for word in group
            )

            if not output_has_effect:
                return False

    return True


def verify_simplification(original_text, simplified_text):
    """
    Main verification function.

    Compares extracted information and critical values.
    Returns the original text as safe output if any
    required verification check fails.
    """

    original_data = extract_medical_information(original_text)

    simplified_data = extract_medical_information(simplified_text)

    checks = {}

    # 1. Drug name
    source_drug = normalize(original_data["drug_name"])
    output_drug = normalize(simplified_data["drug_name"])

    checks["drug_name"] = (
        source_drug == "not identified"
        or source_drug == output_drug
    )

    # 2. Strength
    source_strength = normalize(original_data["strength"])
    output_strength = normalize(simplified_data["strength"])

    checks["strength"] = (
        source_strength == "not identified"
        or source_strength == output_strength
    )

    # 3. Dosage
    source_dosage = normalize(original_data["dosage"])
    output_dosage = normalize(simplified_data["dosage"])

    checks["dosage"] = (
        source_dosage == "not identified"
        or source_dosage == output_dosage
    )

    # 4. Frequency
    source_frequency = normalize_frequency(
        original_data["frequency"]
    )

    output_frequency = normalize_frequency(
        simplified_data["frequency"]
    )

    checks["frequency"] = (
        source_frequency == "not identified"
        or source_frequency == output_frequency
    )

    # 5. Duration
    source_duration = normalize(
        original_data["duration"].replace("for ", "")
    )

    output_duration = normalize(
        simplified_data["duration"].replace("for ", "")
    )

    checks["duration"] = (
        source_duration == "not identified"
        or source_duration == output_duration
    )

    # 6. Numeric values and units
    source_numbers = extract_numeric_units(original_text)
    output_numbers = extract_numeric_units(simplified_text)

    checks["numeric_values"] = all(
        number in output_numbers for number in source_numbers
    )

    # 7. Warnings
    source_warnings = original_data["warnings"]

    if source_warnings == ["Not identified"]:
        checks["warnings"] = True
    else:
        checks["warnings"] = all(
            check_warning_preservation(warning, simplified_text)
            for warning in source_warnings
        )

    # 8. Side effects
    source_effects = original_data["side_effects"]

    if source_effects == "Not identified":
        checks["side_effects"] = True
    else:
        checks["side_effects"] = check_side_effect_preservation(
            source_effects,
            simplified_text
        )

    # Overall result
    verification_passed = all(checks.values())

    # Fail-safe output
    safe_output = (
        simplified_text if verification_passed else original_text
    )

    return {
        "verification_passed": verification_passed,
        "checks": checks,
        "safe_output": safe_output,
        "original_information": original_data,
        "simplified_information": simplified_data
    }


# Test the verification module
if __name__ == "__main__":

    original = (
        "DemoMed-A 250 mg. "
        "Take one tablet orally twice daily for 5 days. "
        "Warning: Avoid driving if drowsy. "
        "Side effects include nausea and dizziness."
    )

    simplified = (
        "DemoMed-A 250 mg. "
        "Take one tablet by mouth two times a day for 5 days. "
        "Warning: Do not drive if sleepy. "
        "Possible unwanted effects include nausea and dizziness."
    )

    result = verify_simplification(original, simplified)

    print("\nFAITHFULNESS VERIFICATION")
    print("=" * 45)

    for field, status in result["checks"].items():
        print(f"{field}: {'PASS' if status else 'FAIL'}")

    print("\nOVERALL RESULT:")
    print("PASS" if result["verification_passed"] else "FAIL")

    print("\nSAFE OUTPUT:")
    print(result["safe_output"])
