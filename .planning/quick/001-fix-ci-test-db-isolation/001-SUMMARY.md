# Quick Task 001: Fix CI Test DB Isolation — SUMMARY

**Status:** Complete
**Date:** 2026-02-22

## Problem

CI pipeline (GitHub Actions) tests failed because 5 test files (`test_beans.py`, `test_brew.py`, `test_history.py`, `test_analytics.py`, `test_insights.py`) imported the production database engine directly from `app.database`. In CI, the `data/` directory doesn't exist (gitignored), causing `sqlite3.OperationalError: unable to open database file`.

## Root Cause

`app/database.py` creates the SQLAlchemy `engine` at module import time using `settings.effective_database_url`, which defaults to `sqlite:///./data/beanbay.db`. When tests imported `engine`/`SessionLocal` from `app.database` directly (instead of using dependency injection), they bypassed the conftest's in-memory fixtures and hit the missing production DB path.

## Solution

### 1. `tests/conftest.py` — Hardened shared fixtures
- Added `os.environ.setdefault("BEANBAY_DATABASE_URL", "sqlite:///:memory:")` at top (before any app imports) so the production engine also points to in-memory SQLite
- Test engine uses `StaticPool` + `check_same_thread=False` so the single in-memory DB is accessible across threads (required by Starlette's TestClient which runs the ASGI app in a background thread)
- Added `after_transaction_end` event listener for savepoint restart pattern
- Added `client` fixture that overrides FastAPI's `get_db` dependency with the test `db_session`

### 2. Five test files refactored
Removed all direct imports of `engine`, `SessionLocal`, and `Base` from `app.database`. Removed local `setup_db`, `client`, and `db` fixtures. All now use the shared `client` and `db_session` fixtures from conftest.

**Files modified:**
- `tests/conftest.py`
- `tests/test_beans.py`
- `tests/test_brew.py`
- `tests/test_history.py`
- `tests/test_analytics.py`
- `tests/test_insights.py`

**Files already correct (no changes):**
- `tests/test_models.py`
- `tests/test_optimizer.py`

## Verification

- `uv run pytest tests/ -v` — **108 passed, 0 failed** (1.80s)
- `grep -r "from app.database import.*engine" tests/` — no matches (no stale imports)
