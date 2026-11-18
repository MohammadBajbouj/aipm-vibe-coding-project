# Project Instructions for Claude Code

## Product

- Target user: fraud analyst in a bank's fraud operations team (D10). Team lead and AI engineer see the same screen but get no own features (D27).
- User problem: when a fraud alert arrives, the analyst cannot see whether the copilot's reasons are supported by the records – in synthetic case A-1042 a wrong reason led to blocking a genuine customer's card (D11, D12).
- Intended outcome: on one screen the analyst sees the alert, each copilot reason checked against its record value (✓ matches / ⚠ not available / ✗ mismatch) and a non-binding suggestion with mocked weights for release, block or call – then decides (D12).
- Core journey: alert list (3 synthetic alerts) → open alert → payment details, "funds available: yes / no", copilot reasons with claim check → suggestion with mocked weights and warning line → analyst clicks release / block / call + short reason → "Decision saved", status shown ("payment released" / "call planned" / "card blocked"), alert marked done (D13, D14, D22, D23).
- Current milestone: M5 – package the showcase: product README (dev only) + 2 screenshots, safe phone-test command (D43) and template line removed (D47), Gemini setup test on the README (D45), `DECISIONS.md` + `SHOWCASE.md` (Claude Cowork), push to dev only after Mohammad (AI PM)'s explicit OK. No new features (D50).

## Scope

Required for the core slice (see `PRODUCT_BRIEF.md` for details):

- Core journey from alert list to saved decision, with exactly 3 synthetic alerts: A-1042 (2 × ✗), one all ✓, one with device data missing (⚠) (D24).
- Claim-check rules (D19): yes/no facts – different = ✗; numbers – ✗ if more than 25 % away from the record value; record value missing = ⚠; otherwise ✓.
- Traffic-light colours always with word + symbol (D15): claim check green ✓ matches / orange ⚠ not available / red ✗ mismatch; status green released / orange call planned / red blocked.
- Suggestion is non-binding: fixed, pre-written weights labelled "mocked" (D22); only the analyst's click sets a status (D14).
- Decision needs a short reason – empty → "Please enter a reason"; a saved decision is final and read-only (D23).
- States: empty list once all alerts are decided; note "Demo – decisions are lost when the page is reloaded" (D24); "device data not available" with at most 3 previous devices, labelled "previous devices, not from this payment", no matching (D13, D25).
- At phone width the alert screen stacks into one column; buttons and reason field reachable with the Tab key (D26).
- Constraints: no new system installs, no Node.js; project-level Python packages via uv allowed (D8); no browser-test tool – manual tests in Chrome + one automated claim-check test that runs without a browser and without Node.js (D9, D20); preferred: one self-contained HTML file that opens on Mac, Windows and phones, also offline (D21).

Explicit non-goals (D16):

- Login / authentication (D11).
- Card-owner version (D10).
- Balance amounts – only "funds available: yes / no".
- Connection to real bank systems – synthetic data only.
- Real AI-model call – explanations pre-written and labelled "mocked".
- Database – decisions kept only while the page is open.
- Real notifications – the alert list is the starting point.
- Team-lead reopen (extension E1) – only after the core slice and quality gate, if time remains (D27).

Do not add features outside the current milestone without first explaining why
they are necessary.

## Technical Context

- Stack (D30): Python 3.9+ standard library only (claim-check logic, build script, `unittest` test); one generated, self-contained HTML file with inline CSS and plain JavaScript for the journey. No packages, no Node.js, no server, no database. Python code must stay compatible with Python 3.9.
- Architecture: `alerts.json` (synthetic data) → `claim_check.py` (D19 rules, the only place the rule exists) → `build.py` writes `index.html` from `template.html`; JavaScript in the page handles clicks and keeps decisions in memory only.
- Important paths: `app/data/alerts.json`, `app/claim_check.py`, `app/build.py`, `app/template.html`, `index.html` (generated – never edit by hand), `tests/test_claim_check.py`.
- Data: synthetic only – 3 pre-written alerts, no real bank, customer or AI-model data; analyst IDs instead of names (D16, D24; analyst IDs: `PRODUCT_BRIEF.md`, privacy line).

## Commands

- Install: none (Python 3.9+ only; coaches and recruiters only open `index.html`)
- Run: `python3 app/build.py`, then open `index.html` in Chrome; own phone test (D20, D31, D43 – shares only a folder with `index.html`, never the repo): `mkdir -p /tmp/fraud-demo && cp index.html /tmp/fraud-demo/ && python3 -m http.server 8000 --directory /tmp/fraud-demo` → `http://<Mac IP>:8000/index.html`
- Test: `python3 -m unittest discover -s tests -v`
- Lint or format: none (deliberately left out, D2)
- Build: `python3 app/build.py` (re-run after any change to data, rules or template)

Do not report a command as passing unless it was actually run successfully.

## Product and Design Rules

- Optimize the primary journey for the target user and product context.
- Keep the interface responsive and accessible.
- Include useful loading, empty, success, and error states where relevant.
- Use realistic, non-sensitive demonstration content.
- Identify mocked, generated, estimated, or unverified output clearly.
- Prefer a small coherent product over broad unfinished functionality.

## Working Agreement

- Inspect the current repository and product brief before proposing changes.
- For a substantial milestone, present a short plan, assumptions, expected file
  changes, and verification approach before editing.
- Keep changes within the agreed milestone.
- Explain new dependencies and meaningful architecture decisions.
- Run the relevant checks after implementation and report any unverified work.
- Never commit, push, deploy, delete data, or perform an irreversible action
  without explicit permission.
- Never expose secrets or place sensitive data in source files, logs, examples,
  screenshots, or prompts.

## Definition of Done

A milestone is complete when its acceptance criteria are met, the relevant
checks pass, the journey has been exercised, documentation reflects the current
behavior, and remaining limitations are stated.

---
© 2026 Mohammad Bajbouj. All rights reserved. Product and scope content from the decisions of Mohammad Bajbouj (AI PM) (D8–D32); placeholders filled with Claude by Anthropic (Claude Cowork), confirmed by Mohammad (AI PM) (D29); no ownership of AI-generated text is claimed. Template structure from the neuefische AI PM bootcamp. Practice document; case and data are synthetic.
