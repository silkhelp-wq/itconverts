# Handoff: Karo Convert — universal converter, calculator, AI study helper & supporter system

## Overview
**Karo Convert** is a fast, free, mobile-first web app with four connected features:
1. **Universal unit converter** — a natural-language command bar ("100 km to miles") plus a converter card with custom dropdowns and live results across 18 measurement categories.
2. **Scientific + graphing calculator** — an original calculator (Calc + Graph tabs) opened in a modal from anywhere, or as a standalone page.
3. **AI Study Helper** — an educational-only Q&A box that returns factual answers with clean, ad-free sources.
4. **Supporter system** — a "Go ad-free" donate flow with one-tap social sign-in that removes ads and unlocks saved history.

This bundle is the chosen design direction ("Direction C — Bold"): a near-black warm canvas with a coral accent, `Space Grotesk` display type and `Inter Tight` body type.

---

## About the design files
**The files in this bundle are design references built in plain HTML/CSS/vanilla JS** — working prototypes that demonstrate the intended look, behavior, and logic. They are **not meant to be shipped as-is** into production.

Your task is to **recreate these designs in the target codebase's environment** (React, Vue, Svelte, SwiftUI, native, etc.), using its established patterns, component library, routing, and state management. If no codebase exists yet, choose an appropriate stack (e.g. Next.js + TypeScript) and implement there. The pure logic modules (`convert.js`, `mathcore.js`) can be ported almost verbatim; the UI should be rebuilt with the target system's components while matching the visuals documented below.

The prototype intentionally uses **front-end mocks** for things that require a backend (social sign-in, payments, the AI call, cross-device history). Replacing those mocks with real services is the main "implement the functionality" work — see **Production implementation tasks** at the end.

## Fidelity
**High-fidelity.** Colors, typography, spacing, radii, shadows, and interactions are final. Recreate the UI pixel-accurately using the codebase's libraries, then wire up real services.

---

## File map
| File | Type | Responsibility |
|---|---|---|
| `Karo Convert.html` | Main app (was `direction-bold.html`) | The whole site: header, command bar, converter card, AI study helper, browse pills, donate/account/history modals, reserved ad slot. Inline `<style>` + inline `<script>` (IIFE). |
| `calculator.html` | Standalone page | Scientific + graphing calculator. Loaded into a modal by `calc-modal.js`, or usable on its own. |
| `convert.js` | Logic (no deps) | `window.ITC` — all categories, `convert()`, `convertString()`, `format()`. Pure data + functions; port directly. |
| `mathcore.js` | Logic (no deps) | `window.MATH.evaluate(expr, {deg, vars, ans})` — safe recursive-descent expression parser (no `eval`). Used by the calculator. |
| `icons.js` | Logic (no deps) | `window.ITCICON(name)` → inline SVG string for category/line icons. |
| `supporter.js` | **MOCK — replace** | `window.ITC_USER` — identity, supporter status, and activity history, persisted to `localStorage`. This is the seam where real auth/payments/history go. |
| `calc-modal.js` | Shared widget | Injects the calculator modal (iframe → `calculator.html`); any `[data-open-calc]` element opens it. Listens for a `postMessage` from the calculator to grow the modal in Graph mode. |

Load order in `Karo Convert.html`: `convert.js` → `icons.js` → `supporter.js` → `calc-modal.js` → inline app script.
Load order in `calculator.html`: `mathcore.js` → `supporter.js` → inline calculator script.

---

## Design tokens

### Color — Dark (default)
| Token | Hex | Use |
|---|---|---|
| `--bg` | `#0c0b0a` | page base (a radial gradient from `--bg-2` to `--bg`) |
| `--bg-2` | `#15130f` | gradient top |
| `--surface` | `#1a1714` | cards, modals, inputs |
| `--surface-2` | `#221d18` | insets, segments, secondary fills |
| `--text` | `#f7f3ec` | primary text |
| `--muted` | `#a39a8c` | secondary text |
| `--faint` | `#6f675b` | tertiary/labels |
| `--border` | `#2a2520` | hairlines |
| `--border-2` | `#3a322a` | stronger borders / inputs |
| `--accent` | `#ff5c38` | primary coral (buttons, highlights, equals) |
| `--accent-2` | `#ff7a55` | accent gradient end / hover |
| `--accent-ink` | `#ffb59f` | accent text on dark |
| `--accent-soft` | `#2a160f` | accent-tinted fills (chips, selected, ad-free badge) |

