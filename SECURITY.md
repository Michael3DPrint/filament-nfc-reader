# Security

This is a personal project, and only the latest `main` is supported. Report a vulnerability privately with GitHub's "Report a vulnerability" button on this repository's Security tab, and do not post exploit details in a public issue. There is no guaranteed response time.

## Design limits

- The unit talks to Bambuddy and Spoolman over plain HTTP on a trusted local network. This is a design limit and not a bug to report. Do not expose either service to the internet for this project.
- The Bambuddy API key, if you use one, is stored in `esphome/secrets.yaml` on your computer and compiled into the firmware on the unit. Someone with physical access to the unit can probably extract it, because the firmware is not set up with flash encryption, so give the key only the read and inventory permissions. This has not been tested.
- The Wi-Fi password and ESPHome API encryption key are stored the same way.

## What has been checked

The repository was scanned for secrets and personal data with the author's commit hook, and `esphome/secrets.yaml` is git-ignored. No dependency or firmware security scan has been run.
