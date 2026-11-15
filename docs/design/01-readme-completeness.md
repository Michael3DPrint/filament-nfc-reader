# 01: README completeness (OI-06)
Status: DESIGNED 2026-11-14 and built the same day, from the owner's request to check whether the README, diagrams and BOM let a newcomer build the unit without outside help, and whether the API side is covered.

In short: the README was accurate but incomplete, so this design adds an API reference page, a screen-flow diagram, first-flash steps and BOM fixes. Section 0 lists the sourced facts the changes rely on, and the later sections give the plan.

## 0. What was checked, and where it came from
Each point says where it was read. "Vendor page" is the display board's product page on lcdwiki.com and "vendor schematic" is the PDF linked from it. "Bambuddy source" is the public repository `maziggy/bambuddy`, "Spoolman source" is `Donkie/Spoolman`. All were read on 2026-11-14, read only.

**Confirmed by a source**
- The slot assignment is `POST /api/v1/spoolman/inventory/slot-assignments` with the body fields `spoolman_spool_id`, `printer_id`, `ams_id`, `tray_id`, `move`. Source: Bambuddy source, `backend/app/api/routes/spoolman_inventory.py`, request model and route.
- The route needs the inventory-update permission and refuses an archived spool with HTTP 400 and an unknown printer or spool with 404. It stores the assignment in Bambuddy's own database only; Spoolman's `location` field is not touched. Source: same file, docstring and handler.
- `move: true` makes the spool leave any other slot it is in, in the same transaction. The field exists in Bambuddy v1.3.0 and v1.3.1 and not in v1.2.5.7. Source: same file at those three release tags.
- The status call is `GET /api/v1/printers/{printer_id}/status` and needs the printers-read permission. Source: Bambuddy source, `backend/app/api/routes/printers.py`.
- The printer list is `GET /api/v1/printers/`. Source: same file, router prefix and list route.
- The `X-API-Key` header is accepted by Bambuddy. Source: Bambuddy source, `backend/app/core/auth.py`, and its own scripts that send it.
- Status fields the firmware reads exist: `ams[].humidity`, `temp`, `tray[].id`, `tray_type`, `tray_sub_brands`, `tray_color`, `remain`, `exists`. `exists` can be null. Source: Bambuddy source, `backend/app/schemas/printer.py`.
- The tag endpoint is `PATCH /api/v1/spoolman/inventory/spools/{spool_id}/tag` with body `{"tag_uid": "..."}` (8 to 30 hex characters, not all zeros) or `{"tray_uuid": "..."}` (32 hex characters). It writes `extra.tag` and returns 409 if another spool holds the tag. With Spoolman 0.27 or newer it also writes a native tag. Source: Bambuddy source, `spoolman_inventory.py`, tag route and its request model.
- Spoolman's `GET /api/v1/spool` has an optional `limit`, so with none it returns every spool. Source: Spoolman source, `spoolman/api/v1/spool.py`.
- The display board's I2C socket is P4 on the vendor schematic: pin 1 = 3V3, 2 = GND, 3 = SCL, 4 = SDA. It is 1.25 mm, 4 pin, and shares the bus with the touch controller (IO16 data, IO15 clock). There are other 1.25 mm 4-pin sockets for SPI and UART. Source: vendor schematic and vendor page.
- To enter download mode, hold the BOOT key while powering up, then release; or hold BOOT, press and release RESET, then release BOOT. The board has a Type-C port for programming and power, and runs at 3.0 to 3.6 V on its own regulator. Source: vendor page.
- ESPHome's command line has `config`, `compile`, `upload`, `logs` and `run`. `run` validates, builds, uploads and shows logs. Source: `esphome --help`, version 2026.10.2.
- Latest stable releases on 2026-11-14: ESPHome 2026.10.2 (PyPI), Bambuddy v1.3.1, Spoolman v0.27.1 (GitHub releases).

**Read from the firmware, not from any outside source**
- Poll every 5 s for status and every 1 s for NFC, 10 s HTTP timeout, 65536-byte buffer for status and for the spool list, 4096 bytes for the assignment reply. Source: `esphome/filament-selector.yaml`.
- The lookup skips archived spools, takes the first spool whose `extra.tag` matches, and shows these messages: "Lookup failed: HTTP <code>", "Lookup failed: no connection to Spoolman", "Lookup failed: bad reply", "Unknown tag" plus the UID, "Assigned to slot N", "Assign failed: HTTP <code>", "Assign failed: no connection to Bambuddy". Source: same file.

**Not found, so not to be claimed**
- Bambuddy's on-screen names for API key permissions. Upstream's fields are `can_read_status` and `can_manage_inventory`; the README's "Read and Inventory" is the owner's wording and unchecked.
- Whether Spoolman has any built-in authentication. Not found in its README; not claimed either way.
- The physical position of pin 1 on the board, the PN532 V3's supply range and its header order, what happens when a Bambuddy older than 1.3.0 receives `move`, and whether the case needs fasteners. None of these were found in a source.

## 1. Write-up
**Goal.** A reader with the parts and no prior knowledge of this project can wire, configure, flash and use the unit, and can find every outside call the firmware makes.

