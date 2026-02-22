---
phase: 05
plan: "01"
name: "recommendation-insights"
subsystem: "optimizer-ui"
tags: ["baybe", "insights", "explore-exploit", "posterior-stats", "jinja2", "css"]

dependency-graph:
  requires:
    - "03-01: OptimizerService with recommend/add_measurement"
    - "03-02: brew router with pending_recommendations pattern"
  provides:
    - "OptimizerService.get_recommendation_insights()"
    - "_recommendation_insights.html partial"
    - "Explore/exploit phase detection via BayBE select_recommender()"
    - "Predicted taste range via campaign.posterior_stats()"
  affects:
    - "05-02: Trend charts (can use shot_count and phase from insights)"

tech-stack:
  added: []
  patterns:
    - "BayBE TwoPhaseMetaRecommender.select_recommender() for phase detection"
    - "campaign.posterior_stats() for predicted taste mean/std"
    - "Insights computed synchronously after async recommend() completes"
    - "Insights stored in pending_recommendations dict alongside recipe params"
    - "Jinja2 include pattern for recommendation partial"

key-files:
  created:
    - "app/templates/brew/_recommendation_insights.html"
  modified:
    - "app/services/optimizer.py"
    - "app/routers/brew.py"
    - "app/templates/brew/recommend.html"
    - "app/static/css/main.css"
    - "tests/test_optimizer.py"
    - "tests/test_brew.py"

decisions:
  - id: "05-01-a"
    description: "get_recommendation_insights acquires _lock independently (not inside recommend)"
    rationale: "recommend() releases lock after campaign.recommend(); insights needs separate lock acquisition to avoid deadlock"
  - id: "05-01-b"
    description: "Insights stored inside rec dict as rec['insights'] in pending_recommendations"
    rationale: "Single dict in app.state keeps the data co-located with the recommendation — no separate store needed"
  - id: "05-01-c"
    description: "predicted_range uses em dash (–) not hyphen for proper typography"
    rationale: "Matches design convention; Unicode literal used directly in Python string"

metrics:
  duration: "3 minutes"
  completed: "2026-02-22"
  tests-added: 5
  tests-total: 92
---

# Phase 5 Plan 01: Recommendation Insights Summary

**One-liner:** Explore/exploit phase detection via BayBE `select_recommender()` + predicted taste range via `posterior_stats()`, surfaced on the recommendation page as a phase badge + contextual explanation.

## What Was Built

Added transparent recommendation explanations to the BrewFlow optimization loop. Every recommendation page now shows:

1. **Phase badge** — "Random exploration" (blue) or "Bayesian optimization" (gold)
2. **Contextual explanation** — adapts based on shot count and recent improvement trends
3. **Predicted taste range** — shown after 2+ measurements when the surrogate model has enough data to predict

## Tasks Completed

| Task | Name | Commit | Key Files |
|------|------|--------|-----------|
| 1 | Add get_recommendation_insights to OptimizerService | 902c65d | app/services/optimizer.py, tests/test_optimizer.py |
| 2 | Wire insights into brew router + create partial + CSS | 93d0054 | app/routers/brew.py, _recommendation_insights.html, recommend.html, main.css, tests/test_brew.py |

## Implementation Notes

### Phase Detection
Uses `TwoPhaseMetaRecommender.select_recommender()` to determine whether BayBE is in the random or Bayesian phase:
```python
selected = meta_rec.select_recommender(
    batch_size=1,
    searchspace=campaign.searchspace,
    objective=campaign.objective,
    measurements=campaign.measurements,
)
is_random = isinstance(selected, RandomRecommender)
```

### Contextual Explanations
- **Random phase:** "Exploring randomly — building initial understanding of the parameter space."
- **Bayesian, < 5 shots:** "Building a map of the flavor space — the model is starting to learn your preferences."
- **Bayesian, ≥ 5 shots, improving:** "Zeroing in — recent shots are improving. The model is finding promising regions."
- **Bayesian, ≥ 5 shots, not improving:** "Exploring new territory — looking for something better than the current best."

### Predicted Taste Range
Only shown when `not is_random and shot_count >= 2`. Uses `campaign.posterior_stats(rec_df)` which returns `taste_mean` and `taste_std`. Range is clamped to [1.0, 10.0]:
```
lo = max(1.0, mean - std)
hi = min(10.0, mean + std)
predicted_range = f"{lo} – {hi}"
```

### Thread Safety
`get_recommendation_insights` acquires `self._lock` independently — called after `recommend()` returns, not inside it. This avoids deadlock since `recommend()` releases the lock after `campaign.recommend()`.

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Lock strategy | Separate lock acquisition in get_recommendation_insights | recommend() releases lock before returning; separate call avoids deadlock |
| Insights storage | rec["insights"] inside pending_recommendations dict | Co-located with recipe params, no separate store needed |
| Typography | Em dash (–) in predicted_range | Matches design conventions; cleaner than hyphen |
| Prediction threshold | >= 2 measurements | Minimum for surrogate model to produce meaningful posterior stats |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Updated test_trigger_recommend_generates_and_redirects to mock get_recommendation_insights**

- **Found during:** Task 2 implementation
- **Issue:** The existing test used `AsyncMock()` for the optimizer and didn't mock `get_recommendation_insights`, which is now called synchronously in `trigger_recommend()`. This would cause an `AttributeError` or unexpected BayBE call.
- **Fix:** Updated the test to use `MagicMock()` with explicit mocks for both `recommend` (AsyncMock) and `get_recommendation_insights` (MagicMock returning a fake insights dict).
- **Files modified:** tests/test_brew.py
- **Commit:** 93d0054

## Verification Results

```
92 passed, 2 warnings in 2.17s
```

All 92 tests pass including:
- 3 new optimizer tests (random phase, bayesian phase, improvement detection)
- 2 new brew router tests (shows insights, no prediction on first shot)

## Next Phase Readiness

Phase 5 Plan 02 (trend charts) can proceed. The `shot_count` field from insights provides shot volume data. `posterior_stats()` pattern is proven for Phase 5.
