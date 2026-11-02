# Call of Duty 4 (CoD4x)

## From their [Github](https://github.com/callofduty4x/CoD4x_Server)

CoD4x is a modification of the Call of Duty 4: Modern Warfare server. It fixes bugs in the original
binaries and adds variables, plugins and an automatic client update for players.

## Install notes

- The server binary (`cod4x18_dedrun`) and the Linux plugins are downloaded from the GitHub release.
- **You must upload the original game files from your own copy of CoD4:**
  - every `.iwd` from `<CoD4>/main/` into `main/`
  - everything from `<CoD4>/zone/` into `zone/`
- CoD4x fetches its own `xbase_00.iwd` / `cod4x_patchv2.ff` on first start.
- The binary is 32-bit, so the egg runs on the SteamCMD Debian image, which ships the i386 libraries.
- Server settings live in `main/server.cfg`. Mods go into `mods/<name>` and are enabled with the *Mod* variable.
- The console accepts server commands (`map mp_crash`, `status`, `kick`, ...). Stop sends `quit`.

## Installation/System Requirements

|  | Bare Minimum | Recommended |
|---------|---------|---------|
| RAM | 512 MiB | 1 GiB |
| Storage | 8 GiB (with game files) | 10 GiB |
| Game Ownership | Game files required | |

## Server Ports

| Port | default | Protocol |
|------|---------|----------|
| Game | 28960 | UDP (+ TCP for downloads) |
