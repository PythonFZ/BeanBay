---
phase: "15"
plan: "02"
subsystem: brew-router
tags: [brew, campaign-key, pour-over, templates, setup]
one-liner: "Brew router wired to campaign_key with method-aware forms for pour-over and espresso"

dependency-graph:
  requires:
    - "15-01: campaign_key scheme and OptimizerService API"
    - "14-05: active_setup_id cookie and BrewSetup model"
  provides:
    - "_get_method_from_setup(setup) → brew method name"
    - "_get_campaign_key(bean, setup) → compound campaign key"
    - "record_measurement() stores brew_setup_id on Measurement"
    - "Method-aware templates: pour-over shows bloom/brew_volume, espresso-only fields guarded"
  affects:
    - "15-03: integration tests verify brew_setup_id storage and method routing"

tech-stack:
  added: []
  patterns:
    - "Method derivation from setup.brew_method.name.lower()"
    - "Optional form fields for method-specific params (preinfusion_pct, target_yield, saturation)"
    - "Hidden method/brew_setup_id fields in forms carry context through POST"

key-files:
  created: []
  modified:
    - app/routers/brew.py
    - app/templates/brew/recommend.html
    - app/templates/brew/manual.html

decisions:
  - id: "15-02-A"
    summary: "Method derived from setup.brew_method.name.lower(), defaults to 'espresso'"
    why: "Simplest path: brew_method is a direct relationship on BrewSetup"
  - id: "15-02-B"
    summary: "preinfusion_pct, target_yield, saturation are Optional form fields"
    why: "Pour-over measurements don't have these; nullable at DB level was confirmed sufficient"
  - id: "15-02-C"
    summary: "Hidden method + brew_setup_id fields in recommend/manual forms"
    why: "Passes context from GET recommendation display through POST record without cookies"

metrics:
  duration: "~25 minutes"
  completed: "2026-02-23"
  tests-before: 193
  tests-after: 193
---

# Phase 15 Plan 02: Brew Router Method Integration Summary

## What Was Built

Wired the campaign key system into the brew router. `trigger_recommend` now derives method from the active setup and builds a compound campaign key. `record_measurement` accepts method-specific optional params and stores `brew_setup_id` on the Measurement. Templates conditionally show pour-over vs espresso parameters.

## Tasks Completed

| Task | Name | Commit | Key Files |
|------|------|--------|-----------|
| 1 | Add _get_method_from_setup and _get_campaign_key helpers | 24612c3 | app/routers/brew.py |
| 2 | Update trigger_recommend and record_measurement | 24612c3 | app/routers/brew.py |
| 3 | Update recommend.html and manual.html templates | 24612c3 | app/templates/brew/ |

## Decisions Made

| ID | Decision | Rationale |
|----|----------|-----------|
| 15-02-A | Method derived from `setup.brew_method.name.lower()` | Direct relationship on BrewSetup; no need to traverse brewer.methods |
| 15-02-B | `preinfusion_pct`, `target_yield`, `saturation` are `Optional` form fields | Pour-over measurements omit these; DB allows NULL for these columns |
| 15-02-C | Hidden `method` + `brew_setup_id` in forms | Carries context from recommendation display through the record POST |

## Deviations from Plan

None — plan executed exactly as written.

## Next Phase Readiness

- ✅ `brew_setup_id` stored on Measurement when provided
- ✅ Pour-over and espresso routes fully functional
- ✅ 193/193 tests passing
