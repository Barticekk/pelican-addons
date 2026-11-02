# n8n – návod

Automatizace s vizuálním editorem. Například notifikace na Discord, když spadne herní server, pravidelné
zálohy, webhooky z GitHubu nebo napojení na API.

## 1. Import a vytvoření serveru

1. Import `egg-n8n.yaml` / `egg-pterodactyl-n8n.json`.
2. Server:

| Pole | Hodnota |
|---|---|
| Alokace | 1 port (HTTP), např. `5678` |
| RAM | min. 1 GiB, doporučeno 2 GiB |
| Disk | **min. 4 GiB** (samotná instalace má cca 3 GB) |
| Docker image | `Node.js 24` |

3. Proměnné:

| Proměnná | Hodnota |
|---|---|
| Public URL | adresa **s lomítkem na konci**. Test: `http://IP_NODU:PORT/`, provoz: `https://n8n.tvoje-domena.cz/` |
| Secure Cookie | `true` za HTTPS. Pro test přes čisté HTTP **musí být `false`**, jinak se nepřihlásíš. |
| Send Diagnostics | `false` = n8n neposílá telemetrii |
| n8n Version | `latest` nebo konkrétní verze |

## 2. Instalace

Trvá několik minut (npm stahuje stovky balíčků). Na konci logu:

```
2.45.7
n8n installed
```

## 3. První start

```
No encryption key found - Auto-generating and saving to: /home/container/.n8n/config
n8n ready on 0.0.0.0, port 5678
Migrations in progress, please do NOT stop the process.
...
Editor is now accessible via:
```

Během prvních migrací server **nevypínej**. Pak otevři Public URL a vytvoř účet vlastníka (owner).

## 4. Rychlý test

```bash
curl http://IP_NODU:PORT/healthz
# {"status":"ok"}
```

Workflow test: **Create workflow** → *Manual Trigger* → *HTTP Request* na `https://httpbin.org/get` → **Execute**.

## 5. Webhooky

Webhook URL se skládá z Public URL, např. `https://n8n.tvoje-domena.cz/webhook/abc123`.
Když Public URL nesedí s veřejnou adresou, budou webhooky ukazovat jinam.

## 6. Zálohy

Zálohuj složku `.n8n/`, hlavně:
- `.n8n/config` – šifrovací klíč. **Bez něj nejdou dešifrovat uložená přihlašovací údaje.**
- `.n8n/database.sqlite` – workflow, credentials, historie

## 7. Test checklist

- [ ] Instalace doběhne a vypíše verzi
- [ ] První start: migrace a `Editor is now accessible via`
- [ ] `/healthz` vrací `{"status":"ok"}`
- [ ] Owner účet jde vytvořit a přihlášení drží (pozor na Secure Cookie)
- [ ] Testovací workflow proběhne
- [ ] Webhook z venku dorazí (přes Public URL)
- [ ] Stop server ukončí čistě (`Stopping n8n...`)

## Řešení problémů

| Problém | Řešení |
|---|---|
| Přihlášení se hned ztratí / chyba o secure cookie | Přistupuješ přes HTTP a `Secure Cookie = true`. Použij HTTPS, nebo dočasně `false`. |
| Instalace spadne na místě | Zvětši disk na 4 GiB+ |
| Po reinstalu nejdou credentials | Smazal se `.n8n/config`, obnov ho ze zálohy |
| Server zabije OOM | Přidej RAM (2 GiB) |
