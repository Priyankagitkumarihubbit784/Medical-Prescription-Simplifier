
import re


def clean_text(text):
    """Normalize common OCR formatting issues."""

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    # Separate letters and numbers when OCR removes their space.
    # Example: DemoMed-A260 mg -> DemoMed-A 260 mg
    text = re.sub(
        r"([A-Za-z])(\d)",
        r"\1 \2",
        text
    )

    return text.strip()


def extract_drug_name(text):
    pattern = (
        r"\b([A-Za-z][A-Za-z0-9-]*)\s+"
        r"(?=\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|%|IU)\b)"
    )

    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(1) if match else "Not identified"


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
    """Extract actual warnings while ignoring test disclaimers."""

    warning_keywords = [
        "warning:",
        "caution:",
        "avoid",
        "do not",
        "don't",
        "keep away",
        "never"
    ]

    disclaimer_keywords = [
        "fictional",
        "software testing",
        "not a real prescription",
        "do not use for real medication"
    ]

    # Split text into individual sentences
    sentences = re.split(r"[\n.!?]+", text)

    warnings = []

    for sentence in sentences:
        sentence = sentence.strip()
        lower_sentence = sentence.lower()

        if not sentence:
            continue

        # Ignore fictional or testing-related disclaimers
        if any(
            phrase in lower_sentence
            for phrase in disclaimer_keywords
        ):
            continue

        # Extract actual warning statements
        if any(
            keyword in lower_sentence
            for keyword in warning_keywords
        ):
            warnings.append(sentence)

    return warnings if warnings else ["Not identified"]


def extract_side_effects(text):
    pattern = (
        r"(?:possible\s+side\s+effects?|side\s+effects?|"
        r"may cause|can cause)"
        r"\s*:?\s*(?:include\s+)?(.*?)(?:[.!?]|\n|$)"
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
