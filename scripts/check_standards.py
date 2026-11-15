#!/usr/bin/env python3
"""Language-neutral standards checks. Exit 1 with a list of problems, 0 when clean.

Checks (each can be tuned in `standards.json` next to this script's project root, see CONFIG below):
  1. a finished open item ("[x]" heading in docs/OPEN_ITEMS.md) has a row in docs/TASK_LEDGER.md that names it
  2. every docs/design/*.md file is named in docs/PROJECT_OVERVIEW.md (the document map)
  3. live documents carry no test counts, commit hashes or `File.ext:123` line citations (status goes stale)
  4. source files stay within the line limit (an allowlist with a reason is allowed)
  5. no obvious secrets (private keys, long literal api keys or tokens) in text files
Run from the project root:  python3 scripts/check_standards.py
Language-specific rules (formatter, linter, forbidden constructs) belong in the project's own build.

CONFIG: optional `standards.json` in the project root:
  {"max_lines": 400, "source_ext": [".py", ".kt"], "skip_dirs": ["build", "node_modules"],
   "line_limit_allowlist": {"path/to/file.py": "reason"}, "line_limit_skip_globs": ["*Test.*"], "ledger_id_pattern": "OI-\\d+",
   "live_docs": ["CLAUDE.md", "docs/design/*.md"]}
"""
import fnmatch
import json
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
CFG = {
    "max_lines": 400,
    "source_ext": [".py", ".kt", ".java", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".swift", ".c", ".cpp", ".h"],
    "skip_dirs": [".git", "build", "dist", "node_modules", ".gradle", ".idea", "__pycache__", ".venv", "venv", "target", "out"],
    "line_limit_allowlist": {},
    # Test files are not held to the source line limit by default; remove this to include them.
    "line_limit_skip_globs": ["*/test/*", "*/tests/*", "*Test.*", "*_test.*", "*.test.*", "*.spec.*"],
    "ledger_id_pattern": r"OI-\d+",
    # Only live documents are checked for stale facts; historical write-ups and generated artifacts are left alone.
    "live_docs": ["CLAUDE.md", "README.md", "docs/OPEN_ITEMS.md", "docs/PROJECT_OVERVIEW.md", "docs/ENGINEERING_STANDARDS.md", "docs/design/*.md"],
}
cfg_path = os.path.join(ROOT, "standards.json")
if os.path.exists(cfg_path):
    CFG.update(json.load(open(cfg_path)))

problems = []


def walk(exts=None):
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in CFG["skip_dirs"]]
        for f in files:
            if exts is None or os.path.splitext(f)[1] in exts:
                yield os.path.join(base, f)


def rel(p):
    return os.path.relpath(p, ROOT)


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        return ""


# 1. finished items need a ledger row
open_items = os.path.join(ROOT, "docs", "OPEN_ITEMS.md")
ledger = os.path.join(ROOT, "docs", "TASK_LEDGER.md")
if os.path.exists(open_items) and os.path.exists(ledger):
    idp = CFG["ledger_id_pattern"]
    ledger_text = read(ledger)
    for line in read(open_items).splitlines():
        m = re.match(r"^##\s+(" + idp + r")\b.*\[x\]", line)
        if m and m.group(1) not in ledger_text:
            problems.append(f"{m.group(1)} is marked done in docs/OPEN_ITEMS.md but has no row in docs/TASK_LEDGER.md")

# 2. design docs are in the document map
overview = os.path.join(ROOT, "docs", "PROJECT_OVERVIEW.md")
design_dir = os.path.join(ROOT, "docs", "design")
if os.path.isdir(design_dir) and os.path.exists(overview):
    ov = read(overview)
    for f in sorted(os.listdir(design_dir)):
        if f.endswith(".md") and f != "TEMPLATE.md" and f not in ov:
            problems.append(f"docs/design/{f} is not listed in docs/PROJECT_OVERVIEW.md")

# 3. documents carry no stale facts (the ledger is history and may name them)
STALE = [
    (re.compile(r"(?<![-\w])\d{2,4}\s+(unit\s+)?tests\b", re.I), "a test count"),
    (re.compile(r"\bcommit\s+[0-9a-f]{7,40}\b", re.I), "a commit hash"),
    (re.compile(r"\b[\w/.-]+\.(kt|py|ts|tsx|js|go|rs|java|swift|c|cpp|h):\d+\b"), "a file:line citation"),
]
live = []
for p in walk({".md"}):
    r = rel(p).replace(os.sep, "/")
    if r != "docs/TASK_LEDGER.md" and any(fnmatch.fnmatch(r, g) for g in CFG["live_docs"]):
        live.append(p)
for p in live:
    r = rel(p)
    for i, line in enumerate(read(p).splitlines(), 1):
        for rx, what in STALE:
            if rx.search(line):
                problems.append(f"{r}:{i} contains {what} (status goes stale; keep it in the ledger or leave it out)")

# 4. file length
for p in walk(set(CFG["source_ext"])):
    r = rel(p).replace(os.sep, "/")
    n = sum(1 for _ in open(p, encoding="utf-8", errors="ignore"))
    skipped = any(fnmatch.fnmatch(r, g) for g in CFG["line_limit_skip_globs"])
    if n > CFG["max_lines"] and r not in CFG["line_limit_allowlist"] and not skipped:
        problems.append(f"{r} has {n} lines (limit {CFG['max_lines']}); split it or add it to line_limit_allowlist with a reason")

# 5. secrets
SECRET = [
    (re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"), "a private key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "an AWS access key id"),
    (re.compile(r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]"), "a literal secret"),
]
for p in walk():
    if os.path.splitext(p)[1] in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".apk", ".jar", ".zip", ".keystore", ".jks", ".ttf", ".otf", ".woff"}:
        continue
    text = read(p)
    for rx, what in SECRET:
        if rx.search(text):
            problems.append(f"{rel(p)} looks like it contains {what}")

if problems:
    print("Standards check failed:")
    for p in problems:
        print(" -", p)
    sys.exit(1)
print("Standards check passed.")
