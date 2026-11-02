# MySQL 8.4 LTS

## From their [Website](https://dev.mysql.com/downloads/mysql/8.4.html)

MySQL Community Server, the 8.4 long-term-support line. The egg uses Oracle's generic
"Linux - Generic (glibc 2.28) x86_64 minimal" build and runs it on the plain Debian yolk.

## Install notes

- x86_64 only. Oracle does not publish a minimal generic build for ARM.
- `libaio`, `libnuma` and `libncurses` are copied into `mysql/lib/private` during install
  because the runtime image does not ship them.
- `root` exists only as `root@localhost` and is used by the panel console through `.root.cnf`.
  Create remote users with the optional *Database User* variables or from the console.
- Reinstalling upgrades the binaries and keeps `data/`. MySQL upgrades the data dictionary on the next start.
- InnoDB prints NUMA `Operation not permitted` warnings inside containers. They are harmless.

## Installation/System Requirements

|  | Bare Minimum | Recommended |
|---------|---------|---------|
| Processor | x86_64 | x86_64 |
| RAM | 512 MiB | 2 GiB+ |
| Storage | 1 GiB | depends on data |

The InnoDB buffer pool is sized to roughly half of the server's memory limit.

## Server Ports

| Port    | default |
|---------|---------|
| MySQL   | 3306    |
