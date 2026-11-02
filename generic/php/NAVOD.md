# PHP Web (FrankenPHP) – návod

Hostování PHP webů a Laravel aplikací přímo z panelu. Uvnitř běží FrankenPHP (PHP + web server Caddy
v jednom statickém souboru), takže není potřeba žádný speciální Docker image.

## Proč ne Apache uvnitř kontejneru

Pelican kontejnery běží z hotových „yolk“ images a Apache s PHP v nich není. FrankenPHP je jeden soubor,
který jde stáhnout do serveru a běží na standardním `yolks:debian`. Apache zůstává tam, kam patří:
na hostiteli jako HTTPS reverse proxy (viz [REVERSE_PROXY.cs.md](../../REVERSE_PROXY.cs.md)).

## 1. Import

Admin → **Eggs** → **Import** → `egg-php-web.yaml` (Pelican) nebo `egg-pterodactyl-php-web.json` (Pterodactyl).

## 2. Vytvoření serveru

| Pole | Doporučení |
|---|---|
| Alokace | 1 port (HTTP), např. `8080` |
| RAM | 512 MiB pro malý web, 1–2 GiB pro Laravel s frontou |
| Disk | 2 GiB+ |

Hlavní proměnné:

| Proměnná | Význam |
|---|---|
| Document Root | složka uvnitř `www/`, která je veřejná. Laravel/Symfony = `public`, WordPress = `.` |
| Git Repository / Branch | volitelné – repozitář se naklonuje do `www/` |
| Git Username / Access Token | pro privátní repo. Token se posílá jen v hlavičce a neukládá se do `.git/config`. |
| Pull On Start | při každém startu `git pull --ff-only` |
| Composer Install On Start | `composer install --no-dev` při startu |
| Laravel | při startu `artisan migrate --force` + `artisan optimize` |
| Laravel Scheduler / Queue Worker | spustí `schedule:work` / `queue:work` na pozadí |
| PHP Memory Limit / Upload Limit | `memory_limit`, `upload_max_filesize`, `post_max_size` |
| Secure Session Cookie | `1` za HTTPS proxy (doporučeno), `0` jen pro test přes čisté HTTP |

## 3. Struktura souborů

```
/home/container
├── Caddyfile      ← konfigurace web serveru (při reinstalu se nepřepisuje)
├── start.sh       ← startovací logika (při reinstalu se obnoví)
├── bin/php        ← příkaz "php" (wrapper na frankenphp php-cli)
├── composer.phar
├── frankenphp     ← binárka (zakázaná v editoru souborů)
└── www/           ← tvoje aplikace
    └── public/    ← jediná složka dostupná z webu
```

## 4. Test 1 – jednoduchý web

1. Vytvoř server bez Git proměnných.
2. Po instalaci a startu otevři `http://IP_NODU:PORT/` – uvidíš stránku **It works**.
3. Nahraj přes SFTP/File Manager vlastní `www/public/index.php` a obnov stránku.

## 5. Test 2 – Laravel aplikace

1. Proměnné: `Git Repository` = URL tvého Laravel projektu, `Laravel` = `1`.
2. Po instalaci vytvoř v `www/` soubor `.env` (zkopíruj `.env.example`) a nastav minimálně:
   ```dotenv
   APP_ENV=production
   APP_DEBUG=false
   APP_URL=https://tvoje-domena.cz
   DB_CONNECTION=mysql
   DB_HOST=IP_DATABAZE
   DB_PORT=3306
   DB_DATABASE=...
   DB_USERNAME=...
   DB_PASSWORD=...
   SESSION_SECURE_COOKIE=true
   APP_KEY=
   ```
3. `APP_KEY` nech prázdný – při startu se vygeneruje sám (`artisan key:generate`). Když `.env` chybí,
   start se zastaví s hláškou `www/.env is missing`. `.env.example` se schválně nekopíruje automaticky,
   protože obsahuje `APP_DEBUG=true`.
4. Start → v konzoli uvidíš migrace a `Caching framework bootstrap ... DONE`, potom `FrankenPHP started`.
5. Za reverse proxy přidej do Laravelu důvěru proxy (`bootstrap/app.php`):
   ```php
   ->withMiddleware(function (Middleware $middleware) {
       $middleware->trustProxies(at: ['127.0.0.1', '172.16.0.0/12', '10.0.0.0/8', '192.168.0.0/16']);
   })
   ```
   Jinak Laravel generuje `http://` odkazy místo `https://`.

## 6. WordPress

- `Document Root` = `.` a nahraj WordPress do `www/`.
- Za HTTPS proxy přidej do `wp-config.php` před `require_once ABSPATH . 'wp-settings.php';`:
  ```php
  if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https') {
      $_SERVER['HTTPS'] = 'on';
  }
  ```

## 7. Ověření zabezpečení

Všechny tyto adresy musí vracet **404**:

```bash
curl -I http://IP:PORT/.env
curl -I http://IP:PORT/.git/config
curl -I http://IP:PORT/composer.json
curl -I http://IP:PORT/dump.sql
```

A hlavičky na hlavní stránce:

```bash
curl -sI http://IP:PORT/ | grep -iE "x-frame|x-content|referrer|permissions"
```

## 8. Test checklist

- [ ] Instalace stáhne FrankenPHP (v logu `FrankenPHP v1.x PHP 8.x`)
- [ ] Bez Gitu se objeví stránka *It works*
- [ ] S Gitem se repo naklonuje do `www/` a proběhne `composer install`
- [ ] Laravel: migrace a `optimize` proběhnou při startu
- [ ] `.env`, `.git/config`, `composer.json` vrací 404
- [ ] Za reverse proxy funguje HTTPS a přihlášení (cookies)
- [ ] **Stop** server ukončí do pár sekund

## Řešení problémů

| Problém | Řešení |
|---|---|
| `composer install failed` při instalaci | Zkontroluj, že node má přístup na GitHub/Packagist. Při startu se pokus opakuje. |
| Přihlášení se neudrží (přes `http://IP:PORT`) | Cookie má flag Secure – testuj přes HTTPS proxy, nebo dočasně `Secure Session Cookie = 0` (a v Laravelu `SESSION_SECURE_COOKIE=false`) |
| Laravel 500 chyba | Podívej se do `www/storage/logs/laravel.log` (z webu nedostupné) |
| Potřebuji jinou verzi PHP | Statický FrankenPHP má PHP podle verze release. Starší release zvolíš v `FrankenPHP Version` a reinstalem. |
