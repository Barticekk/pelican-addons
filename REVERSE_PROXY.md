# HTTPS reverse proxy (Apache on the host)

> Česká verze: [REVERSE_PROXY.cs.md](REVERSE_PROXY.cs.md)

The web eggs (PHP Web, BookStack, Vaultwarden, n8n, Jellyfin, Open WebUI, the Syncthing GUI) serve plain
HTTP inside their container. TLS is terminated by Apache on the host, with one vhost per service, so
the sites stay independent of each other. If you have no public server, use the Cloudflare Tunnel egg instead.

## 1. Bind allocations to localhost

In the panel (Admin → Nodes → Allocations) create allocations on IP **`127.0.0.1`** and assign them to
the web servers. The service is then reachable only by Apache on the host, not from the internet, so
there is no port to firewall.

## 2. Modules

```bash
sudo a2enmod ssl proxy proxy_http headers rewrite
```

```bash
sudo systemctl reload apache2
```

WebSockets (n8n, Jellyfin, Open WebUI, Vaultwarden) are handled by `upgrade=websocket` on `ProxyPass`,
which needs Apache 2.4.47 or newer (Debian 12 and Ubuntu 24.04 ship newer versions).

## 3. Virtual host

`/etc/apache2/sites-available/wiki.example.com.conf` (adjust the name and port):

```apache
<VirtualHost *:80>
    ServerName wiki.example.com

    RewriteEngine On
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>

<VirtualHost *:443>
    ServerName wiki.example.com

    SSLEngine on
    SSLCertificateFile    /etc/letsencrypt/live/wiki.example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/wiki.example.com/privkey.pem

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

    ErrorLog  ${APACHE_LOG_DIR}/wiki.example.com-error.log
    CustomLog ${APACHE_LOG_DIR}/wiki.example.com-access.log combined
</VirtualHost>
```

Certificate (Let's Encrypt) and activation:

```bash
sudo certbot certonly --apache -d wiki.example.com
```

```bash
sudo a2ensite wiki.example.com && sudo apache2ctl configtest && sudo systemctl reload apache2
```

## 4. Per-egg settings

| Egg | Set in the egg | Proxy notes |
|---|---|---|
| PHP Web | `Secure Session Cookie = 1`, Laravel `trustProxies` | – |
| BookStack | `App URL = https://wiki.example.com` | – |
| Vaultwarden | `Domain = https://vault.example.com` | the web vault does not work without HTTPS |
| n8n | `Public URL = https://n8n.example.com/`, `Secure Cookie = true` | WebSockets required |
| Jellyfin | Dashboard → Networking → Known proxies: `172.18.0.1` | large uploads: `LimitRequestBody 0` in the vhost |
| Open WebUI | `Public URL = https://ai.example.com` | WebSockets required, `timeout=300` for long answers |
| Syncthing | – | keep the GUI private, e.g. `Require ip ...` |

`172.18.0.1` is the default gateway of Pelican's Docker network. Check it with
`docker network inspect pelican_nw`. Connections from Apache through `127.0.0.1` reach the app from that address.

## 5. Check

```bash
curl -sI https://wiki.example.com | grep -iE "strict-transport|x-frame|x-content|referrer"
```

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://wiki.example.com/
```

The second command must print `301` (redirect to HTTPS).
