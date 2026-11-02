# BookStack – návod

Wiki pro pravidla serveru, návody a interní dokumentaci. Běží na stejném základu jako egg PHP Web (FrankenPHP)
a potřebuje databázi MySQL/MariaDB.

## 1. Databáze

Nejjednodušší je MySQL 8.4 egg z této sady:

| Proměnná MySQL eggu | Hodnota |
|---|---|
| Database Name | `bookstack` |
| Database User | `bookstack` |
| Database Password | silné heslo (bez mezer, uvozovek, `\`, `$`, `#`) |

Jde to i přes databázi z panelu (Admin → Databases → databázový host). Pak použij údaje, které panel vygeneruje.

## 2. Import a vytvoření serveru

1. Import `egg-bookstack.yaml` (Pelican) / `egg-pterodactyl-bookstack.json` (Pterodactyl).
2. Server: 1 alokace (HTTP), RAM 512 MiB, disk 2 GiB.
3. Proměnné:

| Proměnná | Hodnota |
|---|---|
| App URL | adresa, na které bude wiki dostupná, **bez lomítka na konci**. Pro test `http://IP_NODU:PORT`, v provozu `https://wiki.tvoje-domena.cz` |
| Database Host | IP alokace MySQL serveru (ne `localhost`, ten by ukazoval do vlastního kontejneru) |
| Database Port | port MySQL alokace |
| Database Name / User / Password | stejné jako v kroku 1 |
| Auto Update | `1` = při startu aktualizovat na nejnovější release |
| Upload Limit | max. velikost nahrávaného souboru |

## 3. První start

V konzoli uvidíš postupně:

```
INFO  Application key set successfully.
INFO  Running migrations.
  2014_10_12_000000_create_users_table ...... DONE
  ...
{"level":"info", ... "msg":"FrankenPHP started 🐘" ...}
```

Pokud se opakuje `Database not reachable yet, retrying in 10 seconds`, jsou špatně údaje k databázi,
nebo databáze neběží. Oprav proměnné a restartuj, `.env` se přepíše sám.

## 4. Přihlášení

1. Otevři App URL → přesměruje na `/login`.
2. Přihlas se jako `admin@admin.com` / `password`.
3. **Hned** změň e-mail a heslo: vpravo nahoře → *My Account*.

## 5. Provoz za HTTPS

1. Nastav reverse proxy podle [REVERSE_PROXY.cs.md](../../REVERSE_PROXY.cs.md).
2. Změň `App URL` na `https://...` a restartuj. Cookies se pak automaticky posílají jako Secure.

## 6. Test checklist

- [ ] Instalace doběhne (`BookStack installed`)
- [ ] První start proběhne migracemi a končí `FrankenPHP started`
- [ ] `/login` se načte a přihlášení adminem funguje
- [ ] Vytvoření knihy, stránky a nahrání obrázku funguje
- [ ] `/.env` a `/composer.json` vrací 404
- [ ] Po restartu data zůstanou
- [ ] `Auto Update = 1` při startu zkontroluje novou verzi

## Řešení problémů

| Problém | Řešení |
|---|---|
| Po přihlášení tě to vrátí na login | Nesedí `App URL` s adresou v prohlížeči, nebo máš `https` App URL a přistupuješ přes `http` |
| Obrázky se nenačtou | `App URL` musí přesně odpovídat veřejné adrese |
| Chyba 413 při uploadu | Zvětši `Upload Limit` a v Apache proxy případně `LimitRequestBody` |
| Logy aplikace | `www/storage/logs/laravel.log` |
