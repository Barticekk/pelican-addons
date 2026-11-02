# SCUM – návod

Survival hra na ostrově s vězni. Oficiální dedikovaný server je jen pro Windows, v eggu běží pod Wine.
Server se stahuje přes SteamCMD **anonymně**, hru vlastnit nemusíš.

## 1. Alokace (důležité)

SCUM používá několik portů po sobě. Když je primární port `7777`, přidej serveru tyto alokace:

| Port | K čemu |
|---|---|
| `7777` | primární (game) |
| `7778` | raw UDP (game + 1) |
| `7779` | **připojení hráčů** (game + 2) |
| `27015` | Steam query (proměnná *Query Port*) |

Query port nesmí být v rozsahu 27020–27050.

## 2. Vytvoření serveru

1. Import `egg-scum.yaml` / `egg-pterodactyl-scum.json`.
2. Server:

| Pole | Hodnota |
|---|---|
| RAM | **min. 12 GiB**, doporučeno 16 GiB |
| Disk | **min. 25 GiB** (server má cca 15 GB) |
| CPU | 4+ jádra |
| Docker image | `Wine Staging` (když nepůjde, zkus `Wine Latest`) |

3. Proměnné: název, popis, heslo, max. hráčů, PVP/PVE, query port, BattlEye.

## 3. Instalace

SteamCMD stáhne cca 15 GB. Instalace trvá podle linky 5–30 minut. Konec logu:

```
Success! App '3792580' fully installed.
SCUM server installed
```

Když instalace spadne uprostřed stahování, dej **Reinstall**. SteamCMD navazuje.

## 4. První start

- Na začátku proběhne SteamCMD update a winetricks `vcrun2022`. První start je proto delší.
- Do konzole se vypisuje `SCUM/Saved/Logs/SCUM.log`.
- Server je připravený (*Running*), když se objeví `Config entry: GameID scum`.
  Kdyby panel zůstal na *Starting*, ale hráči se připojí, je to jen kosmetika. Dej vědět a upravím done-string.
- První start vygeneruje kompletní `ServerSettings.ini` a `GameUserSettings.ini`.

## 5. Připojení

Ve hře: **Play → Servers → Connect via IP** → `IP_NODU:7779` (game port + 2).
V server browseru se server objeví po pár minutách.

## 6. Admini

Do `SCUM/Saved/Config/WindowsServer/AdminUsers.ini` přidej SteamID64 (jedno na řádek):

```
76561198000000000
76561198000000001
```

Po restartu fungují příkazy `#` v chatu.

## 7. Test checklist

- [ ] Instalace stáhne server (`fully installed`)
- [ ] Start: Wine naběhne, v konzoli se objeví log SCUM
- [ ] Panel přejde do *Running* (done-string)
- [ ] Hráč se připojí přes `IP:game+2`
- [ ] Server je vidět v browseru (query port)
- [ ] Název a heslo z proměnných se propíšou do hry
- [ ] **Stop** server vypne do 30 s
- [ ] Po restartu postava a svět zůstanou

## Řešení problémů

| Problém | Řešení |
|---|---|
| Server spadne hned po startu, OOM | Málo RAM, SCUM potřebuje 12 GiB+ |
| Nejde se připojit | Chybí alokace game+1 / game+2, nebo se připojuješ na primární port místo +2 |
| Není vidět v browseru | Chybí alokace query portu, nebo je v rozsahu 27020–27050 |
| Chyby `vcruntime` v logu | Nech `Winetricks = vcrun2022`, smaž `.wine` a restartuj |
| Start trvá dlouho | Při `Auto Update = 1` se při každém startu kontroluje update |
