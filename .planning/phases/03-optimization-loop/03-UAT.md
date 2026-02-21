---
status: diagnosed
phase: 03-optimization-loop
source: [03-01-SUMMARY.md]
started: 2026-02-21T23:32:57Z
updated: 2026-02-21T23:38:00Z
---

## Current Test

[testing complete]

## Tests

### 1. Brew Entry Page & Navigation
expected: Visit /brew (with an active bean selected). You see a "Get Recommendation" button. Before any shots have been recorded for this bean, the "Repeat Best" button should NOT appear.
result: pass

### 2. Get a Recommendation
expected: Tap "Get Recommendation". You're shown 6 recipe parameters in large, arm's-length-readable text: grind setting, temperature, pre-infusion %, dose, yield, and saturation. The brew ratio (e.g. "1:2.1") is also displayed alongside.
result: pass

### 3. Submit a Taste Score
expected: After reviewing the recommendation, use the taste slider (1–10 in 0.5 steps) to rate a shot and optionally enter an extraction time in seconds. Tap submit. You're redirected back and the cycle is ready to start again.
result: pass

### 4. Mark a Shot as Failed
expected: On the recommendation/rating page, toggle the "Failed shot" option (for a choked or gusher shot). The taste score input becomes irrelevant — submit the form. The failed shot is recorded with taste=1 automatically.
result: pass

### 5. Repeat Best Recipe
expected: After recording at least one successful shot, return to /brew. A "Repeat Best" button now appears. Tap it — you see the highest-rated (non-failed) recipe for this bean displayed, with its brew ratio. No new BayBE recommendation is triggered.
result: issue
reported: "when I brew a 8/10 and rate it higher, that does not appear to get saved as I am again only seeing the best recipe if I click it again to only show 8/10"
severity: major

### 6. No Active Bean Guard
expected: Clear your active bean (or visit /brew without one selected). All brew routes (/brew, /brew/recommend, /brew/best) redirect you to /beans instead of showing an error.
result: issue
reported: "pass that works well. however there is no way to clear the active bean"
severity: minor

## Summary

total: 6
passed: 4
issues: 2
pending: 0
skipped: 0

## Gaps

- truth: "Repeat Best shows the highest-rated non-failed recipe for this bean, updating after each new measurement"
  status: failed
  reason: "User reported: when I brew a 8/10 and rate it higher, that does not appear to get saved as I am again only seeing the best recipe if I click it again to only show 8/10"
  severity: major
  test: 5
  root_cause: "brew/best.html uses hardcoded recommendation_id='best-{{ best.id }}' — stable across every page visit, so the deduplication guard in POST /brew/record blocks all but the first Brew Again submission. The new measurement is never inserted."
  artifacts:
    - path: "app/templates/brew/best.html"
      issue: "Line 25: recommendation_id hardcoded to 'best-{{ best.id }}' — same value every visit"
    - path: "app/routers/brew.py"
      issue: "Lines 171–173: deduplication guard correctly blocks re-inserts but fires on every Brew Again because id never changes"
  missing:
    - "Generate a fresh UUID in show_best route and pass as best_session_id to template"
    - "Use {{ best_session_id }} as recommendation_id in best.html instead of 'best-{{ best.id }}'"
  debug_session: ".planning/debug/resolved/best-recipe-not-updating.md"

- truth: "User can clear/deselect the active bean from the UI"
  status: failed
  reason: "User reported: there is no way to clear the active bean"
  severity: minor
  test: 6
  root_cause: "Missing feature — activate_bean endpoint and UI exist but no deactivate_bean endpoint or UI was ever implemented. Cookie persists for 1 year with no deletion path."
  artifacts:
    - path: "app/routers/beans.py"
      issue: "Has POST /beans/{id}/activate with set_cookie. Missing: deactivate endpoint with delete_cookie."
    - path: "app/templates/beans/detail.html"
      issue: "Active bean branch shows badge only. Missing: Deselect button/form."
    - path: "app/templates/base.html"
      issue: "Nav active-bean-indicator shows name but no clear action."
  missing:
    - "POST /beans/deactivate endpoint calling response.delete_cookie('active_bean_id')"
    - "Deselect form on beans/detail.html in the active-bean branch"
    - "Optional: clear button in base.html nav indicator"
  debug_session: ".planning/debug/resolved/no-ui-to-deselect-active-bean.md"
