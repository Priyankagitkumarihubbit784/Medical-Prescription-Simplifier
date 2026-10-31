
from src.batch_processor import process_batch, create_batch_csv

from pathlib import Path


files = []

test_file = Path("test_prescription.png")

if test_file.exists():

    files.append((
        test_file.name,
        test_file.read_bytes()
    ))

else:
    print("Test image not found.")
    raise SystemExit


results = process_batch(files)

print("\nBATCH PROCESSING RESULTS")
print("=" * 45)

for result in results:

    print("\nFile:", result["filename"])
    print("Status:", result["status"])

    if result["status"] == "Processed":

        print("Drug:", result["extracted"].get("drug_name"))
        print("Completeness:", result["completeness"], "%")
        print("Verification:", result["verification_passed"])

    else:
        print("Error:", result["error"])


csv_data = create_batch_csv(results)

Path("batch_results.csv").write_bytes(csv_data)

print("\nCSV report saved as batch_results.csv")
