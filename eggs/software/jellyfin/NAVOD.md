# Jellyfin – návod

Vlastní „Netflix“ pro filmy, seriály, hudbu a fotky. Aplikace jsou pro TV, mobil i prohlížeč.

## 1. Import a vytvoření serveru

1. Import `egg-jellyfin.yaml` / `egg-pterodactyl-jellyfin.json`.
2. Server:

| Pole | Hodnota |
|---|---|
| Alokace | 1 port (HTTP), např. `8096` |
| CPU | čím víc, tím líp (překódování běží na CPU) |
| RAM | 2–4 GiB |
| Disk | 2 GiB + velikost knihovny |

3. Proměnná `Jellyfin Version`: `latest`, nebo konkrétní verze.

## 2. Instalace

Stáhne server a jellyfin-ffmpeg z `repo.jellyfin.org`. Konec logu:

```
Installed jellyfin_12.4-amd64.tar.xz with jellyfin-ffmpeg_8.1.3-1_portable_linux64-gpl.tar.xz
Put media into /home/container/media
```

## 3. První start

```
[INF] Main: Kestrel is listening on 0.0.0.0
[INF] MediaBrowser.MediaEncoding.Encoder.MediaEncoder: Found ffmpeg version 8.1.3
[INF] Main: Startup complete 0:00:08
```

Varování `Microsoft.EntityFrameworkCore.Migrations ... rebuild of table` při **prvním** startu jsou normální.

## 4. Průvodce nastavením

1. Otevři `http://IP_NODU:PORT/` → spustí se setup wizard.
2. Vytvoř admin účet (silné heslo).
3. **Add Media Library** → typ (Movies/Shows/Music) → složka `/home/container/media/filmy` (vytvoř si podsložky).
4. Dokonči průvodce.

Nahrávání médií: SFTP z panelu do `media/`. Struktura podle doporučení Jellyfinu:
```
media/
├── filmy/Avatar (2009)/Avatar (2009).mkv
└── serialy/Dark/Season 01/Dark S01E01.mkv
```

## 5. Doporučené nastavení (CPU only)

- Dashboard → **Playback → Transcoding**: hardware acceleration `None`, *Throttle transcodes* zapnout.
- Uživatelům omez *Internet streaming bitrate limit* (např. 8 Mbps), aby server nepřekódovával 4K.
- Na klientech preferuj Direct Play (Jellyfin Media Player, Kodi, Infuse).

## 6. Provoz za HTTPS

Reverse proxy podle [REVERSE_PROXY.cs.md](../../REVERSE_PROXY.cs.md). V Dashboard → **Networking** nastav
*Known proxies* na IP proxy (u Apache na stejném stroji typicky `172.18.0.1`, což je gateway sítě kontejnerů).

## 7. Test checklist

- [ ] Instalace stáhne server i ffmpeg
- [ ] Start končí `Startup complete` a log ukazuje `Found ffmpeg version`
- [ ] Web otevře setup wizard na správném portu
- [ ] Knihovna se naskenuje, u filmů se stáhnou obrázky (to ověřuje SkiaSharp/fontconfig)
- [ ] Přehrání videa v prohlížeči funguje (i s překódováním)
- [ ] Změna portu alokace se po restartu propíše (`config/network.xml`)
- [ ] Reinstall zachová knihovnu a uživatele

## Řešení problémů

| Problém | Řešení |
|---|---|
| Žádné obrázky / v logu `NullImageEncoder` | Chybí `lib/libfontconfig.so.1`, udělej Reinstall |
| Video se seká | Překódování je na CPU moc náročné. Sniž bitrate nebo použij Direct Play klienta. |
| Běží na 8096 místo alokace | Zkontroluj `config/network.xml` a restartuj |
| Titulky se špatnými znaky | Vlastní fonty dej do složky `fonts/` |
