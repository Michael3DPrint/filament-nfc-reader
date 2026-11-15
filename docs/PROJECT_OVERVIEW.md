# Filament NFC Reader: overview
This project is a small ESP32-S3 touchscreen unit that shows what is loaded in a Bambu Lab AMS and assigns a spool to a slot when its NFC tag is scanned. It looks the spool up in Spoolman and records the assignment through Bambuddy, and it was built for the owner's own printer. `README.md` is the guide for anyone building one.

## Reading order
1. `CLAUDE.md`
2. this file
3. `docs/ENGINEERING_STANDARDS.md`
4. `docs/OPEN_ITEMS.md`

## Document map
The table lists every document. `scripts/check.sh` fails if a file under `docs/design` is missing from it.

| Document | What it covers |
|---|---|
| `README.md` | what it is, setup, configuration, troubleshooting |
| `LICENSE` | the Apache License 2.0 that covers the project |
| `THIRD_PARTY_NOTICES.md` | licenses of the programs the project talks to or builds with |
| `SECURITY.md` | how to report a problem, design limits, what was checked |
| `docs/BOM.md` | parts list |
| `docs/API.md` | every outside call the firmware and setup make, with behavior notes |
| `docs/wiring-diagram.svg` | PN532 to display board wiring |
| `hardware/case/README.md` | printable case and print settings |
| `docs/ENGINEERING_STANDARDS.md` | the rules and the definition of done |
| `docs/DOCUMENTATION_GUIDE.md` | where each kind of content goes, what to update on a change, writing rules |
| `docs/design/01-readme-completeness.md` | sourced facts and plan for finishing the README, diagrams and BOM |
| `docs/design/02-documentation-guide.md` | plan for the documentation guide and the two documentation checks |
| `docs/OPEN_ITEMS.md` | live status |
| `docs/TASK_LEDGER.md` | history of finished work |
