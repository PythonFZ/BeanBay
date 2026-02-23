---
phase: 14-equipment-management
plan: "01"
subsystem: database
tags: [sqlalchemy, alembic, migration, sqlite, equipment, brew-setup, many-to-many]

# Dependency graph
requires:
  - phase: 13-02
    provides: Alembic migration infrastructure + idempotency patterns (inspector checks, named FK constraints, render_as_batch)
  - phase: 13-01
    provides: Base equipment models (Grinder, Brewer, Paper, WaterRecipe, BrewSetup) with id/name/created_at
provides:
  - Extended Grinder model with dial_type, step_size, min_value, max_value, is_retired
  - Extended Brewer model with is_retired and many-to-many to BrewMethod via brewer_methods table
  - Extended Paper model with description, is_retired
  - Extended WaterRecipe model with notes + individual mineral fields (gh, kh, ca, mg, na, cl, so4) + is_retired
  - Extended BrewSetup model with is_retired
  - Alembic migration e32844be4891 applying all schema changes idempotently
  - brewer_methods association table enabling multi-method brewer support
affects:
  - 14-02 (grinder/brewer CRUD routes need dial_type, is_retired, methods relationship)
  - 14-03 (paper/water recipe CRUD routes need description, mineral fields, is_retired)
  - 14-04 (brew setup wizard needs is_retired for filtering)
  - 14-05 (retire/restore lifecycle uses is_retired on all equipment + brew setups)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Idempotent migration: inspector.get_column_names() checks before each batch_alter"
    - "Association table (brewer_methods) for SQLAlchemy many-to-many without extra model"
    - "server_default='0' on Boolean columns for SQLite NOT NULL compatibility"
    - "Post-add UPDATE statements to set defaults on existing rows"

key-files:
  created:
    - migrations/versions/e32844be4891_add_equipment_fields_and_retire_.py
  modified:
    - app/models/equipment.py
    - app/models/brew_setup.py

key-decisions:
  - "brewer_methods association table defined in equipment.py (not a standalone model) — consistent with SQLAlchemy many-to-many pattern"
  - "Idempotent migration reusing 13-02 inspector pattern — guards against create_all pre-existence"
  - "server_default='0' on Boolean NOT NULL columns — SQLite requires a default for batch alter on existing tables"

patterns-established:
  - "Association tables defined at module level before referencing models in equipment.py"
  - "Use _get_column_names() helper in migrations to check column existence before add"

# Metrics
duration: 3min
completed: 2026-02-23
---

# Phase 14 Plan 01: Equipment Model Extension + Migration Summary

**Extended all Phase 13 equipment models with full field set (dial config, mineral fields, retire lifecycle, brewer-method many-to-many) and created idempotent Alembic migration e32844be4891**

## Performance

- **Duration:** ~3 min
- **Started:** 2026-02-23T00:02:57Z
- **Completed:** 2026-02-23T00:05:35Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- Extended `app/models/equipment.py`: Grinder gets dial_type/step_size/min_value/max_value/is_retired; Brewer gets is_retired + many-to-many `methods` relationship via `brewer_methods` association table; Paper gets description/is_retired; WaterRecipe gets notes + 7 mineral fields (gh, kh, ca, mg, na, cl, so4) + is_retired
- Extended `app/models/brew_setup.py`: BrewSetup gets is_retired
- Generated and refined Alembic migration `e32844be4891` — idempotent upgrade/downgrade using inspector checks, creates `brewer_methods` table, adds all new columns with proper defaults for existing rows
- Migration runs cleanly: `alembic upgrade head` succeeds, `alembic current` = `e32844be4891 (head)`
- All 153 tests pass after migration

## Task Commits

Each task was committed atomically:

1. **Task 1: Extend SQLAlchemy models with all required fields** - `edfbdfd` (feat)
2. **Task 2: Create Alembic migration for schema changes** - `c637033` (feat)

**Plan metadata:** (docs commit follows)

## Files Created/Modified

- `app/models/equipment.py` — Extended with full field set + brewer_methods association table
- `app/models/brew_setup.py` — Added is_retired Boolean field
- `migrations/versions/e32844be4891_add_equipment_fields_and_retire_.py` — Idempotent migration for all equipment schema changes

## Decisions Made

- **brewer_methods as module-level Table()**: Defined as `Table(...)` at module level in `equipment.py` before the `Brewer` class, using SQLAlchemy's standard association table pattern. Kept in `equipment.py` since it's the natural home (connects Brewer to BrewMethod).
- **Idempotent migration with `_get_column_names()` helper**: Reused the inspector pattern from Phase 13-02 since `app/main.py` calls `Base.metadata.create_all()` at startup — tables/columns may already exist before the migration runs.
- **`server_default='0'` for Boolean NOT NULL**: SQLite's batch alter requires a server_default when adding a NOT NULL column to a table that may have existing rows. Used `"0"` (SQLite truthy false) plus explicit UPDATE statement for rows where the value is NULL.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added brewer_methods table creation to migration**

- **Found during:** Task 2 — autogenerate ran but did not detect the new `brewer_methods` table
- **Issue:** `alembic revision --autogenerate` only detected column changes, not the new association table (table didn't exist in DB when autogenerate compared against the current schema state)
- **Fix:** Manually added `op.create_table("brewer_methods", ...)` with idempotency guard to the upgrade function, and corresponding `op.drop_table("brewer_methods")` in downgrade
- **Files modified:** `migrations/versions/e32844be4891_add_equipment_fields_and_retire_.py`
- **Verification:** `alembic upgrade head` creates the table; `alembic current` = head

**2. [Rule 2 - Missing Critical] Added idempotency guards and explicit default UPDATEs**

- **Found during:** Task 2 — raw autogenerate output lacked inspector checks
- **Issue:** Autogenerated migration was not idempotent (would fail if `create_all` had already created columns). Also missing `server_default` for `is_retired` Boolean NOT NULL, and missing UPDATE statements to set defaults on existing rows.
- **Fix:** Wrapped each `batch_alter_table` call in `if col_name not in existing_cols` guards; added `server_default="0"` on Boolean columns; added `UPDATE ... SET is_retired = 0 WHERE is_retired IS NULL` statements after each add
- **Files modified:** `migrations/versions/e32844be4891_add_equipment_fields_and_retire_.py`
- **Verification:** Migration runs cleanly on existing DB; 153/153 tests pass

---

**Total deviations:** 2 auto-fixed (both Rule 2 - Missing Critical)
**Impact on plan:** Both fixes essential for correct migration behavior on existing databases. No scope creep.

## Issues Encountered

None — both deviations were anticipated patterns from Phase 13-02.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- **14-02 (Equipment router + CRUD):** All model fields now exist. Grinder has `dial_type`, `step_size`, `min_value`, `max_value`, `is_retired`. Brewer has `is_retired` and `methods` many-to-many. Ready for route + template implementation.
- **14-03 (Paper/Water CRUD):** Paper has `description`/`is_retired`; WaterRecipe has all mineral fields + `notes` + `is_retired`. Ready.
- **Blockers:** None.

---
*Phase: 14-equipment-management*
*Completed: 2026-02-23*
