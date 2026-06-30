# Element-card CSS scheme (oriental-destiny.com)

When writing articles that break out individual five-element sections (Wood, Fire, Earth, Metal, Water), use a `.element-card` class with per-element left-border colors. The scheme below matches the seo-generator's `ELEMENT_THEMES` constant and reads as visually consistent with the site's other element-themed pages (day-master series, zodiac series).

## CSS

```css
.element-card { border: 1px solid var(--line); border-left: 4px solid var(--pine);
                padding: 22px 24px; margin: 22px 0;
                border-radius: 0 8px 8px 0;
                background: rgba(255, 252, 246, 0.55); }
.element-card.wood  { border-left-color: #3a7d34; }
.element-card.fire  { border-left-color: #a63a2c; }
.element-card.earth { border-left-color: #b78a42; }
.element-card.metal { border-left-color: #8a8aa0; }
.element-card.water { border-left-color: #2a5a8c; }
```

The colors are desaturated to match the site's `--paper` background. Saturated primary-element colors (e.g. pure `#ff0000` for Fire) look out of place against the cinnabar/pine/gold palette — use the desaturated versions above.

## Markup

```html
<div class="element-card wood">
  <span class="tag">Wood</span>
  <h3>Wood: vertical lines, green and teal, growth and upward motion</h3>
  <p>Body text...</p>
  <div class="note"><strong>How to spot excess Wood:</strong> ...</div>
</div>
```

The `.tag` (uppercase, cinnabar, small) and `.note` (rounded green-grey background) sub-elements are reused from the `.mistake-card` pattern in the existing 06-27 article template, so the visual rhythm stays consistent across content types.

## When to use

- Articles that walk through 3+ elements individually (e.g. a "what each element looks like in a room" article)
- Articles comparing the elements side by side
- Articles with element-specific cure cards (e.g. "5 cures by element")

For articles that mention elements in passing, use the prose-level cues (color word, material word) and skip the card class — pulling the card class out for one or two elements reads as visual noise.

## Source

Verified by reverse-engineering `/home/ubuntu/oriental-destiny/seo-generator/generate.js` (the `ELEMENT_THEMES` constant, lines 18-44) and cross-checking against the published day-master pages (jia-day-master.html uses the Wood theme, bing-day-master.html uses Fire, etc.) on 2026-06-28.
