# Phase 15: Multi-Method Brewing & Setup Integration - Context

**Gathered:** 2026-02-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Brew flow supports multiple methods — user selects a brew setup before getting recommendations, and each method+setup+bean combo gets its own BayBE campaign. The selected brew setup already lives in a cookie from Phase 14. This phase wires that selection into campaign scoping and adds method-specific parameter sets.

Core work:
1. **OptimizerService**: campaign key changes from `bean_id` → `{bean_id}__{method}__{setup_id}`. Method-specific parameter sets (espresso = current 6 params; pour-over adds bloom).
2. **Brew flow**: active_setup drives the campaign key. Method is derived from the setup's brewer's associated brew method.
3. **Backward compat**: existing campaigns (keyed by `bean_id` only) are migrated/aliased to the default espresso setup so no data is lost.
4. **History/insights/analytics**: show method and setup name as context on measurements.

</domain>

<decisions>
## Implementation Decisions

### Campaign key scheme
- New key format: `{bean_id}__{method_name}__{setup_id}`
- Old key format: `{bean_id}` (bare UUID)
- Backward compat: at startup, scan campaigns_dir for files named `{uuid}.json` (old format). Copy/rename to new key `{bean_id}__espresso__{default_setup_id}` using the default espresso setup. If no default setup exists yet, use `{bean_id}__espresso__none` as fallback key.
- Campaign files: `{campaign_key}.json` and `{campaign_key}.bounds`

### Method-specific parameter sets
- **Espresso**: grind_setting, temperature, preinfusion_pct, dose_in, target_yield, saturation (unchanged from Phase 13)
- **Pour-over**: grind_setting, temperature, bloom_weight (g, continuous), dose_in, brew_volume (continuous, replaces target_yield), saturation optional
- **Other**: same as espresso (generic fallback) — no special params
- Pour-over bloom parameter bounds: bloom_weight 20–80g; brew_volume 150–500ml
- The method is derived from the active setup's brewer's brew methods. If setup has no brewer, default to espresso.

### Brew flow integration
- `brew_index()` already has active_setup from cookie (Phase 14)
- `trigger_recommend()` now passes `campaign_key` (derived from bean + setup) to optimizer
- `record_measurement()` stores `brew_setup_id` on Measurement (column already exists from Phase 13)
- Manual brew: uses same campaign key as the active setup

### Measurement model changes
- `brew_setup_id` column already exists (nullable) from Phase 13 — just need to populate it
- No new columns needed on Measurement for method — method is derived from the setup's brewer

### Existing data migration
- Existing measurements have `brew_setup_id = NULL` — leave them as-is (backward compat)
- Existing BayBE campaigns (keyed by bare bean_id) are migrated to `{bean_id}__espresso__none` key
- This happens once at optimizer startup via a migration scan

### History, insights, analytics
- These pages display existing measurements — add setup name as optional context label
- "Show method" badge only if measurement has a brew_setup_id
- No behavioral change — purely additive display change

### OpenCode's Discretion
- Exact pour-over parameter names and units
- Whether to show method in recommendation/record flow or just in history
- Exact campaign key separator (__ is safe since UUIDs don't contain it)
- Error handling if setup is retired mid-session

</decisions>

<specifics>
## Specific Ideas

- The campaign key change is the core of this phase — everything else flows from it
- Espresso users see NO UI change (their setup just invisibly scopes the campaign)
- Pour-over users get a different recommendation form with bloom + brew volume
- The migration at startup is critical for backward compat — no data loss

</specifics>

<deferred>
## Deferred Ideas

- Equipment comparison analytics (Phase 16+ scope)
- Per-method custom parameter ranges beyond defaults
- "Other" method custom parameter configuration

</deferred>

---

*Phase: 15-multi-method-brewing*
*Context gathered: 2026-02-23*
