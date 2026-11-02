# Cloudflare Tunnel – návod

Zveřejní weby a webové aplikace z panelu (PHP Web, BookStack, Vaultwarden, n8n, Jellyfin, Open WebUI…)
přes Cloudflare s HTTPS, **bez otevírání portů** a bez certifikátů na serveru.

> Hodí se pro HTTP/HTTPS. Pro herní servery (TCP/UDP) použij egg playit.gg.

## 1. Tunel v Cloudflare

1. Doména musí být v Cloudflare (DNS u Cloudflare).
2. <https://one.dash.cloudflare.com> → **Networks → Tunnels → Create a tunnel** → typ **Cloudflared**.
3. Pojmenuj ho (např. `pelican-node1`).
4. V kroku instalace zvol libovolný systém a z příkazu zkopíruj **jen token**, tedy dlouhý řetězec za `--token`.

## 2. Vytvoření serveru

1. Import `egg-cloudflared.yaml` / `egg-pterodactyl-cloudflared.json`.
2. Server: RAM 128 MiB, disk 100 MiB, alokace libovolná.
3. Proměnné:

| Proměnná | Hodnota |
|---|---|
| Tunnel Token | token z kroku 1 |
| Protocol | `auto`. Když node blokuje odchozí UDP 7844, dej `http2`. |
| Log Level | `info` |

## 3. Start

V konzoli uvidíš:

```
INF Starting tunnel tunnelID=...
INF Registered tunnel connection connIndex=0 ... location=prg01
```

Po `Registered tunnel connection` je server *Running* a v Cloudflare dashboardu se tunel ukáže jako **Healthy**.

## 4. Public hostname → služba v panelu

V tunelu → **Public Hostname → Add**:

| Pole | Příklad |
|---|---|
| Subdomain + Domain | `wiki` + `tvoje-domena.cz` |
| Type | `HTTP` |
| URL | `172.18.0.1:8080` (gateway Docker sítě + port alokace cílového serveru) nebo `IP_NODU:8080` |

> `localhost` nepoužívej, ukazoval by do kontejneru cloudflared.

Po uložení je web na `https://wiki.tvoje-domena.cz`. V cílové aplikaci nastav tuto HTTPS adresu
(BookStack `App URL`, n8n `Public URL`, Vaultwarden `Domain`…).

## 5. Bezpečnost

- Port cílové služby pak nemusí být veřejný. Alokaci dej na interní IP (např. `172.18.0.1`), nebo port zablokuj firewallem.
- Admin rozhraní (např. Vaultwarden `/admin`) můžeš schovat za **Cloudflare Access** (Zero Trust → Access → Applications).
- Token je tajný. Kdo ho má, může tunel spustit. Při úniku tunel v dashboardu smaž nebo vyměň token.

## 6. Test checklist

- [ ] Instalace vypíše verzi cloudflared
- [ ] Bez tokenu start skončí hláškou `Set the Tunnel Token variable first`
- [ ] S tokenem: `Registered tunnel connection` (obvykle 4×) a tunel je *Healthy*
- [ ] Public hostname otevře web z panelu přes HTTPS
- [ ] **Stop** tunel ukončí (v dashboardu *Down*)

## Řešení problémů

| Problém | Řešení |
|---|---|
| `failed to dial to edge with quic` | Nastav `Protocol = http2` |
| Web vrací 502 Bad Gateway | Špatná URL služby, nebo cílový server neběží. Zkus `IP_NODU:PORT`. |
| Aplikace generuje `http://` odkazy | V aplikaci nastav veřejnou `https://` URL a důvěru proxy |
