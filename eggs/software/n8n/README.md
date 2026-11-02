# n8n

## From their [Website](https://n8n.io/)

Fair-code workflow automation with a visual editor and 400+ integrations.

## Install notes

- Installed from npm into the server folder (`node_modules/`, about 3 GB). n8n 2.x requires Node.js 24.
- Data lives in `.n8n/`: SQLite database, the auto-generated encryption key in `.n8n/config`, and logs.
  Back up the whole folder. Without `config` the stored credentials cannot be decrypted.
- `Public URL` is used for webhook URLs and the editor. Behind HTTPS keep `Secure Cookie` on `true`.
- Reinstall to update. `.n8n/` is kept.

## Installation/System Requirements

|  | Bare Minimum | Recommended |
|---------|---------|---------|
| RAM | 1 GiB | 2 GiB |
| Storage | 4 GiB | 6 GiB+ |

## Server Ports

| Port | default |
|------|---------|
| HTTP | 5678    |
