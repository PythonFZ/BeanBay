# Phase 4: Shot History & Feedback Depth - Context

**Gathered:** 2026-02-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Users can review their brewing history for any bean and optionally capture richer feedback — flavor dimension ratings, free-text notes, and flavor descriptor tags — for shots they want to analyze more deeply. The quick taste-score flow must not be disrupted; all additional feedback is optional and expandable.

Creating shots and the core rating flow are Phase 3 (complete). Visualizations, charts, and optimizer insights are Phase 5.

</domain>

<decisions>
## Implementation Decisions

### Shot History List

- Single global "Brew History" view (not a separate per-bean view)
- Bean detail page links into Brew History with that bean's filter pre-applied
- Each row in the collapsed list shows: datetime brewed, taste score, grind setting, failed shot indicator, notes indicator (icon if notes exist)
- List is scrollable (no pagination)
- Tapping a shot row opens a floating modal for detail/edit

### Filtering

- Filter UI: collapsed behind a "Filter" button on mobile; always-open side panel on wider/web viewports
- Filter options: by bean (single bean selection) and by minimum taste score threshold (e.g., "show shots ≥ 7")
- Bean filter pre-populated when navigating from a bean's detail page

### Notes

- Notes field appears at shot submission time: collapsed/expandable below the taste score — optional, never blocks the quick flow
- Retroactive note editing: tap shot row → floating modal with an edit button → opens edit view within or over the modal
- Notes are free-text

### Flavor Dimensions (6 sliders)

- 6 dimensions: acidity, sweetness, body, bitterness, aroma, intensity
- Scale: 1–5
- Input: sliders
- Panel is collapsed by default during shot rating — user must expand it
- Editable from history too (same expandable panel in the shot detail/edit modal)

### Flavor Descriptor Tags

- Up to 10 flavor tags per shot
- Input: type-to-search with predefined suggestions; user can also enter free-text tags not in the list
- Predefined list to be populated during implementation (common coffee flavor descriptors)
- Also accessible from history edit modal (not just at submission time)

### Shot Data Stored

- All existing fields (recipe parameters, taste score, extraction time, is_failed)
- Datetime of the brew (already stored as timestamp — must be surfaced in UI)
- Free-text notes
- Flavor dimension ratings (6 × 1–5 values, nullable)
- Flavor descriptor tags (up to 10, stored as list/array)

### OpenCode's Discretion

- Exact predefined flavor tag list (standard specialty coffee descriptors)
- Modal design and animation
- Slider visual style
- How the filter side panel transitions between mobile/web layouts
- Notes indicator icon choice
- Whether flavor dimensions and flavor tags share one expandable panel or are separate sections

</decisions>

<specifics>
## Specific Ideas

- "Once a bean is selected there could be a history for that bean that if clicked goes to the Brew History and applies the filter for that specific bean" — navigation pattern: bean detail → pre-filtered history view
- Flavor notes inspiration: up to 10 tags per shot, type-to-search with suggestions (similar in spirit to the WOW wheel from mystery.coffee — see Deferred Ideas)
- Mobile-first as established in Phase 2: 48px+ touch targets, 375px primary width, dark espresso theme

</specifics>

<deferred>
## Deferred Ideas

- **Interactive WOW flavor wheel (mystery.coffee)** — Render the full WOW wheel as a clickable UI where users tap categories and specific flavor notes. This is a distinct UI feature worth its own phase or plan. The Phase 4 tag input captures the same data more simply; the wheel can be layered on top later without a data model change.
- **Shot editing beyond notes/flavor** — Ability to correct recipe parameters or taste score retroactively was not discussed; not in scope for Phase 4.

</deferred>

---

*Phase: 04-shot-history-feedback-depth*
*Context gathered: 2026-02-22*
