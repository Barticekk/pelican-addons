# Pelican Addons

Server eggs for [Pelican Panel](https://pelican.dev) and [Pterodactyl](https://pterodactyl.io): games that
had no egg yet, and self-hosted software that is useful to run next to game servers.

> Česká verze a testovací návody: [README.cs.md](README.cs.md)

Every egg ships in both formats:

| File | Panel | Format |
|---|---|---|
| `egg-<name>.yaml` | Pelican | `PLCN_v3` |
| `egg-pterodactyl-<name>.json` | Pterodactyl | `PTDL_v2` |

Each egg folder also has a `README.md` (requirements, ports, notes) and a `NAVOD.md` with a step-by-step
setup guide and test checklist (in Czech).

## Eggs

### Games

| Egg | Runs on | Install source | Status |
|---|---|---|---|
| [SCUM](steamcmd/scum) | Wine | SteamCMD `3792580`, anonymous | ⚠️ untested |
| [Assetto Corsa Competizione](steamcmd/assetto_corsa_competizione) | Wine | SteamCMD `1430110`, account that owns ACC | ⚠️ config pipeline tested |
| [Call of Duty 4 (CoD4x)](games/cod4x) | SteamCMD Debian (i386 libs) | CoD4x GitHub release + your game files | ⚠️ untested |
| [Farming Simulator 25](games/farming_simulator_25) | Wine + Xvfb | your installed, licensed game | 🧪 experimental |

### Software

| Egg | What it is | Runs on | Status |
|---|---|---|---|
| [PHP Web (FrankenPHP)](generic/php) | PHP sites and Laravel apps, git deploy, Composer, scheduler and queue | Debian | ✅ tested |
| [BookStack](software/bookstack) | Wiki for rules, guides and staff docs | Debian | ✅ tested |
| [MySQL 8.4 LTS](database/sql/mysql) | Oracle MySQL, for plugins that expect MySQL rather than MariaDB | Debian | ✅ tested |
| [Vaultwarden](software/vaultwarden) | Bitwarden-compatible password manager | Debian | ✅ tested |
| [n8n](software/n8n) | Workflow automation | Node.js 24 | ✅ tested |
| [Jellyfin](software/jellyfin) | Media server | Debian | ✅ tested |
| [Open WebUI + Ollama](software/open-webui) | Self-hosted AI chat with local models | Python 3.12 | ✅ tested |
| [Syncthing](software/syncthing) | Peer-to-peer file sync | Debian | ✅ tested |
| [playit.gg Agent](software/playit) | Reach game servers without a public IP | Debian | ✅ tested |
| [Cloudflare Tunnel](software/cloudflared) | Publish web services over HTTPS without open ports | Debian | ✅ tested |

**Tested** means the install script and the server were run in Docker the way Wings runs them: the install script
in the installer image against `/mnt/server`, then the startup command in the runtime image as an unprivileged user,
with a 1 GiB installer memory limit and a 100 MB `/tmp`. **Untested** eggs could not be run end to end without a
game licence or large downloads. Reports are welcome.

All runtime images are the stock `ghcr.io/pelican-eggs/yolks` and `ghcr.io/pelican-eggs/steamcmd` images.
No custom images are needed.

## Installing an egg

**Pelican:** Admin → Eggs → Import → upload `egg-<name>.yaml`, or paste the raw GitHub URL of the file.

**Pterodactyl:** Admin → Nests → pick or create a nest → Import Egg → upload `egg-pterodactyl-<name>.json`.

Then create a server with the egg, check the egg's `README.md` for the ports it needs, and fill in the variables.
Several eggs need a second allocation (SCUM, Syncthing, Farming Simulator 25). The variable descriptions say which.

## Design notes

- **Only the public folder is served.** The PHP and BookStack eggs serve `www/public` only. Dotfiles (except
  `/.well-known/`), `.env`, `.sql`, `.log`, `.bak`, `.ini`, `.yml` and Composer files return 404, security headers are
  set, and `expose_php`, `display_errors` and `allow_url_include` are off.
- **No unauthenticated APIs are published.** Ollama listens on `127.0.0.1` inside its container, and cloudflared's
  metrics endpoint does too.
- **Secrets stay out of files and logs where possible.** Git access tokens are sent as an HTTP header and never written
  to `.git/config`, tunnel tokens are passed through the environment, and generated secret files are mode `600`.
- **TLS belongs on the host.** Web eggs serve plain HTTP on their allocation and are meant to sit behind a reverse
  proxy. See [REVERSE_PROXY.md](REVERSE_PROXY.md) for an Apache setup, or use the Cloudflare Tunnel egg.
- **Failures are visible.** Install scripts print `Install failed at line …` with the failing command, and startup
  commands explain what is missing instead of failing with `No such file or directory`.
- **Big installs happen where the resources are.** Open WebUI installs on the first start in the runtime container,
  because Wings caps installer containers at 1 GiB RAM by default and runs `/tmp` as a small tmpfs.

## Requirements at a glance

| Egg | RAM | Disk | Ports |
|---|---|---|---|
| SCUM | 12–16 GiB | 25 GiB+ | game, game+1, game+2, query |
| Assetto Corsa Competizione | 2–4 GiB | 4 GiB | game (TCP + UDP) |
| Call of Duty 4 (CoD4x) | 1 GiB | 10 GiB | game |
| Farming Simulator 25 | 6–8 GiB | 40 GiB+ | web, game |
| PHP Web | 512 MiB+ | 2 GiB+ | HTTP |
| BookStack | 512 MiB | 2 GiB | HTTP |
| MySQL 8.4 | 512 MiB–2 GiB | 1 GiB + data | MySQL |
| Vaultwarden | 256 MiB | 1 GiB | HTTP |
| n8n | 1–2 GiB | 4 GiB+ | HTTP |
| Jellyfin | 2–4 GiB | 2 GiB + media | HTTP |
| Open WebUI + Ollama | 4 GiB+ | 6 GiB + models | HTTP |
| Syncthing | 256–512 MiB | data | GUI, sync |
| playit.gg Agent | 128 MiB | 100 MiB | none used |
| Cloudflare Tunnel | 128 MiB | 100 MiB | none used |

## Repository layout

```
.
├── database/sql/mysql/
├── games/
│   ├── cod4x/
│   └── farming_simulator_25/
├── generic/php/
├── software/
│   ├── bookstack/  cloudflared/  jellyfin/  n8n/
│   └── open-webui/ playit/  syncthing/  vaultwarden/
├── steamcmd/
│   ├── assetto_corsa_competizione/
│   └── scum/
├── tools/build.py
└── REVERSE_PROXY.md
```

The folders mirror the upstream [pelican-eggs](https://github.com/pelican-eggs) repositories, so an egg can be
moved into a pull request there as-is.

## Editing eggs

The YAML files are the source of truth. After changing one, regenerate the Pterodactyl export and validate everything:

```bash
python3 tools/build.py
```

```bash
python3 tools/build.py --check
```

`--check` validates without writing: required keys, variable names and rules, and that every `{{VARIABLE}}` used in a
startup command is declared. It needs Python 3 with PyYAML.

## Reporting problems

Open an issue with:

- the egg and panel (Pelican or Pterodactyl) version,
- the install output (also stored on the node in `/var/log/pelican/install/<server-uuid>.log`),
- the last 50 or so lines of the server console.
