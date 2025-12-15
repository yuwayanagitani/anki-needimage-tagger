# NeedImage Tagger

AnkiWeb: https://ankiweb.net/shared/by-author/2117859718

NeedImageTagger scans your notes and adds a tag (default: `NeedImage`) when a note likely needs an image. A note is tagged only if it contains enough configured keywords and does not already include an `<img>` tag.

## Features
- Detects candidate notes for image addition using keyword matching
- Skips notes that already contain images
- Configurable keywords, required count and tag name

## Installation
1. Tools → Add-ons → Open Add-ons Folder.
2. Copy the add-on into `addons21/`.
3. Restart Anki.

## Usage
- Tools → NeedImage Tagger → Scan selected notes or whole collection.
- Tags are applied to notes; use the Browser to review `tag:NeedImage`.

## Configuration
`config.json` contains:
- keywords (array)
- threshold (minimum keyword hits)
- tag_name (default `NeedImage`)

Example:
```json
{
  "keywords": ["diagram", "illustrate", "image", "map"],
  "threshold": 2,
  "tag_name": "NeedImage"
}
```

## Issues & Support
Report false positives/negatives and include example notes or regex rules you wish supported.

## License
See LICENSE.
