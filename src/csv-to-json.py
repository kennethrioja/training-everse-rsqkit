import csv
import yaml
import json
import re
from pathlib import Path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def is_valid_url(url):
    pattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'
    return bool(re.match(pattern, url))

def main():
    input_dir = Path('csv')
    output_dir = Path('json')
    output_dir.mkdir(parents=True, exist_ok=True)
    mapping_path = Path('src/config.yaml')

    with open(mapping_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    spreadsheet_entries = config['spreadsheet']
    skip = []
    for e in spreadsheet_entries:
        if e['skip'] is True:
            skip.append(e['name'])

    mapping_list = config['mapping']
    mapping = {item['tess']: item['schema'] for item in mapping_list}

    for csv_file in input_dir.glob('*.csv'):
        name = str(csv_file).removeprefix('csv/').removesuffix('.csv')
        if name in skip:
            continue

        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            mapped_fields = [k for k in mapping if k in reader.fieldnames]
            materials = []

            for row in reader:
                resource = {
                    '@context': 'https://schema.org',
                    '@type': next(
                        (entry.get("schemaType") for entry in spreadsheet_entries if entry.get("name") == name),
                        None
                        )
                }
                for src_key in mapped_fields:
                    dst_key = mapping[src_key]
                    value = row.get(src_key, '').strip()
                    if value:
                        resource[dst_key] = value
                        if dst_key == "URL" and not is_valid_url(value):
                            print(f"{bcolors.WARNING}[URL {resource.__len__}/{len(reader)}]{bcolors.ENDC} URL is wrong for {resource.get("name")}")
                materials.append(resource)
                print(f"{bcolors.OKGREEN}[SUCCESS {resource.__len__}/{len(reader)}]{bcolors.ENDC} Added {resource.get("name")}")

        output_path = output_dir / f'{csv_file.stem}.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(materials, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
