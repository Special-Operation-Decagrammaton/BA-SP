# Blue Archive Scenario Parser

Parses Blue Archive (JP) scenario data into per-story TOML files for easier access and readable story content.

## Output

| Folder | Content |
|---|---|
| `CharacterScenario/` | Character Momotalk scenario stories, one folder per character (`{Id}_{DevName}/`) |
| `CharacterMessanger/` | Character Momotalk messages, one file per character |
| `CharacterValentine/` | Character valentine stories |
| `MainStory/` | Campaign stories: `Main`, `Prologue`, `SpecialOperation`, `Sub`, `Mini` — organized as `{ModeType}/{SubType}/{VolumeId}/{ChapterId}/{GroupId}_{Episode}.toml` |

Character Ids / DevNames can be looked up at:

- [SchaleDB](https://schaledb.com/home)
- [Rentry Paste](https://rentry.org/qewdu)

## Usage

Requires Python 3.13+.

```bash
pip install -r requirements.txt

# Download the Excel tables from electricgoat/ba-data (jp) into ./Excels
python get_excel.py

# Parse everything into the output folders
python parse.py
```

Source data: [electricgoat/ba-data](https://github.com/electricgoat/ba-data/tree/jp/DB) (`jp` branch).
