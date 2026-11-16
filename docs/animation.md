# Optional Syntyr animation library

`syntyr.animate.mjs` is an **opt-in, dependency-free ES module** for
application-triggered motion. It delegates timing and compositing to the native
**Web Animations API** and viewport detection to **IntersectionObserver**.
There are no imports, startup side effects, global listeners, background timers,
framework adapters, CSS resets, or changes to core Syntyr.

Use the CSS-only `syntyr.motion.css` for static declarative effects. Load this
JavaScript module only when you actually need to trigger animations in code or
observe viewport entry; either add-on can be used without the other.

## Install and invoke

Copy `dist/syntyr.animate.mjs` and, if desired, `dist/syntyr.core.css` to
your own static directory. The module needs no bundler and runs in evergreen
browsers that support ES modules.

```html
<link rel="stylesheet" href="/css/syntyr.core.css">
<main class="syn-root">
  <button id="show" type="button">Animate card</button>
  <article id="card">Card content stays visible without JavaScript.</article>
</main>
<script type="module" src="/js/animation-demo.mjs"></script>
```

```js
// /js/animation-demo.mjs
import { animate, stagger, observeReveals } from '/js/syntyr.animate.mjs';

document.querySelector('#show')?.addEventListener('click', () => {
  const card = document.querySelector('#card');
  animate(card, 'enter', { direction: 'up', duration: 280 });
});

stagger(document.querySelectorAll('.syn-root .card'), 'fade', {
  interval: 75, delay: 0,
});

// This does nothing until invoked, and only animates opted-in descendants.
const disconnect = observeReveals(document);
// Call disconnect() when unmounting the page/region.
```

When the experimental `@syntyr/css` npm package is published, the module
also has a dedicated typed subpath:

```js
import { animate } from '@syntyr/css/animate';
```

That subpath exposes only the optional animation code and matching TypeScript
declarations. The default package import remains the CSS entrypoint.

## Minimal API

| Export | Purpose | Result |
| --- | --- | --- |
| `animate(element, preset = 'enter', options?)` | Animate one element on demand | Native `Animation` or `null` |
| `stagger(iterable, preset = 'enter', options?)` | Animate each element with an incremental WAAPI delay | Array of animations or `null` entries |
| `observeReveals(root = document)` | Observe `.syn-root [data-syn-reveal]` once per element | `disconnect()` cleanup function |

Presets are `fade` (opacity), `enter` (opacity plus individual `translate`),
and `scale` (opacity plus individual `scale`). There is no infinite or
autoplay animation preset. `enter` supports `direction: 'up' | 'down' |
'left' | 'right'` and `distance: '.75rem'`. Use `scaleFrom` to override the
initial scale.

All presets accept `duration` and `delay` in milliseconds and `easing`
as a CSS timing function. `stagger` additionally accepts `interval` in
milliseconds. The module reads existing CSS custom properties when options
are omitted: `--syn-motion-duration` (220ms default),
`--syn-motion-stagger` (65ms), `--syn-motion-distance` (.75rem),
`--syn-motion-scale-from` (.96), and `--syn-ease-out`
(`cubic-bezier(.22, 1, .36, 1)`). These defaults also work without a Syntyr
stylesheet, and per-element CSS tokens can override them.

Unknown presets and invalid directions throw `TypeError`; missing target,
missing Web Animations API, or a reduced-motion preference return `null`
without modifying the DOM. Prefer `animation?.cancel()` for interruption and
`animation?.finished` when coordinating an actual transition (cancellation
rejects its promise). Animation properties are released at the end rather
than persisting a hidden or transformed element.

## Viewport reveals

```html
<section class="syn-root">
  <h2>Visible with CSS alone</h2>
  <p data-syn-reveal="enter">Animate on first viewport entry.</p>
  <p data-syn-reveal="fade">Fade when first seen.</p>
</section>
```

```js
import { observeReveals } from '/js/syntyr.animate.mjs';
const disconnect = observeReveals(document);
```

No `IntersectionObserver` is created automatically; call `observeReveals`
after rendering the relevant HTML fragment. It observes only descendants of
`.syn-root` with a `data-syn-reveal` attribute, runs each animation once,
and does **not** add `opacity: 0` to page content before JavaScript starts.
A region can be re-scanned after HTMX/Datastar/React renders new nodes.
The root argument limits the query, and the return function disconnects it.
There is no `MutationObserver` or automatic event interception.

## Accessibility and performance

- `prefers-reduced-motion: reduce` takes precedence over all presets and
  custom durations. Reduced-motion users always get visible, immediate content;
  if that preference changes while observing, animation is checked again.
- Content is never hidden while waiting for JavaScript, scroll observation,
  or native feature detection. Effects do not replace semantic HTML, focus
  management, ARIA announcements, or actual state-change notifications.
- Keyframes use composited `opacity`, `translate`, and `scale` rather than
  layout dimensions. Avoid animating essential text and high-density data,
  where fading can temporarily reduce readability. An element with custom
  individual transform properties may need a wrapper for composition.
- The module uses one-shot `fill: 'none'` and `iterations: 1`, so focus and
  disabled states cannot remain overridden by a completed animation.
- For layout changes, prefer native View Transitions where available. For
  interactive scrubbing and complex timelines, use a specialized animation
  engine *outside* Syntyr instead of expanding this low-level module.

## Verification

```sh
node --test tests/animate.test.mjs
python3 scripts/build.py --check
python3 -m unittest discover -s tests -v
```

Node is for the optional JavaScript behavior tests, **not** for building
Syntyr or using the CSS library. The production JS is copied byte-for-byte
by Syntyr's existing Python build, allowing deterministic release checks.
