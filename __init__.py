from __future__ import annotations

import json
import os
import re
from typing import Any

from anki.collection import Collection
from anki.notes import Note
from aqt import gui_hooks, mw
from aqt.operations import QueryOp
from aqt.qt import (
    QAction,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)
from aqt.utils import getText, showInfo

ADDON_PACKAGE = __name__


# -------------------- config helpers --------------------

def get_config() -> dict[str, Any]:
    cfg = mw.addonManager.getConfig(ADDON_PACKAGE)
    if not isinstance(cfg, dict):
        return {}
    return cfg


def _load_packaged_defaults() -> dict[str, Any]:
    """
    Load default config from packaged config.json (the one shipped with the add-on).
    """
    # Newer Anki provides addonConfigDefaults()
    try:
        d = mw.addonManager.addonConfigDefaults(ADDON_PACKAGE)
        if isinstance(d, dict):
            return d
    except Exception:
        pass

    # Fallback: read config.json from add-on folder
    try:
        folder = mw.addonManager.addonFolder(ADDON_PACKAGE)
        path = os.path.join(folder, "config.json")
        with open(path, "r", encoding="utf-8") as f:
            d = json.load(f)
        if isinstance(d, dict):
            return d
    except Exception:
        pass

    # Last resort hardcoded defaults (should match your shipped config.json)
    return {
        "need_image_tag": "NeedImage",
        "keywords": ["ct", "mri", "x-ray", "xray", "ultrasound", "echo", "ecg", "ekg"],
        "min_keyword_hits": 1,
        "case_sensitive": False,
        "use_regex": True,
        "remove_tag_if_resolved": True,
    }


def _keywords_to_text(keywords: list[Any]) -> str:
    out: list[str] = []
    for k in keywords or []:
        if isinstance(k, str) and k.strip():
            out.append(k.strip())
    return "\n".join(out)


def _text_to_keywords(text: str) -> list[str]:
    out: list[str] = []
    for line in (text or "").splitlines():
        k = line.strip()
        if k:
            out.append(k)
    return out


# -------------------- core logic --------------------

def prepare_keywords(config: dict[str, Any]) -> tuple[list[str], bool, bool]:
    """Preprocess keyword list once."""
    case_sensitive = bool(config.get("case_sensitive", False))
    use_regex = bool(config.get("use_regex", True))
    raw_keywords = config.get("keywords", [])

    if not isinstance(raw_keywords, list) or not raw_keywords:
        return [], case_sensitive, use_regex

    processed: list[str] = []
    for k in raw_keywords:
        if not isinstance(k, str):
            continue
        k = k.strip()
        if not k:
            continue
        k_norm = k if case_sensitive else k.lower()
        processed.append(k_norm)

    return processed, case_sensitive, use_regex


def note_needs_image(
    note: Note,
    keywords: list[str],
    min_hits: int,
    case_sensitive: bool,
    use_regex: bool,
) -> bool:
    """
    Determine whether this note needs an image.

    Conditions:
      1) No field contains <img
      2) Keyword hits >= min_hits
    """
    if not keywords:
        return False

    hits = 0
    need_more_hits = True

    for fname in note.keys():
        raw = note[fname] or ""
        if not raw:
            continue

        text = raw if case_sensitive else raw.lower()

        # Image already present → not a target
        if "<img" in text:
            return False

        if need_more_hits:
            for kw in keywords:
                if use_regex:
                    pattern = r"\b" + re.escape(kw) + r"\b"
                    if re.search(pattern, text):
                        hits += 1
                else:
                    if kw in text:
                        hits += 1

                if hits >= min_hits:
                    need_more_hits = False
                    break

    return hits >= min_hits


