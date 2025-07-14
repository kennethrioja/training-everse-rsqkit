import csv
import json
import os
from pathlib import Path

# Config paths
mapping_path = Path("mapping.json")
input_dir = Path("raw")
output_dir = Path("jsonld")
output_dir.mkdir(exist_ok=True)

# Load mapping
with open(mapping_path, "r", encoding="utf-8") as f:
    mapping = json.load(f)

# Process each CSV in raw/
for csv_file in input_dir.glob("*.csv"):
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        mapped_fields = [k for k in mapping if k in reader.fieldnames]
        output_fields = [mapping[k] for k in mapped_fields]

        materials = []
        for row in reader:
            resource = {
                "@context": "https://schema.org",
                "@type": "LearningResource"
            }
            for src_key in mapped_fields:
                dst_key = mapping[src_key]
                value = row.get(src_key, "").strip()
                if value:
                    resource[dst_key] = value
            materials.append(resource)

    output_path = output_dir / f"{csv_file.stem}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(materials, f, indent=2, ensure_ascii=False)
