/* ==========================================================================
   DESTILL — design prototype behaviour
   - Real: local file selection through the browser File API, metadata read
     by the browser's own media decoder, and a still frame drawn on this device.
   - Synthetic: every timestamp, claim, story beat and prompt below comes from
     the DEMO object (invented for design review). Nothing is uploaded, analysed
     or rendered. Analysis is intentionally blocked for real files because this
     build has no analysis service.
   ========================================================================== */
(() => {
  'use strict';

  /* ---------- SYNTHETIC DEMO CONTENT (invented for design review) ---------- */
  const DEMO = {
    duration: 222,            // scripted 3:42 clip
    target: 90,               // default target length in seconds
    message:
      'A small team argues that its new scheduling tool returns about two hours a week. The clip states that claim, shows the booking screen, supports it with a testimonial and a figure, then closes with a call to action.',
    story: [
      { id: 'hook', name: 'Hook', start: 0, end: 12, note: 'States the two-hour claim' },
      { id: 'problem', name: 'Problem', start: 12, end: 44, note: 'Manual rescheduling' },
      { id: 'demo', name: 'Demo', start: 44, end: 106, note: 'Booking screen, plus a pricing aside' },
      { id: 'proof', name: 'Proof', start: 106, end: 154, note: 'Testimonial, then a figure' },
      { id: 'recap', name: 'Recap', start: 154, end: 182, note: 'Repeats the opening' },
      { id: 'cta', name: 'Call to action', start: 182, end: 222, note: 'Link and outro' }
    ],
    segments: [
      { id: 's1', start: 0, end: 12, title: 'Hook: the two-hour claim', why: 'States the claim the rest of the clip depends on. Nothing on screen supports the figure yet.', suggest: 'keep', trim: null, tags: ['said'] },
      { id: 's2', start: 12, end: 44, title: 'Problem: manual rescheduling', why: 'The whiteboard sketch is clear; the second half repeats it.', suggest: 'change', trim: 20, tags: ['shown'] },
      { id: 's3', start: 44, end: 80, title: 'Demo: booking screen at normal speed', why: 'The first 14 seconds show the screen clearly; the rest is a slow pan.', suggest: 'change', trim: 14, tags: ['shown'] },
      { id: 's4', start: 80, end: 106, title: 'Pricing aside', why: 'Pricing is not connected to the scheduling claim.', suggest: 'drop', trim: null, tags: ['unclear'] },
      { id: 's5', start: 106, end: 130, title: 'Testimonial with a role, no company', why: 'Adds a human voice. The company cannot be checked from this clip.', suggest: 'keep', trim: null, tags: ['said'] },
      { id: 's6', start: 130, end: 154, title: 'Proof figure: 40% spoken, 14% on screen', why: 'The narrator and the on-screen figure disagree. Destill will not choose between them.', suggest: null, trim: null, tags: ['conflict'], conflict: true },
      { id: 's7', start: 154, end: 182, title: 'Recap of the opening', why: 'Repeats 0:00–0:12 almost word for word.', suggest: 'drop', trim: null, tags: ['said'] },
      { id: 's8', start: 182, end: 222, title: 'Call to action and outro', why: 'The link line is clear; the outro is about 20 seconds of logo.', suggest: 'change', trim: 12, tags: ['said', 'shown'] }
    ],
    evidence: [
      { id: 'e1', t: 4, kind: 'said', text: 'Spoken claim: “Two hours back every week.” No figure appears on screen.' },
      { id: 'e2', t: 18, kind: 'shown', text: 'Whiteboard sketch of manual rescheduling loops.' },
      { id: 'e3', t: 52, kind: 'shown', text: 'Booking screen at normal speed. The first 14 seconds are legible.' },
      { id: 'e4', t: 94, kind: 'unclear', text: 'Pricing is discussed, with no visible link to the scheduling claim.' },
      { id: 'e5', t: 118, kind: 'said', text: 'The testimonial names a role but no company, so it cannot be checked here.' },
      { id: 'e6', t: 142, kind: 'conflict', text: 'Spoken: “40% fewer conflicts.” On screen: 14%.' },
      { id: 'e7', t: 168, kind: 'said', text: 'The recap repeats the opening claim almost word for word.' },
      { id: 'e8', t: 200, kind: 'said', text: 'The spoken call to action names a link that is not shown on screen.' }
    ]
  };

  const KIND = {
    shown: { label: 'Shown', cls: '' },
    said: { label: 'Said', cls: '' },
    unclear: { label: 'Unclear', cls: '' },
    conflict: { label: 'Conflicting', cls: 'tag-warn' }
  };

  const STAGES = [
    { label: 'Checking the source', ms: 900 },
    { label: 'Sampling frames', ms: 1600 },
    { label: 'Transcribing speech', ms: 1700 },
    { label: 'Finding claims and evidence', ms: 1500 },
    { label: 'Drafting story structure', ms: 1300 }
  ];

  const MEDIA_ERR = {
    1: 'playback was aborted',
    2: 'a network error interrupted reading the file',
    3: 'the file could not be decoded',
    4: 'this format is not supported by this browser'
  };

  const OUTCOMES = {
    error: {
      eyebrow: 'Couldn’t read this video',
      title: 'This browser can’t play the file',
      body: 'Nothing was uploaded or changed. Try an MP4 (H.264) or WebM file, or continue with the synthetic demo, which uses no footage at all.',
      icon: 'alert',
      actions: [
        { label: 'Choose another video', act: 'pick', primary: true },
        { label: 'Use synthetic demo instead', act: 'demo' }
      ]
    },
    cancelled: {
      eyebrow: 'Stopped',
      title: 'Demo analysis cancelled',
      body: 'The scripted steps were stopped. No results were kept, and nothing was sent anywhere.',
      icon: 'x',
      actions: [
        { label: 'Start the demo again', act: 'demo', primary: true },
        { label: 'Back to source', act: 'to-source' }
      ]
    },
    decision: {
      eyebrow: 'Needs your decision',
      title: 'The spoken and on-screen figures disagree',
      body: 'At 2:10–2:34 the narrator says “40% fewer conflicts”, but the on-screen figure reads 14%. Destill won’t pick one for you. Choose how this moment should be handled in the demo cut.',
      icon: 'info',
      choices: true,
      actions: [
        { label: 'Apply decision', act: 'apply', primary: true },
        { label: 'Back to refine', act: 'to-refine' }
      ]
    }
  };

  const ROUTES = {
    welcome: 'Welcome',
    source: 'Source',
    blocked: 'Analysis blocked',
    processing: 'Synthetic demo running',
    understanding: 'Understanding (synthetic demo)',
    refine: 'Refine (synthetic demo)',
    result: 'Result concept (not rendered)',
    error: 'Error',
    cancelled: 'Cancelled',
    decision: 'Needs your decision'
  };
  const SCREEN_OF = {
    welcome: 'welcome', source: 'source', blocked: 'blocked', processing: 'processing',
    understanding: 'understanding', refine: 'refine', result: 'result',
    error: 'outcome', cancelled: 'outcome', decision: 'outcome'
  };
  const RESULT_ROUTES = ['understanding', 'refine', 'result', 'decision'];

  /* ---------- HELPERS ---------- */
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const clamp = (n, a, b) => Math.min(b, Math.max(a, n));
  const fmt = (sec) => {
    const s = Math.max(0, Math.round(sec));
    return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
  };
  const fmtRange = (a, b) => `${fmt(a)}–${fmt(b)}`;
  const fmtBytes = (n) => (n < 1e6 ? `${Math.max(1, Math.round(n / 1e3))} KB` : n < 1e9 ? `${(n / 1e6).toFixed(1)} MB` : `${(n / 1e9).toFixed(2)} GB`);
  const segDur = (s) => s.end - s.start;
  const pctOf = (t) => `calc(12px + (100% - 24px) * ${(t / DEMO.duration).toFixed(5)})`;
  const spanOf = (a, b) => `calc((100% - 24px) * ${((b - a) / DEMO.duration).toFixed(5)} - 2px)`;
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const icon = (name, cls = 'i') => `<svg class="${cls}" aria-hidden="true" focusable="false"><use href="#i-${name}"/></svg>`;

  /* ---------- STATE ---------- */
  const state = {
    route: null,
    mode: 'none',            // 'none' | 'file' (real file, not analysed) | 'demo' (synthetic content)
    results: false,          // synthetic results exist for this session
    file: null,
    url: null,
    meta: null,
    poster: null,
    errorDetail: null,
    consent: false,
    length: DEMO.target,
    intent: '',
    decisions: {},
    trims: {},
    s6Note: null,
    playhead: 0,
    evFilter: 'all',
    feedback: {},
    stage: 0,
    timers: [],
    lastEvKey: null
  };
  DEMO.segments.forEach((s) => {
    state.decisions[s.id] = s.suggest;
    state.trims[s.id] = s.trim ?? segDur(s);
  });

  const projected = () => DEMO.segments.reduce((sum, s) => {
    const d = state.decisions[s.id];
    if (d === 'keep') return sum + segDur(s);
    if (d === 'change') return sum + state.trims[s.id];
    return sum;
  }, 0);
  const countDecisions = () => DEMO.segments.reduce((c, s) => {
    const d = state.decisions[s.id] || 'open';
    c[d] = (c[d] || 0) + 1;
    return c;
  }, { keep: 0, change: 0, drop: 0, open: 0 });

  /* ---------- TIMERS ---------- */
  const schedule = (ms, fn) => state.timers.push(window.setTimeout(fn, ms));
  const clearTimers = () => { state.timers.forEach(clearTimeout); state.timers = []; };

  /* ---------- ROUTING ---------- */
  function go(route, opts = {}) {
    const requested = route;
    if (!(route in ROUTES)) route = 'welcome';
    if ((route === 'source' || route === 'blocked') && !state.file) route = 'welcome';
    if (requested !== route && opts.fromHash) history.replaceState({ route }, '', `#${route}`);
    if (RESULT_ROUTES.includes(route) && !state.results) {
      state.results = true;                // review jumps get the synthetic session
      if (state.mode === 'none') state.mode = 'demo';
      else if (state.mode === 'file') state.mode = 'demo';
    }
    if (route === state.route && !opts.force) return;

    if (state.route === 'processing' && route !== 'processing') clearTimers();
    if (route === 'processing') { state.mode = 'demo'; state.results = false; }
    if (route === 'blocked') state.mode = 'file';
    if (route === 'source' && state.mode === 'none' && state.file) state.mode = 'file';

    state.route = route;
    paintAll();
    if (route === 'processing') startRun();
    if (route === 'decision') $$('input[name="decision"]').forEach((i) => { i.checked = false; });
    if (route === 'error' || route === 'cancelled' || route === 'decision') paintOutcome();

    if (!opts.fromHash) history.pushState({ route }, '', `#${route}`);
    document.title = `Destill — ${ROUTES[route]}`;
    if (!opts.silent) {
      window.scrollTo({ top: 0, behavior: 'auto' });
      focusHeading();
    }
  }

  function focusHeading() {
    const scr = $('.screen:not([hidden])');
    const h = scr && scr.querySelector('h1');
    if (h) h.focus({ preventScroll: true });
  }

  function stageOf(route) {
    switch (route) {
      case 'welcome': case 'source': case 'blocked': return 'source';
      case 'processing': case 'understanding': return 'analyze';
      case 'refine': return 'refine';
      case 'result': return 'result';
      default: return state.results ? 'analyze' : 'source';
    }
  }

  /* ---------- PAINTERS ---------- */
  function paintAll() {
    paintScreens();
    paintStepper();
    paintMode();
    paintWells();
    paintFacts();
    paintTransport();
    paintBlocked();
    paintLength();
    paintUnderstanding();
    paintRefine();
    paintResult();
  }

  function paintScreens() {
    const want = SCREEN_OF[state.route];
    $$('.screen').forEach((s) => { s.hidden = s.dataset.screen !== want; });
  }

  function paintStepper() {
    const stage = stageOf(state.route);
    $$('[data-stage]').forEach((b) => {
      const k = b.dataset.stage;
      const needsResults = k !== 'source';
      b.disabled = needsResults && !state.results;
      if (k === stage) b.setAttribute('aria-current', 'step');
      else b.removeAttribute('aria-current');
    });
  }

  function paintMode() {
    const pill = $('#modePill');
    let tone = 'none';
    let msg = 'No video selected';
    if (state.route === 'processing') { tone = 'demo'; msg = 'Synthetic demo running · no footage'; }
    else if (state.route === 'blocked') { tone = 'blocked'; msg = 'Analysis blocked · no service connected'; }
    else if (state.mode === 'demo') {
      tone = 'demo';
      msg = state.file ? 'Demo results · your file is not analysed' : 'Synthetic demo · no footage';
    } else if (state.mode === 'file' && state.file) { tone = 'file'; msg = 'Your file · read in this browser'; }
    pill.dataset.tone = tone;
    $('#modeText').textContent = msg;
  }

  function paintWells() {
    const synth = state.mode === 'demo' || state.route === 'processing';
    const hasFile = !!state.file;
    $$('.well').forEach((w) => {
      if (w.dataset.well === 'result') return;
      const video = w.querySelector('.well-video');
      const img = w.querySelector('.well-poster');
      const synthEl = w.querySelector('.well-synth');
      const empty = w.querySelector('.well-empty');
      // Source well shows the live (muted, paused) video; other wells show a still frame.
      const showVideo = !synth && hasFile && !!video;
      const showPoster = !synth && hasFile && !video && !!state.poster;
      if (synthEl) synthEl.hidden = !synth;
      if (video) video.hidden = !showVideo;
      if (img) {
        img.hidden = !showPoster;
        if (showPoster) img.src = state.poster;
      }
      if (empty) {
        empty.hidden = synth || showVideo || showPoster;
        empty.firstElementChild.textContent = hasFile ? 'Preparing still frame…' : 'No video selected';
      }
      $$('[data-tc]', w).forEach((el) => { el.textContent = fmt(state.playhead); });
    });
  }

  function paintFacts() {
    const m = state.meta;
    const set = (sel, v) => $$(sel).forEach((el) => { el.textContent = v; });
    set('#fName', m ? m.name : 'No file selected');
    set('#fSize', m ? fmtBytes(m.size) : '—');
    set('#fType', m ? m.type : '—');
    set('#fDur', m && m.duration != null ? (isFinite(m.duration) && m.duration > 0 ? fmt(m.duration) : 'Unknown') : (m ? 'Reading…' : '—'));
    set('#fRes', m && m.res ? m.res : (m ? 'Reading…' : '—'));
    set('#fMod', m ? m.modified : '—');
    set('[data-fname]', m ? m.name : 'No file selected');
    set('[data-fsize]', m ? fmtBytes(m.size) : '—');
  }

  function paintTransport() {
    const show = !!state.file && state.mode === 'file' && state.route === 'source';
    $('[data-transport]').hidden = !show;
  }

  function paintBlocked() {
    const sw = $('#consentSwitch');
    sw.setAttribute('aria-checked', String(state.consent));
    $('#consentDesc').textContent = state.consent
      ? 'Consent noted. It cannot be used yet, because no analysis service is connected to this build.'
      : 'Sending selected frames and audio to an analysis service needs your explicit permission.';
  }

  function paintLength() {
    $$('[data-len]').forEach((b) => {
      const on = Number(b.dataset.len) === state.length;
      b.setAttribute('aria-checked', String(on));
      b.tabIndex = on ? 0 : -1;
    });
  }

  function paintUnderstanding() {
    $('#message').textContent = DEMO.message;
    $('#storyList').innerHTML = DEMO.story.map((b) => `
      <li><button class="story-row" type="button" data-seek="${b.start}" data-band="${b.id}" aria-label="${esc(b.name)}, ${fmtRange(b.start, b.end)}. Jump to start">
        <span class="s-main"><span class="s-name">${esc(b.name)}</span><br><span class="s-note">${esc(b.note)}</span></span>
        <span class="s-time">${fmtRange(b.start, b.end)}</span>
      </button></li>`).join('');

    $('#tlBands').innerHTML = DEMO.story.map((b) =>
      `<span class="band" data-band="${b.id}" style="left:${pctOf(b.start)};width:${spanOf(b.start, b.end)}"></span>`).join('');
    $('#tlMarks').innerHTML = DEMO.evidence.map((e) =>
      `<span class="mark-dot" data-kind="${e.kind}" style="left:${pctOf(e.t)}" title="${fmt(e.t)} · ${KIND[e.kind].label}"></span>`).join('');

    const ph = $('#playhead');
    ph.max = DEMO.duration;
    ph.value = state.playhead;
    paintScrubFill(ph);

    $('#decisionNotice').hidden = state.decisions.s6 != null;
    state.lastEvKey = null;
    paintEvidence(true);
    setPlayhead(state.playhead, { fromInput: false });
  }

  function paintEvidence(force) {
    const near = state.evFilter === 'near';
    const list = DEMO.evidence.filter((e) => !near || Math.abs(e.t - state.playhead) <= 20);
    const key = list.map((e) => e.id).join(',');
    if (!force && key === state.lastEvKey) { updateEvidenceCurrent(); return; }
    state.lastEvKey = key;
    $('#evidenceList').innerHTML = list.length
      ? list.map(evCard).join('')
      : '<p class="caption">No observations within 20 seconds of this point. Move the playhead, or choose All moments.</p>';
    updateEvidenceCurrent();
  }

  function evCard(e) {
    const fb = state.feedback[e.id];
    const k = KIND[e.kind];
    return `<article class="evidence${e.kind === 'conflict' ? ' is-conflict' : ''}" data-ev="${e.id}" aria-label="${fmt(e.t)}, ${k.label}">
      <div class="ev-top">
        <button class="tchip" type="button" data-seek="${e.t}" aria-label="Jump to ${fmt(e.t)}">${fmt(e.t)}</button>
        <span class="tag ${k.cls}">${k.label}</span>
      </div>
      <p class="ev-text">${esc(e.text)}</p>
      <div class="ev-foot">
        <div class="fb" role="group" aria-label="Feedback on this observation">
          <button class="fb-btn" type="button" data-fb="right" data-ev="${e.id}" aria-pressed="${fb === 'right'}">Looks right</button>
          <button class="fb-btn" type="button" data-fb="wrong" data-ev="${e.id}" aria-pressed="${fb === 'wrong'}">Not right</button>
        </div>
      </div>
    </article>`;
  }

  function updateEvidenceCurrent() {
    $$('#evidenceList .tchip[data-seek]').forEach((b) => {
      const t = Number(b.dataset.seek);
      b.setAttribute('aria-current', String(Math.abs(t - state.playhead) <= 3));
    });
  }

  function paintScrubFill(el) {
    const min = Number(el.min || 0);
    const max = Number(el.max || 100);
    const pct = ((Number(el.value) - min) / (max - min)) * 100;
    el.style.setProperty('--fill', `${pct}%`);
  }

  function setPlayhead(sec, { fromInput = false } = {}) {
    state.playhead = clamp(Math.round(sec), 0, DEMO.duration);
    const ph = $('#playhead');
    if (!fromInput) ph.value = state.playhead;
    paintScrubFill(ph);
    ph.setAttribute('aria-valuetext', fmt(state.playhead));
    $('#tlReadout').textContent = `${fmt(state.playhead)} of ${fmt(DEMO.duration)}`;
    $$('.band').forEach((b) => {
      const s = DEMO.story.find((x) => x.id === b.dataset.band);
      b.setAttribute('aria-current', String(state.playhead >= s.start && state.playhead < s.end));
    });
    $$('.story-row').forEach((r) => {
      const s = DEMO.story.find((x) => x.id === r.dataset.band);
      r.setAttribute('aria-current', String(state.playhead >= s.start && state.playhead < s.end));
    });
    $$('[data-tc]').forEach((el) => { el.textContent = fmt(state.playhead); });
    if (state.evFilter === 'near') paintEvidence(false);
    else updateEvidenceCurrent();
  }

  function paintRefine() {
    $('#segmentList').innerHTML = DEMO.segments.map(segHTML).join('');
    $$('#segmentList .track[role="radiogroup"]').forEach(rovingInit);
    paintSummary();
  }

  function segHTML(s) {
    const d = state.decisions[s.id];
    const range = fmtRange(s.start, s.end);
    const open = !d;
    const decideBtn = (k) => {
      const on = d === k;
      const roving = d ? on : k === 'keep';
      return `<button class="seg seg-dec" type="button" role="radio" aria-checked="${on}" tabindex="${roving ? 0 : -1}" data-decide="${k}" data-id="${s.id}">${k}</button>`;
    };
    const trim = d === 'change' ? `
      <div class="trim" role="group" aria-label="Trim length for ${range}">
        <span>Trim to</span>
        <button class="medallion" type="button" data-trim="-2" data-id="${s.id}" aria-label="Shorten by 2 seconds" ${state.trims[s.id] <= 4 ? 'disabled' : ''}>${icon('minus')}</button>
        <output aria-live="polite">${state.trims[s.id]} s</output>
        <button class="medallion" type="button" data-trim="2" data-id="${s.id}" aria-label="Lengthen by 2 seconds" ${state.trims[s.id] >= segDur(s) ? 'disabled' : ''}>${icon('plus')}</button>
      </div>` : '';
    const note = s.conflict && state.s6Note ? `<p class="caption">${esc(state.s6Note)}</p>` : '';
    const tags = s.tags.map((k) => `<span class="tag ${KIND[k].cls}">${KIND[k].label}</span>`).join('');
    return `<li class="segment${open ? ' is-open' : ''}" data-id="${s.id}">
      <div class="seg-time">
        <button class="tchip" type="button" data-tl="${s.start}" aria-label="Show ${range} on the source timeline">${range}</button>
      </div>
      <div class="seg-main">
        <p class="seg-title">${esc(s.title)}</p>
        <p class="seg-why">${esc(s.why)}</p>
        <div class="seg-tags">${tags}${open ? '<span class="tag tag-warn">Decision needed</span>' : ''}</div>
        <div class="seg-decide">
          <div class="track" role="radiogroup" aria-label="Decision for ${range}">
            ${decideBtn('keep')}${decideBtn('change')}${decideBtn('drop')}
          </div>
          ${trim}
          ${s.conflict && open ? '<button class="btn sm" type="button" data-action="decide-seg">Decide with evidence</button>' : ''}
        </div>
        ${note}
      </div>
    </li>`;
  }

  function cutBarHTML() {
    return DEMO.segments.map((s) => {
      const d = state.decisions[s.id];
      if (!d) return `<span class="cut-block" data-d="open" style="flex:${segDur(s)} 1 0" title="${fmtRange(s.start, s.end)} · open"></span>`;
      if (d === 'drop') return '';
      const w = d === 'change' ? state.trims[s.id] : segDur(s);
      return `<span class="cut-block" data-d="${d}" style="flex:${w} 1 0" title="${fmtRange(s.start, s.end)} · ${d}"></span>`;
    }).join('');
  }

  function paintSummary() {
    const p = projected();
    const c = countDecisions();
    $('#projected').textContent = fmt(p);
    const diff = state.length - p;
    $('#targetLine').textContent = `Target ${fmt(state.length)} · ${diff === 0 ? 'on target' : diff > 0 ? `${diff} s under` : `${-diff} s over`}`;
    $('#cKeep').textContent = c.keep;
    $('#cChange').textContent = c.change;
    $('#cDrop').textContent = c.drop;
    $('#cOpen').textContent = c.open;
    $('#openNote').textContent = c.open
      ? `${c.open} open. Open moments stay out of the demo cut until you decide.`
      : 'Every segment has a decision.';
    $('#cutBar').innerHTML = cutBarHTML();
  }

  function paintResult() {
    const rows = DEMO.segments.map((s) => {
      const d = state.decisions[s.id];
      const t = fmtRange(s.start, s.end);
      const link = `<button class="tchip" type="button" data-tl="${s.start}" aria-label="Show ${t} on the source timeline">${t}</button>`;
      if (!d) return `<li>${link}<span>Open. Left out of the draft until someone decides.</span></li>`;
      const verb = d === 'keep' ? 'Kept.' : d === 'change' ? `Trimmed to ${state.trims[s.id]} s.` : 'Dropped.';
      const extra = s.conflict && state.s6Note ? ` ${state.s6Note}` : '';
      return `<li>${link}<span>${verb} ${esc(s.why)}${esc(extra)}</span></li>`;
    });
    $('#rationale').innerHTML = rows.join('');
    $('#promptText').value = buildPrompt();
    $('#renderBtn').textContent = `Render ${fmt(projected())} MP4 — unavailable`;
    $('#resultBar').innerHTML = cutBarHTML();
  }

  function buildPrompt() {
    const L = [];
    L.push(`Target tool: CapCut EditPilot (paste manually). Source: a scripted ${fmt(DEMO.duration)} demo clip with synthetic timings, not measured from any footage.`);
    if (state.intent.trim()) L.push(`Editor's intent: ${state.intent.trim()}`);
    L.push(`Goal: a draft of about ${fmt(state.length)}. Use only the moments listed below, in source order. Do not add claims, captions or footage.`);
    L.push('');
    L.push('Decisions by source timecode:');
    DEMO.segments.forEach((s) => {
      const d = state.decisions[s.id];
      const t = fmtRange(s.start, s.end);
      if (d === 'keep') L.push(`- KEEP ${t}: ${s.title}.`);
      else if (d === 'change') L.push(`- CHANGE ${t}: ${s.title}. Trim to ${state.trims[s.id]} seconds.`);
      else if (d === 'drop') L.push(`- DROP ${t}: ${s.title}.`);
      else L.push(`- OPEN ${t}: ${s.title}. Do not place this moment until the editor decides.`);
    });
    if (state.s6Note) L.push(`- Editor note for 2:10–2:34: ${state.s6Note}`);
    L.push('');
    L.push(`Expected output: about ${fmt(projected())}. Flag any moment marked SAID but not SHOWN for editor review before export.`);
    return L.join('\n');
  }

  function paintOutcome() {
    const v = state.route;
    const o = OUTCOMES[v];
    if (!o) return;
    $('#outEyebrow').textContent = o.eyebrow;
    $('#outTitle').textContent = o.title;
    $('#outBody').textContent = o.body;
    $('#outIconUse').setAttribute('href', `#i-${o.icon}`);
    const detail = state.errorDetail || (v === 'error' ? 'Example state for review. No file was read.' : '');
    $('#outDetail').hidden = !detail;
    $('#outDetail').textContent = detail;
    $('#outChoices').hidden = !o.choices;
    $('#outError').hidden = true;
    $('#outActions').innerHTML = o.actions.map((a) =>
      `<button class="btn ${a.primary ? 'primary' : 'subtle'}" type="button" data-act="${a.act}">${a.label}</button>`).join('');
  }

  function rovingInit(grp) {
    const items = $$('[role="radio"]', grp);
    const checked = items.find((i) => i.getAttribute('aria-checked') === 'true') || items[0];
    items.forEach((i) => { i.tabIndex = i === checked ? 0 : -1; });
  }

  /* ---------- RUN (synthetic) ---------- */
  function startRun() {
    clearTimers();
    state.stage = 0;
    state.results = false;
    $('#seeDemo').hidden = true;
    $('#cancelBtn').hidden = false;
    renderStages(false);
    schedule(STAGES[0].ms, nextStage);
  }

  function nextStage() {
    state.stage += 1;
    if (state.stage >= STAGES.length) { renderStages(true); return; }
    renderStages(false);
    schedule(STAGES[state.stage].ms, nextStage);
  }

  function renderStages(done) {
    $('#stages').innerHTML = STAGES.map((s, i) => {
      const st = done || i < state.stage ? 'done' : i === state.stage ? 'active' : 'queued';
      const mark = st === 'done' ? icon('check') : st === 'active' ? '<span class="pulse" aria-hidden="true"></span>' : '<span class="pulse-quiet" aria-hidden="true"></span>';
      return `<li class="stage" data-state="${st}">
        <span class="medallion" aria-hidden="true">${mark}</span>
        <span><span class="stage-name">${esc(s.label)}</span><br><span class="stage-note">Scripted step${st === 'done' ? ' · complete' : ''}</span></span>
        <span class="tag">${st === 'done' ? 'Done' : st === 'active' ? 'Running' : 'Queued'}</span>
      </li>`;
    }).join('');
    $('#procStatus').textContent = done
      ? 'Scripted steps finished. These results are synthetic.'
      : `Scripted step ${state.stage + 1} of ${STAGES.length}`;
    $('#seeDemo').hidden = !done;
    $('#cancelBtn').hidden = done;
    if (done) state.results = true;
  }

  function startDemo() { go('processing', { force: true }); }

  function cancelRun() {
    clearTimers();
    state.results = false;
    state.mode = state.file ? 'file' : 'none';
    go('cancelled', { force: true });
  }

  /* ---------- REAL FILE (browser-local, no upload) ---------- */
  function openPicker() { $('#fileInput').click(); }

  function releaseUrl() {
    if (state.url) URL.revokeObjectURL(state.url);
    state.url = null;
  }

  function loadFile(file) {
    if (!file) return;
    const looksVideo = /^video\//.test(file.type) || /\.(mp4|m4v|mov|webm)$/i.test(file.name);
    if (!looksVideo) {
      state.errorDetail = `${file.name}: not a video file type Destill accepts (MP4, MOV or WebM).`;
      releaseUrl(); state.file = null; state.meta = null; state.mode = 'none';
      go('error', { force: true });
      return;
    }
    releaseUrl();
    state.file = file;
    state.url = URL.createObjectURL(file);
    state.meta = {
      name: file.name,
      size: file.size,
      type: file.type || 'Unknown',
      modified: file.lastModified ? new Date(file.lastModified).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' }) : 'Unknown',
      duration: null,
      res: null
    };
    state.poster = null;
    state.mode = 'file';
    state.results = false;
    state.errorDetail = null;
    state.consent = false;

    const v = $('.well-video');
    v.pause();
    v.removeAttribute('src');
    v.src = state.url;
    v.load();
    v.onloadedmetadata = () => {
      state.meta.duration = v.duration;
      state.meta.res = v.videoWidth ? `${v.videoWidth} × ${v.videoHeight}` : 'Unknown';
      paintFacts();
      const onSeeked = () => capturePoster(v);
      v.addEventListener('seeked', onSeeked, { once: true });
      v.currentTime = Math.min(0.5, (isFinite(v.duration) ? v.duration : 1) / 2);
      paintTransport();
    };
    v.onerror = () => {
      const code = v.error ? v.error.code : 0;
      state.errorDetail = `${file.name}: ${MEDIA_ERR[code] || 'the browser reported an unknown media error'} (MediaError code ${code || 'n/a'}).`;
      releaseUrl();
      v.removeAttribute('src');
      state.file = null; state.meta = null; state.poster = null; state.mode = 'none';
      go('error', { force: true });
    };
    go('source', { force: true });
  }

  function capturePoster(v) {
    try {
      const c = document.createElement('canvas');
      c.width = 640;
      c.height = v.videoWidth ? Math.round((640 * v.videoHeight) / v.videoWidth) : 360;
      c.getContext('2d').drawImage(v, 0, 0, c.width, c.height);
      state.poster = c.toDataURL('image/jpeg', 0.85);
    } catch (err) {
      state.poster = null;
    }
    paintWells();
  }

  function removeFile() {
    const v = $('.well-video');
    v.pause();
    v.removeAttribute('src');
    v.load();
    releaseUrl();
    state.file = null; state.meta = null; state.poster = null;
    state.mode = 'none'; state.results = false; state.errorDetail = null;
    clearTimers();
    go('welcome', { force: true });
  }

  function copyPrompt() {
    const ta = $('#promptText');
    const status = $('#copyStatus');
    const done = (ok) => {
      status.textContent = ok ? 'Prompt copied.' : 'Copy was blocked by the browser. The text is selected, so copy it manually.';
    };
    const fallback = () => {
      ta.focus(); ta.select();
      let ok = false;
      try { ok = document.execCommand('copy'); } catch (err) { ok = false; }
      done(ok);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(ta.value).then(() => done(true), fallback);
    } else {
      fallback();
    }
  }

  function applyDecision() {
    const choice = $('input[name="decision"]:checked');
    if (!choice) {
      const err = $('#outError');
      err.hidden = false;
      err.textContent = 'Choose one option first. Destill won’t decide for you.';
      $('input[name="decision"]').focus();
      return;
    }
    const map = {
      spoken: ['keep', 'Editor kept the spoken figure (40%). Verify it before publishing.'],
      onscreen: ['keep', 'Editor kept the moment and chose the on-screen figure (14%). Verify it before publishing.'],
      leave: ['drop', 'Editor left this moment out of the demo cut.']
    };
    const [d, note] = map[choice.value];
    state.decisions.s6 = d;
    state.s6Note = note;
    go('refine', { force: true });
  }

  function withFocusKept(fn) {
    const a = document.activeElement;
    const id = a && a.closest ? (a.closest('.segment') || {}).dataset : null;
    const segId = id ? id.id : null;
    let sel = null;
    if (a && a.dataset) {
      if (a.dataset.decide) sel = `[data-decide="${a.dataset.decide}"]`;
      else if (a.dataset.trim) sel = `[data-trim="${a.dataset.trim}"]`;
    }
    fn();
    if (segId && sel) {
      const el = $(`.segment[data-id="${segId}"] ${sel}`);
      if (el && !el.disabled) el.focus({ preventScroll: true });
    }
  }

  /* ---------- EVENTS ---------- */
  document.addEventListener('click', (e) => {
    const t = e.target;
    const hit = (sel) => (t.closest ? t.closest(sel) : null);
    let el;

    if ((el = hit('[data-stage]'))) {
      const k = el.dataset.stage;
      if (k === 'source') go(state.file ? 'source' : 'welcome');
      else if (k === 'analyze') go('understanding');
      else if (k === 'refine') go('refine');
      else if (k === 'result') go('result');
      return;
    }

    if ((el = hit('[data-hash]'))) {
      const r = el.dataset.hash;
      if ((r === 'source' || r === 'blocked') && !state.file) { openPicker(); return; }
      if (r === 'error' || r === 'cancelled' || r === 'decision') state.errorDetail = null;
      go(r);
      return;
    }

    if ((el = hit('[data-action]'))) {
      const a = el.dataset.action;
      if (a === 'pick' || a === 'replace') openPicker();
      else if (a === 'demo') startDemo();
      else if (a === 'analyze') { if (state.file) go('blocked'); else go('welcome'); }
      else if (a === 'analyze-blocked') {
        $('#blockReason').textContent = 'Still unavailable. No analysis service is connected to this build, and consent alone cannot start analysis.';
      }
      else if (a === 'to-source') go(state.file ? 'source' : 'welcome');
      else if (a === 'remove') removeFile();
      else if (a === 'cancel') cancelRun();
      else if (a === 'see-demo') { state.mode = 'demo'; go('understanding', { force: true }); }
      else if (a === 'to-refine') go('refine');
      else if (a === 'to-result') go('result');
      else if (a === 'decide' || a === 'decide-seg') go('decision');
      else if (a === 'reset-decisions') {
        DEMO.segments.forEach((s) => { state.decisions[s.id] = s.suggest; state.trims[s.id] = s.trim ?? segDur(s); });
        state.s6Note = null;
        paintRefine(); paintResult(); paintUnderstanding();
        focusHeading();
      }
      else if (a === 'copy') copyPrompt();
      return;
    }

    if ((el = hit('[data-act]'))) {
      const a = el.dataset.act;
      if (a === 'pick') openPicker();
      else if (a === 'demo') startDemo();
      else if (a === 'to-source') go(state.file ? 'source' : 'welcome');
      else if (a === 'apply') applyDecision();
      else if (a === 'to-refine') go('refine');
      return;
    }

    if ((el = hit('[data-seek]'))) {
      if (state.route !== 'understanding') go('understanding');
      setPlayhead(Number(el.dataset.seek));
      return;
    }

    if ((el = hit('[data-tl]'))) {
      go('understanding');
      setPlayhead(Number(el.dataset.tl));
      return;
    }

    if ((el = hit('[data-fb]'))) {
      const id = el.dataset.ev;
      const v = el.dataset.fb;
      state.feedback[id] = state.feedback[id] === v ? undefined : v;
      $$(`[data-ev="${id}"][data-fb]`).forEach((b) => {
        b.setAttribute('aria-pressed', String(state.feedback[id] === b.dataset.fb));
      });
      return;
    }

    if ((el = hit('[data-len]'))) {
      state.length = Number(el.dataset.len);
      paintLength();
      paintSummary();
      $('#promptText').value = buildPrompt();
      $('#renderBtn').textContent = `Render ${fmt(projected())} MP4 — unavailable`;
      return;
    }

    if ((el = hit('[data-filter]'))) {
      state.evFilter = el.dataset.filter;
      $$('[data-filter]').forEach((b) => {
        const on = b.dataset.filter === state.evFilter;
        b.setAttribute('aria-checked', String(on));
        b.tabIndex = on ? 0 : -1;
      });
      paintEvidence(true);
      return;
    }

    if ((el = hit('[data-decide]'))) {
      const id = el.dataset.id;
      const k = el.dataset.decide;
      withFocusKept(() => {
        state.decisions[id] = k;
        paintRefine();
        paintResult();
        paintUnderstanding();
      });
      return;
    }

    if ((el = hit('[data-trim]'))) {
      const id = el.dataset.id;
      const s = DEMO.segments.find((x) => x.id === id);
      withFocusKept(() => {
        state.trims[id] = clamp(state.trims[id] + Number(el.dataset.trim), 4, segDur(s));
        paintRefine();
        paintResult();
      });
      return;
    }

    if ((el = hit('#consentSwitch'))) {
      state.consent = !state.consent;
      paintBlocked();
      return;
    }

    if ((el = hit('#depthSwitch'))) {
      const off = document.documentElement.dataset.depth === 'off';
      document.documentElement.dataset.depth = off ? 'on' : 'off';
      el.setAttribute('aria-checked', String(off));
      $('#depthLabel').textContent = off ? 'Shadows on' : 'Shadows off (flat check)';
      return;
    }

    if ((el = hit('#playBtn'))) {
      const v = $('.well-video');
      if (v.paused) v.play().catch(() => {}); else v.pause();
      return;
    }

  });

  /* arrow-key roving for every radiogroup */
  document.addEventListener('keydown', (e) => {
    const keys = ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'];
    if (!keys.includes(e.key)) return;
    const grp = e.target.closest ? e.target.closest('[role="radiogroup"]') : null;
    if (!grp) return;
    const items = $$('[role="radio"]:not([disabled])', grp);
    const i = items.indexOf(e.target);
    if (i < 0) return;
    e.preventDefault();
    let n = i;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = (i + 1) % items.length;
    else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = (i - 1 + items.length) % items.length;
    else if (e.key === 'Home') n = 0;
    else if (e.key === 'End') n = items.length - 1;
    items[n].focus();
    items[n].click();
  });

  /* inputs */
  $('#playhead').addEventListener('input', (e) => {
    setPlayhead(Number(e.target.value), { fromInput: true });
  });

  $('#intent').addEventListener('input', (e) => {
    state.intent = e.target.value;
    $('#promptText').value = buildPrompt();
  });

  $('#fileInput').addEventListener('change', (e) => {
    loadFile(e.target.files && e.target.files[0]);
    e.target.value = '';
  });

  const dz = $('#dropzone');
  dz.addEventListener('dragover', (e) => { e.preventDefault(); dz.classList.add('is-over'); });
  dz.addEventListener('dragleave', () => dz.classList.remove('is-over'));
  dz.addEventListener('drop', (e) => {
    e.preventDefault();
    dz.classList.remove('is-over');
    loadFile(e.dataTransfer.files && e.dataTransfer.files[0]);
  });

  /* real preview controls */
  (function bindPreview() {
    const v = $('.well-video');
    const btn = $('#playBtn');
    const scrub = $('#scrub');
    const tc = $('#tcReal');
    const setIcon = () => {
      const playing = !v.paused;
      btn.innerHTML = icon(playing ? 'pause' : 'play');
      btn.setAttribute('aria-label', playing ? 'Pause preview' : 'Play preview');
    };
    const readout = () => {
      const d = isFinite(v.duration) ? v.duration : 0;
      tc.textContent = `${fmt(v.currentTime)} / ${d ? fmt(d) : '0:00'}`;
      if (d) scrub.value = Math.round((v.currentTime / d) * 1000);
      paintScrubFill(scrub);
    };
    v.addEventListener('play', setIcon);
    v.addEventListener('pause', setIcon);
    v.addEventListener('ended', setIcon);
    v.addEventListener('timeupdate', readout);
    v.addEventListener('loadedmetadata', readout);
    scrub.addEventListener('input', () => {
      const d = isFinite(v.duration) ? v.duration : 0;
      if (d) v.currentTime = (Number(scrub.value) / 1000) * d;
      paintScrubFill(scrub);
    });
    scrub.setAttribute('max', '1000');
  })();

  /* ---------- INIT ---------- */
  function init() {
    // Static markup has segment/evidence chips; render dynamic parts once
    paintLength();
    const hash = location.hash.slice(1);
    const start = ROUTES[hash] ? hash : 'welcome';
    go(start, { fromHash: true, silent: true, force: true });
    window.addEventListener('popstate', () => {
      const h = location.hash.slice(1);
      go(ROUTES[h] ? h : 'welcome', { fromHash: true, force: true });
    });
    $$('[role="radiogroup"]').forEach(rovingInit);
  }

  init();
})();