**Gaps being closed** (each from the review)
1. First flash has no steps (download mode, install, command).
2. API calls are described in prose only; no single reference.
3. Behavior the user will notice is undocumented: `move`, assignment is Bambuddy-only, archived spools show as unknown, first match wins, polling times.
4. No screen-flow diagram with error paths.
5. Tagging a spool gives no request body.
6. Troubleshooting lacks "Lookup failed: bad reply" and "Unknown tag" for archived spools.
7. BOM: soldering is "helpful" but the cable route requires it; no filament, quantities or supply rating; one link.

**Decisions and why**
- Put the API reference in `docs/API.md` as tables (method, path, who calls it, auth, body, replies the firmware handles). A table is the form a builder can scan, and it is what the firmware really sends. See the amendment above for why it is not in the README.
- Add a screen-flow diagram next to the architecture diagram, in Mermaid like the existing one, so both render on GitHub.
- Put first-flash steps in the existing "Flashing notes", ordered as numbered steps, using the vendor's BOOT procedure and `esphome run`.
- Keep versions as already recorded; do not add more.
- Things nobody has confirmed are written as "to confirm" in the open items, not as facts in the README.

**Alternatives rejected.** Putting the table in the README (too large, owner's call). Rewriting the README from scratch: the existing text is accurate where checked and the changes are additions.

**Risks.** An API table can drift from the firmware. Mitigation: a check in `scripts/check.sh` that every URL path in the YAML appears in the README table (see section 5).

**Amendment 2026-11-14, owner's answers**
- The API reference is too large for the README. It goes in `docs/API.md`, linked from the README. The README keeps a short "good to know" list.
- Case fastening: magnets are suggested, anything else is fine. No size or count was given, so the BOM says so and does not invent one.
- Later amendment: measuring the v10 mesh showed no magnet pockets that join parts, and the owner said magnets in the base recesses cannot hold the unit. Magnets were dropped, and the case is fastened with M3 screws (see the ledger rows OI-11 to OI-13).
- No filament rows in the BOM. A supply rating was not answered, so it is not added.
- Soldering is required for this build, so the iron and solder move to the BOM's required list.

## 2. Wireframe (README outline after the change)
```
Filament Selector
  what it does (4 steps)                      unchanged
  How it works
     architecture diagram                     unchanged
     screen flow diagram                      NEW
  What you need  hardware / wiring / software unchanged (wiring and versions done)
  Setup (7 steps)                            step 5 points to the numbered flash steps
  What to change and where                    unchanged
  Tagging a spool                             + request body, how to find the spool id
  Good to know + link to docs/API.md          NEW  (short list; the tables live in docs/API.md)
  Flashing notes                              reworked into numbered first-flash steps
  Without Home Assistant                      unchanged
  Troubleshooting                             + 2 rows
  Limitations                                 unchanged
```

## 3. Flowchart: screen flow (to be drawn in the README, including error paths)
```
Main (4 slot cards, refresh every 5 s)
  | tap a slot
  v
Scan ("Hold a spool tag on the reader") --Cancel--> Main
  | tag read
  v
GET Spoolman /api/v1/spool
  |-- no connection ------------> Result "Lookup failed: no connection to Spoolman"
  |-- HTTP not 200 -------------> Result "Lookup failed: HTTP <code>"
  |-- reply not JSON array -----> Result "Lookup failed: bad reply"
  |-- no spool has this tag ----> Result "Unknown tag" + UID   (archived spools do not count)
  v found (first match)
Confirm ("Assign spool #N (material) to slot S?", color swatch) --Cancel--> Main
  | Confirm
  v
POST Bambuddy .../slot-assignments   (one attempt, no retry)
  |-- no connection ------------> Result "Assign failed: no connection to Bambuddy"
  |-- HTTP 2xx -----------------> Result "Assigned to slot S"
  |-- other HTTP ---------------> Result "Assign failed: HTTP <code>"
Result --OK--> Main (and an immediate status refresh)
Idle scan (no slot selected): log the UID; send tag_scanned to Home Assistant if enabled
```

## 4. Data flow
```
touch -> ESP32 -> (5 s) GET Bambuddy status  -> slot cards
tag   -> PN532 -> ESP32 -> GET Spoolman spool list -> match extra.tag -> Confirm screen
Confirm -> ESP32 -> POST Bambuddy slot-assignments -> Bambuddy checks the spool exists in Spoolman,
           stores the assignment in its own database (printer and Spoolman location untouched)
```

## 5. Steps (each its own commit, check green between)
1. `docs/API.md` with the reference tables, a short "good to know" list in the README, and a `scripts/check.sh` step that fails if a URL path used in the YAML is missing from `docs/API.md`.
2. Screen-flow diagram.
3. First-flash steps and the tagging request body.
4. Two troubleshooting rows.
5. BOM fixes: soldering required, magnets suggested, link to the vendor schematic for the socket.

## 6. Risks and tests
| Risk | Mitigation |
|---|---|
| `docs/API.md` drifts from the firmware | New check in `scripts/check.sh`: every `/api/v1/...` path in the YAML is in `docs/API.md` |
| A claim is wrong because a source was misread | Each API row cites the upstream route in the ledger row; owner flashes and tries the flow |
| Flash steps untested on hardware | Written as the vendor's procedure with its source named; the ledger row says it was not run here |
| Mermaid fails to render | Render check by eye on GitHub preview; ASCII version stays in this design doc |
