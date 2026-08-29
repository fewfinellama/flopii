# Flopii

A practical, turnkey crypto intelligence agent for Technocore. Flopii is built around the idea of one permanent identity, useful output, and consistent value rather than spammy one-off posts.

It combines a Streamlit-based setup experience with a backend agent loop that can:

- generate or import an identity
- configure an LLM provider
- fetch market data and news
- publish structured updates to a Technocore room
- manage state in local SQLite
- run headlessly once configured

![Flopii dashboard](flopii_screenshot.jpg)

---

## Why this project exists

The project follows the design in the Flopii agent blueprint: a useful, persistent agent should do one job well and do it consistently.

This implementation focuses on a crypto pulse agent that:

- tracks major coins such as BTC, ETH, and SOL
- collects market data from public sources
- gathers headline/news items from RSS feeds
- produces concise, structured summary updates
- posts those updates into a dedicated room in Technocore

The goal is not volume. The goal is useful and attributable output that another agent or human can actually consume.

---

## Core features

### Identity management

- create a new Ed25519 identity
- import an existing PEM identity
- encrypt/decrypt the private key with a passphrase
- store the DID and related settings locally in SQLite

### Setup wizard

A simple onboarding flow guides the user through:

- identity setup
- LLM provider selection
- API key configuration
- target room configuration
- source configuration

### Admin dashboard

The project includes a control panel for:

- toggling the agent on or off
- setting crypto tickers and RSS feeds
- choosing the target Technocore room
- forcing a manual run
- reviewing recent logs and status information

### Autonomous execution loop

Once configured, the agent can run continuously in the background and execute periodic cycles to:

- pull market prices
- fetch news headlines
- synthesize content
- broadcast updates to a room

### Public-facing status view

The app surfaces the latest generated payload in a dashboard so the operator can review the last successful update and confirm the system is broadcasting as expected.

---

## Architecture

This project is designed as a light, practical Python stack rather than a heavy front-end framework.

### Components

- Streamlit UI: local setup wizard, dashboard, admin controls
- FastAPI backend: JSON API endpoints for identity, settings, and automation
- SQLite: durable local settings, state, and post logs
- LLM integration layer: provider-specific API usage
- Technocore networking layer: posts, fetches, and room metadata
- Data source layer: crypto market and RSS feed retrieval

### Runtime model

The system is intentionally split into layers:

- UI layer: presentation and operator input
- service layer: agent logic, data fetching, LLM interactions, Technocore posting
- storage layer: SQLite-based settings and logs

This keeps the app easy to run by non-technical users while still allowing infrastructure to be managed programmatically.

---

## Project structure

```text
.
├── app.py                  # Streamlit app entry
├── main.py                 # FastAPI backend entry
├── core/
│   ├── agent.py            # main workflow logic
│   ├── db.py               # SQLite helpers
│   ├── identity.py         # DID / PEM key management
│   ├── llm.py              # model/provider checks
│   └── network.py          # Technocore HTTP calls
├── templates/              # HTML templates for the web UI
├── static/                 # static CSS/JS/image assets
├── tests/                  # test suite
├── requirements.txt        # Python dependencies
├── package.json            # Node tooling metadata
├── .gitignore              # ignore rules for secrets/generated files
├── agent_state.db          # local SQLite DB (generated locally)
├── identity.pem            # local encryption key material (generated locally)
├── flopii_screenshot.jpg   # project screenshot used in docs
└── README.md
```

---

## Local setup

### Prerequisites

- Python 3.11+
- pip
- Optional: Node tooling for Tailwind assets

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit UI

```bash
streamlit run app.py
```

This launches the setup wizard and dashboard for interactive use.

### 4. Run the backend server

```bash
python main.py
```

This runs the FastAPI backend, which powers API endpoints and the autonomous agent loop.

---

## Typical usage flow

1. Launch the app
2. Open the Setup Wizard
3. Generate or import an identity
4. Add the LLM provider and API key
5. Configure crypto tickers and RSS feeds
6. Choose the target Technocore room
7. Start the agent
8. Review the dashboard and execution logs

Once configured, the agent can continue operating in the background while the UI remains available for auditing and manual adjustments.

---

## Configuration

### Identity

The application stores identity data locally in `identity.pem` and related values in SQLite. This file should be treated as sensitive and should never be committed to a shared repository.

### LLM

The app supports multiple providers such as:

- OpenAI
- Groq
- Ollama
- Anthropic

The selected provider and API key are saved in the database and used by the agent pipeline during generation.

### Data sources

The agent uses:

- crypto tickers for asset data
- RSS feeds for headline/news discovery
- a configurable target room for posting output

### Target room

The default room is usually set to something like:

```text
/r/flopii
```

This can be changed in the dashboard or admin settings if you want to post to a different room.

---

## How the agent works

The agent workflow is straightforward:

1. gather configured market data
2. gather configured news sources
3. filter for relevance
4. summarize or reframe content
5. generate a structured payload
6. post the payload to Technocore
7. store the result in SQLite for later review

The design deliberately favors a small, predictable loop over noisy or repetitive activity. This aligns with the project’s goal of useful work instead of empty churn.

---

## Security notes

This project handles local secrets and identity material. Please use care:

- never commit real API keys
- never commit private keys or PEM files
- store secrets in local environment or encrypted local storage when practical
- use `.env` or local config only, not hardcoded credentials in source files
- keep the `.gitignore` current so generated files are not accidentally tracked

The repository already includes ignore rules for common items like:

- Python cache files
- local SQLite databases
- `.env` files
- Node modules
- editor directories
- PEM files

---

## Development notes

### Running tests

```bash
pytest
```

### Formatting

```bash
black .
```

### Static checks

Additional static analysis is recommended for production-quality work, especially if the project grows.

---

## Deployment considerations

The design is intentionally flexible:

- local machine for personal testing
- always-on VPS for unattended operation
- lightweight hosting for headless mode after initial setup

The design document specifically emphasizes a zero-budget or low-cost deployment path, with a focus on practicality over complexity.

---

## Roadmap and direction

The project direction is aligned with the Flopii design document:

- one permanent DID
- useful crypto market and news output
- low-noise posting cadence
- durable state tracking
- simple setup for non-technical users
- clean operator dashboard

Possible future improvements include:

- better failover for LLM providers
- richer market summaries
- improved rate-limit handling
- deduplication of headlines
- a more polished public-facing dashboard
- richer room and mailbox monitoring

---

## License and usage

This repository does not currently include a dedicated project license file. The package metadata includes an ISC license declaration in the Node package config, but the Python project is primarily intended for local experimentation and controlled deployment as described in the design document.

Use this project in a way that respects local security practices and Technocore network rules.

---

## Summary

Flopii is a focused, practical agent aimed at producing useful crypto-pulse content in a low-noise, durable way. It blends a friendly setup flow, local SQLite state, LLM-driven output generation, and Technocore publishing into a project that is easy to run and easy to extend.

The overall goal is simple: build an agent that survives, gives value, and remains useful to other humans and agents without behaving like spam.
