import json
import subprocess
from pathlib import Path
import sys

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

def main():
    if len(sys.argv) != 3:
        print(f"{bcolors.WARNING}Usage: 'python download-csv.py {bcolors.BOLD}<path_to_gid.json> <output_dir>'")
        sys.exit(1)

    # Paths
    gid_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load JSON
    with open(gid_path, "r", encoding="utf-8") as f:
        gid_data = json.load(f)
    spreadsheet_id = gid_data.get("id")

    # Download each sheet
    for name, gid in gid_data.items():
        if name == "id":
            continue

        url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?gid={gid}&exportFormat=csv"
        output_file = output_dir / f"{name}_google.csv"
        print(f"{bcolors.OKBLUE}[INFO]{bcolors.ENDC} Fetching '{name}' from gid {gid}...")

        try:
            result = subprocess.run(["curl", "-L", url, "-o", str(output_file)], check=True, capture_output=True)
            print(f"{bcolors.OKGREEN}[SUCCESS]{bcolors.ENDC} Saved to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"{bcolors.FAIL}[FAILED]{bcolors.ENDC} Could not download '{name}'")
            print(f"{bcolors.WARNING}URL:{bcolors.ENDC} {url}")
            print(f"{bcolors.WARNING}Curl stderr:{bcolors.ENDC} {e.stderr.decode().strip()}")

if __name__ == "__main__":
    main()