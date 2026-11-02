# Assetto Corsa Competizione – návod

Dedikovaný server pro ACC (GT3/GT4 závody, ligy). Server je jen pro Windows a běží pod Wine.

## 0. Než začneš

- Potřebuješ **Steam účet, který vlastní ACC**. Anonymní stažení nejde.
- Doporučuji založit samostatný Steam účet a koupit na něj ACC ve slevě, ať v panelu není tvůj hlavní účet.
- Steam Guard:
  - **e-mail**: kód z e-mailu zadáš do *Steam Guard Code* (platí pár minut, pak spusť instalaci),
  - **mobilní aplikace**: nech kód prázdný a během instalace potvrď přihlášení v aplikaci Steam.

## 1. Vytvoření serveru

1. Import `egg-assetto-corsa-competizione.yaml` / `egg-pterodactyl-assetto-corsa-competizione.json`.
2. Server:

| Pole | Hodnota |
|---|---|
| Alokace | 1 port, např. `9600`, **TCP i UDP** (Pelican alokuje oboje) |
| RAM | 2–4 GiB |
| Disk | 4 GiB |
| Docker image | `Wine Latest` |

3. Proměnné: Steam login, název serveru, admin heslo, heslo pro připojení, max. připojení, lobby ano/ne.
   Název a hesla se zapíšou jen při **první** instalaci, potom je měníš v `acc-config/settings.json`.

## 2. Konfigurace

Všechno upravuješ v **`acc-config/`** v běžném editoru panelu (UTF-8):

| Soubor | Co v něm je |
|---|---|
| `settings.json` | název, hesla, `carGroup` (GT3, GT4, GT2, GTC, TCX, FreeForAll), požadavky na rating |
| `event.json` | trať (`track`), počasí, sessions (P/Q/R a jejich délky) |
| `assistRules.json` | povolené asistenty |
| `eventRules.json`, `entrylist.json`, `bop.json` | volitelné, pro ligy – stačí je sem nahrát |

Názvy tratí do `event.json`: např. `monza`, `spa`, `nurburgring`, `silverstone`, `barcelona`, `imola`,
`zandvoort`, `misano`, `paul_ricard`, `brands_hatch`, `hungaroring`, `kyalami`, `suzuka`, `laguna_seca`,
`mount_panorama`, `oulton_park`, `donington`, `snetterton`, `cota`, `indianapolis`, `watkins_glen`, `valencia`, `red_bull_ring`.

`configuration.json` (porty) se generuje automaticky z alokace, neupravuj ho.
Při startu se vše převede do UTF-16 do `server/cfg/`. Soubory ve `server/cfg/` ručně neupravuj, přepíšou se.

## 3. První start

- SteamCMD zkontroluje update a pak se spustí `accServer.exe` pod Wine.
- V konzoli uvidíš výpis serveru. *Running* nastane po řádku `Server starting with version ...`.
- S `Register To Lobby = 1` se server za chvíli objeví ve hře v seznamu serverů.

## 4. Připojení a admin

- Ve hře: **Multiplayer → Server list** → vyhledej název. Pro privátní server použij v `settings.json` heslo.
- Admin v chatu: `/admin TVOJE_ADMIN_HESLO`, pak např. `/next`, `/restart`, `/kick`.

## 5. Test checklist

- [ ] Instalace se přihlásí na Steam a stáhne server (`accServer.exe` existuje)
- [ ] Start převede `acc-config/*.json` a spustí server
- [ ] Panel přejde do *Running*
- [ ] Server je vidět v lobby
- [ ] Připojení a jízda bez odpojování
- [ ] Změna tratě v `event.json` + restart = jiná trať
- [ ] `/admin` heslo funguje

## Řešení problémů

| Problém | Řešení |
|---|---|
| Instalace: `can only be downloaded by a Steam account that owns ACC` | Vyplň Steam login |
| Instalace: `Invalid Password` / `Two-factor code mismatch` | Špatné heslo nebo kód. Vygeneruj nový Steam Guard kód a spusť reinstall hned. |
| Panel zůstane na *Starting*, ale server běží | Jen done-string. Pošli mi první řádky výpisu a upravím ho. |
| Hráči se odpojují po pár sekundách | Zkontroluj, že `ignorePrematureDisconnects` je `0` v `acc-config/settings.json` |
| Server není v lobby | Ověř, že port je otevřený pro TCP i UDP. Za NAT vyplň `Public IP`. |
| Server nenaběhne, že TCP a UDP port jsou stejné | Napiš mi. Upravím egg na dva porty (UDP = primární, TCP = +1). |
| Auto update při startu chce Steam Guard | Nastav `Auto Update = 0` a aktualizuj reinstallem |
