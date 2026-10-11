# Destill — Sculpted Light

> **DESIGN PROPOSAL — PRODUCT OWNER REVIEW REQUIRED.**
> This is a self-review by the design agent. It is not an approval, and it is not a statement of accessibility compliance.

A local-first HTML prototype of the Destill editing companion. It is self-contained: no build step, no npm dependencies, no remote fonts, no remote scripts.

| File | Purpose |
|---|---|
| `index.html` | Semantic markup for all eight application states plus the review footer |
| `styles.css` | Centralised design tokens (`:root`), material recipes, components, responsive rules, motion and forced-colours fallbacks |
| `app.js` | State machine, real browser-local file handling, synthetic demo content, review tooling |
| `screenshots/` | Real headless-Chromium renders (see *Capture method*) |

## Run it

```bash
cd design/destill
python3 -m http.server 8080      # then open http://localhost:8080/index.html
```

Deep links: `#welcome #source #blocked #processing #understanding #refine #result #error #cancelled #decision`.

---

## 1. Design rationale

Destill is a *reading* tool before it is a *cutting* tool, so the interface is organised around one question at a time: **what does this clip say, and what is the evidence?** The sculpted material carries the hierarchy rather than decoration:

- **Recessed** surfaces are where the user's *source* sits: the video well, the intent field, the timeline track, the segmented tracks. Pressing into the material is the physical metaphor for "content goes in here".
- **Raised** objects are things you *act on*: the single primary action, secondary buttons, medallions, source-time chips, the thumb of a slider.
- **Flat** planes hold reading content (message, rationale, evidence groups) so the sculpted objects have room to breathe.
- The **Analyze** steps (Source → Analyze → Refine) are grouped in one track; **Destill** (rendering) is a separate, locked track labelled *later*. The two capabilities are never mixed in one control.

Truthfulness is structural. Real file metadata comes from the browser's media decoder; every timestamp, claim and prompt comes from a clearly labelled synthetic object (`DEMO` in `app.js`). Analysis of a real file is blocked with the actual reasons, and no result is faked for it.

## 2. Composition and user-flow logic

```
Welcome ──choose file──▶ Source ──Analyze──▶ Blocked (no service, consent shown)
   │                       │                    │
   └──synthetic demo──▶ Demo running ◀─────────┘ (Run synthetic demo instead)
                           │   └─Cancel─▶ Cancelled
                           ▼
                      Understanding ──Decide 2:10──▶ Needs decision ──Apply──▶ Refine
                           │                                                  │
                           └──────────────── Review cuts ──────────────────────┘
                                                                              ▼
                                                        Result concept (no MP4, English prompt)

Decode failure of a real file ──▶ Error (browser's own MediaError reported)
```

Layout: a single **shell** (32 px) holds a top bar (brand · workflow tracks · source-mode pill), one **stage** per state, and a footer with the design-proposal label and the review-state map. Desktop uses a two-column split (well on the left, intent or content on the right); tablet and phone stack the same content in the same order.

## 3. Design tokens (exact values from `styles.css`)

### 3.1 Colour

| Token | Value | Use |
|---|---|---|
| `--pearl` | `#EEF1F6` | page, flat planes |
| `--porcelain` | `#F8FAFC` | highlight end of convex gradient |
| `--surface` | `#F2F5F9` | shell and raised surface |
| `--recess` | `#E8EDF3` | recessed surface |
| `--ink` | `#151922` | primary text (≈16:1 on surface, hand-calculated) |
| `--ink-2` | `#4D5566` | secondary text (≈6.8:1 on surface, hand-calculated) |
| `--ink-3` | `#5E6679` | tertiary text (≈5.3:1 on surface, ≈4.9:1 on recess, hand-calculated) |
| `--accent` | `#3559CB` | primary action, selected state (≈5.6:1 on surface, hand-calculated) |
| `--accent-ink` | `#2A47A8` | accent text on `--accent-soft` (≈6.9:1, hand-calculated) |
| `--accent-soft` | `#E6ECFF` | selected chip / switch track |
| `--warn` `#7A4E00` · `--ok` `#2B6248` · `--danger` `#8F2F2F` | semantic only (blocked, conflict, available) |

