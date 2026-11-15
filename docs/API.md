# API reference

This page lists every outside call the firmware makes, plus the two calls you make by hand once during setup. All of them use plain HTTP on your local network, and `<bambuddy>` and `<spoolman>` stand for the addresses you set in `esphome/filament-selector.yaml`.

The calls were checked against the public source of [Bambuddy](https://github.com/maziggy/bambuddy) (releases 1.3.0 and 1.3.1), the source of [Spoolman](https://github.com/Donkie/Spoolman) (0.27.1) and the firmware in this repository. They were read from source and not sent to a live server.

## Calls the firmware makes

| # | When | Request | Auth | Replies the firmware handles |
|---|---|---|---|---|
| 1 | Every 5 s while on the main screen | `GET <bambuddy>/api/v1/printers/{printer_id}/status` | `X-API-Key` header (the firmware always sends it; Bambuddy only checks it when its authentication is on). Needs the printers-read permission. | 200: reads `ams[0]` (humidity, temp) and each `tray` (id, exists, tray_type, tray_sub_brands, tray_color, remain). Anything else is logged and the screen keeps its last data. |
| 2 | After a tag is read with a slot selected | `GET <spoolman>/api/v1/spool` | None sent. | 200 with a JSON array: skips archived spools, takes the first whose `extra.tag` matches. Other replies show "Lookup failed" messages. |
| 3 | When you tap Confirm | `POST <bambuddy>/api/v1/spoolman/inventory/slot-assignments` | `X-API-Key` header. Needs the inventory-update permission. | 2xx: "Assigned to slot N". Anything else: "Assign failed: HTTP code". One attempt, no retry. |

Body of call 3 (JSON):

| Field | Value sent | Meaning |
|---|---|---|
| `spoolman_spool_id` | the spool found in call 2 | Spoolman's id for the spool |
| `printer_id` | `printer_id` from the YAML | Bambuddy's printer id |
| `ams_id` | `0` | AMS unit. Fixed to the first unit. |
| `tray_id` | selected slot minus 1 (0 to 3) | Slot in that unit |
| `move` | `true` | The spool leaves any other slot it was in. Needs Bambuddy 1.3.0 or newer. |

The firmware allows each request 10 s, accepts up to 65536 bytes in the status and spool-list replies and 4096 bytes in the assignment reply, and polls the NFC reader every second.

If your spools live in Bambuddy's own inventory instead of Spoolman, the YAML has a commented alternative: `/api/v1/inventory/assignments` with the field `spool_id`. Call 2 still reads Spoolman, so that setup needs the lookup changed as well.

## Calls you make once, by hand

| Purpose | Request | Notes |
|---|---|---|
| Find your printer id | `GET <bambuddy>/api/v1/printers/` | Lists your printers with their ids. With one printer the id is normally `1`. Add `-H "X-API-Key: <key>"` if Bambuddy authentication is on. |
| Store a tag on a spool | `PATCH <bambuddy>/api/v1/spoolman/inventory/spools/{spool_id}/tag` with JSON `{"tag_uid": "04A1B2C3D4E5F6"}` | `{spool_id}` is Spoolman's spool id. The UID is 8 to 30 hex characters and not all zeros. Bambuddy writes it into the spool's `tag` extra field and returns 409 if another spool already holds it. With Spoolman 0.27 or newer it also stores a native tag. Needs the inventory-update permission. |

Example request that stores a tag:

```
curl -X PATCH "http://<bambuddy>/api/v1/spoolman/inventory/spools/12/tag" \
  -H "Content-Type: application/json" \
  -d '{"tag_uid": "04A1B2C3D4E5F6"}'
```

Add `-H "X-API-Key: <key>"` if authentication is on. The request writes to your Spoolman data, so run it only for spools you mean to tag.

## Behavior you will notice

- Confirm records the assignment in Bambuddy only. Bambuddy's own documentation string says the assignment is stored in its database and that Spoolman's `location` field is not touched, and nothing is sent to the printer.
- Because `move` is true, assigning a spool to a new slot removes it from its old slot.
- An archived spool never matches: the lookup skips it, and Bambuddy would refuse it with HTTP 400 anyway. The screen shows "Unknown tag".
- If two spools carry the same tag, the first one in Spoolman's list wins.
- The status reply can contain an AMS tray whose `exists` value is unknown (null). The firmware treats that as not present and shows "Empty". This comes from reading the code and has not been seen on hardware.
- A spool list larger than the 65536-byte buffer is most likely cut off, which would show "Lookup failed: bad reply". This is inferred from the buffer size and has not been reproduced.

## Not verified

- The names Bambuddy's settings page shows for API key permissions. Its source calls them `can_read_status` and `can_manage_inventory`.
- Whether Spoolman has any built-in authentication.
- Behavior of a Bambuddy older than 1.3.0 when it receives the `move` field.
