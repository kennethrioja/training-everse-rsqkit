import csv
import json
import sys
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print("Usage: 'python csv-to-json.py <input_dir> <output_dir>'")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)
    mapping_path = Path("mapping-colnames.json")

    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    for csv_file in input_dir.glob("*.csv"):
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            mapped_fields = [k for k in mapping if k in reader.fieldnames]
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

if __name__ == "__main__":
    main()
