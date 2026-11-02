# Syncthing

## From their [Website](https://syncthing.net/)

Syncthing is a continuous file synchronisation program. It synchronises files between two or more
computers in real time, encrypted and peer to peer.

## Install notes

- The binary is taken from the official apt repository (`apt.syncthing.net`, stable-v2 channel).
- Keys and config are generated on the first install with the GUI user/password from the variables
  (stored as a bcrypt hash). Built-in upgrades are disabled; reinstall to update.
- The GUI runs on the primary allocation. The sync protocol (TCP) needs a **second allocation** set as *Sync Port*.
  The panel keeps `listenAddress` in `config/config.xml` in sync with it.
- Synced folders must live under `/home/container`, e.g. `/home/container/data/<folder>`.
- NAT-PMP/UPnP and local discovery are disabled; global discovery and relays stay on.

## Server Ports

| Port | default | Protocol |
|------|---------|----------|
| GUI | 8384 | TCP |
| Sync | 22000 | TCP |
