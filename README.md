# dataiku-automations

Automations, scripts and project configuration for our Dataiku DSS instance, kept under version control.

## What's in this repo

- Python scripts that talk to Dataiku through its public API (`dataiku-api-client`)
- Exported Dataiku projects and scenario definitions
- Custom plugins and reusable recipes
- Environment and setup notes for the Dataiku instance

## Repo structure

```
dataiku-automations/
├── README.md
├── .gitignore
├── requirements.txt        # Python dependencies for local scripts
├── .env.example            # Variable names only, never real values
├── projects/               # Exported project configs / bundles
├── scripts/                # Automation and admin scripts (API client)
├── plugins/                # Custom Dataiku plugins
├── docs/                   # Setup notes, runbooks, decisions
└── tests/                  # Tests for scripts
```

## Getting started

### 1. Prerequisites

- A running Dataiku instance (Free Edition, trial, or server install)
- Python 3.9+
- Git

### 2. Clone and set up

```bash
git clone https://github.com/<your-username>/dataiku-automations.git
cd dataiku-automations
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure access

Copy `.env.example` to `.env` and fill in your values:

```
DSS_URL=http://localhost:10000
DSS_API_KEY=<your personal API key>
```

Create the API key in Dataiku under your profile settings. Never commit `.env`.

### 4. Run a script

```bash
python scripts/hello_dataiku.py
```

## Workflow

- `main` is always stable
- Work on short-lived branches: `feature/<name>`, `fix/<name>`
- Open a pull request for each change, even when working solo
- Export Dataiku projects after meaningful changes and commit the export

## Environments

| Environment | URL | Notes |
|---|---|---|
| Local / dev | http://localhost:10000 | Free Edition |
| Prod | TBD | |

## Roadmap

- [ ] Install Dataiku instance
- [ ] Add first API script (connection test)
- [ ] Set up project export routine
- [ ] Add first scenario automation

## License

TBD
