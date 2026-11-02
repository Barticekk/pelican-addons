# Assetto Corsa Competizione

## From [Steam](https://store.steampowered.com/app/805550/Assetto_Corsa_Competizione/)

Official GT World Challenge racing simulator by Kunos Simulazioni. The dedicated server
(Steam app `1430110`) is Windows only and runs under Wine.

## Install notes

- **Steam login required.** Only accounts that own ACC can download the server. Use a separate
  account if possible. With e-mail Steam Guard, put the code into *Steam Guard Code* for the first install.
- Edit configs in `acc-config/` as normal UTF-8 JSON (`settings.json`, `event.json`, `assistRules.json`,
  and optionally `eventRules.json` / `entrylist.json` / `bop.json`). On every start they are converted to
  UTF-16 LE into `server/cfg/`, which is what accServer reads.
- `configuration.json` is rebuilt from the egg variables on every start. TCP and UDP both use the primary allocation port.
- `ignorePrematureDisconnects` is set to `0`, as required when running under Wine/containers.

## Installation/System Requirements

|  | Bare Minimum | Recommended |
|---------|---------|---------|
| Processor | 2 cores | 4 cores |
| RAM | 2 GiB | 4 GiB |
| Storage | 2 GiB | 4 GiB |
| Game Ownership | Required for download | |

## Server Ports

| Port | default | Protocol |
|------|---------|----------|
| Game | 9600 | TCP + UDP |
