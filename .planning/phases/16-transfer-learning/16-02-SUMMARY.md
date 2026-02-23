---
phase: "16"
plan: "02"
subsystem: "transfer-learning"
tags: ["baybe", "task-parameter", "optimizer", "router", "template", "integration"]

dependency-graph:
  requires: ["16-01"]
  provides: ["transfer learning wire-up", "OptimizerService TL integration", "transfer badge UI"]
  affects: []

tech-stack:
  added: []
  patterns: [".transfer metadata sidecar file pattern", "TYPE_CHECKING guard for optional ORM params"]

key-files:
  created:
    - tests/test_transfer_learning_integration.py
  modified:
    - app/services/optimizer.py
    - app/routers/brew.py
    - app/templates/brew/recommend.html
    - app/static/css/main.css
    - tests/test_brew.py

decisions:
  - id: "D-16-02-1"
    decision: "Transfer metadata stored as {campaign_key}.transfer JSON sidecar file"
    rationale: "Consistent with existing .bounds sidecar pattern; easy to check for presence without loading campaign"
  - id: "D-16-02-2"
    decision: "transfer_metadata stored inside pending recommendation dict (persisted to disk)"
    rationale: "Survives server restarts; show_recommendation can read metadata from the pending store without extra optimizer call"
  - id: "D-16-02-3"
    decision: "TYPE_CHECKING guard for Bean/Session imports in optimizer.py"
    rationale: "Avoids circular import at module load time; only needed for type hints, not runtime"

metrics:
  duration: "~20 minutes"
  completed: "2026-02-23"
---

# Phase 16 Plan 02: Wire Transfer Learning into Optimizer Summary

**One-liner:** Transfer learning fully wired into OptimizerService.get_or_create_campaign with .transfer sidecar files, brew router bean+db forwarding, and recommend.html badge UI.

## What Was Built

### `app/services/optimizer.py` updates
- `get_or_create_campaign` accepts optional `target_bean` and `db` — on first campaign creation, calls `SimilarityService().find_similar_beans()` and `build_transfer_campaign()` if similar beans exist
- Writes `{campaign_key}.transfer` JSON sidecar when transfer learning activates
- `get_transfer_metadata(campaign_key)` reads the `.transfer` file, returns `None` for standard campaigns
- `add_measurement` accepts `target_bean_id`; injects `bean_task` column for transfer campaigns
- `recommend()` accepts and forwards `target_bean`/`db` to `get_or_create_campaign`
- Rebuild branch updated to filter out `bean_task` column when rebuilding from measurements

### `app/routers/brew.py` updates
- `trigger_recommend`: passes `target_bean=bean, db=db` to `optimizer.recommend()`; calls `get_transfer_metadata()` after; stores result in pending recommendation dict
- `show_recommendation`: reads `transfer_metadata` from pending rec, passes to template context
- `record_measurement`: passes `target_bean_id=str(bean.id)` to `add_measurement()`

### Template + CSS
- `app/templates/brew/recommend.html`: transfer badge appears below insights section when `transfer_metadata` is not None — shows contributing bean count + bean name tags
- `app/static/css/main.css`: `.transfer-badge`, `.badge-info`, `.transfer-details`, `.transfer-bean-tag` using existing CSS variables (same blue as `insight-badge-random`)

### Integration tests
- `tests/test_transfer_learning_integration.py`: 10 tests — all passing
  - Covers: activation, no-metadata, no-similar-beans, .transfer file existence, get_transfer_metadata, add_measurement with/without bean_task, method isolation (espresso ≠ pour-over)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] test_brew.py mock missing get_transfer_metadata return value**

- **Found during:** Final test run
- **Issue:** `MagicMock()` returned another `MagicMock` for `get_transfer_metadata()`, which failed JSON serialization when stored in pending recommendation
- **Fix:** Added `mock_optimizer.get_transfer_metadata = MagicMock(return_value=None)` to the test
- **Files modified:** `tests/test_brew.py`
- **Commit:** Included in feat(16-02) commit

**2. [Rule 2 - Missing Critical] Rebuild branch needs to filter bean_task column**

- **Found during:** Task 1
- **Issue:** When bounds fingerprint changes trigger a rebuild, transfer campaign measurements include `bean_task` column which doesn't exist in fresh standard campaigns
- **Fix:** Filter `available_cols` to only columns present in the standard search space
- **Files modified:** `app/services/optimizer.py`

## Phase 16 Complete

Both plans executed:
- 16-01: SimilarityService + TransferLearningService (20 unit tests)
- 16-02: Optimizer wire-up + router + template + 10 integration tests
- **Total tests: 240 passing** (up from 210 at start of Phase 16)
- Phase 16 = v0.2.0 capstone feature ✅
