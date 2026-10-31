from src.extraction import extract_medical_information

text = """
DemoMed-B 100 mg.
Take one capsule once daily for 7 days.
Warning: Avoid alcohol.
Side effects may include headache.
"""

result = extract_medical_information(text)

for key, value in result.items():
    print(key, ":", value)