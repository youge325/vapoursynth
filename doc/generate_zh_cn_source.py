#!/usr/bin/env python3
"""Generate direct Chinese .rst sources in zh_CN_source from existing PO translations.

This script is migration-oriented: PO files are used only as translation input,
while the resulting build consumes .rst sources directly.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import re
import socket
import sys
from typing import Dict, Iterable

import polib

try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
except Exception:  # pragma: no cover - optional dependency
    GoogleTranslator = None
    MyMemoryTranslator = None

DOC_ROOT = Path(__file__).resolve().parent
PO_ROOT = DOC_ROOT / "locale" / "zh_CN" / "LC_MESSAGES"
TARGET_ROOT = DOC_ROOT / "zh_CN_source"
EXCLUDED_TOP_LEVEL = {"_build", "zh_CN_source"}

ENGLISH_PHRASE_RE = re.compile(r"[A-Za-z]{3,}(?:\s+[A-Za-z]{3,})+")
WHITESPACE_RE = re.compile(r"\s+")
TOKEN_RE = re.compile(
    r"``[^`]*``"
    r"|`[^`\n]+`_?"
    r"|:[a-zA-Z0-9_+.-]+:`[^`\n]+`"
    r"|https?://\S+"
)
HAS_CJK_RE = re.compile(r"[\u4e00-\u9fff]")
HAS_ENGLISH_RE = re.compile(r"[A-Za-z]{2,}")
ONLY_PLACEHOLDER_RE = re.compile(r"^(?:\s*__VSTOK\d+__\s*)+$")
FUNCTION_SIGNATURE_RE = re.compile(r"^[A-Za-z_][\w\s\*:\[\]<>]*\([^\n]*\)\s*;?$")
CODE_STATEMENT_RE = re.compile(
    r"^(from\s+\w+\s+import|import\s+\w+|def\s+\w+\(|class\s+\w+\(|for\s+\w+\s+in\s+|"
    r"while\s+|if\s+|elif\s+|else:|return\b|print\(|with\s+|try:|except\b|finally:)"
)
ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][\w\.\[\]]*\s*=")
LITERAL_COMMAND_RE = re.compile(r"^``[^`]+``$")
OPTION_LINE_RE = re.compile(r"^``-{1,2}[A-Za-z0-9][^`]*``$")


def iter_source_rst() -> list[str]:
    files: list[str] = []
    for rst_path in DOC_ROOT.rglob("*.rst"):
        rel = rst_path.relative_to(DOC_ROOT).as_posix()
        top = rel.split("/", 1)[0]
        if top in EXCLUDED_TOP_LEVEL:
            continue
        files.append(rel)
    return sorted(files)


def normalize_occurrence(path_text: str) -> str:
    path_text = path_text.replace("\\", "/")
    while path_text.startswith("../"):
        path_text = path_text[3:]
    if path_text.startswith("./"):
        path_text = path_text[2:]
    if path_text.startswith("doc/"):
        path_text = path_text[4:]
    return path_text


def build_translation_map() -> dict[str, dict[str, str]]:
    translation_map: Dict[str, Dict[str, str]] = defaultdict(dict)

    for po_path in sorted(PO_ROOT.glob("*.po")):
        po = polib.pofile(str(po_path))
        for entry in po:
            if entry.obsolete or not entry.msgid:
                continue
            if not entry.msgstr or not entry.msgstr.strip():
                continue
            if entry.msgid == entry.msgstr:
                continue

            for occurrence_path, _line in entry.occurrences:
                rel = normalize_occurrence(occurrence_path)
                if rel.endswith(".rst"):
                    translation_map[rel][entry.msgid] = entry.msgstr

    return dict(translation_map)


def to_ws_pattern(source: str) -> re.Pattern[str]:
    # Normalize any whitespace run in msgid to a regex whitespace run.
    parts = WHITESPACE_RE.split(source.strip())
    escaped = [re.escape(part) for part in parts if part]
    if not escaped:
        return re.compile(r"$^")
    return re.compile(r"\s+".join(escaped), flags=re.MULTILINE)


def replace_with_po_entries(text: str, replacements: dict[str, str]) -> tuple[str, int, int, int]:
    exact_hits = 0
    fuzzy_hits = 0
    unmatched_entries = 0

    # Replace longer source strings first to reduce substring conflicts.
    for msgid, msgstr in sorted(replacements.items(), key=lambda pair: len(pair[0]), reverse=True):
        hits = text.count(msgid)
        if hits > 0:
            text = text.replace(msgid, msgstr)
            exact_hits += hits
            continue

        # Fallback to whitespace-normalized matching to bridge wrapping/indent differences.
        pattern = to_ws_pattern(msgid)
        text, replaced = pattern.subn(msgstr, text, count=1)
        if replaced > 0:
            fuzzy_hits += replaced
            continue

        unmatched_entries += 1

    return text, exact_hits, fuzzy_hits, unmatched_entries


def protect_tokens(text: str) -> tuple[str, list[str]]:
    tokens: list[str] = []

    def repl(match: re.Match[str]) -> str:
        idx = len(tokens)
        tokens.append(match.group(0))
        return f"__VSTOK{idx}__"

    return TOKEN_RE.sub(repl, text), tokens


def restore_tokens(text: str, tokens: Iterable[str]) -> str:
    restored = text
    for idx, token in enumerate(tokens):
        placeholder = f"__VSTOK{idx}__"
        restored = restored.replace(placeholder, token)
        restored = restored.replace(placeholder.lower(), token)
    return restored


def looks_like_english_content(text: str) -> bool:
    probe = re.sub(r"__VSTOK\d+__", " ", text)
    probe = probe.strip()
    if len(probe) < 3:
        return False
    if ONLY_PLACEHOLDER_RE.fullmatch(probe):
        return False
    if not HAS_ENGLISH_RE.search(probe):
        return False
    if FUNCTION_SIGNATURE_RE.fullmatch(probe):
        return False
    if LITERAL_COMMAND_RE.fullmatch(probe):
        return False
    if OPTION_LINE_RE.fullmatch(probe):
        return False
    if CODE_STATEMENT_RE.match(probe):
        return False
    if ASSIGNMENT_RE.match(probe):
        return False

    # Ignore symbol-heavy lines that are likely declarations/options rather than prose.
    alpha_num = sum(ch.isalnum() for ch in probe)
    symbol = sum((not ch.isalnum()) and (not ch.isspace()) for ch in probe)
    if alpha_num > 0 and symbol / (alpha_num + symbol) > 0.45:
        return False

    return True


def line_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def translate_batch_cached(lines: list[str], cache: dict[str, str]) -> None:
    if not lines:
        return
    if GoogleTranslator is None and MyMemoryTranslator is None:
        return

    translators = []
    if MyMemoryTranslator is not None:
        try:
            translators.append(MyMemoryTranslator(source="en-US", target="zh-CN"))
        except Exception:
            pass
    if GoogleTranslator is not None:
        try:
            translators.append(GoogleTranslator(source="en", target="zh-CN"))
        except Exception:
            pass
    if not translators:
        return

    primary_translator = translators[0]
    pending = [line for line in lines if line not in cache]
    batch_size = 25
    previous_timeout = socket.getdefaulttimeout()
    requests_module = None
    original_requests_get = None

    # Prevent indefinite network stalls in translation requests.
    socket.setdefaulttimeout(12.0)

    try:
        import requests as _requests

        requests_module = _requests
        original_requests_get = _requests.get

        def _patched_get(*args, **kwargs):
            kwargs.setdefault("timeout", 12)
            kwargs.setdefault("verify", False)
            return original_requests_get(*args, **kwargs)

        _requests.get = _patched_get

        try:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        except Exception:
            pass
    except Exception:
        requests_module = None
        original_requests_get = None

    try:
        for i in range(0, len(pending), batch_size):
            batch = pending[i : i + batch_size]
            translated: list[str]
            try:
                translated = primary_translator.translate_batch(batch)
            except Exception:
                translated = []

            if not translated or len(translated) != len(batch):
                translated = []
                for item in batch:
                    translated_item = item
                    for translator in translators:
                        try:
                            candidate = translator.translate(item)
                        except Exception:
                            continue
                        if isinstance(candidate, str) and candidate.strip():
                            translated_item = candidate
                            break
                    translated.append(translated_item)

            for src, dst in zip(batch, translated):
                try:
                    cache[src] = dst if isinstance(dst, str) and dst.strip() else src
                except Exception:
                    cache[src] = src
    finally:
        if requests_module is not None and original_requests_get is not None:
            try:
                requests_module.get = original_requests_get
            except Exception:
                pass
        socket.setdefaulttimeout(previous_timeout)


def auto_translate_english_lines(text: str, enabled: bool) -> tuple[str, int, int]:
    lines = text.splitlines()
    if not enabled or GoogleTranslator is None:
        return text, 0, count_english_lines(text)

    in_code = False
    code_indent = 0
    expect_literal = False
    literal_base_indent = 0

    candidates: list[tuple[int, str, str, list[str]]] = []

    for idx, line in enumerate(lines):
        stripped = line.strip()
        indent = line_indent(line)

        if in_code:
            if stripped and indent < code_indent:
                in_code = False
            else:
                continue

        if expect_literal:
            if not stripped:
                continue
            if indent > literal_base_indent:
                in_code = True
                code_indent = indent
                continue
            expect_literal = False

        if stripped.startswith(".. code-block::") or stripped.startswith(".. code::"):
            expect_literal = True
            literal_base_indent = indent
            continue

        if stripped.endswith("::"):
            expect_literal = True
            literal_base_indent = indent
            continue

        if not stripped:
            continue
        if stripped.startswith(".. "):
            continue
        if stripped.startswith(":"):
            continue
        if re.fullmatch(r"[=~`^\-\*#+\"]{3,}", stripped):
            continue
        if FUNCTION_SIGNATURE_RE.fullmatch(stripped):
            continue
        if LITERAL_COMMAND_RE.fullmatch(stripped):
            continue
        if OPTION_LINE_RE.fullmatch(stripped):
            continue
        if CODE_STATEMENT_RE.match(stripped):
            continue
        if ASSIGNMENT_RE.match(stripped):
            continue

        protected, tokens = protect_tokens(stripped)
        if not looks_like_english_content(protected):
            continue

        prefix = line[: len(line) - len(line.lstrip(" "))]
        candidates.append((idx, prefix, protected, tokens))

    unique_candidates = sorted({item[2] for item in candidates})
    cache: dict[str, str] = {}
    translate_batch_cached(unique_candidates, cache)

    translated_count = 0
    for idx, prefix, protected, tokens in candidates:
        translated = cache.get(protected, protected)
        restored = restore_tokens(translated, tokens)
        if restored and restored != lines[idx].strip():
            lines[idx] = prefix + restored
            translated_count += 1

    result = "\n".join(lines)
    if text.endswith("\n"):
        result += "\n"
    remaining_english = count_english_lines(result)
    return result, translated_count, remaining_english


def count_english_lines(text: str) -> int:
    in_code = False
    code_indent = 0
    expect_literal = False
    literal_base_indent = 0
    count = 0

    for line in text.splitlines():
        stripped = line.strip()
        indent = line_indent(line)

        if in_code:
            if stripped and indent < code_indent:
                in_code = False
            else:
                continue

        if expect_literal:
            if not stripped:
                continue
            if indent > literal_base_indent:
                in_code = True
                code_indent = indent
                continue
            expect_literal = False

        if stripped.startswith(".. code-block::") or stripped.startswith(".. code::"):
            expect_literal = True
            literal_base_indent = indent
            continue

        if stripped.endswith("::"):
            expect_literal = True
            literal_base_indent = indent
            continue

        if not stripped:
            continue
        if stripped.startswith(".. "):
            continue
        if stripped.startswith(":"):
            continue
        if FUNCTION_SIGNATURE_RE.fullmatch(stripped):
            continue
        if LITERAL_COMMAND_RE.fullmatch(stripped):
            continue
        if OPTION_LINE_RE.fullmatch(stripped):
            continue
        if CODE_STATEMENT_RE.match(stripped):
            continue
        if ASSIGNMENT_RE.match(stripped):
            continue

        if HAS_ENGLISH_RE.search(stripped) and not HAS_CJK_RE.search(stripped):
            count += 1

    return count


def render_translated_text(
    source_path: Path,
    target_path: Path,
    replacements: dict[str, str],
    incremental: bool,
    auto_translate: bool,
) -> tuple[str, int, int, int, int, str]:
    source_text = source_path.read_text(encoding="utf-8")

    if incremental and target_path.exists():
        # Incremental mode: preserve manual edits and keep applying available replacements.
        text = target_path.read_text(encoding="utf-8")
        mode = "updated"
    else:
        # Rebuild mode starts from source to avoid stale mixed-language artifacts.
        text = source_text
        mode = "generated" if not target_path.exists() else "rebuilt"

    # In incremental mode, files not covered by PO keep manual edits once present.
    if incremental and not replacements and target_path.exists():
        kept = target_path.read_text(encoding="utf-8")
        return kept, 0, 0, 0, 0, "preserved"

    text, exact_hits, fuzzy_hits, unmatched_entries = replace_with_po_entries(text, replacements)
    text, auto_translated_lines, remaining_english = auto_translate_english_lines(text, enabled=auto_translate)

    return text, exact_hits, fuzzy_hits, unmatched_entries, auto_translated_lines, mode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate zh_CN_source rst files from PO and fallback translation.")
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Use existing zh_CN_source files as base instead of rebuilding from source rst files.",
    )
    parser.add_argument(
        "--no-auto-translate",
        action="store_true",
        help="Disable fallback machine translation for remaining English lines.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    auto_translate = not args.no_auto_translate

    has_po_root = PO_ROOT.exists()
    po_files = list(PO_ROOT.glob("*.po")) if has_po_root else []

    if not po_files:
        # After migration completes and .po files are removed, keep zh_CN_source as source of truth.
        if TARGET_ROOT.exists():
            print(f"WARNING: No .po files found under {PO_ROOT}")
            print("Keeping existing zh_CN_source unchanged.")
            return 0
        print(f"ERROR: PO directory/files not found and target source missing: {TARGET_ROOT}")
        return 1

    source_files = iter_source_rst()
    translation_map = build_translation_map()

    TARGET_ROOT.mkdir(parents=True, exist_ok=True)

    generated_count = 0
    rebuilt_count = 0
    updated_count = 0
    preserved_count = 0
    total_exact_hits = 0
    total_fuzzy_hits = 0
    total_unmatched = 0
    total_auto_translated_lines = 0
    total_remaining_english = 0

    report_lines = [
        "# zh_CN_source generation report",
        f"source_root: {DOC_ROOT}",
        f"target_root: {TARGET_ROOT}",
        f"po_root: {PO_ROOT}",
        f"source_rst_files: {len(source_files)}",
        f"incremental_mode: {bool(args.incremental)}",
        f"auto_translate_enabled: {bool(auto_translate and GoogleTranslator is not None)}",
        f"auto_translate_backend: {'deep-translator:GoogleTranslator' if GoogleTranslator is not None else 'disabled (dependency missing)'}",
        "",
        "## file stats",
        "file\tmode\tpo_entries\texact_hits\tfuzzy_hits\tunmatched_entries\tauto_translated_lines\tremaining_english_lines",
    ]

    for rel in source_files:
        source_path = DOC_ROOT / rel
        target_path = TARGET_ROOT / rel
        replacements = translation_map.get(rel, {})

        output_text, exact_hits, fuzzy_hits, unmatched_entries, auto_translated_lines, mode = render_translated_text(
            source_path=source_path,
            target_path=target_path,
            replacements=replacements,
            incremental=args.incremental,
            auto_translate=auto_translate,
        )

        remaining_english = count_english_lines(output_text)

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(output_text, encoding="utf-8")

        if mode == "generated":
            generated_count += 1
        elif mode == "rebuilt":
            rebuilt_count += 1
        elif mode == "updated":
            updated_count += 1
        else:
            preserved_count += 1

        total_exact_hits += exact_hits
        total_fuzzy_hits += fuzzy_hits
        total_unmatched += unmatched_entries
        total_auto_translated_lines += auto_translated_lines
        total_remaining_english += remaining_english

        report_lines.append(
            f"{rel}\t{mode}\t{len(replacements)}\t{exact_hits}\t{fuzzy_hits}\t{unmatched_entries}\t{auto_translated_lines}\t{remaining_english}"
        )

    report_lines.extend(
        [
            "",
            "## summary",
            f"generated_files: {generated_count}",
            f"rebuilt_files: {rebuilt_count}",
            f"updated_files: {updated_count}",
            f"preserved_files: {preserved_count}",
            f"total_exact_replacement_hits: {total_exact_hits}",
            f"total_fuzzy_replacement_hits: {total_fuzzy_hits}",
            f"total_unmatched_entries: {total_unmatched}",
            f"total_auto_translated_lines: {total_auto_translated_lines}",
            f"total_remaining_english_lines: {total_remaining_english}",
        ]
    )

    report_path = TARGET_ROOT / "_translation_report.txt"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"source rst files: {len(source_files)}")
    print(f"generated files: {generated_count}")
    print(f"rebuilt files: {rebuilt_count}")
    print(f"updated files: {updated_count}")
    print(f"preserved files: {preserved_count}")
    print(f"exact replacement hits: {total_exact_hits}")
    print(f"fuzzy replacement hits: {total_fuzzy_hits}")
    print(f"unmatched entries: {total_unmatched}")
    print(f"auto translated lines: {total_auto_translated_lines}")
    print(f"remaining english lines: {total_remaining_english}")
    print(f"report: {report_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
