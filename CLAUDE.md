# Filament NFC Reader: read this first

ESP32-S3 touchscreen with a PN532 NFC reader: shows the Bambu AMS slots and assigns a scanned spool to a slot through Bambuddy and Spoolman. Firmware is one ESPHome YAML file.

## Where things are
- `docs/PROJECT_OVERVIEW.md`: the whole picture and reading order. `docs/OPEN_ITEMS.md`: **live status** of everything open. `docs/TASK_LEDGER.md`: **history** of finished work.
- `docs/ENGINEERING_STANDARDS.md`: the rules and the definition of done. `docs/design/`: one design per feature, written before the code.
- `esphome/filament-selector.yaml`: firmware. `esphome/secrets.yaml.example`: secrets template. `hardware/case/`: printable case. `docs/BOM.md`, `docs/API.md`, `docs/wiring-diagram.svg`.
- `docs/DOCUMENTATION_GUIDE.md`: which form (diagram, table, list, narrative) and which file each kind of content goes in, what to update when something changes, and the writing rules. **Read it before editing any document.**

## Hard rules (the owner's, in priority order)
1. **No unrequested action on the owner's hardware, accounts or servers.** Reads are fine; writes are never sent "as a test". Specifically: never flash the device, never call the owner's Bambuddy or Spoolman with a write (POST/PATCH/DELETE), never touch the printer. Verify with `esphome config`, fakes or a local mock server, then ask the owner to try it.
2. **Design before code** for any new feature or behavior change, in `docs/design/NN-name.md` (NN = highest number + 1).
3. **Secrets never in code, logs, URLs or docs.** WiFi and API keys live only in `esphome/secrets.yaml`, which is git-ignored; the repo carries `secrets.yaml.example` with placeholders. Server addresses in the YAML stay as `YOUR-...-HOST` placeholders.
4. **Do not claim more than you checked.** "Every X" needs a scan of every X. Prefer a build check over prose.
5. Status lives in `docs/OPEN_ITEMS.md` and `docs/TASK_LEDGER.md` and nowhere else; no test counts, commit hashes or line numbers in documents (name the YAML key instead).
6. **When something changes, update every place it appears** (the change table in `docs/DOCUMENTATION_GUIDE.md`): the diagram, the table, the list and the narrative that describe it must agree, and each fact has one home that the others link to.
7. Commit identity is the owner's GitHub login and its no-reply address. Never `--no-verify`; never create or push a repository without the owner's say-so.

## Before you say a task is done
`scripts/check.sh` must be green. It runs `scripts/check_standards.py`, a no-line-numbers check on the docs, a check that every API path, result message and `CHANGE ME` key in the YAML is documented, a check that `secrets.yaml` is untracked, and `esphome config` against the firmware with dummy secrets (needs `esphome` on PATH or `ESPHOME_BIN`). Update the open-items row, add the ledger row, commit with the co-author line.

## How to write and report here
- Lead with the point the reader needs, then the support. Write complete sentences, use US spelling, and read the page aloud before you finish.
- Every factual claim says how it was established (measured, read from a named source, or the owner said so) and what was not checked. Do not use first person in repository documents.
- Show a design before building any new feature or behavior change, and show sources before the conclusions that rest on them.
- Commits are small, one concern each, made only when the owner asks, with the co-author line.

## Pitfalls seen here
- `esphome config` validates syntax and components only. It does not prove the firmware works on the device: display, touch, NFC and the HTTP calls to Bambuddy and Spoolman are **untested by the check** and need the owner to flash and try.
- The firmware YAML is longer than the 400-line limit and is allowlisted in `standards.json`.
- `docs/API.md` must list every `/api/v1/` path the YAML uses, and the README must carry every result message and `CHANGE ME` key. `scripts/check.sh` fails when one is missing.
