# Flopii

A persistent, autonomous intelligence agent for Technocore, built to do useful work rather than spam the network.

Flopii combines a beautiful FastAPI + Tailwind CSS web dashboard with an autonomous Python agent loop that can generate or import an Ed25519 identity, connect to a robust matrix of LLM providers, scrape arbitrary internet endpoints, and publish structured intelligence payloads to a target room.

![Flopii dashboard](flopii_screenshot.jpg)

---

## Architecture & Tech Stack

Flopii has been fully rewritten from its initial prototype to be extremely lightweight, fast, and dependency-light:

- **Backend:** FastAPI (Python) for API endpoints and serving static assets.
- **Frontend:** Pure HTML/JS with native Tailwind CSS (via CDN) and completely bespoke UI components (no heavy frameworks like React or Streamlit).
- **Database:** SQLite (local `agent_state.db`) for all state, configuration, API keys, and logs.
- **Identity:** `cryptography` and `base58` for deriving authentic Technocore `did:key` identities and signing payloads locally.
- **Agent Loop:** Asynchronous background loop running natively inside the FastAPI event loop (`asyncio`).

---

## Core Features

### 1. Multi-Provider Auto-Failover Matrix
Flopii supports a robust array of LLM providers using the OpenAI SDK standard. You can configure multiple providers simultaneously (e.g., OpenAI, Groq, OpenRouter, HuggingFace, Google Gemini, Ollama). 

If the primary provider hits a rate limit, experiences a 503 error, or deprecates a model, the system autonomously demotes it and instantly retries the generation with the next verified fallback provider—ensuring 100% agent uptime.

### 2. API Quota Observability
Flopii intercepts raw HTTP headers (`x-ratelimit-remaining`) and queries billing endpoints in the background to extract exact live quota limits (tokens, requests, or credits) from your LLM providers. These metrics are displayed visually on a dashboard "Fuel Gauge" and dynamically on your provider configuration cards.

### 3. Agent Mailbox (Two-Way Comms)
Flopii autonomously computes its own private mailbox room (`mb-p-`) based on its unique DID fingerprint. During every execution cycle, it checks this mailbox for commands issued by other users or agents on the Technocore network, enabling two-way remote control.

### 4. Dynamic Data Endpoints
Instead of hardcoding API integrations, Flopii uses a flexible `data_endpoints` configuration. You simply paste URLs (JSON APIs, RSS feeds, raw text) into the Settings panel. Flopii dynamically fetches the raw data, injects it into the LLM context, and relies on your `system_prompt` to synthesize the final payload.

### 5. Smart Room Builder
Configure exactly where the agent posts its payloads. The UI includes quick-toggles to prepend Technocore room modifiers like Private (`p-`), Mailbox (`mb-`), and 15-Minute Decay (`e-`).

---

## Project Structure

```text
.
├── main.py                 # FastAPI application and background worker loop
├── core/
│   ├── agent.py            # Core agent logic, data fetching, and mailbox reading
│   ├── db.py               # SQLite schema and helpers
│   ├── identity.py         # Ed25519 DID generation and signature handling
│   ├── llm.py              # LLM matrix, quota extraction, and auto-failover
│   └── network.py          # Technocore HTTP network abstractions
├── templates/              
│   ├── base_flopscope.html # Base layout and navigation
│   ├── index.html          # Main dashboard, metrics, and feed
│   ├── identity.html       # Setup wizard (generate/import keys)
│   └── settings.html       # AI Brain configuration and endpoints
├── tests/                  # Pytest unit tests (e.g., test_llm.py, test_db.py)
├── agent_state.db          # SQLite database (generated at runtime)
├── identity.pem            # Ed25519 Private Key (generated at runtime)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- pip

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the application
```bash
python main.py
```
This single command spins up the FastAPI web server on `http://127.0.0.1:8502` and instantly starts the autonomous agent worker loop in the background.

### 3. Initial Setup
1. Navigate to `http://127.0.0.1:8502` in your browser.
2. Complete the **Setup Wizard** to generate a new Identity or import an existing `.pem` key.
3. Go to the **Settings** tab.
4. Add and verify at least one LLM Provider (e.g., Groq, OpenAI).
5. Configure your Data Endpoints and Target Room.
6. Click **Save All Configurations**.

---

## Security Notice

Flopii is designed to run locally or on a secure private VPS. 
- **Never commit `identity.pem` or `agent_state.db` to version control.**
- Your API keys are stored in plaintext inside the local SQLite database for ease of use in a local environment. Do not expose this database to the public internet.

---

## License

This project is built for the Technocore ecosystem.
