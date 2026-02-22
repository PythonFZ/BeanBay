---
phase: 09-deployment-templates
plan: 01
subsystem: infra
tags: [docker, docker-compose, dockerfile, unraid, ghcr, deployment]

# Dependency graph
requires:
  - phase: 07-rebrand-cleanup
    provides: BeanBay naming conventions and BEANBAY_ env prefix established
  - phase: 08-documentation-release
    provides: GitHub Actions Docker publish workflow publishing to ghcr.io/grzonka/beanbay
provides:
  - docker-compose.yml with BeanBay naming and ghcr.io image reference
  - Dockerfile with BEANBAY_DATA_DIR env var and OCI LABEL metadata
  - .dockerignore with comprehensive dev/test exclusions
  - unraid/beanbay.xml Unraid Community Apps installable template
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "ghcr.io/grzonka/beanbay:latest as canonical Docker image reference"
    - "Unraid CA XML template format for community app distribution"

key-files:
  created:
    - unraid/beanbay.xml
  modified:
    - docker-compose.yml
    - Dockerfile
    - .dockerignore

key-decisions:
  - "docker-compose.yml references ghcr.io image so users can pull instead of build"
  - "Icon URL in Unraid XML will 404 gracefully until beanbay-icon.png is manually added"

patterns-established:
  - "OCI LABELs in Dockerfile for GHCR discoverability"

# Metrics
duration: 2min
completed: 2026-02-22
---

# Phase 9 Plan 01: Deployment Templates Summary

**Updated Docker deployment files with BeanBay naming and ghcr.io image reference; created Unraid Community Apps XML template installable via custom repo at unraid/beanbay.xml**

## Performance

- **Duration:** ~2 min
- **Started:** 2026-02-22T14:03:10Z
- **Completed:** 2026-02-22T14:04:40Z
- **Tasks:** 2
- **Files modified:** 4 (3 updated + 1 created)

## Accomplishments
- Updated `docker-compose.yml`: service/volume renamed to `beanbay`, added `image: ghcr.io/grzonka/beanbay:latest` and `container_name: beanbay`, env var updated to `BEANBAY_DATA_DIR`
- Updated `Dockerfile`: `BREWFLOW_DATA_DIR` → `BEANBAY_DATA_DIR`, added OCI LABEL metadata (source, description, license) for GHCR discoverability
- Updated `.dockerignore`: added `.github/`, `unraid/`, `my_espresso.py`, `.pytest_cache/` exclusions for cleaner Docker builds
- Created `unraid/beanbay.xml`: valid Unraid Community Apps XML template pointing to `ghcr.io/grzonka/beanbay:latest`, port 8000, appdata volume at `/mnt/user/appdata/beanbay`

## Task Commits

Each task was committed atomically:

1. **Task 1: Update Docker files with BeanBay naming** - `bc7904a` (chore)
2. **Task 2: Create Unraid Community Apps XML template** - `a492336` (feat)

**Plan metadata:** pending (docs commit)

## Files Created/Modified
- `docker-compose.yml` - Service/volume renamed to beanbay, ghcr.io image added, BEANBAY_DATA_DIR env var
- `Dockerfile` - BREWFLOW_DATA_DIR → BEANBAY_DATA_DIR, OCI LABEL metadata added for GHCR
- `.dockerignore` - Added .github/, unraid/, my_espresso.py, .pytest_cache/ exclusions
- `unraid/beanbay.xml` - Unraid Community Apps XML template, valid XML, GHCR image reference

## Decisions Made
- Added `image: ghcr.io/grzonka/beanbay:latest` to docker-compose.yml so users can pull the published image instead of building from source — this is the primary deployment flow post-v0.1.0.
- Icon URL in Unraid XML (`unraid/beanbay-icon.png`) will 404 gracefully until a PNG icon is manually created and committed. Unraid CA shows a default icon in that case. BRAND-03 (app icon) is deferred.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 9 complete — all v0.1.0 deployment templates in place
- v0.1.0 milestone complete (5/5 plans done)
- To make BeanBay installable via Unraid Community Apps custom repo: add the repo URL `https://github.com/grzonka/beanbay` to Unraid Community Apps settings
- Optional: Create `unraid/beanbay-icon.png` (32x32 or 64x64) and commit to repo for the Unraid CA icon display
- Ready to deploy to Unraid: `docker compose up -d` or install via Unraid CA

---
*Phase: 09-deployment-templates*
*Completed: 2026-02-22*
