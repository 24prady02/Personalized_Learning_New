# Data directory

**Why this folder looks empty on GitHub**

Dataset files under `data/` are **not committed**. They are large (often gigabytes), may have separate licenses, and can include personal or downloaded artifacts. The repository keeps them **local only** via `.gitignore`.

**What is in git**

- `data/raw/.gitkeep` and `data/processed/.gitkeep` — so the folder layout exists in the repo without storing blobs.

**How to populate `data/` on your machine**

1. Copy `config.yaml` from `.env.example` / docs as needed and follow `INSTALLATION.md` and `DATASETS.md` in the repo root.
2. Use the project’s download and processing scripts. Legacy bulk download helpers live under `_archive/download/` and `_archive/scripts_legacy/` if you need them; active paths may also be documented in `scripts/` and root docs.

After downloading, your local `data/` will match what the code expects, but those files will still not appear on GitHub unless you change the ignore rules (not recommended for full datasets).
