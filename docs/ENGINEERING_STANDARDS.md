# Engineering standards (Filament NFC Reader)
Applies to every change, by every contributor (human or AI). Checks marked **[build]** are enforced by `scripts/check.sh`; the rest are enforced in review.

## 0. Process rule: design before code
For any new feature or behavior change, write `docs/design/NN-name.md` FIRST and show it:
1. **Wireframe(s)** (ASCII is fine) of every new or changed screen or interface.
2. **Flowchart** of the flow, including error and empty paths.
3. **Data-flow diagram**: which part calls which, and what flows back.
4. **Write-up**: goal, decisions and why, alternatives rejected, risks, open questions, test plan.
Then code. Tiny fixes (a few lines, no new behavior) are exempt. A change to something just reviewed gets an amendment section.

## 1. Language and style (ESPHome YAML with C++ lambdas)
- The firmware passes `esphome config` with no errors or warnings. **[build]**
- Every value a user must change is marked `CHANGE ME` and is a placeholder, never a real address. **[review]**
- Files stay within 400 lines; the firmware YAML is an allowlisted exception (owner's decision). **[build]**
- Lambdas: keep decisions (tag-UID normalisation, response parsing) in small, separately readable blocks. Pure logic that can move out of the YAML into a testable header should. **[review]**

## 2. Architecture
One device, three outside services (Bambuddy, Spoolman, optional Home Assistant). The device only reads from Spoolman and Bambuddy, and makes exactly one write: the slot assignment, after the user taps Confirm.

## 3. Resilience and operations
- Timeouts on every network call. Retry only idempotent reads, bounded, with backoff. **Never retry the slot-assignment write.**
- On failure keep the last good screen data and show what failed and what to do.
- The slot assignment shows spool and color for confirmation first, is a single attempt, and refuses with a reason (unknown tag, no slot selected).
- Log failures with a tag and a reason, never secrets.

## 4. Security and privacy
- Secrets only in `esphome/secrets.yaml` (git-ignored), referenced with `!secret`. **[build: check_standards.py, check.sh]**
- Server addresses, WiFi names and serial numbers of the owner's setup never appear in the repository; use `YOUR-...-HOST` placeholders. **[build: pii-guard commit hook]**
- Plain HTTP on a trusted LAN only; do not expose the services to the internet. **[review]**
- Writes to the owner's systems are never sent as a "test": use `esphome config` or a local mock server and ask the owner to flash and try.
- Print-project files (`.3mf`) are checked for identity fields before commit. **[review]**
- New dependencies need a reason in the ledger; prefer none.

## 5. Documentation
- Follow `docs/DOCUMENTATION_GUIDE.md` for where each kind of content goes, what to update when something changes, and how to write. **[review]**
- Status lives in `docs/OPEN_ITEMS.md` (live) and `docs/TASK_LEDGER.md` (history) only. Other documents carry no test counts, commit hashes or line numbers; refer to a YAML key instead. **[build]**
- A finished item has a ledger row. **[build]** Every design doc is listed in the overview's document map. **[build]**
- Every API path, result message and `CHANGE ME` key in the firmware is in the documentation. **[build]**

## 6. Testing
- `esphome config` proves the file is valid, not that it works. Behavior on the device (display, touch, NFC read, HTTP calls) is verified by the owner flashing and trying it; say so in the ledger row. **[review]**
- Use recorded, redacted fixtures for contracts with outside services if a mock server is ever added.

## 7. Definition of done
`scripts/check.sh` is green; the open-items row is updated; a ledger row is added when an item is finished; the design doc matches what was built. Say what was not verified.
