import urllib.request
import argparse

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def download_file(file_info):
    url, destination = file_info
    file_name = destination.name
    
    try:
        print(f"Starting download: {file_name}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req) as response:
            with open(destination, 'wb') as out_file:
                out_file.write(response.read())
        print(f"✅ Finished: {file_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {file_name}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        required=True,
        help="Base URL of the files",
    )
    args = parser.parse_args()
    base_url = args.base_url
    
    files_to_get = [
        "AcademyMessanger.json",
        "Character.json",
        "ScenarioScript.json"
    ]
    
    output_dir = Path("Excels")
    output_dir.mkdir(exist_ok=True)

    tasks = [
        (f"{base_url}/{name}", output_dir / name) 
        for name in files_to_get
    ]

    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        results = list(executor.map(download_file, tasks))

    if all(results):
        print("\nAll files downloaded successfully.")
    else:
        print("\nSome downloads failed.")