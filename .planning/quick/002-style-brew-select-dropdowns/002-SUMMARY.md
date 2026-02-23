---
phase: quick-002
plan: 01
status: complete
date: 2026-02-23

changes:
  - file: app/templates/brew/index.html
    action: "Changed both select elements from undefined `form-control` class to `form-input`"
  - file: app/static/css/main.css
    action: "Added select-specific styling: appearance reset, custom SVG dropdown arrow in theme color, dark option menu background"

tests: 240/240 passing
---

## Summary

Fixed brew page setup/bean select dropdowns that rendered as generic grey browser-default elements. The selects used an undefined `form-control` CSS class instead of the existing `form-input` class.

### Changes

1. **Template fix** — Switched both `<select>` elements on the brew page to use `form-input` class, giving them the dark background (`--bg-input`), light text (`--text-primary`), and accent focus border already defined for all form inputs.

2. **Select-specific CSS** — Added `select.form-input` rules:
   - `appearance: none` to remove browser-default grey chrome
   - Custom SVG chevron arrow in `--text-secondary` color (#b0a090)
   - Proper padding-right for arrow spacing
   - Dark `option` element styling (`--bg-card` background, `--text-primary` text) so the dropdown menu itself matches the theme

### Result

The setup and bean dropdowns now match the dark espresso theme used throughout BeanBay — consistent with selects already used on the beans, history filter, and detail pages.