Semantic status is never conveyed by colour alone: every status also has a text label (*Not connected*, *Conflicting*, *Decision needed*) and a distinct physical state (recessed vs raised).

### 3.2 Shape

| Token | Value | Use |
|---|---|---|
| `--r-shell` | 32 px | workspace shell |
| `--r-card` | 28 px | primary cards, plane containers |
| `--r-well` | 24 px | recessed wells, notices, dropzone |
| `--r-row` | 22 px | rows, evidence cards, choices |
| `--r-control` | 18 px | buttons |
| `--r-field` | 16 px | text fields, media inside wells (24 − 8 bezel = 16, concentric) |
| `--r-chip` | 12 px | chips, review buttons |
| `--r-pill` | 999 px | switches, slider tracks, status pill, medallions |

Concentric pairs: shell 32 → well 24 (inside an 8 px bezel) → media 16. Segmented tracks are 18 px with 14 px segments (4 px inset).

### 3.3 Compound shadows (light source: upper-left)

| Token | Value | Use |
|---|---|---|
| `--shadow-dark` | `7px 8px 17px rgba(154,168,188,.25)` | raised ambient |
| `--shadow-light` | `-7px -7px 17px rgba(255,255,255,.93)` | raised counter-light |
| `--shadow-gleam` | `inset 0 1px 0 rgba(255,255,255,.9)` | upper rim highlight |
| `--shadow-raised` | dark + light + gleam | default button |
| `--shadow-inset` | `inset 4px 4px 9px rgba(154,168,188,.34), inset -4px -4px 9px rgba(255,255,255,.9)` | wells, notices |
| `--shadow-inset-s` | `inset 3px 3px 7px rgba(154,168,188,.32), inset -3px -3px 7px rgba(255,255,255,.9)` | inputs, tracks |
| `--shadow-pressed` | `inset 3px 3px 7px rgba(154,168,188,.30), inset -3px -3px 7px rgba(255,255,255,.85)` | pressed raised control |
| `--shadow-small` | `3px 4px 9px rgba(154,168,188,.30), -3px -3px 9px rgba(255,255,255,.92), inset 0 1px 0 rgba(255,255,255,.8)` | medallions, chips, time chips |
| `--shadow-small-inset` | `inset 2px 2px 5px rgba(154,168,188,.32), inset -2px -2px 5px rgba(255,255,255,.9)` | recessed small items, active segment track |
| `--shadow-card` | `6px 7px 16px rgba(154,168,188,.22), -6px -6px 14px rgba(255,255,255,.9), inset 0 1px 0 rgba(255,255,255,.9)` | primary raised cards |
| `--shadow-shell` | `10px 12px 26px rgba(154,168,188,.20), -10px -10px 24px rgba(255,255,255,.85), inset 0 1px 0 rgba(255,255,255,.9)` | shell |
| Primary button | `6px 8px 16px rgba(53,89,203,.26)`, `-5px -5px 12px rgba(255,255,255,.9)`, top gleam | the one dominant action |

Shadow intensity is reduced on dense components (rows, chips, the review footer) and on small controls, as the brief asked.

### 3.4 Gradients

- `--grad-raised`: `linear-gradient(145deg, #F8FAFC 0%, #F2F5F9 46%, #E9EDF4 100%)` — convex: light top-left, darker bottom-right.
- `--grad-recess`: `linear-gradient(145deg, #E3E9F0 0%, #E8EDF3 46%, #EEF2F7 100%)` — concave: the reverse.
- `--grad-primary`: `linear-gradient(160deg, #4468D8 0%, #3559CB 58%, #2D4BB5 100%)`.

### 3.5 Type

Stack: `-apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Segoe UI", "Helvetica Neue", Arial, sans-serif`. No web font is loaded. **Note:** the sandbox used for these renders has no SF Pro, so screenshots show the fallback face. Real SF Pro will differ in metrics.

