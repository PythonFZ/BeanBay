---
status: complete
phase: 05-insights-trust
source: 05-01-SUMMARY.md, 05-02-SUMMARY.md
started: 2026-02-22T02:30:09Z
updated: 2026-02-22T02:45:00Z
---

## Current Test

[testing complete]

## Tests

### 1. Phase badge on recommendation page
expected: After tapping "Get Recommendation", the recommendation page shows a colored phase badge — either "Random exploration" (blue) or "Bayesian optimization" (gold) — above or near the recipe parameters.
result: issue
reported: "seems good but odd that it shows Bayesian optimization after the very first test — BayBE's switch is technically correct but the label may be misleading since the model has no real data yet"
severity: minor

### 2. Contextual explanation text
expected: Below the phase badge, there is a short plain-language explanation of what BayBE is doing. For early shots it should say something like "Exploring randomly — building initial understanding..." or "Building a map of the flavor space...". For more established beans it describes whether it's zeroing in or exploring new territory.
result: pass

### 3. Predicted taste range
expected: On a bean that has 2 or more recorded shots, the recommendation page shows a predicted taste range like "6.5 – 8.0" (using an em dash, not a hyphen). On a brand-new bean with 0–1 shots, no predicted range is shown.
result: issue
reported: "App crashed with NotImplementedError: 'UNSPECIFIED' has no Boolean representation — traceback in baybe/campaign.py line 515, campaign.recommend() calls and cache check fails with UNSPECIFIED sentinel value"
severity: blocker

### 4. Insights page loads
expected: Navigating to /insights (or tapping the "Insights" nav link) loads a page without error. The page shows a heading and content for the active bean.
result: pass

### 5. Progress chart renders
expected: On the insights page for a bean with 2 or more shots, a Chart.js chart is visible showing two datasets: a rising cumulative-best taste line, and scatter dots for individual shots. Failed shots appear red, normal shots appear amber/yellow.
result: pass

### 6. Convergence badge
expected: The insights page displays a colored pill badge showing the optimization stage — e.g., "Getting started", "Early exploration", "Narrowing in", "Refining", or "Near optimal" — with a brief plain-language description below it.
result: pass

### 7. Optimizer mode indicator on insights
expected: The insights page also shows whether BayBE is currently in "Random exploration" or "Bayesian optimization" mode — the same label used on the recommendation page.
result: pass

### 8. No chart on bean with fewer than 2 shots
expected: On the insights page for a brand-new bean (0 or 1 shots recorded), the chart area is not shown or shows an appropriate empty-state message rather than a broken/empty chart.
result: pass

## Summary

total: 8
passed: 6
issues: 2
pending: 0
skipped: 0

## Gaps

- truth: "Phase badge accurately reflects the optimizer's actual behavior at very low shot counts"
  status: failed
  reason: "User reported: badge shows 'Bayesian optimization' after just 1 shot — BayBE switches phase after 1 recommendation by default, but the model has essentially no data; label feels misleading"
  severity: minor
  test: 1
  root_cause: ""
  artifacts: []
  missing: []
  debug_session: ""

- truth: "Recommendation page loads without crashing when campaign.recommend() is called"
  status: failed
  reason: "User reported: App crashed — NotImplementedError: 'UNSPECIFIED' has no Boolean representation — in baybe/campaign.py line 515, the campaign.recommend() method tries to evaluate a cached_recommendation sentinel value as a boolean"
  severity: blocker
  test: 3
  root_cause: ""
  artifacts: []
  missing: []
  debug_session: ""
