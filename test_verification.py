
from src.verification import verify_simplification

original = (
    "DemoMed-A 250 mg. "
    "Take one tablet orally twice daily for 5 days. "
    "Warning: Avoid alcohol. "
    "Side effects include nausea."
)

# Test 1: Correct simplification
correct = (
    "DemoMed-A 250 mg. "
    "Take one tablet by mouth two times a day for 5 days. "
    "Warning: Do not drink alcohol. "
    "Possible unwanted effects include nausea."
)

# Test 2: Incorrect strength
incorrect = (
    "DemoMed-A 125 mg. "
    "Take one tablet by mouth two times a day for 5 days. "
    "Warning: Do not drink alcohol. "
    "Possible unwanted effects include nausea."
)

print("\nTEST 1: Correct simplification")

result1 = verify_simplification(original, correct)

print("Verification:", result1["verification_passed"])

print("\nTEST 2: Changed medicine strength")

result2 = verify_simplification(original, incorrect)

print("Verification:", result2["verification_passed"])
print("Safe output is original:",
      result2["safe_output"] == original)