| Role | Size | Weight | Tracking |
|---|---|---|---|
| Display (welcome) | `clamp(34px, 4.4vw, 44px)` | 640 | −0.03em |
| Screen heading | 26 px (24 px on phone) | 620 | −0.02em |
| Section heading | 18 px | 620 | −0.01em |
| Lede | 17 px (16 px phone) | 400 | 0 |
| Body | 15 px | 400 | −0.005em, line-height 1.55 |
| Label / small | 13 px | 600 | 0 |
| Caption / eyebrow | 12 px | 600 (eyebrow uppercase, +0.08em) | — |

Timestamps and counters use `font-variant-numeric: tabular-nums`.

### 3.6 Motion and focus

- Transitions: 0.18–0.22 s on shadow/background; the switch knob uses `cubic-bezier(.2,.7,.3,1)`.
- Progress sweep and status pulse are infinite animations, both disabled under `prefers-reduced-motion`.
- Focus: `2px solid #3559CB`, `outline-offset: 3px`. Programmatically focused headings suppress the ring.

## 4. Signature components — dimensions and states

| Component | Geometry | Elevation | States |
|---|---|---|---|
| Workspace shell | radius 32, padding 28/36/24 | `--shadow-shell` | — |
| Recessed source well | radius 24, 8 px bezel, aspect 4:3 (16:10 phone), media radius 16 | `--shadow-inset` | empty · preparing · still frame · live video · synthetic clip |
| Raised primary | min-height 48, padding 0 22, radius 18 | cobalt raised | default · hover (lighter) · pressed (inset) · focus (ring) · disabled (recessed, `#7D8598` text) |
| Subtle secondary | min-height 44, text-only | none; recess on hover | default · hover · pressed · disabled |
| Default (secondary) | min-height 48, radius 18 | `--shadow-raised` | default · hover · pressed · disabled · focus |
| Circular medallion | 44 (sm 36, lg 72) | `--shadow-small` | default · pressed · disabled · semantic colour |
| Segmented track | 4 px inset, radius 18; segment 36 high, radius 14 | recessed track; selected segment raised | selected · unselected · hover · focus · disabled (arrow keys, roving tabindex) |
| Text field | min-height 48, radius 16, padding 14/16 | `--shadow-inset-s` | default · focus (ring) · readonly |
| Timeline + sculpted thumb | track 10 px, thumb 24 px raised with 1 px inner rim | recessed track, raised thumb | default · active (thumb inset) · focus ring |
| Source-time chip | height 28, radius 12, tabular digits | `--shadow-small`; active = recessed + accent | default · hover · pressed · current |
| Evidence card | radius 22, padding 16/16/14 | `--shadow-small`; conflict = recessed | default · conflict |
| Feedback control | height 28, radius 12 | `--shadow-small`; pressed = recessed accent | off · on (aria-pressed) · focus |
| Processing indicator | 10 px recessed bar; stage medallions raised (done), accent (active), recessed (queued) | — | queued · active · done · reduced-motion static |
| Blocked / error notice | radius 24, recessed, semantic medallion | `--shadow-inset-s` | blocked · error · honest-no-render |
| Switch | 52×30, knob 24 | recessed track; knob raised | off · on · focus |
| Decision row | radius 22, flat plane | — | open (raised, "Decision needed") · decided |

## 5. States inventory

| # | State | Type | How reached | Notes |
|---|---|---|---|---|
| 1 | Welcome / empty | **Functional** | default | real file chooser and drag-and-drop; "Try the synthetic demo" |
| 2 | Source selected | **Functional (real file)** | choose a video | real name, size, type, frame size; duration from the browser; still frame; live preview with play/scrub |
| 3 | Blocked | **Functional, truthfully blocked** | Analyze with a real file | consent switch works; service is *Not connected*; Analyze stays disabled; demo is offered |
| 4 | Demo processing | **Synthetic** | demo, or review map | scripted five steps, no percentages, Cancel available |
| 5 | Understanding | **Synthetic** | after the demo | message, story structure, timeline, 8 time-linked evidence cards, feedback, near-playhead filter |
| 6 | Refine | **Synthetic** | after understanding | KEEP / CHANGE / DROP per segment, trim ±2 s, live projected duration against the 90 s target, open-decision count |
| 7 | Result concept | **Synthetic + blocked** | after refine | "No MP4 rendered"; render button disabled; English CapCut EditPilot prompt (copyable); rationale |
| 8a | Error | **Functional** (real decode failure) or example | real unreadable file, or review map | shows the browser's MediaError reason |
| 8b | Cancelled | **Functional** | Cancel during demo | nothing kept, nothing sent |
| 8c | Needs editor decision | **Functional** | "Decide 2:10" from understanding or refine | three choices; apply is refused until one is chosen |

