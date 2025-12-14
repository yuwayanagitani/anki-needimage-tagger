# NeedImage Tagger – Configuration Guide

NeedImage Tagger is an add-on that  
**automatically detects notes that would benefit from an image and adds a `NeedImage` tag.**

It scans all fields in a note and marks it as “needs image” when:

- There is **no `<img>` tag** in any field, and  
- The configured **keywords** appear **at least a certain number of times**.

<br>

## 🔧 Settings (`config.json`)

### **need_image_tag**

The name of the tag to add when a note needs an image.  
Default: `"NeedImage"`

<br>

### **keywords**

A list of keywords used to decide whether a note probably needs an image.  
All text fields of the note are scanned.

Example:

```
"keywords": ["ct", "mri", "xray", "echo", "anatomy"]
```

<br>

### **min_keyword_hits**

How many keyword hits are required before the note is considered as `NeedImage`.

Examples:

- `1` (default) → one or more keyword matches is enough
- `2` → only notes where **two or more** keywords are found are tagged

<br>

### **case_sensitive**

Whether to treat upper/lower case as different.

- `false` (default)
- `true`

<br>

### **remove_tag_if_resolved**

Whether to automatically remove the `NeedImage` tag when an `<img>` is later added.

- `true` (default)
- `false`

<br>

### **use_regex**

Controls how keywords are matched.

- `true` → word-boundary regex (`\bkeyword\b`)
- `false` → simple substring match

<br>

## 🔍 How to Run

**Tools → Add NeedImage Tag…**

Search syntax is the same as the Anki Browser.

Examples:

```
deck:Anatomy
tag:PCOS
deck:"Year 4 Medicine" tag:"renal failure"
```

<br>

## ⚠ Tips

Short keywords (e.g., `"ct"`) may cause false positives.  
Solutions:

- Use more specific keywords  
- Enable regex mode  
- Increase `min_keyword_hits`

<br>

## 📌 Recommended Default Settings

```
{
  "need_image_tag": "NeedImage",
  "keywords": [
    "ct",
    "mri",
    "x-ray",
    "xray",
    "ultrasound",
    "echo",
    "ecg",
    "ekg"
  ],
  "min_keyword_hits": 1,
  "case_sensitive": false,
  "use_regex": true,
  "remove_tag_if_resolved": true
}
```

