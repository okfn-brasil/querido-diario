# Quick Start: Using GitHub Codespaces for Querido-Diario

## Step 1: Launch Codespace
1. Go to the repository on GitHub.
2. Click the **Code** button → **Open with Codespaces** → **New Codespace**.
3. Wait until setup finishes.

## Step 2: Verify Environment
```bash
pip install -r requirements.txt
```

## Step 3: Run Scrapers
```bash
scrapy crawl <spider_name> -o data.csv -s LOG_FILE=log_<municipality>.txt
```

Inspect output files (`data.csv`, logs) for correctness.

## Step 4: Commit Changes
```bash
git checkout -b my-update
git add .
git commit -m "Add new scraper or test update"
git push origin my-update
```

## Step 5: Close Codespace
After testing, close or delete the codespace from the GitHub UI to save resources.

---

## Example Devcontainer Configuration
```json
{
  "name": "Querido-Diario Dev",
  "image": "mcr.microsoft.com/devcontainers/python:3.10",
  "features": {
    "git": "latest"
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "forwardPorts": [8888],
  "workspaceFolder": "/workspace"
}
```
Place this file in `.devcontainer/devcontainer.json`.
