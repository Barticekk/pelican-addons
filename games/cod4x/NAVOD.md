# Call of Duty 4 (CoD4x) – návod

Server pro Call of Duty 4: Modern Warfare v udržované verzi CoD4x (opravy chyb, pluginy, nový master server).

## 1. Vytvoření serveru

1. Import `egg-cod4x.yaml` / `egg-pterodactyl-cod4x.json`.
2. Server:

| Pole | Hodnota |
|---|---|
| Alokace | `28960` (UDP; Pelican alokuje TCP i UDP) |
| RAM | 1 GiB |
| Disk | 10 GiB |
| Docker image | `Debian (32-bit libs)` |

3. Proměnné:

| Proměnná | Hodnota |
|---|---|
| Max Players | počet slotů |
| Server Config | `server.cfg` (soubor v `main/`) |
| RCON Password | zapíše se do `server.cfg` při první instalaci |
| Auth Token | token z cod4x.ovh, aby byl server vidět v master listu |
| Mod (fs_game) | např. `mods/promod`, prázdné = čistá hra |

## 2. Herní soubory (povinné)

Instalace stáhne jen CoD4x server. Původní data hry nahraj ze své kopie CoD4 (Steam: `steamapps/common/Call of Duty 4`)
přes SFTP:

| Ze hry | Do serveru |
|---|---|
| `main/*.iwd` (iw_00.iwd … iw_13.iwd, localized_*.iwd) | `main/` |
| obsah `zone/` (složka `english` atd.) | `zone/` |

Bez nich server hned spadne na chybějících souborech. Konzole po instalaci vypíše připomínku.

## 3. Konfigurace

Uprav `main/server.cfg`: název (`sv_hostname`), heslo (`g_password`), RCON, gametype a rotaci map.
Při použití modu (např. promod) dej konfiguraci do složky modu (`mods/promod/server.cfg`), protože `exec`
hledá soubory v aktivním modu.

## 4. První start

Server je *Running* po řádku:

```
By using this software you agree to the usage conditions ...
```

Konzole přijímá příkazy, např. `status`, `map mp_crash`, `map_rotate`, `kick jméno`.

## 5. Připojení

Ve hře: konzole `~` → `/connect IP_NODU:28960`. Hráčům se při prvním připojení nainstaluje CoD4x klient automaticky.

## 6. Test checklist

- [ ] Instalace stáhne `cod4x18_dedrun` a pluginy
- [ ] Po nahrání `main/*.iwd` a `zone/` server naběhne
- [ ] Panel přejde do *Running*
- [ ] Hráč se připojí, mapa se načte
- [ ] `map_rotate` a příkazy v konzoli fungují
- [ ] **Stop** (`quit`) server ukončí
- [ ] S Auth Tokenem je server vidět v master listu

## Řešení problémů

| Problém | Řešení |
|---|---|
| `error while loading shared libraries` | Musí být zvolený image `Debian (32-bit libs)` |
| `Couldn't load default_mp.cfg` / chybí soubory | Chybí `main/*.iwd` nebo `zone/` z originální hry |
| Server není v seznamu | Vyplň `Auth Token` z cod4x.ovh |
| Hráči nestahují custom mapy | `sv_allowDownload 1`, mapy patří do `usermaps/` |
| Instalace nestáhne binárku | Ověř tag v `CoD4x Version` (např. `21.2`) nebo použij `latest` |
