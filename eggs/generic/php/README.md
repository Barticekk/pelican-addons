# PHP Web (FrankenPHP)

## From their [Website](https://frankenphp.dev/)

[FrankenPHP](https://github.com/php/frankenphp) is a modern PHP app server built on the Caddy web server.
This egg downloads the fully static release binary (PHP plus web server in one file), so it runs on the
plain Debian yolk without any extra image.

## Features

- Serves only `www/<Document Root>` (default `www/public`). Everything else in the server folder stays private.
- Blocks dotfiles (except `/.well-known/`) and sensitive extensions such as `.env`, `.sql`, `.log`, `.bak`, `.ini`, `.yml`.
- Sends `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` and hides `Server` / `X-Powered-By`.
- Hardened `php.ini` defaults: `expose_php`, `display_errors` and `allow_url_include` are off, and the session cookie uses HttpOnly, SameSite=Lax and strict mode.
- Trusts `X-Forwarded-For` only from private ranges, so it sits cleanly behind a reverse proxy on the node.
- Optional git deploy (the token is sent as a header and never stored), `composer install`, Laravel migrations/optimize, `schedule:work` and `queue:work`.
- `bin/php` gives a normal `php` command for Composer scripts and artisan.

## Install notes

- The static binary ships whatever PHP version the current FrankenPHP release is built with (PHP 8.5 as of FrankenPHP 1.13).
  Pin `FrankenPHP Version` if you need to stay on an older release.
- TLS is meant to be terminated by a reverse proxy (Apache, nginx, Caddy) that forwards to the allocation.
  HSTS belongs on that proxy.
- `Caddyfile` and the app in `www/` are kept on reinstall. `start.sh`, `bin/php`, `composer.phar` and the binary are replaced.

## Server Ports

| Port | default |
|------|---------|
| HTTP | 8080    |
