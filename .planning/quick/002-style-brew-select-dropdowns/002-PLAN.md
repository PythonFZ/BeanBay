---
phase: quick-002
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - app/templates/brew/index.html
  - app/static/css/main.css
autonomous: true

must_haves:
  truths:
    - "Brew page setup/bean dropdowns use the same dark espresso styling as all other form inputs"
    - "Select dropdowns have custom arrow indicator matching the theme"
    - "Dropdowns are touch-friendly (48px min-height) on mobile"
  artifacts:
    - path: "app/templates/brew/index.html"
      provides: "Corrected CSS class on select elements"
    - path: "app/static/css/main.css"
      provides: "Select-specific styling for dark theme"
  key_links:
    - from: "app/templates/brew/index.html"
      to: "app/static/css/main.css"
      via: "form-input class"
      pattern: "class=\"form-input\""
---

<objective>
Fix brew page setup/bean select dropdowns that render as generic grey browser-default, making them match the app's dark espresso theme.

Purpose: The selects use undefined `form-control` class instead of `form-input`, and lack select-specific styling (appearance reset, custom arrow, option styling).
Output: Themed dropdowns consistent with the rest of the app.
</objective>

<tasks>

<task type="auto">
  <name>Task 1: Fix select class and add select-specific CSS</name>
  <files>app/templates/brew/index.html, app/static/css/main.css</files>
  <action>
  1. In brew/index.html: Change both `class="form-control"` to `class="form-input"` on the setup_id and bean_id selects.
  2. In main.css: Add select-specific styling after the `.form-input` rules to handle:
     - Reset `-webkit-appearance: none` / `appearance: none`
     - Custom dropdown arrow using SVG data URL (in theme-appropriate color)
     - `padding-right` for arrow space
     - `option` background/color to match dark theme (for dropdown menu itself)
     - `cursor: pointer` on selects
  </action>
  <verify>Visual inspection — selects should show dark background, light text, accent-colored focus border, custom arrow</verify>
  <done>Both select dropdowns on brew page use form-input class and render with dark espresso theme styling matching all other inputs</done>
</task>

</tasks>

<success_criteria>
- Select dropdowns have dark background (--bg-input), light text (--text-primary), themed border
- Custom dropdown arrow visible (not browser default)
- Focus state shows accent border
- Dropdown option list has dark background (not white)
- Touch-friendly size maintained
</success_criteria>
