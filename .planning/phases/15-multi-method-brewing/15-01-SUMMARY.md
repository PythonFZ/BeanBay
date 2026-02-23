---
phase: "15"
plan: "01"
subsystem: optimizer
tags: [baybe, campaign-key, pour-over, migration, optimizer]
one-liner: "Compound campaign key (bean+method+setup) with pour-over param set and legacy migration"

dependency-graph:
  requires:
    - "14-05: brew setup active selection (provides active_setup_id cookie)"
  provides:
    - "Campaign key scheme: {bean_id}__{method}__{setup_id}"
    - "make_campaign_key / parse_campaign_key / is_legacy_key helpers"
    - "OptimizerService method-aware: pour-over vs espresso param sets"
    - "migrate_legacy_campaigns() for startup migration"
  affects:
    - "15-02: brew router uses campaign_key from this plan"
    - "15-03: tests verify this scheme"

tech-stack:
  added: []
  patterns:
    - "Compound campaign key pattern: {bean_id}__{method}__{setup_id}"
    - "Legacy migration at startup (rename-on-startup pattern)"
    - "Method-dispatched parameter sets"

key-files:
  created:
    - app/services/optimizer_key.py
  modified:
    - app/services/optimizer.py
    - app/main.py
    - tests/test_optimizer.py

decisions:
  - id: "15-01-A"
    summary: "SEPARATOR = '__' (double underscore)"
    why: "UUID characters never include __ so no ambiguity; readable in filenames"
  - id: "15-01-B"
    summary: "setup_id='none' sentinel in key when no setup selected"
    why: "Avoids trailing separator; consistent key format for all cases"
  - id: "15-01-C"
    summary: "Pour-over: 5 continuous params, no categorical (bloom_weight, brew_volume)"
    why: "Pour-over has no saturation/preinfusion analog; cleaner model"

metrics:
  duration: "~30 minutes"
  completed: "2026-02-23"
  tests-before: 193
  tests-after: 193
---

# Phase 15 Plan 01: Campaign Key Scheme Summary

## What Was Built

Introduced a compound campaign key format (`{bean_id}__{method}__{setup_id}`) for the BayBE optimizer service, enabling separate optimization campaigns per brewing method and equipment setup. Added pour-over parameter set support and a startup migration for legacy bare-UUID campaign files.

## Tasks Completed

| Task | Name | Commit | Key Files |
|------|------|--------|-----------|
| 1 | Create optimizer_key.py helpers | c555e8f | app/services/optimizer_key.py |
| 2 | Rewrite OptimizerService with campaign_key API | c555e8f | app/services/optimizer.py |
| 3 | Add migrate_legacy_campaigns() call at startup | c555e8f | app/main.py |
| 4 | Update test_optimizer.py for new key format | c555e8f | tests/test_optimizer.py |

## Decisions Made

| ID | Decision | Rationale |
|----|----------|-----------|
| 15-01-A | SEPARATOR = `__` (double underscore) | UUIDs never contain `__`; readable in filenames |
| 15-01-B | `setup_id="none"` sentinel in key | Avoids trailing separator; consistent key format |
| 15-01-C | Pour-over: 5 continuous params, no categorical | No saturation/preinfusion analog for pour-over |

## Deviations from Plan

None — plan executed exactly as written.

## Next Phase Readiness

- ✅ `make_campaign_key` exported and usable by brew router
- ✅ `OptimizerService.recommend()` and `add_measurement()` accept `campaign_key` + `method`
- ✅ `migrate_legacy_campaigns()` runs at startup
- ✅ 193/193 tests passing
