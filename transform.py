import csv
import json
import os
from pathlib import Path

# File paths
mapping_json = "mapping.json"
input_dir = Path("raw")
output_dir = Path("ingestion_ready")
output_dir.mkdir(exist_ok=True)

# Load mapping
with open(mapping_json, "r", encoding="utf-8") as f:
    mapping = json.load(f)

# Process each CSV in raw/
for csv_file in input_dir.glob("*.csv"):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        filtered_rows = []
        for row in reader:
            filtered_row = {mapping[key]: row[key] for key in mapping if key in row}
            filtered_rows.append(filtered_row)

    output_file = output_dir / f"{csv_file.stem}_ready.csv"
    with open(output_file, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[mapping[k] for k in mapping if k in reader.fieldnames])
        writer.writeheader()
        writer.writerows(filtered_rows)