Blocked in this build: analysis of any real file, MP4 rendering, any cut or export, any upload. Each is shown as blocked or labelled.

## 6. QA report

Status key: **PASS** (verified by a run in this session), **FAIL** (a defect was found and is recorded in the ledger; it is not failing now), **NOT_TESTED** (not run; the reason is given).

| ID | Check | Status | Evidence |
|---|---|---|---|
| QA-01 | Page loads with no console errors or page errors | PASS | Headless Chromium 131 run through every state; `CONSOLE ERRORS: []` |
| QA-02 | Horizontal overflow | PASS (partial coverage) | `scrollWidth ≤ clientWidth`: all eight screens at 1440; refine at 1280; understanding, refine and decision at 390; understanding and welcome at 320 |
| QA-03 | Real file path: pick, metadata, preview, still frame | PASS | Generated WebM via MediaRecorder; name, size, type, frame `320 × 180` read; duration `Unknown` (WebM from MediaRecorder carries no duration; shown honestly) |
| QA-04 | Analyze with a real file is blocked with truthful reasons | PASS | `aria-disabled="true"`; reason text updates on click; consent toggles without enabling analysis |
| QA-05 | Demo path runs, shows synthetic labels, and completes | PASS | processing → understanding; "Synthetic demo" chips and pill text present |
| QA-06 | Cancel during demo produces Cancelled, not a result | PASS | screen `outcome`; state reset to file-or-none |
| QA-07 | Timeline: story-row seek, playhead readout, near-playhead filter | PASS | story click → `1:46 of 3:42`; near filter → 2 cards at playhead |
| QA-08 | Refine: decisions update projected duration | PASS | KEEP on s2: `1:22 → 1:34` |
| QA-09 | Needs-decision: apply refused without choice; applied choice closes the open count | PASS | `Choose one option first…` shown; after apply, open count `0` |
| QA-10 | Result: copy to clipboard | PASS (headless) | status `Prompt copied.` in headless Chromium; not verified in a real browser profile |
| QA-11 | Keyboard: arrow keys move and select inside a radiogroup | PASS | ArrowRight moves KEEP → CHANGE, aria-checked updated |
| QA-12 | Depth-off (flatness) test | PASS (visual) | `d-11-flat-check.png`: outlines and selected states still distinguish controls |
| QA-13 | Visual review of the rendered material (convex / concave / pressed separation, light direction) | PASS (visual, by the agent) | reviewed desktop and phone renders; corrected issues listed in the ledger |
| QA-14 | Contrast of text and interactive elements | NOT_TESTED (partly hand-calculated) | ratios listed in §3.1 come from sRGB luminance by hand, not from a measurement tool. No axe or Lighthouse run. |
| QA-15 | Full keyboard-only walkthrough of every state | NOT_TESTED | only the radiogroup arrow path was exercised |
| QA-16 | Focus visibility in each state | NOT_TESTED | the focus style is defined in CSS; not captured per state |
| QA-17 | 200% text zoom and reflow | NOT_TESTED | not run |
| QA-18 | Reduced-motion behaviour | NOT_TESTED | CSS rule exists; not run with the emulation flag |
| QA-19 | Forced-colours / high-contrast mode | NOT_TESTED | CSS fallback exists; not run |
| QA-20 | Touch-target size (≥ 44 px) | NOT_TESTED | most controls are ≥ 44 px by CSS; the segment controls and review buttons are 30–36 px and are not measured |
| QA-21 | Screen reader announcements | NOT_TESTED | no assistive technology was run |
| QA-22 | Real SF Pro rendering | NOT_TESTED | the sandbox has no SF Pro; fallback face was used |
| QA-23 | Figma artefact | NOT_TESTED / unavailable | no Figma connector is available in this session; see §8 |
| QA-24 | Safari / Firefox rendering | NOT_TESTED | only Chromium 131 (headless) was used. `:has()` and the range-track styling need checking in other engines. |
| QA-25 | Repository hygiene suite (`tests/repo`) | PASS | `44 passed` after adding this directory |

