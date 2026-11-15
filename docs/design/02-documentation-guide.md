# 02: Documentation guide and two more checks (OI-19)
Status: DESIGNED 2026-11-14 and built the same day, from the owner's request to make agents put each kind of content in the right place and update every place that repeats it.

In short: a guide says which form (diagram, table, list, narrative) and which file each kind of content uses, and two build checks keep the firmware and the README in step.

## 1. Write-up
**Goal.** A person or an agent changing the firmware, wiring or parts updates every document that mentions it, and nothing is stated in two places.

**Decisions.**
- A separate `docs/DOCUMENTATION_GUIDE.md` holds the tables and rules, and `CLAUDE.md` only points to it, because `CLAUDE.md` must stay short.
- The guide's change table is enforced where a script can enforce it: every `/api/v1/` path (already done), every result message, and every `CHANGE ME` key must appear in the documentation. The remaining rows stay as review rules, marked as such.
- Each fact has one home. The BOM now links to the case README for screw and feet details instead of repeating them.

**Alternatives rejected.** Putting everything in `CLAUDE.md` (too long to read first), and checking prose style with a script (it cannot judge whether a sentence carries a complete thought).

**Risks.** A message check that matches strings can miss a message built from pieces at run time. The firmware builds "Lookup failed: HTTP " and a number, so the check compares the fixed text only.

## 2. Wireframe
```
CLAUDE.md  --pointer-->  docs/DOCUMENTATION_GUIDE.md
                           form table | home table | change table | writing rules | build list
```

## 3. Flowchart
```
change made
  -> look up the change in the change table
  -> update every listed place (diagram, table, list, narrative)
  -> run scripts/check.sh
       fails on a missing path, message or key -> fix the documents, run again
       passes -> add the ledger row, remove the open item
```

## 4. Data flow
```
esphome/filament-selector.yaml --paths--> docs/API.md
                               --messages, CHANGE ME keys--> README.md
scripts/check.sh reads all three and fails on a mismatch
```

## 5. Steps
1. Write the guide and link it from `CLAUDE.md`, the standards and the overview.
2. Add the two checks to `scripts/check.sh` and show each failing once.
3. Remove duplicated facts the guide forbids.

## 6. Risks and tests
| Risk | Mitigation |
|---|---|
| A check passes while a message is undocumented | Each check was shown failing by removing a message and a key, then restored |
| The guide goes stale | Its enforced items are in the build, and the rest are in the review rules |
