# Open WebUI + Ollama – návod

Vlastní „ChatGPT“ na serveru. Open WebUI je webové rozhraní s účty a historií, Ollama v témže serveru
pouští lokální AI modely. Nic se neposílá do cloudu.

> Bez GPU běží modely na CPU. Rozumně fungují malé modely (1–4B parametrů). Velké modely (70B) bez GPU nepoužívej.

## 1. Vytvoření serveru

1. Import `egg-open-webui-ollama.yaml` / `egg-pterodactyl-open-webui-ollama.json`.
2. Server:

| Pole | Hodnota |
|---|---|
| Alokace | 1 port (HTTP), např. `8080` |
| RAM | min. 4 GiB. Model potřebuje RAM zhruba jako jeho velikost + 1–2 GiB. |
| CPU | co nejvíc jader |
| Disk | min. 6 GiB + modely (1B ≈ 1,3 GB, 3B ≈ 2 GB, 8B ≈ 5 GB) |
| Docker image | `Python 3.12` |

3. Proměnné:

| Proměnná | Hodnota |
|---|---|
| Public URL | `https://ai.tvoje-domena.cz` (nebo prázdné pro test přes IP) |
| Allow Signups | `true` – první účet je admin. Další čekají na schválení. |
| Bundled Ollama | `1` = Ollama v tomto serveru (doporučeno) |
| Models To Pull | modely ke stažení při startu, např. `llama3.2:1b` nebo `llama3.2:3b,qwen2.5:3b` |
| External Ollama URL | jen když Bundled Ollama = `0` |

## 2. Instalace (Reinstall)

Instalace stáhne jen Ollamu (pár desítek MB) a připraví `start.sh`. Trvá chvilku. Konec logu:

```
Install finished. Open WebUI itself is installed on the first start (watch the console).
```

## 3. První start (instaluje Open WebUI)

Open WebUI se instaluje **při prvním startu** přímo v serveru. Platí pro něj RAM a disk serveru
a celý průběh pipu vidíš v konzoli. Trvá 5–15 minut (stahuje se cca 2,5 GB):

```
Installing Open WebUI (latest). The first start takes 5-15 minutes.
...
Successfully installed ... open-webui-0.12.5 ...
Open WebUI 0.12.5 installed
Starting Ollama (log: logs/ollama.log)
Pulling model llama3.2:1b in the background
Open WebUI is ready on port 8080
Model llama3.2:1b ready
```

- Během instalace je server ve stavu *Starting*, to je v pořádku. Nevypínej ho.
- Při prvním spuštění Open WebUI ještě stáhne embedding model (pro práci s dokumenty).
- *Running* nastane po řádku `Open WebUI is ready on port ...`.
- Další starty už nic neinstalují a naběhnou za pár desítek sekund.
- Změna `Open WebUI Version` nainstaluje danou verzi při dalším startu. **Reinstall** + `latest` aktualizuje na nejnovější.

## 4. První přihlášení

1. Otevři `http://IP_NODU:PORT/` (nebo Public URL).
2. **Sign up**. První účet je **admin**.
3. Nahoře vyber model a piš.
4. Další modely: *Admin Panel → Settings → Models → Pull a model from Ollama.com* (např. `qwen2.5:3b`, `gemma3:4b`, `phi4-mini`).
5. Po vytvoření účtů dej `Allow Signups = false`, nebo nové uživatele schvaluj v *Admin Panel → Users*.

## 5. Bezpečnost

- Ollama API je jen uvnitř kontejneru (`127.0.0.1:11434`), z internetu na něj nikdo nedosáhne.
- Veřejný provoz dej přes HTTPS ([REVERSE_PROXY.cs.md](../../REVERSE_PROXY.cs.md), websockety jsou nutné).
- `.webui_secret_key` (v kořeni serveru) podepisuje přihlášení, nemaž ho (jinak se všichni odhlásí).

## 6. Test checklist

- [ ] Reinstall doběhne (`Install finished`)
- [ ] První start nainstaluje Open WebUI (`Open WebUI x.y.z installed`)
- [ ] Start: `Open WebUI is ready on port ...`
- [ ] Druhý start už nic neinstaluje a naběhne rychle
- [ ] Model se stáhne (`Model ... ready`)
- [ ] První registrace = admin, chat odpovídá
- [ ] Druhá registrace čeká na schválení (nebo je zakázaná)
- [ ] Nahrání PDF do chatu a dotaz na obsah funguje (RAG)
- [ ] Restart: účty, chaty i modely zůstanou
- [ ] Odpověď 8B modelu se vejde do RAM (jinak OOM, viz níže)

## Když instalace selže

**Reinstall** při chybě vypíše `Install failed at line ...` (týká se jen stažení Ollamy).
**Instalace Open WebUI při prvním startu** při chybě vypíše výstup pipu a pak:

```
Installing Open WebUI failed, see the pip output above.
```

| Příčina | Poznáš podle | Řešení |
|---|---|---|
| Málo místa na disku | `No space left on device` | Disk serveru min. **6 GiB** (+ modely) |
| Málo RAM | server spadne s `Out of memory: true` | RAM serveru min. 4 GiB |
| Síť | chyba připojení u `pip` / `curl` | Node musí mít přístup na `pypi.org`, `files.pythonhosted.org`, `download.pytorch.org`, `ollama.com`, `github.com`, `huggingface.co` |

Po opravě stačí server znovu spustit, instalace se zopakuje.

## Řešení problémů

| Problém | Řešení |
|---|---|
| `bash: ./start.sh: No such file or directory` / `Open WebUI is not installed` (starší verze eggu) | Aktualizuj egg (Import → přepsat), na serveru dej **Reinstall** a pak **Start**. Pozůstatky starého pokusu (`venv/`) start uklidí sám. |
| `Pulling ... failed` | Podívej se do `logs/ollama.log`. Většinou výpadek sítě nebo překlep v názvu modelu. |
| Server spadne při odpovědi (OOM) | Model je na RAM moc velký. Použij menší, nebo přidej RAM. |
| Odpovědi jsou velmi pomalé | CPU inference. Použij menší model nebo kvantizaci (`:q4_K_M`). |
| V UI není žádný model | Model se ještě stahuje, nebo je Bundled Ollama = 0 bez externí URL |
| Chci GPU | Jen pokud node předává GPU do kontejnerů. Admin pak nastaví `Ollama GPU Libraries = 1` a dá reinstall. |
