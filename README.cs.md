# Pelican Addons – eggy

> English version: [README.md](README.md)

14 eggů ve složce `eggs/`, ve struktuře oficiálních repozitářů `pelican-eggs/*`. Pluginy pro Pelican patří do `plugins/`. Každý egg má:

- `egg-*.yaml` – Pelican (formát PLCN_v3) → importuj na Pelicanu
- `egg-pterodactyl-*.json` – Pterodactyl (PTDL_v2) → importuj na Pterodactylu
- `README.md` – anglický popis ve stylu upstream repozitářů (pro případný PR)
- `NAVOD.md` – český návod s testovacím checklistem

Společný návod na HTTPS přes Apache na hostiteli: [eggs/REVERSE_PROXY.cs.md](eggs/REVERSE_PROXY.cs.md).

## Přehled a stav testování

Testy proběhly lokálně v Dockeru: instalační skript v installer kontejneru → start v runtime image
jako uživatel 988, stejně jako to dělá Wings.

| Egg | Složka | Lokální test |
|---|---|---|
| MySQL 8.4 LTS | `eggs/database/sql/mysql` | ✅ instalace, start, SQL konzole, vzdálený uživatel, čisté vypnutí |
| PHP Web (FrankenPHP) | `eggs/generic/php` | ✅ Laravel z gitu, composer, migrace, scheduler, 404 na `.env`/`.git`, hlavičky * |
| BookStack | `eggs/software/bookstack` | ✅ instalace, migrace proti MySQL eggu, přihlášení admina * |
| Vaultwarden | `eggs/software/vaultwarden` | ✅ stažení z Docker Hubu, start, `/alive`, admin token (Argon2) |
| n8n | `eggs/software/n8n` | ✅ instalace (Node 24), migrace, `/healthz`, editor |
| Jellyfin | `eggs/software/jellyfin` | ✅ server + ffmpeg, port z alokace, web UI, SkiaSharp |
| Open WebUI + Ollama | `eggs/software/open-webui` | ✅ instalace, registrace admina, stažení modelu, chat odpověď |
| Syncthing | `eggs/software/syncthing` | ✅ instalace z apt repa, GUI login, sync port na 2. alokaci |
| playit.gg Agent | `eggs/software/playit` | ✅ binárka z ghcr, start, chování s chybějícím/neplatným klíčem |
| Cloudflare Tunnel | `eggs/software/cloudflared` | ✅ start, token se nevypisuje do logu ** |
| Assetto Corsa Competizione | `eggs/steamcmd/assetto_corsa_competizione` | ⚠️ ověřena konverze configů do UTF-16; server sám ne (potřeba Steam účet s ACC) |
| SCUM | `eggs/steamcmd/scum` | ⚠️ ověřené App ID / anonymní depot; server má 15 GB, lokálně nespuštěn |
| Call of Duty 4 (CoD4x) | `eggs/games/cod4x` | ⚠️ název release souboru a done-string ověřeny ze zdrojáků; binárka nespuštěna |
| Farming Simulator 25 | `eggs/games/farming_simulator_25` | 🧪 **experimentální**, neověřené (Wine + licence) |

\* FrankenPHP statická binárka se stahuje z GitHub Releases, které v testovacím prostředí byly blokované.
Test proto běžel se stejnou verzí FrankenPHP (1.13.4, PHP 8.5) z oficiálního Docker image. Název release souboru
je ověřený z oficiálního `install.sh`.
\*\* binárka z oficiálního apt repa Cloudflare (stejná verze jako na GitHubu).

## Vynechané z původního seznamu

| Hra | Proč |
|---|---|
| Chivalry 2 | Neexistují veřejně stažitelné serverové soubory (ani přes SteamCMD). Hostují jen partneři Torn Banner. |
| Stardew Valley | Nemá dedikovaný server. Jde jen o hack s modem a virtuálním displejem nad vlastní kopií hry. To není spolehlivý egg. |

## Doporučené pořadí testování

1. **MySQL 8.4** (potřebuje ho BookStack)
2. **PHP Web** → **BookStack** (proti MySQL)
3. **Vaultwarden**, **n8n**, **Jellyfin**, **Open WebUI** (za HTTPS proxy podle eggs/REVERSE_PROXY.cs.md)
4. **Cloudflare Tunnel** / **playit.gg** (nasměrovat na servery výše)
5. **Syncthing**
6. Hry: **SCUM**, **ACC**, **CoD4x**, nakonec **FS25** (experiment)

Když něco nepůjde, pošli mi z konzole instalace/startu posledních ~50 řádků a upravím to.

## Úpravy eggů

Zdroj pravdy jsou `egg-*.yaml`. Po úpravě vygeneruj Pterodactyl JSON:

```bash
python3 tools/build.py
```

```bash
python3 tools/build.py --check
```
