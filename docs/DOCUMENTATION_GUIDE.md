# Documentation guide

Each fact belongs in one place, in the form that suits it, and every place that repeats it must change together. This guide says which form and which file to use, what to update when something changes, and how to write. It is for anyone who edits this repository, human or AI.

## Which form for which content

| Content | Form | Example here |
|---|---|---|
| A flow with branches, or a physical layout | Diagram (Mermaid for flows, SVG for wiring) | Screen flow, wiring diagram |
| Facts a reader looks up: values, parts, calls, messages, symptoms | Table | BOM, API calls, troubleshooting |
| Short parallel facts, or steps in a fixed order | Bullet list, or numbered list for steps | Setup steps, "behavior you will notice" |
| Reasoning: why, trade-offs, caveats | Narrative paragraph, with the point first | "How it works" introduction, design documents |
| Open work and finished work | The open-items list and the ledger, nowhere else | `docs/OPEN_ITEMS.md`, `docs/TASK_LEDGER.md` |

A diagram, a table and a list that describe the same thing must agree. The screen-flow diagram and the result-message table are one example.

## Where each kind of content lives

| Content | Home |
|---|---|
| What the unit is, setup, configuration, troubleshooting | `README.md` |
| Parts and quantities | `docs/BOM.md` |
| Every outside call and its behavior | `docs/API.md` |
| Wiring | `docs/wiring-diagram.svg`, with the pin table in `README.md` |
| Case files, print settings, fastening | `hardware/case/README.md` |
| Rules for working here | `CLAUDE.md`, `docs/ENGINEERING_STANDARDS.md` |
| A plan for a change, written before the code | `docs/design/NN-name.md` |
| Open work, finished work | `docs/OPEN_ITEMS.md`, `docs/TASK_LEDGER.md` |
| The secrets template | `esphome/secrets.yaml.example` |

Other files link to the home instead of repeating the fact.

## When something changes, update these

| Change | Update |
|---|---|
| A key or default in the firmware that a user may edit | The README "What to change and where" tables and the `CHANGE ME` comment in the YAML |
| An outside call (path, header, body, timing) | `docs/API.md`, and the README architecture diagram if the flow changes |
| A screen or a message the unit shows | The screen-flow diagram, the result-message table and the "behavior" bullets in the README |
| Wiring, a pin or a socket | The SVG, the README pin table, the BOM if parts change, and the troubleshooting rows |
| A part or a quantity | `docs/BOM.md`, and `hardware/case/README.md` if it is a printed part or a fastener |
| A printed file or a print setting | The tables in `hardware/case/README.md`, and the BOM if fastener sizes change |
| A minimum or tested software version | The README software table and tested-versions sentence, and the header of `docs/API.md` |
| A new feature or a changed behavior | A design document first, listed in the overview's document map |
| Anything finished | A ledger row, and remove it from the open-items list |
| A fact that could not be verified | Say so next to the claim, and add an open-items row if the owner can settle it |

## Writing rules

- Open each section and each paragraph with the point the reader needs, and put supporting detail after it.
- Write full sentences that each carry one complete thought. Avoid runs of very short sentences, and use fragments only in table cells and list items.
- Do not repeat a fact in two files. Link to it.
- Use US spelling, and use one word for one thing (for example "I2C socket" and "Result screen").
- Name YAML keys, never line numbers. Do not put test counts or commit hashes in any document except the ledger.
- Say how a claim was established ("measured from the mesh", "read from the source", "the owner said") and what was not checked. Do not use first person in repository documents.
- Avoid stock phrases and filler, such as "robust", "seamless" or "note that".
- Read the page aloud before you finish, and fix every place you stumble.

## Enforced by the build

`scripts/check.sh` fails when:
- a finished open item has no ledger row, or a design document is missing from the overview's document map;
- a live document carries a stale fact, or a source file passes the line limit;
- a document cites a line number;
- a `/api/v1/` path in the firmware is missing from `docs/API.md`;
- a result message in the firmware is missing from the README message table;
- a `CHANGE ME` key in the firmware is missing from the README;
- `esphome/secrets.yaml` is tracked, or the firmware fails `esphome config`.

Everything else in this guide is checked in review.
