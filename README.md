# Anki NeedImage Tagger

🔗 **AnkiWeb**  
https://ankiweb.net/shared/info/287405236

---

## What this add-on does

**Anki NeedImage Tagger** automatically tags cards that are likely to **benefit from an image**.  
It helps you quickly identify text-only cards where adding a diagram, photo, or figure would improve understanding.

This add-on is especially useful for:

- Medical and biological subjects
- Anatomy, pathology, histology, radiology
- Any topic where **visual information matters**

---

## Core Features

- 🖼 Automatically assigns a **“need image” tag** to cards
- 🔍 Detects cards with insufficient visual content
- 🏷 Fully customizable tag name
- 🔁 Dynamic tagging (tags can be added or removed)
- 🪶 Lightweight and fast
- 🧩 Works with any deck and note type

---

## How It Works

1. The add-on inspects configured fields of a card
2. It checks whether images are present
3. If no image is detected, a **NeedImage tag** is added
4. If an image is later added, the tag can be removed automatically

This keeps your collection visually optimized over time.

---

## Why Use NeedImage Tags?

Using this add-on allows you to:

- Create filtered decks such as:
  - `tag:needimage`
- Systematically improve card quality
- Prioritize cards that need diagrams or figures
- Avoid missing important visual learning opportunities

It turns “I should add an image later” into a **trackable workflow**.

---

## Installation

### From AnkiWeb (recommended)

1. Open Anki  
2. Tools → Add-ons → Get Add-ons  
3. Enter the code from AnkiWeb  
4. Restart Anki  

👉 https://ankiweb.net/shared/info/287405236

---

### Manual (GitHub)

1. Download or clone this repository
2. Place it in:

   `Anki2/<profile>/addons21/anki-needimage-tagger/`

3. Restart Anki

---

## Configuration

Open:

**Tools → Add-ons → Anki NeedImage Tagger → Config**

Available options include:

- Enable / disable tagging
- Target fields to inspect
- Tag name (default: `needimage`)
- Whether to remove the tag when an image is added
- Scope (review-time / batch processing)

---

## Usage

- Review cards normally, or
- Run the add-on on selected cards in the Browser

Tagged cards can then be reviewed, edited, or grouped into filtered decks for image enrichment.

---

## Performance & Safety

- No background polling
- No network or AI usage
- Does **not** modify scheduling or intervals
- Safe for large collections

---

## Compatibility

- Anki 24.x  
- Anki 25.x  
- Windows / macOS / Linux  

---

## License

MIT License

---

## Author

Created by **@yuwayanagitani**

---

## Related Add-ons

- **Anki Difficulty Tagger** – Automatically tag card difficulty
- **Anki Bar Graph** – Visualize recent review activity
- **HTML Exporter for Anki** – Export cards to HTML / PDF

These add-ons together support a **systematic, high-quality Anki card workflow**.