Known defects still open:

- Forced-colours mode and focus rings were not exercised in a browser (see QA-16, QA-19).
- The mobile welcome and the 320 px welcome were captured but not visually reviewed in this session.
- The "Looks right / Not right" feedback is session-local and does not persist. This is intentional.

## 7. Product Change Ledger (proposed)

The repository had no earlier Destill design, so BEFORE means the first draft produced during this session. Each row was verified in a render or a run.

| # | Change | BEFORE | AFTER | OUTCOME | Type |
|---|---|---|---|---|---|
| L1 | Title-focus ring | Programmatic focus on screen headings drew a blue box around the title | Suppressed on `h1/h2[tabindex=-1]` | Clean headline | CHANGE |
| L2 | Synthetic-clip chip | Chip stretched across the whole well | `align-items: flex-start`; caption row full width | Chip reads as a tag | CHANGE |
| L3 | Refine spacing | Segment list touched the screen heading | Heading margin 12 px; list offset 8 px | Clear hierarchy | CHANGE |
| L4 | List indentation | Browser default padding indented rationale and story lists | `ul, ol { padding: 0 }` | Lists align to their plane | CHANGE |
| L5 | Phone decision notice | Text column collapsed to a few characters wide | Notice wraps; text takes 220 px basis; action full width | Readable on 390 and 320 | CHANGE |
| L6 | Duplicated editor note | "Editor note: Editor kept…" | Note text only | Copy is correct | CHANGE |
| L7 | Story-row grid | Three-column grid with two children | Two-column grid | Row aligns | CHANGE |
| L8 | Dropzone, pulse and segment-decision styles | Referenced classes with no rules | Rules added | Welcome dropzone renders as designed; pulse and decision styles exercised in the run | ADD |
| L9 | Well media logic | Poster could overlap live video; empty text contradicted state | Source well shows live video; other wells show still frame; empty copy follows state | Correct media per state | CHANGE |
| L10 | Source-time chips | Static decoration in refine | Chips jump to the source timeline | Source-time navigation works from every evidence view | ADD |
| L11 | Demo cut arithmetic | — | Projected duration recomputed from decisions and trims | Visible consequence of each decision | ADD |
| L12 | Flatness control | — | "Shadows on / off" switch in the footer | Reviewers can test flat usability | ADD |
| L13 | Analysis of real files | — | Blocked with the actual reasons; no fabricated result | Truthful | PRESERVE |
| L14 | Design-proposal label | — | Footer on every screen | Not self-approved | PRESERVE |
| L15 | Destill vs Analyze separation | — | Separate tracks; Destill locked "later" | Clear capability boundary | PRESERVE |
| L16 | Heavy borders and dashboard cards | Not present in any draft | Not used | Material language kept | REMOVE (not introduced) |

## 8. Figma

Not delivered. No Figma connector is available in this session, so no editable Figma file, variables, auto-layout components or prototype links were produced. The HTML prototype is the only artefact. The material-detail close-ups (source well, primary button, segmented control, slider) are **not** provided as separate enlarged renders. Crop-level inspection was not done beyond the full-screen renders.

## 9. Synthetic and production boundaries

- `DEMO` in `app.js` holds all invented content. It is labelled synthetic in the UI and in the prompt header.
- No network request is made by the prototype. The only file access is the file the user chooses, read in the browser.
- The "analysis service" is `Not connected` by design in this build. No backend exists, so none is mocked.
- The CapCut EditPilot prompt is a draft for the user to paste. The prototype does not send it anywhere, and it is not generated from the user's footage.
- The repository's public-data rules were followed: no email addresses, secrets, or private paths appear in these files.

## Capture method

Screenshots were taken with headless Chromium 131 (via `@sparticuz/chromium` and `puppeteer-core`, run outside the repository). The test clip was generated in the browser with MediaRecorder and not committed. Viewports: 1440×900, 1280×800, 390×844 (mobile, device emulation) and 320 px wide.
