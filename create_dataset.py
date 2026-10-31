
import csv
import os

os.makedirs("data/raw", exist_ok=True)

dataset = [
    {
        "original_text": "DemoMed-A 250 mg. Take one tablet orally twice daily for 5 days. Warning: Avoid driving if drowsy. Side effects include nausea and dizziness.",
        "drug_name": "DemoMed-A",
        "strength": "250 mg",
        "dosage": "one tablet",
        "frequency": "twice daily",
        "duration": "5 days",
        "warnings": "Avoid driving if drowsy",
        "side_effects": "nausea and dizziness"
    },
    {
        "original_text": "DemoMed-B 100 mg. Administer one capsule once daily for 7 days. Warning: Avoid alcohol. Side effects may include headache.",
        "drug_name": "DemoMed-B",
        "strength": "100 mg",
        "dosage": "one capsule",
        "frequency": "once daily",
        "duration": "7 days",
        "warnings": "Avoid alcohol",
        "side_effects": "headache"
    },
    {
        "original_text": "DemoMed-C 500 mg. Take two tablets orally three times daily for 3 days. Warning: Do not exceed the stated amount. Side effects include nausea.",
        "drug_name": "DemoMed-C",
        "strength": "500 mg",
        "dosage": "two tablets",
        "frequency": "three times daily",
        "duration": "3 days",
        "warnings": "Do not exceed the stated amount",
        "side_effects": "nausea"
    },
    {
        "original_text": "DemoMed-D 50 mg. Take one tablet every morning for 10 days. Warning: Store away from children. Side effects may include dizziness.",
        "drug_name": "DemoMed-D",
        "strength": "50 mg",
        "dosage": "one tablet",
        "frequency": "every morning",
        "duration": "10 days",
        "warnings": "Store away from children",
        "side_effects": "dizziness"
    },
    {
        "original_text": "DemoMed-E 200 mg. Take one capsule twice daily for 14 days. Warning: Avoid driving if sleepy. Side effects include headache and nausea.",
        "drug_name": "DemoMed-E",
        "strength": "200 mg",
        "dosage": "one capsule",
        "frequency": "twice daily",
        "duration": "14 days",
        "warnings": "Avoid driving if sleepy",
        "side_effects": "headache and nausea"
    },
    {
        "original_text": "DemoMed-F 10 mg. Take one tablet at bedtime for 5 days. Warning: Do not mix with alcohol. Side effects include sleepiness.",
        "drug_name": "DemoMed-F",
        "strength": "10 mg",
        "dosage": "one tablet",
        "frequency": "at bedtime",
        "duration": "5 days",
        "warnings": "Do not mix with alcohol",
        "side_effects": "sleepiness"
    },
    {
        "original_text": "DemoMed-G 25 mg. Take one tablet once daily for 6 days. Warning: Keep the medicine in a dry place. Side effects may include nausea.",
        "drug_name": "DemoMed-G",
        "strength": "25 mg",
        "dosage": "one tablet",
        "frequency": "once daily",
        "duration": "6 days",
        "warnings": "Keep the medicine in a dry place",
        "side_effects": "nausea"
    },
    {
        "original_text": "DemoMed-H 75 mg. Take one capsule every evening for 8 days. Warning: Avoid driving if dizzy. Side effects include dizziness.",
        "drug_name": "DemoMed-H",
        "strength": "75 mg",
        "dosage": "one capsule",
        "frequency": "every evening",
        "duration": "8 days",
        "warnings": "Avoid driving if dizzy",
        "side_effects": "dizziness"
    },
    {
        "original_text": "DemoMed-I 300 mg. Take one tablet twice daily for 4 days. Warning: Do not share this medicine. Side effects may include headache.",
        "drug_name": "DemoMed-I",
        "strength": "300 mg",
        "dosage": "one tablet",
        "frequency": "twice daily",
        "duration": "4 days",
        "warnings": "Do not share this medicine",
        "side_effects": "headache"
    },
    {
        "original_text": "DemoMed-J 150 mg. Take one capsule once daily for 9 days. Warning: Store away from direct sunlight. Side effects include nausea and sleepiness.",
        "drug_name": "DemoMed-J",
        "strength": "150 mg",
        "dosage": "one capsule",
        "frequency": "once daily",
        "duration": "9 days",
        "warnings": "Store away from direct sunlight",
        "side_effects": "nausea and sleepiness"
    },
    {
        "original_text": "DemoMed-K 400 mg. Take one tablet every morning for 12 days. Warning: Do not use after expiry. Side effects include dizziness.",
        "drug_name": "DemoMed-K",
        "strength": "400 mg",
        "dosage": "one tablet",
        "frequency": "every morning",
        "duration": "12 days",
        "warnings": "Do not use after expiry",
        "side_effects": "dizziness"
    },
    {
        "original_text": "DemoMed-L 20 mg. Take one tablet twice daily for 2 days. Warning: Keep away from children. Side effects may include headache.",
        "drug_name": "DemoMed-L",
        "strength": "20 mg",
        "dosage": "one tablet",
        "frequency": "twice daily",
        "duration": "2 days",
        "warnings": "Keep away from children",
        "side_effects": "headache"
    },
    {
        "original_text": "DemoMed-M 600 mg. Take one tablet once daily for 5 days. Warning: Do not exceed the stated amount. Side effects include nausea.",
        "drug_name": "DemoMed-M",
        "strength": "600 mg",
        "dosage": "one tablet",
        "frequency": "once daily",
        "duration": "5 days",
        "warnings": "Do not exceed the stated amount",
        "side_effects": "nausea"
    },
    {
        "original_text": "DemoMed-N 125 mg. Take one capsule every evening for 7 days. Warning: Avoid alcohol. Side effects include sleepiness and dizziness.",
        "drug_name": "DemoMed-N",
        "strength": "125 mg",
        "dosage": "one capsule",
        "frequency": "every evening",
        "duration": "7 days",
        "warnings": "Avoid alcohol",
        "side_effects": "sleepiness and dizziness"
    },
    {
        "original_text": "DemoMed-O 80 mg. Take one tablet at bedtime for 3 days. Warning: Do not drive if sleepy. Side effects include headache.",
        "drug_name": "DemoMed-O",
        "strength": "80 mg",
        "dosage": "one tablet",
        "frequency": "at bedtime",
        "duration": "3 days",
        "warnings": "Do not drive if sleepy",
        "side_effects": "headache"
    }
]

file_path = "data/raw/medical_dataset.csv"

with open(file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=dataset[0].keys())
    writer.writeheader()
    writer.writerows(dataset)

print("Dataset created successfully!")
print("Total records:", len(dataset))
print("Saved at:", file_path)
