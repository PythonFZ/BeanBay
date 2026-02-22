---
status: diagnosed
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
  root_cause: "TwoPhaseMetaRecommender is instantiated without switch_after override; BayBE's default is switch_after=1, so after just 1 recorded measurement (len(measurements) >= 1) it permanently switches to BotorchRecommender and the badge follows — even though the GP is essentially uninformed with 1 data point"
  artifacts:
    - path: "app/services/optimizer.py"
      issue: "Line 123: TwoPhaseMetaRecommender(recommender=BotorchRecommender()) — no switch_after supplied, inherits default of 1"
    - path: "app/services/optimizer.py"
      issue: "Lines 280-299: select_recommender() faithfully returns BotorchRecommender after >=1 measurement; phase_label becomes 'Bayesian optimization'"
    - path: "app/templates/brew/_recommendation_insights.html"
      issue: "Badge renders {{ insights.phase_label }} verbatim — no guard for early Bayesian shots"
  missing:
    - "Set switch_after=5 (or 3) in TwoPhaseMetaRecommender instantiation in optimizer.py line 123"
    - "Optionally add a 'bayesian_early' sub-phase label (e.g. 'Learning') for shots between switch and ~8 to smooth the transition"
  debug_session: ".planning/debug/recommendation-phase-badge-too-early.md"

- truth: "Recommendation page loads without crashing when campaign.recommend() is called"
  status: failed
  reason: "User reported: App crashed — NotImplementedError: 'UNSPECIFIED' has no Boolean representation — in baybe/campaign.py line 515, the campaign.recommend() method tries to evaluate a cached_recommendation sentinel value as a boolean"
  severity: blocker
  test: 3
  root_cause: "BayBE 0.14.2 sets campaign.allow_recommending_already_recommended = UNSPECIFIED for hybrid/continuous search spaces (not DISCRETE). The cache fast-path guard in Campaign.recommend() at line 513-518 evaluates this sentinel as a boolean on the 2nd+ call (when _cached_recommendation is non-None and short-circuit evaluation no longer saves it), causing UnspecifiedType.__bool__ to raise NotImplementedError. First call succeeds; every subsequent call crashes."
  artifacts:
    - path: "app/services/optimizer.py"
      issue: "Line 193: campaign.recommend(batch_size=1) — no cache clear before call"
    - path: ".venv/lib/python3.11/site-packages/baybe/campaign.py"
      issue: "Lines 513-518: cache guard evaluates allow_recommending_already_recommended as bool without guarding for UNSPECIFIED"
    - path: ".venv/lib/python3.11/site-packages/baybe/campaign.py"
      issue: "Lines 73-84: factory sets flag to UNSPECIFIED for HYBRID search spaces (our space is hybrid)"
  missing:
    - "Call campaign.clear_cache() immediately before campaign.recommend(batch_size=1) in optimizer.py _recommend method — resets _cached_recommendation to None so the walrus guard always short-circuits before reaching the UNSPECIFIED field"
  debug_session: ".planning/debug/recommend-unspecified-bool-crash.md"
