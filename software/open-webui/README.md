# Open WebUI + Ollama

## From their Websites: [Open WebUI](https://openwebui.com/), [Ollama](https://ollama.com/)

Open WebUI is a self-hosted AI chat interface with user accounts, RAG and tools. Ollama runs local
language models. This egg runs both in one server.

## Install notes

- Ollama comes from `ollama.com/download` (`.tar.zst`). The CUDA/Vulkan runners (about 2.3 GB) are skipped
  by default because containers on a panel node have no GPU.
- Ollama listens on `127.0.0.1:11434` **inside the container only**. Its API has no authentication, so it is never published.
- Open WebUI is installed with pip into `venv/` (Python 3.12) on the **first start**, inside the runtime
  container: the server's own RAM and disk apply (installer containers are capped at 1 GiB RAM by default)
  and pip's output is visible in the console. Temporary files go to the server disk because `/tmp` is a
  small tmpfs. CPU-only PyTorch wheels are installed first, which keeps it at about 3 GB instead of 8+ GB.
- Data: `data/` (users, chats, uploads, embedding model cache), `models/` (Ollama models). Back up both.
- The first account created becomes admin. Later signups wait for admin approval.
- Telemetry is disabled (`SCARF_NO_ANALYTICS`, `DO_NOT_TRACK`, `ANONYMIZED_TELEMETRY`). CORS is limited to the *Public URL* when set.
- With *Bundled Ollama* off, the UI connects to *External Ollama URL*, or only to OpenAI-compatible APIs configured in the admin panel.

## Installation/System Requirements

|  | Bare Minimum | Recommended |
|---------|---------|---------|
| Processor | 4 cores (AVX2) | 8+ cores |
| RAM | 4 GiB (1B models) | 16 GiB (7–8B models) |
| Storage | 6 GiB | 20 GiB+ (models) |

## Server Ports

| Port | default |
|------|---------|
| HTTP | 8080 |
