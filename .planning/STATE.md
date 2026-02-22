# Project State: BeanBay

**Last updated:** 2026-02-22
**Current phase:** Phase 9 — Deployment Templates (complete).

## Project Reference

See: .planning/PROJECT.md (updated 2026-02-22)

**Core value:** Every coffee brew teaches the system something — the app must make it effortless to capture that feedback from a phone at the espresso machine and return increasingly better recommendations.
**Current focus:** v0.1.0 — Rebrand to BeanBay, clean up, ship, deploy.

## Milestone History

| Milestone | Phases | Plans | Status | Date |
|-----------|--------|-------|--------|------|
| v1 MVP | 1-6 | 16 | Shipped | 2026-02-22 |
| v0.1.0 Release & Deploy | 7-9 | 5 | ✅ Complete | 2026-02-22 |

See: .planning/MILESTONES.md

## Phase Status

### v0.1.0 Phases

| Phase | Name | Status |
|-------|------|--------|
| 7 | Rebrand & Cleanup | ✅ Complete & Verified |
| 8 | Documentation & Release | ✅ Complete (2/2 plans done) |
| 9 | Deployment Templates | ✅ Complete (1/1 plans done) |

**Overall progress:** All v0.1.0 phases complete. 5/5 v0.1.0 plans done. Milestone complete.

## Current Position

Phase: 9 of 9 (Deployment Templates) — Complete
Plan: 1 of 1 in Phase 9
Status: Phase complete — v0.1.0 milestone complete
Last activity: 2026-02-22 - Completed 09-01-PLAN.md (Docker files + Unraid CA XML)

Progress: █████ 100% (5/5 v0.1.0 plans)

## Blockers

- ~~GitHub repo not yet created.~~ ✅ `grzonka/beanbay` exists on GitHub.
- ~~Docker build not verified (daemon not available in dev environment).~~ ✅ Docker Publish workflow triggered on v0.1.0 tag — building in GitHub Actions.

## Accumulated Context

### Key Technical Decisions
See: .planning/PROJECT.md (Key Decisions table)

### Backlog
- **Manual brew input** — User can manually enter all 6 recipe parameters and submit a taste score, bypassing BayBE recommendation. Manual entries fed to BayBE via add_measurement. Deferred to v2.

### Tech Debt (from v1 audit — RESOLVED in Phase 7)
- ✅ Duplicated _get_active_bean helper in brew.py and insights.py
- ✅ Dead app/routes/ directory with empty __init__.py
- ✅ In-memory pending_recommendations dict lost on server restart
- ✅ Startup ALTER TABLE migration outside Alembic
- ✅ Silent ValueError on override parsing
See: .planning/phases/07-rebrand-cleanup/07-02-SUMMARY.md

### Branding
- **New name:** BeanBay (was BrewFlow)
- **Domain:** beanbay.coffee
- **Repo:** grzonka/beanbay ✅
- **Docker image:** ghcr.io/grzonka/beanbay ✅ (publishing via GitHub Actions on tags)
- **Release:** v0.1.0 live at https://github.com/grzonka/beanbay/releases/tag/v0.1.0

## Session Continuity

### Last Session
- **Date:** 2026-02-22
- **What happened:** Executed Phase 9 Plan 01. Updated Docker files with BeanBay naming (docker-compose.yml, Dockerfile, .dockerignore) and created Unraid Community Apps XML template at unraid/beanbay.xml. Phase 9 complete. v0.1.0 milestone complete.
- **Where we left off:** All v0.1.0 phases done (5/5 plans). Deploy to Unraid is next.

### Next Steps
1. Deploy to Unraid using `docker compose up -d` or install via Community Apps custom repo
2. Optional: Create `unraid/beanbay-icon.png` for Unraid CA icon display (BRAND-03)

---
*State initialized: 2026-02-21*
*Last updated: 2026-02-22 after 09-01 (Docker files + Unraid CA XML — v0.1.0 complete)*
