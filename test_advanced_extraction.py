
import re


def clean_text(text):
    """Normalize whitespace while preserving important medical information."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def extract_drug_name(text):
    """Extract a drug-like name before its strength."""

    pattern = (
        r"\b([A-Za-z][A-Za-z0-9-]*)\s+"
        r"(?=\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|%|IU)\b)"
    )

    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(1).strip() if match else "Not identified"


def extract_strength(text):
    pattern = (
        r"\b\d+(?:\.\d+)?\s*"
        r"(?:mg|mcg|g|ml|%|IU)\b"
    )

    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(0) if match else "Not identified"


def extract_dosage(text):
    pattern = (
        r"\b(?:one|two|three|four|\d+)\s+"
        r"(?:tablet|tablets|capsule|capsules|"
        r"teaspoon|teaspoons|drops|puff|puffs|"
        r"ml|milliliters?)\b"
    )

    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(0) if match else "Not identified"


def extract_frequency(text):
    patterns = [
        r"\btwice daily\b",
        r"\bthree times daily\b",
        r"\bonce daily\b",
        r"\bevery morning\b",
        r"\bevery evening\b",
        r"\bat bedtime\b",
        r"\bonce a day\b",
        r"\btwice a day\b",
        r"\bthree times a day\b",
        r"\bevery \d+ hours?\b",
        r"\btwo times a day\b",
        r"\bone time a day\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(0)

    return "Not identified"


def extract_duration(text):
    pattern = (
        r"\b(?:for\s+)?\d+\s*"
        r"(?:days?|weeks?|months?)\b"
    )

    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(0) if match else "Not identified"


def extract_warnings(text):
    warning_keywords = [
        "avoid",
        "warning",
        "do not",
        "don't",
        "caution",
        "keep away",
        "store away",
        "not use",
        "never"
    ]

    sentences = re.split(r"(?<=[.!?])\s+", text)

    warnings = [
        sentence.strip()
        for sentence in sentences
        if any(
            word in sentence.lower()
            for word in warning_keywords
        )
    ]

    return warnings if warnings else ["Not identified"]


def extract_side_effects(text):
    """Extract side effects without retaining the word 'include'."""

    pattern = (
        r"(?:side effects?"
        r"(?:\s+(?:may\s+include|include))?"
        r"|possible side effects?"
        r"(?:\s+(?:may\s+include|include))?"
        r"|may cause|can cause)"
        r"\s*:?\s*(.*?)(?:[.!?]|$)"
    )

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        result = match.group(1).strip()

        result = re.sub(
            r"^include\s+",
            "",
            result,
            flags=re.IGNORECASE
        )

        return result if result else "Not identified"

    return "Not identified"


def extract_medical_information(text):
    """
    Extract seven medical information fields.
    Keeps the existing output structure compatible with Flask.
    """

    text = clean_text(text)

    information = {
        "drug_name": extract_drug_name(text),
        "strength": extract_strength(text),
        "dosage": extract_dosage(text),
        "frequency": extract_frequency(text),
        "duration": extract_duration(text),
        "warnings": extract_warnings(text),
        "side_effects": extract_side_effects(text)
    }

    return information


if __name__ == "__main__":

    sample_text = (
        "DemoMed-A 250 mg. "
        "Take one tablet orally twice daily for 5 days. "
        "Warning: Avoid driving if drowsy. "
        "Side effects include nausea and dizziness."
    )

    result = extract_medical_information(sample_text)

    print("\nMEDICAL INFORMATION EXTRACTION")
    print("=" * 45)

    for field, value in result.items():
        print(f"{field}: {value}")
