# playit.gg Agent – návod

Zpřístupní herní servery z panelu do internetu bez veřejné IP a bez přesměrování portů (CGNAT, domácí linka).
Hráči se připojují na adresu od playit.gg, např. `nazev.joinmc.link` nebo `xyz.gl.at.ply.gg:12345`.

## 1. Účet a secret

1. Zaregistruj se na <https://playit.gg>.
2. **Agents → Add Agent** → zvol typ **Docker** (agent poběží v kontejneru).
3. Zkopíruj hodnotu `SECRET_KEY`. Je to dlouhý řetězec písmen a čísel.

## 2. Vytvoření serveru

1. Import `egg-playit.yaml` / `egg-pterodactyl-playit.json`.
2. Server: RAM 128 MiB, disk 100 MiB, alokace libovolná (agent ji nepoužívá, panel ji jen vyžaduje).
3. Proměnná **Secret Key** = zkopírovaný secret.

## 3. Start

```
INFO playitd::daemon: Starting playitd ... version=1.2.0
```

Na playit.gg se agent během pár sekund ukáže jako **online**.
Prázdný secret → start skončí hláškou `Set the Secret Key variable first`.
Neplatný secret → `configured agent secret is no longer valid`.

## 4. Tunel na herní server

Na playit.gg: **Tunnels → Add Tunnel**:

| Pole | Hodnota |
|---|---|
| Tunnel type | Minecraft Java / Bedrock / TCP / UDP / TCP+UDP podle hry |
| Agent | tvůj agent |
| Local address | **IP, na které je alokace herního serveru** – LAN IP nodu (např. `192.168.1.10`), nebo gateway Docker sítě panelu `172.18.0.1` |
| Local port | port alokace herního serveru, např. `25565` |

> `127.0.0.1` nepoužívej. Uvnitř kontejneru ukazuje na kontejner agenta, ne na node.

Hráči se pak připojují na adresu, kterou ukazuje playit.gg u tunelu.

## 5. Test checklist

- [ ] Instalace vypíše `playit agent installed`
- [ ] Bez secretu start skončí s jasnou hláškou
- [ ] Se secretem je agent na playit.gg *online*
- [ ] Tunel na Minecraft/jiný server funguje zvenku
- [ ] UDP hra (např. Valheim/Terraria) přes TCP+UDP tunel funguje
- [ ] **Stop** agenta ukončí, tunel přejde offline

## Řešení problémů

| Problém | Řešení |
|---|---|
| Agent online, ale tunel nefunguje | Špatná *Local address*: použij IP nodu nebo `172.18.0.1`, ne `127.0.0.1` |
| `Could not reach the playit API` | Node nemá odchozí internet nebo DNS |
| Secret prozradil někdo cizí | Na playit.gg agenta smaž, vytvoř nový a vyměň secret |
