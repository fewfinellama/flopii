# CLAUDE.md — Universal Python/Streamlit AI Coding Agreement

> Generic, project-agnostic ruleset for our Python projects. Project-specific 
> details are sourced separately — never baked into this file.

## 0. Precedence Rules
1. This file
2. Project-specific overrides (like FLOPII_AGENT_DESIGN.md)
3. Framework/package defaults
4. Tool suggestions

Non-negotiables always win.

## 1. Session Workflow

At the start of every session:
- Read this file (claude.md)
- Read FLOPII_AGENT_DESIGN.md
- Detect stack:
  - `requirements.txt` / `pyproject.toml`
  - `app.py` / `main.py`
  - Database schema/SQLite structure
- Ask the user directly, before starting work:
  - Is this KISS (simplest viable approach)?
  - Is this DRY (any duplicated logic to reuse/extract)?
  - Is this YAGNI (are we building only what's needed now)?
  - Are tests needed for this change?
  - Does CHANGELOG.md need an entry for this session's work?
  - 3. Check for `CHANGELOG.md`:
   - If missing → create it (Keep a Changelog format) before doing real work.
   - If present → confirm it reflects recent changes.

## 2. Commands

Typical Python commands for this workflow:
```bash
python -m venv venv       # Setup virtual environment
source venv/bin/activate  # Activate it
pip install -r requirements.txt
streamlit run app.py      # Run the UI
pytest                    # Run tests
black .                   # Auto-format code
```
Static analysis (e.g., `flake8` or `mypy`) and `black` formatting are recommended.

## 3. Global Non-Negotiables

- KISS — simplest solution that satisfies the requirement
- DRY — no duplicated logic; extract and reuse
- YAGNI — build only what's needed now
- Tests required for every behavioral change
- CHANGELOG.md must be updated for every session with real work
- No secrets committed to code — use `.env` or local SQLite, never hardcoded
- Never delete, skip, or weaken a test without explicit approval

## 4. Code Conventions

- Python 3.12+ features (type hints, f-strings, match-case if appropriate)
- Explicit return types and argument types on all functions/methods
- Use `black` for formatting.

Naming:
- Classes → PascalCase (e.g. `AgentRunner`)
- Functions/Methods → snake_case (e.g. `fetch_crypto_prices`)
- Variables → snake_case
- Constants → UPPER_SNAKE_CASE

## 5. Architecture

Since this is a Streamlit + headless agent project:
- **UI Layer (Streamlit)**: purely presentation and input collection. Should not contain heavy business logic.
- **Service/Action Layer**: Functions or classes that handle the actual data fetching, LLM integration, and Technocore posting.
- **State/Storage Layer**: SQLite for configuration, API keys, and logs. `sqlite3` or `SQLAlchemy` used cleanly.

## 6. Database Rules

- Use parameterized queries or an ORM to prevent SQL injection.
- Keep table structures simple.
- When deleting soft-deletable unique resources, handle uniqueness constraints properly.

## 7. Comments & Documentation

- Write in a human, simple, conversational tone.
- Explain *why*, not *what*.
- Use docstrings (`"""..."""`) on modules, classes, and complex functions.
- Keep docstrings short and human, not padded boilerplate.

## 8. Security

- Validate all inputs, even from the UI.
- API keys, secrets, tokens must never be logged to file channels. Store them securely (encrypted if possible) in local SQLite.
- Rate limit external calls (e.g., CoinGecko API) to avoid bans. Respect 429s.

## 9. Data Integrity & Async

- Any multi-step write should be handled safely.
- Do not rely on external APIs being fast; handle timeouts gracefully.
- Financial/Money data (if any): Store as integers (minor units) or use Python's `decimal.Decimal`. Never use `float` for money arithmetic.

## 10. Error Handling & Logging

- Use Python's built-in `logging` module.
- `logging.error()` for failures requiring human attention.
- `logging.warning()` for recoverable situations.
- `logging.info()` for audit-trail-worthy business events.
- `logging.debug()` for local diagnostic detail.
- Catch specific exceptions (`requests.exceptions.RequestException`), avoid bare `except Exception:`.

## 11. Git & Commit Conventions

- Use Conventional Commits: `type(scope): short description`
- Types: `feat`, `fix`, `refactor`, `chore`, `test`, `docs`, `style`
- Example: `feat(ui): add setup wizard for API keys`
