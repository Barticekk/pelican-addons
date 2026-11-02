# Vaultwarden

## From their [Github](https://github.com/dani-garcia/vaultwarden)

Unofficial Bitwarden-compatible server written in Rust. Works with the official Bitwarden apps,
browser extensions and CLI.

## Install notes

- Vaultwarden is distributed only as container images. The install script pulls the official
  `vaultwarden/server:<version>-alpine` image from Docker Hub with the registry API and copies its
  statically linked `/vaultwarden` binary and `/web-vault` out of the layers. No Docker on the node is needed.
- The web vault requires HTTPS (browsers only expose Web Crypto on secure origins). Put it behind a reverse proxy with TLS and set `Domain` to that URL.
- Data (SQLite database, attachments, keys) lives in `data/`. Back it up.
- `Admin Token` should be an Argon2 PHC string generated with `vaultwarden hash`. When it is empty, `/admin` is disabled.
- Reinstall to update. `data/` is kept.

## Installation/System Requirements

|  | Bare Minimum | Recommended |
|---------|---------|---------|
| RAM | 64 MiB | 256 MiB |
| Storage | 150 MiB | 1 GiB+ (attachments) |

## Server Ports

| Port | default |
|------|---------|
| HTTP | 8080    |
