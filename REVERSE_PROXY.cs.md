# HTTPS reverse proxy (Apache na hostiteli)

Webové eggy (PHP Web, BookStack, Vaultwarden, n8n, Jellyfin, Open WebUI, Syncthing GUI) běží v kontejneru
na čistém HTTP. TLS řeší Apache na hostiteli, každá služba má vlastní vhost a navzájem se neovlivňují.
(Bez vlastního serveru jde místo toho použít egg Cloudflare Tunnel.)

## 1. Alokace jen na localhost

V panelu (Admin → Nodes → Allocations) vytvoř alokace na IP **`127.0.0.1`** a dej je webovým serverům.
Služba je pak dostupná jen pro Apache na hostiteli, ne z internetu. Port tak není potřeba hlídat firewallem.

## 2. Moduly

```bash
sudo a2enmod ssl proxy proxy_http headers rewrite
```

```bash
sudo systemctl reload apache2
```

Websockety (n8n, Jellyfin, Open WebUI, Vaultwarden) řeší `upgrade=websocket` v `ProxyPass`, potřeba je Apache 2.4.47+
(Debian 12 / Ubuntu 24.04 to splňují).

## 3. Vhost

`/etc/apache2/sites-available/wiki.example.cz.conf` (název a port uprav):

```apache
<VirtualHost *:80>
    ServerName wiki.example.cz

    RewriteEngine On
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>

<VirtualHost *:443>
    ServerName wiki.example.cz

    SSLEngine on
    SSLCertificateFile    /etc/letsencrypt/live/wiki.example.cz/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/wiki.example.cz/privkey.pem

    ProxyRequests Off
    ProxyPreserveHost On
    RequestHeader set X-Forwarded-Proto "https"
    RequestHeader set X-Forwarded-Port "443"

    ProxyPass        / http://127.0.0.1:8080/ upgrade=websocket timeout=300
    ProxyPassReverse / http://127.0.0.1:8080/

    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains"
    Header always setifempty X-Content-Type-Options "nosniff"
    Header always setifempty Referrer-Policy "strict-origin-when-cross-origin"
    Header always setifempty X-Frame-Options "SAMEORIGIN"

    ErrorLog  ${APACHE_LOG_DIR}/wiki.example.cz-error.log
    CustomLog ${APACHE_LOG_DIR}/wiki.example.cz-access.log combined
</VirtualHost>
```

Certifikát (Let's Encrypt) a aktivace:

```bash
sudo certbot certonly --apache -d wiki.example.cz
```

```bash
sudo a2ensite wiki.example.cz && sudo apache2ctl configtest && sudo systemctl reload apache2
```

## 4. Specifika jednotlivých eggů

| Egg | Co nastavit v eggu | Poznámka k proxy |
|---|---|---|
| PHP Web | `Secure Session Cookie = 1`, v Laravelu `trustProxies` | – |
| BookStack | `App URL = https://wiki.example.cz` | – |
| Vaultwarden | `Domain = https://vault.example.cz` | bez HTTPS web vault nefunguje |
| n8n | `Public URL = https://n8n.example.cz/`, `Secure Cookie = true` | websockety nutné |
| Jellyfin | Dashboard → Networking → Known proxies: `172.18.0.1` | velké soubory: `LimitRequestBody 0` ve vhostu |
| Open WebUI | `Public URL = https://ai.example.cz` | websockety nutné, `timeout=300` kvůli dlouhým odpovědím |
| Syncthing | – | GUI raději jen pro sebe (např. `Require ip ...`) |

`172.18.0.1` je výchozí gateway Docker sítě Pelicanu (`pelican0`). Zkontroluj ji příkazem
`docker network inspect pelican_nw`. Spojení z Apache přes `127.0.0.1` vidí aplikace jako tuto IP.

## 5. Kontrola

```bash
curl -sI https://wiki.example.cz | grep -iE "strict-transport|x-frame|x-content|referrer"
```

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://wiki.example.cz/
```

Druhý příkaz musí vrátit `301` (přesměrování na HTTPS).