### Color — Light
| Token | Hex |
|---|---|
| `--bg` `#f6f2ea` · `--bg-2` `#efe9dd` · `--surface` `#ffffff` · `--surface-2` `#f3ede2` |
| `--text` `#1a1611` · `--muted` `#6f6457` · `--faint` `#9a8d7c` |
| `--border` `#e6ddcf` · `--border-2` `#d8ccb9` |
| `--accent` `#e2421e` · `--accent-2` `#c4361a` · `--accent-ink` `#9c2c12` · `--accent-soft` `#fbe6df` |

Theme is toggled by setting `data-theme="light"|"dark"` on `<html>`; persisted in `localStorage` (`itc-theme-c` for the site, `itc-calc-theme` for the calculator). Default is dark. Respect `prefers-color-scheme` if you want (Direction A did; C defaults dark).

### Calculator-specific tokens (warm, same family)
`--device #1a1714` / `--device-2 #221d18` (body gradient), `--bezel #0c0b0a`, `--screen #15110b` (LCD), `--screen-line #2c2418` (grid), `--phos #ff7a55` (entry text + glow), `--phos-dim #9c8b78` (history/result), keys `--key #221d18`/`--key-2 #2a241e`, `--equals #ff5c38`. Graph curve uses `--accent`. Light theme mirrors these with light values.

### Typography
- **Display** (`--disp`): `Space Grotesk`, weights 400–700. Used for headings, the command bar, results, buttons, calculator screen + keys (with `font-variant-numeric: tabular-nums`).
- **Body** (`--sans`): `Inter Tight`, weights 400–600.
- Load via Google Fonts. Fall back to `ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`.
- Hero/lead: `clamp(25px, 3.6vw, 38px)`, weight 700, letter-spacing −0.03em. Command input: 56px tall, `clamp(16px,2vw,19px)`. Result number: `clamp(30px,5vw,52px)`.

### Spacing / radii / shadow
- Content column: `max-width: 660px`, side padding 22px.
- Radii: inputs/segments 12–14px, cards/modals 18–20px, pills 11–13px, avatar 50%.
- Card shadow: `0 10px 34px rgba(0,0,0,.16)`; modal shadow: `0 30px 80px rgba(0,0,0,.5)`; command bar: `0 6px 20px rgba(0,0,0,.12)`.
- Focus ring: `box-shadow: 0 0 0 4px var(--accent-soft)` + `border-color: var(--accent)`.

### Icons / assets
- No external images. All icons are inline SVG line icons from `icons.js` (`ITCICON('ruler'|'scale'|'thermometer'|...)`), plus small inline SVGs in markup (calculator glyph, checkmarks, chevrons, swap, send arrow).
- Provider buttons use **neutral monogram glyphs** (G / A / M circles), NOT official brand logos — when wiring real OAuth, swap these for each provider's official, brand-compliant sign-in button.
- The reserved ad container is class **`.promo-area` / `.promo-unit`** (deliberately NOT named "ad/ads/advert" — ad-blocker cosmetic filters collapse those class names and break layout). Keep a non-ad class name in production.

---

## Screens / views & components

### 1. Header (sticky top of `Karo Convert.html`)
- Left: **brand** "it**converts**" (the "it" in text color, "converts" in `--accent`), with a 30px rounded coral chip showing a "⇄" glyph; the chip rotates 180° on hover.
- Right cluster (flex, gap 10px): **Calculator** button (`.calcbtn`, accent-outlined pill, opens calculator modal via `data-open-calc`; a 3-pulse "nudge" animation on load), an **account control** (`#acctwrap`, see Supporter), and a **theme toggle** (`.tbtn`, sun/moon).
- ≤430px: button text labels hide, leaving icons.

### 2. Hero + command bar
- Kicker "JUST TYPE IT" (accent, uppercase, letter-spacing .16em).
- Lead "What do you want to **convert?**" ("convert?" in accent).
- **Command input** (`#cmd`): placeholder "100 km to miles"; a coral send button (`#ent`) inside on the right. Typing is debounced 160ms and parsed; Enter commits.
- Hint line (`#hint`) shows parse status / suggestions; `.err` modifier turns it accent-ink for errors.

