import urllib.request
import json
import sys

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
                
        print(f"[OK] Finished: {file_name}")
        return True
    except Exception as e:
        print(f"[FAIL] Could not download {file_name}: {e}")
        return False

if __name__ == "__main__":
    base_url = "https://raw.githubusercontent.com/electricgoat/ba-data/refs/heads/jp/DB"
    
    files_to_get = [
        "AcademyMessangerExcelTable.json",
        "CharacterExcelTable.json",
        "ScenarioScriptExcelTable1.json",
        "ScenarioScriptExcelTable2.json",
        "EventContentMeetupExcelTable.json",
        "EventContentScenarioExcelTable.json",
        "ScenarioModeExcelTable.json",
        "ScenarioCharacterNameExcelTable.json",
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
        sys.exit(1)