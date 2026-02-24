# Project State: BeanBay

**Last updated:** 2026-02-24
**Current phase:** Phase 17 — Campaign Storage Migration (planned, not started)

## Project Reference

See: .planning/PROJECT.md (updated 2026-02-24)

**Core value:** Every coffee brew teaches the system something — the app must make it effortless to capture that feedback from a phone at the espresso machine and return increasingly better recommendations.
**Current focus:** v0.3.0 — Equipment intelligence, capability-driven parameters, new brew methods, campaign DB migration, frontend modernization

## Milestone History

| Milestone | Phases | Plans | Status | Date |
|-----------|--------|-------|--------|------|
| v1 MVP | 1-6 | 16 | ✅ Shipped | 2026-02-22 |
| v0.1.0 Release & Deploy | 7-9 | 5 | ✅ Shipped | 2026-02-22 |
| v0.1.1 UX Polish & Manual Brew | 10-12 | 8 | ✅ Shipped | 2026-02-22 |
| v0.2.0 Multi-Method & Intelligence | 13-16 | 13 | ✅ Shipped | 2026-02-23 |
| v0.3.0 Equipment Intelligence & Parameter Evolution | 17-22 | TBD | 🔄 Planned | — |

## Current Position

Phase: 17 of 22 (Campaign Storage Migration) — planned, not started
Plan: 0 of ? — phase not yet plan-detailed
Status: v0.3.0 roadmap complete, awaiting phase planning (/gsd-plan-phase)
Last activity: 2026-02-24 — v0.3.0 roadmap finalized

Progress: [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0% (0/? v0.3.0 plans)

## Performance Metrics

**Velocity:**
  - Total plans completed: 42 (v1: 16, v0.1.0: 5, v0.1.1: 8, v0.2.0: 13)
  - Total phases completed: 16 complete
  - All milestones shipped same day (Feb 22-23, 2026)

## Accumulated Context

### Key Technical Decisions
See: .planning/PROJECT.md (Key Decisions table — 22+ decisions tracked)

### Branding
- **Name:** BeanBay | **Domain:** beanbay.coffee
- **Docker:** ghcr.io/grzonka/beanbay | **Latest release:** v0.2.0

### v0.2.0 Key Design Decisions (from questioning phase)
- **Equipment as context:** Equipment defines the experiment context; BayBE optimizes recipe variables within that context. Comparison between equipment setups happens at analytics level, not optimizer level.
- **Transfer learning via TaskParameter:** BayBE's TaskParameter class enables cross-bean cold-start. Similar beans (by process + variety) provide training data; new bean is the test task. Search spaces must match for transfer learning to work.
- **Bean bags model:** A "coffee" can have multiple bags. Same coffee bought twice shares identity, enabling richer history and transfer learning similarity matching.
- **Beanconqueror import deferred:** Moved to backlog, not in v0.2 scope.

### v0.3.0 Key Design Decisions
- **Capability-driven, not tier-based:** A brewer declares what it can do (capability flags). Tiers are derived for UX progressive disclosure, not stored.
- **Parameter Registry pattern:** `PARAMETER_REGISTRY` dict maps method → parameter definitions. Adding new methods is trivial. Drives dynamic search space building.
- **preinfusion_pct → preinfusion_time:** Physical-unit seconds replaces opaque percentage. Linear migration for existing data.
- **saturation deprecated:** Redundant with preinfusion time (0 = no saturation).
- **Campaign files → DB:** Highest-priority architectural change. Campaign JSON moves to `campaigns` table; pending_recommendations.json moves to `pending_recommendations` table.
- **Frontend Phase 1:** htmx + Tailwind + daisyUI (coffee theme). Low effort, big visual improvement.
- **Espresso advanced params:** pump pressure (bar), flow rate (ml/s), pressure profiling (categorical), pre-infusion (multiple types), bloom/soak, temperature profiling, brew mode (pressure vs flow priority). All conditional on brewer capabilities.

### Phase 14 Key Decisions
- **Retire-only pattern (no deletion):** Preserves history; retired equipment hidden by default, shown with toggle
- **Cascade retire, manual restore:** Retiring a component auto-retires all setups using it; restoring does NOT cascade
- **active_setup_id cookie:** Same pattern as active_bean_id; 1-year expiry; cleared if setup is retired
- **Setup is context for brew page:** Brew action buttons require a bean but setup is optional (for future BayBE integration)

### Phase 15 Key Decisions
- **Campaign key format `bean__method__setup`:** Double-underscore separator avoids collisions with bean IDs that may contain underscores
- **Pour-over param set:** Adds `preinfusion_pct`, `target_yield`, `saturation` (all continuous, ranges tuned for V60-style brewing)
- **Legacy migration at startup:** `migrate_legacy_campaigns()` runs in `main.py` lifespan, transparently maps old `{bean_id}` keys to `{bean_id}__espresso__None`
- **brew_setup_name in shot dict:** Template has no ORM access, so `brew_setup_name` added as plain key to shot dicts in `_build_shot_dicts()` (not ORM relationship access)

### Phase 16 Key Decisions
- **Transfer metadata as .transfer sidecar file:** Consistent with .bounds sidecar pattern; easy presence-check without loading campaign
- **transfer_metadata stored in pending recommendation dict:** Survives server restarts; show_recommendation reads metadata without extra optimizer call
- **TYPE_CHECKING guard for Bean/Session imports in optimizer.py:** Avoids circular import at module load time; type hints only, not runtime
- **None return when no training data:** Even with matching similar_beans, if no actual DB measurements exist for those beans, returns None gracefully

### Quick Tasks Completed

| ID | Task | Date |
|----|------|------|
| 001 | Fix CI test DB isolation | 2026-02-22 |
| 002 | Style brew select dropdowns to match dark theme | 2026-02-23 |

### Known Bugs

| Bug | Description | When to Fix |
|-----|-------------|-------------|
| B001 | Non-espresso brewer still shows "Espresso" on equipment card | Phase 18 or quick task |

## Session Continuity

### Last Session
- **Date:** 2026-02-24
- **What happened:** Finalized v0.3.0 roadmap (6 phases, 17-22). Completed comprehensive research (espresso capabilities, brewing parameters, architecture, stack, pitfalls). Cleaned up ROADMAP.md, STATE.md, PROJECT.md. v0.3.0 ready for phase planning.
- **Where we left off:** v0.3.0 roadmap complete. Next: plan Phase 17 (Campaign Storage Migration) or Phase 18 (Brewer Capability Model) or Phase 22 (Frontend daisyUI) — all three are Wave 1 (independent, can be planned in any order).

### Next Steps
1. Plan Phase 17 (Campaign Storage Migration) — `/gsd-plan-phase 17`
2. Plan Phase 18 (Brewer Capability Model) — `/gsd-plan-phase 18`
3. Plan Phase 22 (Frontend daisyUI) — `/gsd-plan-phase 22`
4. Wave 1 phases are independent — plan and execute in any order or parallel

---
*State initialized: 2026-02-21*
*Last updated: 2026-02-24 — v0.3.0 roadmap finalized (6 phases: 17-22, 3 waves)*
