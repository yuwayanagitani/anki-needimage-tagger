# 🖼️ NeedImageTagger — Keyword-based “Needs Image” tagging for Anki

> **Quick idea:** scan notes, and if a note **mentions imaging keywords** (CT/MRI/X-ray…) but **doesn’t contain an `<img>` yet**, it gets tagged (default: **NeedImage**).  
> Perfect for building “add images later” queues without breaking your study flow.

---

## ✨ What this add-on does

- 🏷️ **Adds a tag** (default: `NeedImage`) to notes that likely need an image
- 🔍 Uses **keyword hits** (you choose the keywords + how many matches are required)
- 🧼 Optionally **removes the tag** when an image is found later (`<img>` detected)
- ⚡ Runs in the background with a progress indicator (won’t freeze Anki)

---

## 🚀 How to use

### 1) Run the scan
1. Open Anki
2. Go to **Tools → Add NeedImage Tag…**
3. Enter a search query (or leave blank = scan all notes)
4. Click OK ✅

You’ll see a summary like:
- Notes scanned
- Tags added
- Tags removed (if enabled)

### 2) Use Browser search to review
- `tag:NeedImage` → view everything waiting for images  
- Combine with decks/tags:
  - `deck:Radiology tag:NeedImage`
  - `deck:"Year 4 Medicine" tag:NeedImage`

---

## 🧠 Matching rules (simple + predictable)

A note is tagged **only if both** are true:

1. ✅ It contains **at least N keyword hits** (configurable)  
2. 🚫 It does **not** already contain an image (`<img` anywhere in the note)

### Keyword matching options
- 🔤 **Case sensitive**: on/off
- 🧩 **Whole word match (recommended)**:
  - `ct` matches “CT” / “ct” as a word, not as part of another word
  - Internally uses word boundaries (`\b...\b`)

---

## 🧰 Settings (GUI)

Open:
- **Tools → Add-ons → NeedImageTagger → Config**

### Tagging
- 🏷️ **Need image tag**: change tag name (e.g. `NeedImage::Radiology`)
- 🧹 **Remove tag if an image is found**: automatically clean up resolved notes

### Matching
- 🎯 **Minimum keyword hits**: require 1 / 2 / 3… matches before tagging
- 🔤 **Case sensitive**
- 🧩 **Match whole words (recommended)**

### Keywords (one per line)
Example list:
- `ct`
- `mri`
- `x-ray`
- `ultrasound`
- `ecg`

Tip: keep keywords short, focused, and consistent with your deck language.

---

## 🎨 Suggested workflows

### 🧪 “Image backlog” pipeline
1. Scan notes → tag `NeedImage`
2. In Browser, search `tag:NeedImage`
3. Add images gradually (or with another tool)
4. Re-scan → resolved notes auto-untagged ✅

### 🩺 Medical student mode
- Use keywords like: `ct`, `mri`, `us`, `doppler`, `angiography`, `ecg`
- Add tags per course deck:
  - `NeedImage::Cardio`
  - `NeedImage::Neuro`

---

## ⚠️ Notes / limitations

- This add-on checks for `<img` in the note fields (HTML).  
  If your note uses non-standard image embedding, adjust your templates/fields accordingly.
- “Whole word match” uses simple boundaries; for languages without spaces, consider disabling it and using substring matching.
- Very large collections: scanning *all notes* can take time — prefer using a Browser-style query to narrow scope.

---

## 🧩 Troubleshooting

### “Nothing happens” / no tags added
- ✅ Make sure **keywords** are not empty
- ✅ Try a smaller query first (e.g. `deck:YourDeck`)
- ✅ Check a note contains keywords but no `<img>`

### Settings don’t show
- If your Anki build is old and doesn’t support custom config dialogs, you can still edit the add-on’s config directly via the standard JSON editor.

---

## 📌 Versioning tip (for your GitHub releases)
If you publish on AnkiWeb, consider adding a short changelog section like:
- ✅ Added whole-word matching toggle
- ✅ Added auto-remove tag option
- ✅ Improved config GUI

Happy tagging! 🌈
