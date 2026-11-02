# MySQL 8.4 LTS – návod

Databázový server MySQL 8.4 (LTS). Hodí se pro FiveM (ESX/QBCore), LuckPerms, CoreProtect a weby,
které vyžadují MySQL, ne MariaDB.

## 1. Import eggu

1. Admin → **Eggs** → **Import**.
2. Nahraj `egg-mysql84.yaml` (Pelican). Na Pterodactylu použij `egg-pterodactyl-mysql84.json`.

## 2. Vytvoření serveru

| Pole | Doporučení |
|---|---|
| Alokace | jeden port, např. `3306` (TCP) |
| RAM | min. 512 MiB, doporučeno 2 GiB+ (buffer pool = cca polovina RAM) |
| Disk | 1 GiB + velikost dat |
| Docker image | `Debian` |

Proměnné:

| Proměnná | Co zadat |
|---|---|
| MySQL Version | `latest` (nejnovější 8.4.x) nebo konkrétní, např. `8.4.13` |
| Root Password | silné heslo, min. 12 znaků, bez mezer, uvozovek a zpětného lomítka |
| Database Name | volitelné – databáze, která se vytvoří při instalaci (např. `fivem`) |
| Database User / Password | volitelné – uživatel s přístupem odkudkoliv (`%`) a plnými právy na tu databázi |

> Root heslo a uživatel se nastaví **jen při první instalaci**, kdy se zakládá prázdný adresář `data/`.
> Pozdější změnu proměnné nic nezmění – heslo pak měň v konzoli příkazem `ALTER USER`.

## 3. První start – co máš vidět

V konzoli proběhne start a server přejde do stavu *Running*, jakmile se objeví:

```
/home/container/mysql/bin/mysqld: ready for connections. Version: '8.4.13' ... port: 3306
```

Hlášky `Failed to set NUMA memory policy ... Operation not permitted` jsou v kontejneru normální a neškodí.

## 4. Konzole = SQL klient

Konzole je přihlášená jako `root`, takže do ní rovnou píšeš SQL (vždy se středníkem):

```sql
SHOW DATABASES;
SELECT user, host FROM mysql.user;
CREATE DATABASE luckperms;
CREATE USER 'lp'@'%' IDENTIFIED BY 'SilneHeslo123!';
GRANT ALL PRIVILEGES ON luckperms.* TO 'lp'@'%';
```

Výstup se vypisuje jako tabulka. Chyba v jednom příkazu konzoli neshodí.

## 5. Připojení zvenku

```bash
mysql -h IP_NODU -P PORT -u game -p
```

Nebo HeidiSQL / DBeaver se stejnými údaji. Z jiného serveru na stejném nodu použij IP alokace.
`root` je záměrně jen `localhost`, takže se zvenku přihlásit nedá.

## 6. Test checklist

- [ ] Instalace doběhne s hláškou `MySQL 8.4.x installed`
- [ ] Server přejde do stavu *Running*
- [ ] `SHOW DATABASES;` v konzoli vrátí tabulku
- [ ] Vzdálené přihlášení uživatelem z proměnných funguje
- [ ] Tlačítko **Stop** server čistě vypne (`Shutdown complete`)
- [ ] Po restartu jsou data pořád tam
- [ ] Reinstall (upgrade) zachová složku `data/`

## Bezpečnost

- Port databáze nevystavuj do internetu, když to není nutné. Ideálně alokuj port na interní IP
  nebo omez přístup firewallem jen na servery, které ho potřebují.
- `.root.cnf` obsahuje root heslo pro konzoli (práva 600). Vidí ho jen ten, kdo má přístup k souborům serveru.
- Uživatelům aplikací dávej práva jen na jejich databázi, ne `*.*`.

## Řešení problémů

| Problém | Řešení |
|---|---|
| Instalace skončí `ARM nodes are not supported` | Oracle nemá minimal build pro ARM, použij x86_64 node nebo MariaDB egg |
| `Access denied for user 'root'` v konzoli | Heslo bylo změněno ručně – uprav `password` v `.root.cnf` |
| Server po startu hned spadne | Podívej se do konzole na `[ERROR]`. Často jde o málo RAM, zkus aspoň 512 MiB. |
| Chci jinou verzi | Změň `MySQL Version` a dej **Reinstall** – data zůstanou |
