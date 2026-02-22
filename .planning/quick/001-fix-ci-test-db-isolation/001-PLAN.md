---
phase: quick
plan: 001
type: execute
wave: 1
depends_on: []
files_modified:
  - tests/conftest.py
  - tests/test_beans.py
  - tests/test_brew.py
  - tests/test_history.py
  - tests/test_analytics.py
  - tests/test_insights.py
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "All tests pass in CI without a data/ directory"
    - "All tests use in-memory SQLite via conftest.py fixtures"
    - "No test file imports engine or SessionLocal from app.database"
    - "Test isolation: each test gets a fresh DB session with rollback"
  artifacts:
    - path: "tests/conftest.py"
      provides: "Shared db_engine, db_session, client fixtures with get_db override"
    - path: "tests/test_beans.py"
      provides: "Bean CRUD tests using shared fixtures"
    - path: "tests/test_brew.py"
      provides: "Brew router tests using shared fixtures"
    - path: "tests/test_history.py"
      provides: "History router tests using shared fixtures"
    - path: "tests/test_analytics.py"
      provides: "Analytics router tests using shared fixtures"
    - path: "tests/test_insights.py"
      provides: "Insights router tests using shared fixtures"
  key_links:
    - from: "tests/conftest.py"
      to: "app/database.py"
      via: "get_db dependency override"
      pattern: "app.dependency_overrides\\[get_db\\]"
---

<objective>
Fix CI test failures caused by 5 test files importing the production database engine
directly, which fails in CI because the `data/` directory doesn't exist.

Purpose: Tests must use in-memory SQLite via conftest.py fixtures, not the production engine.
Output: All 7 test files use shared conftest.py fixtures; CI pipeline passes.
</objective>

<context>
@.planning/STATE.md
@tests/conftest.py
@app/database.py
@app/main.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: Enhance conftest.py with client fixture and get_db override</name>
  <files>tests/conftest.py</files>
  <action>
  Add a `client` fixture that:
  1. Overrides FastAPI's `get_db` dependency to yield the test `db_session`
  2. Wraps the FastAPI `app` in `TestClient`
  3. Clears dependency overrides after yield
  
  The existing `db_engine`, `db_session`, `tmp_campaigns_dir`, `optimizer_service` fixtures stay.
  </action>
  <verify>conftest.py has client fixture that overrides get_db</verify>
  <done>conftest.py provides db_engine, db_session, client fixtures usable by all test files</done>
</task>

<task type="auto">
  <name>Task 2: Refactor 5 test files to use conftest fixtures</name>
  <files>
    tests/test_beans.py
    tests/test_brew.py
    tests/test_history.py
    tests/test_analytics.py
    tests/test_insights.py
  </files>
  <action>
  For each of the 5 files:
  1. Remove `from app.database import Base, engine, SessionLocal`
  2. Remove the `setup_db` autouse fixture
  3. Remove the local `client` fixture (use conftest's)
  4. Remove the local `db` fixture — rename usages to `db_session`
  5. Update `sample_bean`, `second_bean`, and seed helper fixtures to use `db_session` param
  6. Keep all test logic and assertions unchanged
  </action>
  <verify>pytest tests/ -v passes with all tests using in-memory DB</verify>
  <done>No test file imports engine/SessionLocal from app.database; all tests pass</done>
</task>

</tasks>

<verification>
```bash
# Verify no test imports production engine
grep -r "from app.database import.*engine" tests/ && echo "FAIL: still importing engine" || echo "OK"

# Run full test suite
pytest tests/ -v
```
</verification>

<success_criteria>
- All tests pass with in-memory SQLite
- No test file imports `engine` or `SessionLocal` from `app.database`
- CI pipeline would pass (no dependency on `data/` directory)
</success_criteria>
