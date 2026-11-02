# Syncthing – návod

Synchronizace složek mezi zařízeními (P2P, šifrovaně). Typické použití: záloha světů a configů
herních serverů na jiný stroj, sdílení souborů mezi nody nebo náhrada Dropboxu.

## 1. Vytvoření serveru

1. Import `egg-syncthing.yaml` / `egg-pterodactyl-syncthing.json`.
2. Server:

| Pole | Hodnota |
|---|---|
| Alokace | **2 porty**: primární = webové GUI (např. `8384`), druhý = synchronizace (např. `22000`) |
| RAM | 256–512 MiB |
| Disk | podle dat |

3. Proměnné:

| Proměnná | Hodnota |
|---|---|
| GUI User / GUI Password | přihlášení do GUI (heslo min. 12 znaků). Platí jen pro první instalaci. |
| Sync Port | číslo **druhé alokace** |
| Version | `latest` |

## 2. Instalace

```
Downloading pool/syncthing_2.1.6_amd64.deb
Generating keys and configuration
Device ID: MUEKEN4-O2ZCJA4-...
Syncthing installed
```

Device ID si poznamenej, budeš ho zadávat na druhém zařízení (je vidět i v GUI).

## 3. Start a GUI

- *Running* po řádku `GUI and API listening (address=0.0.0.0:8384)`.
- Otevři `http://IP_NODU:GUI_PORT/` a přihlas se.
- Doporučeno: GUI dej za HTTPS reverse proxy ([REVERSE_PROXY.cs.md](../../REVERSE_PROXY.cs.md)), nebo ho nevystavuj veřejně.

## 4. Propojení s jiným zařízením

1. Na druhém zařízení (PC s Syncthingem) → **Add Remote Device** → vlož Device ID serveru.
   Jako adresu můžeš zadat `tcp://IP_NODU:SYNC_PORT`, jinak se najdou přes global discovery.
2. V GUI serveru potvrď nové zařízení.
3. **Add Folder** na serveru: cesta musí být uvnitř `/home/container`, např. `/home/container/data/zalohy`.
4. Sdílej složku s druhým zařízením.

## 5. Záloha herního serveru (tip)

Syncthing nevidí do jiných serverů v panelu (každý má vlastní kontejner). Postup:
- na herním serveru nastav pravidelnou zálohu panelu, nebo
- na hostiteli synchronizuj přímo adresář s volumes (`/var/lib/pelican/volumes/<uuid>`) samostatnou instalací Syncthingu.

## 6. Test checklist

- [ ] Instalace vypíše Device ID
- [ ] GUI na primárním portu vyžaduje přihlášení, špatné heslo neprojde
- [ ] Druhé zařízení se připojí (stav *Connected*)
- [ ] Soubor přidaný na jedné straně se objeví na druhé
- [ ] Po restartu zůstanou zařízení i složky
- [ ] Změna Sync Port + restart se propíše do `config/config.xml`

## Řešení problémů

| Problém | Řešení |
|---|---|
| Zařízení se nepřipojí napřímo | Chybí druhá alokace, nebo `Sync Port` neodpovídá alokaci. Přes relay to jde, ale pomaleji. |
| Zapomenuté heslo GUI | Zastav server, smaž `<user>`/`<password>` v `config/config.xml` v sekci `<gui>` a nastav znovu v GUI |
| `folder path missing` | Cesta složky musí být pod `/home/container` |
