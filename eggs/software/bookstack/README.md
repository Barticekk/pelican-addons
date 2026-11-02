# BookStack

## From their [Website](https://www.bookstackapp.com/)

BookStack is a simple, self-hosted, easy-to-use platform for organising and storing information.

## Install notes

- Needs an external MySQL 8.0+ or MariaDB 10.6+ database (the MySQL 8.4 or MariaDB eggs work).
- Served by the static FrankenPHP binary (see the PHP Web egg). Only `www/public` is reachable from the web.
- `APP_URL` and the `DB_*` values in `www/.env` are rewritten from the egg variables on every start.
- The app key is generated on first start, and migrations run on every start.
- Default login is `admin@admin.com` / `password`. Change it immediately.
- Put it behind an HTTPS reverse proxy and use an `https://` App URL. Session cookies are then marked Secure automatically.

## Installation/System Requirements

|  | Bare Minimum | Recommended |
|---------|---------|---------|
| RAM | 256 MiB | 512 MiB |
| Storage | 500 MiB | 2 GiB+ (uploads) |

## Server Ports

| Port | default |
|------|---------|
| HTTP | 8080    |
