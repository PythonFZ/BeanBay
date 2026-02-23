---
phase: "15"
plan: "03"
subsystem: testing
tags: [tests, history, campaign-key, pour-over, setup-context]
one-liner: "17 multi-method tests + joinedloaded brew_setup_name badge in history rows"

dependency-graph:
  requires:
    - "15-01: optimizer_key helpers"
    - "15-02: brew router with campaign_key and brew_setup_id storage"
  provides:
    - "17 tests covering campaign key, pour-over params, legacy migration, brew_setup_id"
    - "brew_setup_name in shot dicts via joinedload (no N+1)"
    - "Setup name badge on history shot rows"
  affects:
    - "Phase 16: BayBE intelligence integration builds on verified multi-method foundation"

tech-stack:
  added: []
  patterns:
    - "joinedload for related model in shot dicts (N+1 avoidance)"
    - "Dict-based shot rendering (brew_setup_name key, not ORM attribute)"

key-files:
  created:
    - tests/test_brew_multimethod.py
  modified:
    - app/routers/history.py
    - app/templates/history/_shot_row.html

decisions:
  - id: "15-03-A"
    summary: "brew_setup_name added to shot dict, not accessed via ORM in template"
    why: "History renders from plain dicts; template has no ORM access"
  - id: "15-03-B"
    summary: "joinedload(Measurement.brew_setup) added to _build_shot_dicts query"
    why: "Avoids N+1 queries when listing many shots with setup context"

metrics:
  duration: "~20 minutes"
  completed: "2026-02-23"
  tests-before: 193
  tests-after: 210
---

# Phase 15 Plan 03: Multi-Method Tests + History Setup Badge Summary

## What Was Built

Added 17 tests verifying the entire multi-method campaign key system end-to-end, plus setup context display in the history page. The history page now shows a small badge with the setup name on any measurement that has a `brew_setup_id`.

## Tasks Completed

| Task | Name | Commit | Key Files |
|------|------|--------|-----------|
| 1 | Create test_brew_multimethod.py with 17 tests | ab25b38 | tests/test_brew_multimethod.py |
| 2 | Add brew_setup_name to history shot dicts + badge | ab25b38 | app/routers/history.py, _shot_row.html |
| 3 | Full test suite run (210 passing) | ab25b38 | — |

## Tests Added (17)

| # | Test Name | What It Verifies |
|---|-----------|-----------------|
| 1 | test_campaign_key_espresso_no_setup | `b1__espresso__none` format |
| 2 | test_campaign_key_espresso_with_setup | `b1__espresso__s1` format |
| 3 | test_campaign_key_pour_over | `b1__pour-over__s1` format |
| 4 | test_parse_campaign_key_roundtrip | parse(make(...)) == original components |
| 5 | test_parse_campaign_key_none_sentinel | "none" sentinel → None |
| 6 | test_parse_legacy_key | bare UUID → espresso/None defaults |
| 7 | test_is_legacy_key_old_format | bare UUID → True |
| 8 | test_is_legacy_key_new_format | compound key → False |
| 9 | test_legacy_migration_renames_file | {uuid}.json → {uuid}__espresso__none.json |
| 10 | test_legacy_migration_skips_existing | no overwrite if new file exists |
| 11 | test_optimizer_pour_over_campaign_has_bloom_param | bloom_weight + brew_volume in searchspace |
| 12 | test_optimizer_espresso_campaign_has_saturation | saturation + preinfusion_pct in searchspace |
| 13 | test_brew_setup_id_stored_on_measurement | brew_setup_id persisted on Measurement |
| 14 | test_brew_setup_id_null_when_not_provided | no setup → Measurement.brew_setup_id is None |
| 15 | test_method_context_in_history | setup name appears in /history response |
| 16 | test_method_defaults_to_espresso_no_setup | _get_method_from_setup(None) == "espresso" |
| 17 | test_method_from_setup_with_brew_method | setup with method → lowercase method name |

## Decisions Made

| ID | Decision | Rationale |
|----|----------|-----------|
| 15-03-A | `brew_setup_name` in shot dict, not template ORM access | History renders plain dicts; no lazy-load available |
| 15-03-B | `joinedload(Measurement.brew_setup)` in query | Prevents N+1 queries for history list |

## Deviations from Plan

### Auto-fixed Issues

**[Rule 3 - Blocking] Wrong import path for BrewMethod**

- **Found during:** Task 1 (test fixture setup)
- **Issue:** `from app.models.equipment import BrewMethod` raised ImportError; correct path is `app.models.brew_method`
- **Fix:** Updated import in `sample_brew_method` fixture
- **Commit:** ab25b38 (fixed inline before commit; ruff also caught unused `Path` import)

## Next Phase Readiness

- ✅ Phase 15 complete (3/3 plans done)
- ✅ 210/210 tests passing
- ✅ Campaign key system fully tested
- ✅ Pour-over and espresso optimization paths verified
- ✅ Setup context visible in history
- Ready for Phase 16: BayBE intelligence integration (transfer learning, insights)
