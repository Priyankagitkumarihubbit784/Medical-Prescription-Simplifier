
import re


# Common medical and complex word replacements
WORD_REPLACEMENTS = {
    "administer": "give",
    "administered": "given",
    "administering": "giving",
    "oral": "by mouth",
    "orally": "by mouth",
    "consume": "take",
    "consumption": "taking",
    "medication": "medicine",
    "medicinal": "medical",
    "physician": "doctor",
    "pharmaceutical": "medicine",
    "discontinue": "stop",
    "terminate": "stop",
    "commence": "start",
    "subsequent": "next",
    "approximately": "about",
    "drowsiness": "sleepiness",
    "adverse": "unwanted",
    "symptoms": "signs",
    "contraindicated": "not recommended",
    "sufficient": "enough",
    "immediately": "right away",
    "frequently": "often",
    "additional": "extra",
    "observe": "watch",
    "consult": "ask",
    "physician's": "doctor's"
}


# Phrase replacements
PHRASE_REPLACEMENTS = {
    "twice daily": "two times a day",
    "three times daily": "three times a day",
    "once daily": "one time a day",
    "once a day": "one time a day",
    "twice a day": "two times a day",
    "three times a day": "three times a day",
    "at bedtime": "before going to sleep",
    "avoid alcohol": "do not drink alcohol",
    "avoid driving": "do not drive",
    "side effects": "possible unwanted effects",
    "take orally": "take by mouth",
    "for oral use": "to be taken by mouth",
    "as directed": "as instructed"
}


def replace_phrases(text):
    """Replace common complex medical phrases."""

    for old, new in PHRASE_REPLACEMENTS.items():
        pattern = r"\b" + re.escape(old) + r"\b"
        text = re.sub(pattern, new, text, flags=re.IGNORECASE)

    return text


def replace_words(text):
    """Replace complex medical vocabulary."""

    for old, new in WORD_REPLACEMENTS.items():
        pattern = r"\b" + re.escape(old) + r"\b"
        text = re.sub(pattern, new, text, flags=re.IGNORECASE)

    return text


def preserve_critical_information(original, simplified):
    """
    Check whether important numeric instructions remain unchanged.

    This is a preliminary safeguard, not a complete clinical
    equivalence check. The verification module performs
    additional checks.
    """

    numbers = re.findall(
        r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|g|ml|IU|days?|weeks?|months?)?\b",
        original,
        flags=re.IGNORECASE
    )

    for number in numbers:
        if number.lower() not in simplified.lower():
            return False

    return True


def simplify_text(text):
    """
    Main text simplification function.

    Uses rule-based simplification.
    If anything goes wrong, returns the original text.
    """

    if not isinstance(text, str) or not text.strip():
        return "Please enter medical text."

    original = text.strip()

    try:
        simplified = replace_phrases(original)
        simplified = replace_words(simplified)

        simplified = re.sub(r"\s+", " ", simplified).strip()

        # Preliminary preservation check
        if not preserve_critical_information(original, simplified):
            return original

        return simplified

    except Exception:
        # Safe fallback
        return original


# Testing
if __name__ == "__main__":

    original_text = (
        "Administer one tablet orally twice daily for seven days. "
        "Avoid alcohol during treatment. "
        "The medication may cause nausea and dizziness."
    )

    simplified_text = simplify_text(original_text)

    print("\nORIGINAL TEXT:")
    print(original_text)

    print("\nSIMPLIFIED TEXT:")
    print(simplified_text)

    print("\nPRESERVATION CHECK:")
    print(
        preserve_critical_information(
            original_text,
            simplified_text
        )
    )
