# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to Semantic Versioning.

## [Unreleased]

### Added
- Core architecture (SQLite via `core/db.py` and Identity generation via `core/identity.py`).
- Setup Wizard fully wired up to generate `identity.pem` and derive a real Technocore DID (`did:key:z6Mk...`).
- Persisted LLM API keys securely to SQLite instead of env variables or code.
- Added test coverage for SQLite operations (`tests/test_db.py`).
- Added `cryptography` and `base58` for accurate Ed25519 multicodec identity implementation.
- Initial UI layout using Streamlit.
- Configured fonts (Plus Jakarta Sans, JetBrains Mono) via CSS injection.
- Added Light/Dark mode UI toggle.
- Created Universal Python Coding Agreement (`claude.md`).
- Fully implemented "Import Existing Identity" logic in the Setup Wizard.
- Built out the Admin Panel with Data Source management (Tickers, RSS Feeds) and Agent state toggles (Pause/Resume).
- Created `core/agent.py` to fetch live crypto prices from CoinGecko and parse RSS feeds for news.
- Integrated LLM generation (`core/llm.py`) using the OpenAI SDK (supports Groq, OpenAI, Ollama).
- Implemented Technocore network Ed25519 payload signing and API posting logic (`core/network.py`).
- Implemented `run_agent_cycle` in `core/agent.py` to tie all systems together.
- Wired the "Force Run Now" button in the Admin Panel to execute the full agent pipeline.
- Built `runner.py`, an independent headless script that utilizes the `schedule` library to run the agent in the background continuously.
- Renamed project to "Flopii" across UI and design documents.

## [Unreleased]
### Changed
- Replaced Streamlit UI with a FastAPI + pure HTML/JS frontend.
- Implemented Flopscope's native Tailwind CSS design system with reusable @layer components.
### Added (UI & UX Polish)
- Added global staggered fade-in animations for cards on all pages (`card-fade`).
- Added realtime internet connectivity badge in navbar using native `navigator.onLine`.
- Added persistent offline warning toast that pins to the bottom of the screen when disconnected.
- Added "Smart Room Builder" toggles (Private, Mailbox, 15m Decay) in Settings and Post Modal.
- Added visual room badges (🔒 Pvt, ✉️ mb, ⏱️ 15m, 👑 d) to the Execution Feed and Audit Logs.
- Added skeleton loaders to the dashboard stats and execution feed.
- **Agent Mailbox (Two-Way Comms)**: Agent now computes its private `mb-p-` mailbox based on its DID fingerprint, fetches it on every execution cycle using native `requests.get` to Technocore, and logs incoming commands for auditability.
- Replaced emoji toggles with native inline SVGs for cleaner cross-platform rendering.
- Added a floating global footer pinning "Created by Flopscope" and "Powered by Technocore" to the bottom right of the UI.
- Implemented real-time pulsing UI badges on the Inbox nav icon when new unread messages arrive.
- Implemented dynamic database-backed Dashboard Metrics (Success Rate 24h, Total Executions, Mailbox Commands, Last Active) instead of mocked frontend values.
- **Dynamic Agent Core Refactor**: Un-hardcoded `core/agent.py`. Removed explicit crypto price tracking and RSS parsing. Consolidated settings into a universal `data_endpoints` configuration. The LLM now exclusively dictates the final payload based solely on raw scraped endpoints and the user's `system_prompt`.
- **Multi-Provider Auto-Failover Matrix**: Rebuilt the settings architecture to store multiple LLM providers as a unified JSON config. Built a dynamic UI allowing users to configure, verify, and switch between OpenAI, Groq, Ollama, and Anthropic seamlessly.
- Implemented autonomous error handling in `core/llm.py` (`generate_with_failover`). If the primary provider hits a 404/400 (e.g. decommissioned model) or network failure 3 consecutive times, it autonomously promotes the next verified fallback provider to ensure uninterrupted continuous agent operation.
- Added a full unit test suite `tests/test_llm.py` to cryptographically verify the auto-failover logic.
