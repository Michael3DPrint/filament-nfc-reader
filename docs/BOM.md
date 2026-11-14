# Bill of materials

Parts used in the working build. No part here needs a soldered PCB of your own.

## Required

| Qty | Part | Notes |
|---|---|---|
| 1 | LCDWiki ES3C40P, 4.0" ESP32-S3 IPS display board | 320x480 ST7796 display, capacitive touch, ESP32-S3 with 16 MB flash and 8 MB PSRAM, USB-C. Product page: https://www.lcdwiki.com/4.0inch_ESP32-S3_Display |
| 1 | PN532 NFC RFID module V3 | I2C mode (switch 1 ON, switch 2 OFF). Headers or bare pads are fine if you solder wires directly. |
| 1 | MX1.25 (1.25 mm pitch) 4-pin pigtail cable | Plugs into the display board's IIC connector. Bare leads on the other end solder to the PN532. Buy a multipack and test the fit, since 1.25 mm connectors come in several look-alike families (not 1.0 mm or 1.5 mm). |
| 1+ | NFC tags, NTAG213/215 class stickers | One per spool. They report as "Mifare Ultralight" in the ESPHome log. Any ISO 14443A tag with a readable UID works, because the firmware matches on the UID. |
| 1 | USB-C cable and a 5 V supply | Powers the whole unit. |

## Helpful

| Part | Notes |
|---|---|
| Soldering iron and solder | For the four PN532 wires. |
| 26 to 28 AWG stranded silicone wire | Use if you make your own cable. Avoid solid core, which fatigues and breaks. |
| Heat shrink or hot glue | Strain relief at both ends of the cable. |

## Prototyping only (not needed for the final build)

| Part | Notes |
|---|---|
| ESP32-S3-DevKitC-1, N16R8 (CP2102 USB-C) | Used to prove the PN532 and ESPHome setup before moving to the display board. |
| Breadboard | Used with the DevKitC. |

## Case

Print the rigid parts from [hardware/case](../hardware/case/README.md) in PLA. The design also uses TPU washers, which are not in the repo yet.
