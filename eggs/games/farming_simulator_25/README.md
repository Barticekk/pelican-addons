# Farming Simulator 25 (experimental)

## From [GIANTS Software](https://www.farming-simulator.com/)

Farming Simulator 25 ships a dedicated server tool (`dedicatedServer.exe`) with a web interface that
starts and manages the game in server mode.

## Status: experimental

GIANTS supports the dedicated server on Windows only. This egg runs it under Wine with Xvfb and has
**not been verified end to end**. Known risks:

- The game may ask for product key activation in a GUI dialog that cannot be answered headless.
- The game in server mode may need Direct3D features Wine cannot provide without a GPU.

## Install notes

- Nothing is downloaded. Upload your installed, licensed game folder (the one containing
  `dedicatedServer.exe` and `dedicatedServer.xml`) into `game/`.
- The web interface runs on the primary allocation. The game port is a second allocation (`Game Port`).
- The game profile (savegames, mods, `log.txt`) is in the Wine prefix and linked as `profile/`.

## Server Ports

| Port | default | Protocol |
|------|---------|----------|
| Web interface | 8080 | TCP |
| Game | 10823 | TCP + UDP |