### 3. Converter card (`#result`)
- Category pill (`#rpill`): icon + category name, accent-soft chip.
- **Edit row**: a `.seg` containing the value input (`#ev`, Space Grotesk 18px) + a **custom dropdown** (`#efrom`); a circular **swap** button (`#swap`, rotates 180° on click); a second `.seg` with the target **custom dropdown** (`#eto`).
- **Big result** (`#big`): the converted number with a smaller unit suffix (`.u`).
- Result bar: equation text (`#eq`) + **Copy** button (`#copy`, writes result to clipboard).
- **Custom dropdowns** (replacing native `<select>` because option lists can't be themed): a `.dd-btn` (label + chevron) toggles a `.dd-list` of `.dd-opt` rows; selected row uses `--accent-soft`/`--accent`; the list opens on click, closes on outside-click/Esc, scrolls the selected item into view, themed scrollbar. From-dropdown opens left-aligned, To-dropdown right-aligned.

### 4. AI Study Helper (`.ask`)
- Header: an "AI" coral chip + title "Study helper" + one-line description ("educational topics only").
- Input (`#askq`) + send button (`#asksend`).
- Output (`#askout`): loading spinner → either an **answer** (`.ans-text` paragraphs) + **"Clean sources"** list (`.src` link cards: site name in accent + title + ↗, open in new tab) + an AI disclaimer note; OR a **`.refusal`** card for non-educational questions.
- **Resets** (fades out + clears) when the input is emptied.

### 5. Browse pills (`#pills`)
- "OR BROWSE CONVERTERS" label + a flex-wrap of `.cpill` buttons (icon + category name) for all 18 categories.
- The pill matching the **currently active conversion** gets `.cpill.active` (coral). It updates whether the category changed via the command bar, a dropdown, a swap, or a pill click.

### 6. Reserved ad slot (`.promo-area` > `.promo-unit`)
- A slim 90px bordered container with a faint "ADVERTISEMENT" label top-left and placeholder text. Intentionally quiet/non-intrusive. **Hidden entirely (`display:none`) for supporters.**

### 7. Footer
- Copyright + About / Privacy / Contact links.

### 8. Calculator (`calculator.html`, shown in a modal)
- Device body (warm graphite gradient), a deck row: "GRAPHING CALC" label, **Calc / Graph** tab toggle, **DEG/RAD** badge (toggles angle mode for both calc and graphing).
- **Calc tab**: LCD screen with scrolling history (`#hist`), current entry (`#entry`, coral glow), live preview result (`#result`). A 5×7 keypad: `2nd` (toggles inverse trig / eˣ / 10ˣ / ∛), `π e ( )`, `sin cos tan xʸ √`, `ln log x² ! %`, digits, operators (`× ÷ + −`), `DEL`, `AC`, `(-)`, `ans`, `=`. Live-evaluates as you type; `=` commits to history.
- **Graph tab**: a `<canvas>` plot (grid, axes, labels), a `y =` input (`#yinput`), Plot / Zoom + / Zoom − / Reset tools, **plus the full keypad** — and the bottom `ans` key becomes a coral **`x`** key for typing the variable. Drag to pan, wheel to zoom. Pad keys insert into the `y=` field in Graph mode.
- The calculator posts `{type:'itc-calc-mode', mode}` to its parent; `calc-modal.js` grows the modal sheet in Graph mode (`min(96vh,896px)`) and shrinks back in Calc (`min(94vh,720px)`), with a height transition. Layout is height-fit (flex) with a `@media (max-height:560px)` compression so it never clips; falls back to scroll only on extreme short windows.

---

## Interactions & behavior (logic to replicate)

### Natural-language parsing (`Karo Convert.html` `parse()` + `resolve()`)
- Extracts the first number, splits the rest on `to` / `in` / `-`/`–`/`>`.
- `resolve(token)` matches a unit by id, symbol, or name-prefix across all categories, with an alias map (`lbs→lb`, `miles→mi`, `celsius→c`, `cups→cup`, etc.).
- If both sides resolve to the same category → set up that conversion; if different categories → friendly error; if only one resolves → open that category; else try category name; else error.

### Conversion engine (`convert.js`)
- Categories: length, mass, temperature, area, volume, speed, time, data (bytes/bits, SI + IEC), energy, power, pressure, fuel economy, angle, frequency, force, data rate, number base (bin/oct/dec/hex).
- Linear units carry a `factor` (value→base). Non-linear categories (temperature, fuel economy) carry `to`/`from` functions. Number base uses `parseInt`/`toString(radix)` via `convertString()`.
- `format()` trims trailing zeros, groups thousands, uses exponential outside `1e-6 … 1e15`.

### AI Study Helper (`runAsk()`)
- Calls `window.claude.complete({messages:[{role:'user', content: ASK_PROMPT + JSON.stringify(question)}]})`.
- `ASK_PROMPT` (in the file) instructs: answer ONLY educational/academic topics; refuse anything else (shopping, gossip, personal/medical/legal advice, opinions, NSFW, harmful) with a friendly redirect; ONLY factual info; recommend 2–4 reputable ad-free sources from an allowlist; output strict minified JSON `{educational, topic, answer, sources[], refusal}`.
- Client parses the JSON, and **`validSource()` independently filters** sources to an allowlist (`wikipedia.org, khanacademy.org, britannica.com, *.edu, *.gov, nasa.gov, noaa.gov, si.edu, bbc.co.uk, mit.edu`) — defense-in-depth so ad/commercial links can never render even if the model misbehaves.

### Supporter / account / history (`supporter.js` + `Karo Convert.html`)
- **`window.ITC_USER`**: `current()`, `isSupporter()`, `signIn(provider, {plan,name,email})`, `signOut()`, `log({t,label,detail})`, `history()`, `clearHistory()`, `subscribe(fn)`. State persists to `localStorage` (`itc-user`, `itc-history`) and syncs across tabs/iframes via the `storage` event.
- **Donate modal** (`#ov-support`): perks list, plan choice (**$1** or **Custom** with an amount field), then **Continue with Google / Apple / Microsoft** buttons that call `signIn` (the mock immediately marks the user a supporter).
- On sign-in: modal closes, `applyAds()` hides `.promo-area`, header swaps the "Go ad-free" button for an **avatar** with a menu (name, email, "Ad-free · $N donor" badge, **Your history**, **Sign out**).
- **History logging** (supporter-only, deduped): conversions (`commitConv()` on dropdown change / swap / pill / Enter / value `change`), calculator evaluations (logged from `calculator.html`), and answered study questions. Shown newest-first in `#ov-history` with type icons + relative timestamps; Clear history button.

### Misc
- Copy buttons use `navigator.clipboard` with a textarea fallback.
- Theme toggles persist per-surface in `localStorage`.
- Entrance animations use `animation-fill-mode: both` and animate transform only (never opacity to 0 as a resting state) so content is never left invisible if an animation doesn't run.

---

## Responsive behavior
- Mobile-first; the column is `max-width:660px`, fluid below.
- `@media (max-width:560px)`: command input shrinks to 54px.
- `@media (max-width:430px)`: header button text labels hide (icon-only).
- Custom dropdowns and modals are touch-friendly (≥44px targets).
- Calculator: fills its container height with a flexible keypad; `@media (max-height:560px)` compresses screen/keys; modal goes full-screen `<520px`.
- Verified with no horizontal overflow at 390px; works dark/light.

---

## State management (what to model in the target app)
- `theme`: 'light' | 'dark' (persisted).
- `user`: `{provider, name, email, supporter, plan, since}` | null (from auth/entitlement service).
- `history`: array of `{t:'convert'|'calc'|'study', label, detail, ts}` (server-synced for signed-in users; local cache otherwise).
- Converter: `{category, fromUnit, toUnit, value, result}`.
- Calculator: `{tab:'calc'|'graph', expr, ans, deg, second, hist[], graphWindow}`.
- AI helper: `{loading, lastQuestion, answer|refusal, sources[]}`.

---

## Production implementation tasks (the real functionality to build)
1. **Social sign-in (real):** Replace `ITC_USER.signIn` mock with Google Identity Services, Sign in with Apple, and MSAL (Microsoft). Verify the returned ID token **server-side**; create a session. Use each provider's official, brand-compliant button (replace the G/A/M monograms).
2. **Payments:** Replace the donate flow with Stripe Checkout (or PayPal). Support a **$1 preset and a custom amount**. On a verified payment **webhook**, mark the account as a supporter in your DB. **Never trust the client** for supporter status — gate ad-free + history on a server-validated entitlement.
3. **AI endpoint:** Replace `window.claude.complete` with your own server route that calls an LLM using the **same system prompt** (`ASK_PROMPT`) and returns the same JSON shape. Keep `validSource()` on the client as a safety net, and add server-side rate limiting (and a real free/supporter quota if desired — the design no longer advertises a study-answer limit, so default to generous/unlimited).
4. **History sync:** Persist history per user server-side; keep `localStorage` as an offline cache and reconcile on sign-in.
5. **Ads:** Integrate your ad network into `.promo-area` (keep the non-"ad" class name). Hide for supporters via the existing `applyAds()` logic.
6. **Currency (not yet built):** Add a `currency` category fed by live FX rates via a server proxy (don't hard-code rates in `convert.js`).
7. **Routing/SEO:** The chosen direction has no URL routing; add real routes/SSR if you need shareable links and indexable category pages (the engine + a route param is enough).
8. **Accessibility pass:** Add ARIA roles/labels to the custom dropdowns, modals (focus trap), and live regions for results; the prototype is keyboard-operable but production should be audited.

---

## Files in this bundle
- `Karo Convert.html` — main app (rename of the prototype `direction-bold.html`)
- `calculator.html` — calculator
- `convert.js`, `mathcore.js`, `icons.js` — portable logic
- `supporter.js` — mock identity/supporter/history (replace per task 1, 2, 4)
- `calc-modal.js` — calculator modal launcher
- `README.md` — this document

Open `Karo Convert.html` in a browser to interact with the full prototype. The AI Study Helper only responds inside the original preview environment (it relies on a built-in `window.claude` helper); in your build, point it at your own AI endpoint.
