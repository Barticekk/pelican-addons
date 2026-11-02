# Farming Simulator 25 – návod (EXPERIMENTÁLNÍ)

> **Upozornění:** GIANTS podporuje dedikovaný server jen na Windows. Tenhle egg ho spouští pod Wine
> s virtuálním displejem a **nebyl ověřený od začátku do konce**. Tvůj test je to, co rozhodne,
> jestli to jde. Pošli mi prosím výsledky podle checklistu dole, hlavně u kroku aktivace.

## 1. Co potřebuješ

- Licenci FS25 určenou pro server. GIANTS vyžaduje pro dedikovaný server vlastní licenci, oddělenou od té, na které hraješ.
- Nainstalovanou hru z Windows PC, ideálně verzi z GIANTS eShopu. Steam verze potřebuje běžící Steam klienta, což v kontejneru nepůjde. Typicky
  `C:\Program Files (x86)\Farming Simulator 2025\`.
- Na Windows hru aspoň jednou spusť a aktivuj klíčem, ať jsou aktualizace a DLC stažené.

## 2. Vytvoření serveru

1. Import `egg-farming-simulator-25.yaml` / `egg-pterodactyl-farming-simulator-25.json`.
2. Server:

| Pole | Hodnota |
|---|---|
| Alokace | **2 porty**: primární pro web (např. `8080`) + druhý pro hru (např. `10823`) |
| RAM | 6–8 GiB |
| Disk | 40 GiB+ (hra + DLC) |
| CPU | 4 jádra |
| Docker image | `Wine Latest` |

3. Proměnné: `Game Port` (= druhá alokace), `Web Admin User`, `Web Admin Password`.

## 3. Nahrání hry

Celou instalační složku hry nahraj přes SFTP do `game/`. Musí tam být hlavně:

```
game/
├── dedicatedServer.exe
├── dedicatedServer.xml
├── FarmingSimulator2025.exe
├── data/ ...
└── pdlc/ ... (DLC)
```

## 4. Start

1. Start → Wine si při prvním startu založí prefix a nainstaluje `vcrun2022` a `d3dcompiler_47` (několik minut).
2. Skript nastaví v `game/dedicatedServer.xml` port webu, port hry a admin login.
3. Otevři `http://IP_NODU:WEB_PORT/` a přihlas se.
4. Ve webovém rozhraní nastav název, heslo, mapu a klikni **Start**. Tím se spustí samotná hra v serverovém režimu.

Log hry se vypisuje do konzole (`profile/log.txt`), log nástroje je v `logs/dedicatedServer.log`.

## 5. Test checklist – prosím pošli mi výsledky

- [ ] Start bez chyby `game/dedicatedServer.exe not found`
- [ ] Web rozhraní se otevře na portu primární alokace
- [ ] Přihlášení adminem funguje
- [ ] Po kliknutí **Start** ve webu: spustí se `FarmingSimulator2025.exe`? (sleduj konzoli a `profile/log.txt`)
- [ ] **Aktivace:** chce hra zadat klíč? Co je v `profile/log.txt`?
- [ ] Server se objeví ve hře v seznamu / dá se připojit na `IP:GAME_PORT`
- [ ] Mody: nahrané do `profile/mods/` se ve webu zobrazí

Pokud se zasekne na aktivaci nebo grafice (D3D chyby v logu), pošli mi posledních ~50 řádků z
`profile/log.txt` a `logs/dedicatedServer.log`. Podle nich buď egg upravím, nebo uzavřeme, že bez
Windows to nepůjde.

## Řešení problémů

| Problém | Řešení |
|---|---|
| Web rozhraní se neotevře | Zkontroluj `logs/dedicatedServer.log` a že port alokace sedí s `<webserver port=...>` |
| Hra spadne hned po Start | Pošli logy (viz výš). Zkus image `Wine Staging`. |
| Dlouhý první start | Winetricks instaluje runtime knihovny, to je normální |
