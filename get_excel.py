import urllib.request
import argparse
import json

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def download_file(file_info):
    url, destination = file_info
    file_name = destination.name
    
    try:
        print(f"Starting download: {file_name}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req) as response:
            parsed_json = json.loads(response.read().decode('utf-8'))
            with open(destination, 'w', encoding='utf-8') as out_file:
                json.dump(parsed_json, out_file, ensure_ascii=False, indent=2)
                
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
        "ScenarioScript.json",
        "EventContentMeetup.json"
        # "ScenarioMode.json" > TODO
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