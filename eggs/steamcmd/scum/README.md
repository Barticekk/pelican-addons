# SCUM

## From [Steam](https://store.steampowered.com/app/513710/SCUM/)

SCUM is an open world survival game with deep character customisation and a prison island setting.
The dedicated server (Steam app `3792580`, anonymous login) is Windows only and runs under Wine.

## Install notes

- Players connect to **game port + 2**. Allocate the primary port and the two ports after it, plus the query port.
- Server settings live in `SCUM/Saved/Config/WindowsServer/`. Name, description, password, playstyle and
  max players are written into `ServerSettings.ini` on every start. Edit the other settings there or in `GameUserSettings.ini`.
- Admins: add SteamID64s to `SCUM/Saved/Config/WindowsServer/AdminUsers.ini`, one per line.
- The console shows `SCUM/Saved/Logs/SCUM.log`. The server does not read console input.

## Installation/System Requirements

|  | Bare Minimum | Recommended |
|---------|---------|---------|
| Processor | 4 cores x86_64 | 6+ cores, high clock |
| RAM | 12 GiB | 16 GiB |
| Storage | 25 GiB | 40 GiB |
| Game Ownership | Not required (anonymous SteamCMD) | |

## Server Ports

| Port | default | Protocol |
|------|---------|----------|
| Game | 7777 | UDP + TCP |
| Raw UDP (game + 1) | 7778 | UDP |
| Connect (game + 2) | 7779 | UDP |
| Query | 27015 | UDP |
