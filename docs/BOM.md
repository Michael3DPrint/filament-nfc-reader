# Bill of materials

The build needs a display board, a PN532 module, a cable, NFC tags and a USB-C supply, plus a soldering iron, 10 screws and a printed case. No custom PCB is needed, but you solder four wires to the PN532. These are the parts used in the working build.

## Required

| Qty | Part | Notes |
|---|---|---|
| 1 | LCDWiki ES3C40P, 4.0" ESP32-S3 IPS display board | 320x480 ST7796 display, capacitive touch, ESP32-S3 with 16 MB flash and 8 MB PSRAM, and a USB-C port for power and programming. See the vendor's [product page](https://www.lcdwiki.com/4.0inch_ESP32-S3_Display), which links the schematic PDF with the I2C socket pinout. |
| 1 | PN532 NFC RFID module V3 | Set it to I2C mode (switch 1 ON, switch 2 OFF). It can have headers or bare pads, because you solder wires to it. |
| 1 | 1.25 mm pitch, 4-pin pigtail cable (MX1.25) | Plugs into the display board's I2C socket. Its bare leads are soldered to the PN532. Buy a multipack and test the fit, because 1.25 mm connectors come in several look-alike families, and 1.0 mm and 1.5 mm versions will not fit. |
| 1 or more | NFC tags, NTAG213/215 class stickers | One per spool. They report as "Mifare Ultralight" in the ESPHome log. Any ISO 14443A tag with a readable UID works, because the firmware matches on the UID. |
| 1 | USB-C cable and a 5 V supply | Powers the whole unit. |
| 1 | Soldering iron and solder | Required for the four joints between the cable's bare leads and the PN532. |

## Helpful

| Part | Notes |
|---|---|
| 26 to 28 AWG stranded silicone wire | For making your own cable. Avoid solid core, which fatigues and breaks. |
| Heat shrink or hot glue | Strain relief at both ends of the cable. |

## Case

The printed case has five rigid parts and eight TPU washers, described in [hardware/case](../hardware/case/README.md). The fastener sizes below were measured from the v10 files.

| Qty | Part | Notes |
|---|---|---|
| 10 | M3 x 8 mm screws, low-profile heads | One length fits all three screwed joints, and they go straight into the printed holes. The [case README](../hardware/case/README.md#fastening) lists where each one goes and why that length works. |
| 1, optional | Superglue (cyanoacrylate) | Can replace the 2 arm-to-body screws, which leaves 8 screws to buy. See [Fastening](../hardware/case/README.md#fastening) for when to keep the screws. This is a suggestion that has not been tested. |
| 4, optional | Stick-on feet, up to 9 mm across and 1.2 mm thick | They fit the recesses described in [Feet recesses](../hardware/case/README.md#feet-recesses). No foot size has been test-fitted. |

## Prototyping only

You do not need these for the final build. They were used to prove the PN532 and ESPHome setup before moving to the display board.

| Part | Notes |
|---|---|
| ESP32-S3-DevKitC-1, N16R8 (CP2102 USB-C) | A development board for the first tests. |
| Breadboard | Used with the DevKitC. |