def background_needimage_op(
    col: Collection,
    query: str,
    need_tag: str,
    remove_if_resolved: bool,
    keywords: list[str],
    min_hits: int,
    case_sensitive: bool,
    use_regex: bool,
) -> tuple[int, int, int]:
    if query.strip():
        nids = col.find_notes(query)
    else:
        nids = col.db.list("select id from notes")

    total = len(nids)
    added = 0
    removed = 0

    for nid in nids:
        note = col.get_note(nid)
        needs = note_needs_image(
            note=note,
            keywords=keywords,
            min_hits=min_hits,
            case_sensitive=case_sensitive,
            use_regex=use_regex,
        )

        if needs:
            if need_tag not in note.tags:
                note.add_tag(need_tag)
                col.update_note(note)
                added += 1
        else:
            if remove_if_resolved and need_tag in note.tags:
                note.remove_tag(need_tag)
                col.update_note(note)
                removed += 1

    return added, removed, total


def process_notes_for_needimage_tag() -> None:
    config = get_config()
    need_tag = str(config.get("need_image_tag", "NeedImage") or "NeedImage").strip() or "NeedImage"
    remove_if_resolved = bool(config.get("remove_tag_if_resolved", True))

    try:
        min_hits = int(config.get("min_keyword_hits", 1))
    except Exception:
        min_hits = 1
    min_hits = max(1, min_hits)

    keywords, case_sensitive, use_regex = prepare_keywords(config)

    if not keywords:
        showInfo("`keywords` in config.json is empty.\nNeedImage processing will not run.")
        return

    # ---- English UI text ----
    help_text = (
        "Enter a search query (leave blank = all notes)\n\n"
        "Examples:\n"
        "  deck:Endocrinology        → notes in the deck\n"
        "  tag:PCOS                  → notes with this tag\n"
        "  deck:\"Year 4 Medicine\" tag:\"heart failure\"\n\n"
        "Same syntax as the Anki Browser search bar.\n"
        "Use quotes for names with spaces."
    )

    query, ok = getText(help_text, default="")
    if not ok:
        return

    def on_success(result: tuple[int, int, int]) -> None:
        added_, removed_, total_ = result
        lines = [
            f"Notes scanned: {total_}",
            f"Newly added '{need_tag}' tags: {added_}",
        ]
        if remove_if_resolved:
            lines.append(f"Removed '{need_tag}' tags (image found): {removed_}")
        showInfo("\n".join(lines))
        mw.reset()

    op = QueryOp(
        parent=mw,
        op=lambda col: background_needimage_op(
            col=col,
            query=query,
            need_tag=need_tag,
            remove_if_resolved=remove_if_resolved,
            keywords=keywords,
            min_hits=min_hits,
            case_sensitive=case_sensitive,
            use_regex=use_regex,
        ),
        success=on_success,
    )

    op.with_progress(label="NeedImage: scanning notes…").run_in_background()


# -------------------- custom config GUI (no Tools menu entry) --------------------

class ConfigDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("NeedImageTagger - Settings")
        self.setMinimumWidth(680)

        conf = get_config()
        defaults = _load_packaged_defaults()

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # --- Tagging ---
        box_tagging = QGroupBox("Tagging")
        form_tagging = QFormLayout(box_tagging)
        form_tagging.setVerticalSpacing(10)

        self.need_tag = QLineEdit(str(conf.get("need_image_tag", defaults.get("need_image_tag", "NeedImage"))))
        self.need_tag.setPlaceholderText("NeedImage")
        form_tagging.addRow("Need image tag", self.need_tag)

        self.remove_if_resolved = QCheckBox("Remove tag if an image is found")
        self.remove_if_resolved.setChecked(
            bool(conf.get("remove_tag_if_resolved", defaults.get("remove_tag_if_resolved", True)))
        )
        form_tagging.addRow("", self.remove_if_resolved)

        root.addWidget(box_tagging)

        # --- Matching ---
        box_match = QGroupBox("Matching")
        form_match = QFormLayout(box_match)
        form_match.setVerticalSpacing(10)

        self.min_hits = QSpinBox()
        self.min_hits.setMinimum(1)
        self.min_hits.setMaximum(999)
        self.min_hits.setValue(int(conf.get("min_keyword_hits", defaults.get("min_keyword_hits", 1)) or 1))
        form_match.addRow("Minimum keyword hits", self.min_hits)

        self.case_sensitive = QCheckBox("Case sensitive")
        self.case_sensitive.setChecked(bool(conf.get("case_sensitive", defaults.get("case_sensitive", False))))
        form_match.addRow("", self.case_sensitive)

        self.use_regex = QCheckBox("Match whole words (recommended)")
        self.use_regex.setChecked(bool(conf.get("use_regex", defaults.get("use_regex", True))))
        form_match.addRow("", self.use_regex)

        root.addWidget(box_match)

        # --- Keywords ---
        box_kw = QGroupBox("Keywords (one per line)")
        kw_layout = QVBoxLayout(box_kw)
        kw_layout.setSpacing(8)

        self.keywords = QTextEdit()
        self.keywords.setAcceptRichText(False)
        self.keywords.setPlaceholderText("ct\nmri\nx-ray\n...")
        self.keywords.setText(_keywords_to_text(conf.get("keywords", defaults.get("keywords", []))))
        kw_layout.addWidget(self.keywords)

        hint = QLabel("A note is tagged only if it contains enough keywords AND does not already include &lt;img&gt;.")
        hint.setWordWrap(True)
        kw_layout.addWidget(hint)

        root.addWidget(box_kw)

        # --- Buttons ---
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        btn_reset = QPushButton("Reset to defaults")
        buttons.addButton(btn_reset, QDialogButtonBox.ButtonRole.ResetRole)

        buttons.accepted.connect(self._on_save)
        buttons.rejected.connect(self.reject)
        btn_reset.clicked.connect(lambda: self._apply_defaults(defaults))

        root.addWidget(buttons)

    def _apply_defaults(self, defaults: dict[str, Any]) -> None:
        self.need_tag.setText(str(defaults.get("need_image_tag", "NeedImage")))
        self.remove_if_resolved.setChecked(bool(defaults.get("remove_tag_if_resolved", True)))

        try:
            v = int(defaults.get("min_keyword_hits", 1))
        except Exception:
            v = 1
        self.min_hits.setValue(max(1, v))

        self.case_sensitive.setChecked(bool(defaults.get("case_sensitive", False)))
        self.use_regex.setChecked(bool(defaults.get("use_regex", True)))
        self.keywords.setText(_keywords_to_text(defaults.get("keywords", [])))

    def _on_save(self) -> None:
        new_conf = get_config()

        tag = (self.need_tag.text() or "").strip() or "NeedImage"
        new_conf["need_image_tag"] = tag

        new_conf["remove_tag_if_resolved"] = bool(self.remove_if_resolved.isChecked())
        new_conf["min_keyword_hits"] = int(self.min_hits.value())
        new_conf["case_sensitive"] = bool(self.case_sensitive.isChecked())
        new_conf["use_regex"] = bool(self.use_regex.isChecked())
        new_conf["keywords"] = _text_to_keywords(self.keywords.toPlainText())

        mw.addonManager.writeConfig(ADDON_PACKAGE, new_conf)
        showInfo("Settings saved.")
        self.accept()


def open_config_dialog() -> None:
    dlg = ConfigDialog(parent=mw)
    dlg.exec()


# -------------------- hooks --------------------

def on_profile_loaded() -> None:
    # Keep existing Tools action (this add-on's main function)
    action = QAction("Add NeedImage Tag…", mw)
    action.triggered.connect(process_notes_for_needimage_tag)
    mw.form.menuTools.addAction(action)

    # IMPORTANT: Do NOT add a Tools menu entry for settings.
    # Use Add-ons → Config button to open our custom GUI.
    try:
        mw.addonManager.setConfigAction(ADDON_PACKAGE, open_config_dialog)
    except Exception:
        # Older Anki builds may not support this API; then the user can still edit config.json directly.
        pass


gui_hooks.profile_did_open.append(on_profile_loaded)
