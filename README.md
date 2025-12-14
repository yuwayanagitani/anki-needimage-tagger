# NeedImageTagger

NeedImageTagger scans your notes and adds a tag (default: `NeedImage`) when a note likely needs an image. A note is tagged only if it contains enough configured keywords and does not already include an image (`<img>`).

## Features
- Heuristics to detect notes that would benefit from images.
- Configurable keyword lists and threshold.
- Avoids tagging notes that already include images.

## Requirements
- Anki 2.1+
- Works within Anki’s Python environment.

## Installation
1. Download or clone the repository.
2. Open Anki → Tools → Add-ons → Open Add-ons Folder.
3. Place the add-on directory inside the add-ons folder.
4. Restart Anki.

## Usage
- Run the add-on from the Tools → Add-ons menu or via the Browser add-on menu (depending on UI).
- The add-on will scan notes according to the configured keywords and tag matches with the configured tag (default `NeedImage`).

## Configuration
A configuration panel (or `config.json` depending on version) allows you to:
- Set the tag name (default `NeedImage`)
- Define keywords or keyword groups
- Set the minimum match threshold required to tag a note

Example config snippet:
```json
{
  "tag": "NeedImage",
  "keywords": ["diagram", "illustrate", "example"],
  "threshold": 2
}
```

## Troubleshooting
- If notes aren't being tagged, check that your keyword list and threshold are appropriate.
- Ensure notes do not already contain `<img>` tags.

## Development & Contributing
- Open issues for feature requests or bugs. Pull requests welcome.

## License
MIT License — see LICENSE file.

## Contact
Author: yuwayanagitani
