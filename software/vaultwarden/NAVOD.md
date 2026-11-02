# Vaultwarden – návod

Vlastní správce hesel kompatibilní s aplikacemi Bitwarden (desktop, mobil, rozšíření do prohlížeče).

> **HTTPS je povinné.** Webový trezor bez HTTPS nefunguje, protože prohlížeč mimo zabezpečený původ
> nepovolí šifrovací API. Před testem si připrav reverse proxy podle [REVERSE_PROXY.cs.md](../../REVERSE_PROXY.cs.md).

## 1. Import a vytvoření serveru

1. Import `egg-vaultwarden.yaml` / `egg-pterodactyl-vaultwarden.json`.
2. Server: 1 alokace, RAM 256 MiB, disk 1 GiB.
3. Proměnné:

| Proměnná | Hodnota |
|---|---|
| Domain | `https://vault.tvoje-domena.cz` (přesně adresa za proxy) |
| Allow Signups | `true` na začátku, po vytvoření účtů přepni na `false` |
| Allow Invitations | `true` = můžeš zvát lidi přes organizace |
| Admin Token | Argon2 hash (viz níže), prázdné = admin panel vypnutý |
| Show Password Hints | `false` (doporučeno) |
| Version | `latest` nebo konkrétní, např. `1.37.5` |

## 2. Instalace

Instalace stáhne oficiální image z Docker Hubu přes registry API (bez Dockeru) a vytáhne z něj
binárku a web vault. V logu uvidíš:

```
Resolving vaultwarden/server:latest-alpine for linux/amd64
Vaultwarden 1.37.5
Fetching layer sha256:...
Vaultwarden 1.37.5 installed
```

## 3. Admin token (Argon2)

Konzole serveru příkazy nepřijímá, hash si vygeneruj jinde:

**Na Linuxu s Dockerem:**
```bash
docker run --rm -it vaultwarden/server /vaultwarden hash --preset owasp
```

**Nebo přes `argon2` (balíček `argon2`):**
```bash
echo -n 'TvojeAdminHeslo' | argon2 "$(openssl rand -base64 32)" -e -id -k 19456 -t 2 -p 1
```

Výsledek (`$argon2id$v=19$m=19456,t=2,p=1$...`) vlož celý do proměnné **Admin Token**, bez uvozovek.
Na `https://vault.../admin` se pak přihlásíš **původním heslem**, ne hashem.

## 4. První start a test

1. Start – server je *Running*, jakmile se objeví `Rocket has launched from http://0.0.0.0:PORT`.
2. Rychlý test bez prohlížeče:
   ```bash
   curl http://IP_NODU:PORT/alive
   ```
   Vrátí čas, např. `"2026-11-02T16:34:29Z"`.
3. Otevři `https://vault.tvoje-domena.cz` → **Create account** → vytvoř účet.
4. V aplikaci Bitwarden zvol **Self-hosted** a zadej URL serveru.
5. Přepni `Allow Signups` na `false` a restartuj.

## 5. Zálohování

Vše důležité je ve složce `data/` (`db.sqlite3`, `attachments/`, `sends/`, `rsa_key*`).
Zálohuj ji pravidelně přes zálohy v panelu.

## 6. Test checklist

- [ ] Instalace vypíše verzi a `installed`
- [ ] `/alive` vrací čas
- [ ] Přes HTTPS jde vytvořit účet a přihlásit se
- [ ] Bitwarden rozšíření/mobil se připojí (self-hosted URL)
- [ ] `/admin` s Argon2 tokenem funguje, se špatným heslem ne
- [ ] Prázdný Admin Token = `/admin` hlásí, že je vypnutý
- [ ] Reinstall (update) zachová `data/`

## Bezpečnost

- Po vytvoření účtů vypni registrace (`Allow Signups = false`).
- Nepoužívej admin token jako prosté heslo, vždy Argon2 hash.
- Nastav v Bitwardenu dvoufázové ověření (TOTP).
- Port alokace nemusí být veřejný, stačí když na něj dosáhne reverse proxy.

## Řešení problémů

| Problém | Řešení |
|---|---|
| Web vault hlásí chybu kryptografie / nejde se přihlásit | Nepřistupuješ přes HTTPS, nebo `Domain` nesedí s adresou |
| `/admin` vrací 404 / „admin panel is disabled“ | Admin Token je prázdný |
| Aplikace Bitwarden se nepřipojí | Musí jít o HTTPS s platným certifikátem |
| Instalace: `No linux/amd64 image found` | Neexistující verze v `Version`. Použij `latest` nebo existující tag. |
