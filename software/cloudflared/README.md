# Cloudflare Tunnel

## From their [Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)

`cloudflared` connects services to Cloudflare's network through outbound-only connections, so websites
on the node get HTTPS through Cloudflare without opening inbound ports.

## Install notes

- Downloads the official `cloudflared-linux-<arch>` binary from GitHub releases. Auto-update is disabled; reinstall to update.
- Uses a **remotely managed** tunnel: create it in the Zero Trust dashboard and paste the token into *Tunnel Token*.
  The token is passed through the environment and is not printed in the console.
- Public hostnames are configured in the dashboard. Point the service to the node's LAN IP or the
  Docker gateway (`172.18.0.1`) and the target server's allocation port, e.g. `http://172.18.0.1:8080`.
- Metrics listen on `127.0.0.1:<allocation>` inside the container only. The allocation is otherwise unused.
- Cloudflare Tunnel is for HTTP(S) services. For raw TCP/UDP game traffic use the playit.gg egg.

## Server Ports

| Port | default |
|------|---------|
| (metrics, container only) | any |
