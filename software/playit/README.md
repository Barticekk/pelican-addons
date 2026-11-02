# playit.gg Agent

## From their [Website](https://playit.gg/)

playit.gg is a global proxy that makes game and app servers reachable from the internet without a
public IP or port forwarding.

## Install notes

- The daemon (`playitd`) is copied from the official image `ghcr.io/playit-cloud/playit-agent`
  (static binary) with the registry API. No Docker on the node is needed.
- Create an agent of type **Docker** on playit.gg and paste its secret into *Secret Key*.
  The secret is written to `.playit-secret` (mode 600) on start.
- Tunnels are configured on playit.gg. Their *local address* must be reachable from inside this container:
  use the node's LAN IP or the Docker gateway of the panel network (usually `172.18.0.1`) plus the game server's port.
- The allocation is not used by the agent. Pelican just requires one.

## Server Ports

| Port | default |
|------|---------|
| (unused) | any |
