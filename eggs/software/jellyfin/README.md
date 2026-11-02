# Jellyfin

## From their [Website](https://jellyfin.org/)

The free software media system: stream movies, shows, music and photos to any device.

## Install notes

- Uses the official portable Linux tarball (self-contained .NET) from `repo.jellyfin.org` and the newest
  portable `jellyfin-ffmpeg`.
- `libfontconfig`, `libfreetype`, `libpng` and DejaVu fonts are copied into `lib/` because SkiaSharp
  (artwork, blurhash, trickplay images) needs them and the Debian yolk does not ship them.
- The HTTP port in `config/network.xml` is kept in sync with the allocation on every start.
- Media goes into `media/` (SFTP), or into any folder under `/home/container`. Add it as a library in the setup wizard.
- Hardware transcoding is not available because containers get no GPU, so transcoding uses the CPU.
  Prefer Direct Play clients and limit transcoding bitrates.
- Reinstall to update. `config/`, `data/` and `media/` are kept.

## Installation/System Requirements

|  | Bare Minimum | Recommended |
|---------|---------|---------|
| Processor | 2 cores | 4+ cores (transcoding) |
| RAM | 1 GiB | 4 GiB |
| Storage | 2 GiB + media | as much as your library |

## Server Ports

| Port | default |
|------|---------|
| HTTP | 8096    |
