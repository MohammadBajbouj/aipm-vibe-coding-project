# Product Showcase – Fraud-alert claim check

*Status: drafted by Claude Cowork, confirmed by Mohammad (AI PM) (D58). "D" = decision ID in the local decision log (`my_notes/decision_log.md`); key decisions in [DECISIONS.md](DECISIONS.md).*

## Product Story

**User and problem:** A fraud analyst in a bank's fraud operations team (D10). When a fraud alert arrives, the analyst cannot see whether the AI copilot's reasons are supported by the records. In the synthetic case A-1042 a wrong reason led to blocking a genuine customer's card (D11).

**Value demonstrated by the mini-project:** On one screen the analyst sees the alert, each copilot reason checked against its record value (✓ matches / ⚠ not available / ✗ mismatch) and a non-binding suggestion – and then decides: release, block or call (D12, D14).

**Why this scope was chosen:** The claim check closes the gap found in Mohammad (AI PM)'s earlier AI Architecture handout (D12). Everything not needed to show this was left out: login, real bank data, a real AI model, database, notifications, balance amounts (D16).

## Core Journey

Alert list (3 synthetic alerts) → open A-1042 → see 2 × ✗ next to the record values → enter a short reason → Block → "card blocked", alert marked done → decide the other 2 alerts → "No open alerts – all alerts are decided" (D13, D37).

Screenshots: [A-1042 – two reasons not confirmed](assets/screenshot-alert-a1042.png) · [A-1044 – device data not available, previous devices listed](assets/screenshot-alert-a1044.png)

## Evidence

### Product Evidence

- **Acceptance criteria checked:** status shown after each decision; A-1042 shows "mismatch" for "new device" and "6 times"; the copilot never sets a status – only the analyst's click (D14); colour always with word + symbol (D15); phone width stacks into one column (D26).
- **Feedback or observations:** two walkthroughs by Mohammad (AI PM) on the Mac and his own phone (D40) – phone test over the home Wi-Fi, link opened by QR code (Mohammad (AI PM)'s idea, D36), server log shows the phone loaded `index.html` (reply 05); Mohammad (AI PM) also e-mailed `index.html` to himself and opened it on his phone – "it's working well" (2026-11-18), so the file works on a phone without Wi-Fi server or link (sharing via Discord not yet tested); Tab-key check in Safari (D44); independent review of the brief and 2 screenshots by Gemini (Google), which explained user and value correctly without help.
- **Important edge cases reviewed:** empty reason → "Please enter a reason"; no decision chosen; device data missing (⚠) with up to 3 previous devices (D25); empty list after all decisions; double click cannot save twice (Claude Code review, reply 07).

### Technical Evidence

- **Install and run verification:** no install needed – `index.html` opens in any browser, also offline. Clean-start run by Claude Code: build OK, generated `index.html` identical, no external requests (reply 08b).
- **Tests, lint, type checks, or build commands completed:** `python3 -m unittest discover -s tests -v` – 22 of 22 pass (Claude Code, 2026-11-18, Python 3.9.6, reply 09). Build `python3 app/build.py`. Lint left out on purpose (D2).
- **Environment or behaviour not verified:** Windows; screen readers; Chrome on the Mac (did not open – Safari used, D44); Gemini setup test of the README still pending (D45).

## Working with Claude Code

**Where Claude Code accelerated the work:** It proposed the simplest stack – the claim-check rule exists only once, in Python, and a build script writes one self-contained HTML file (D30). Round 1 (app, data, claim check, test, core journey) took about 20 min against 50 min planned.

**Where human review changed or rejected its proposal:** Claude Code proposed a 50 % tolerance for number mismatches; Claude Cowork changed it to 25 %, approved by Mohammad (AI PM) (D19). Mohammad (AI PM) rejected a permanent permission for Claude Code to run the QR-code command on his Wi-Fi (D38).

**Most important lesson about directing Claude Code:** Work only through written handovers that list exactly what is allowed and trace each instruction to a decision ID. The agent then stops where it should: Claude Code's own permission check blocked the QR-code command and it did not retry; Mohammad (AI PM) ran it himself (D36). In the other direction, Claude Code improved a Claude Cowork handover by serving only a copy of `index.html` instead of the whole repo (reply 05; later fixed for good, D43).

## Known Limitations

- Weights are fixed and mocked – A-1042 still suggests "Block 70 %" although 2 of 3 reasons are not confirmed (D22, D46).
- "Decided by" shows the assigned analyst ID, not who clicked – there is no login (D48, D11).
- Decisions are lost on reload – no database (D24, D16).
- Copilot reasons are pre-written; there is no real AI model call (D16).
- Backlog: "required" mark on the reason field, 200-character hint, focus after "Back", list button size on phones, tab icon (D39, D47).

## Bridge to the Capstone

**What is worth carrying forward:** the claim check as a trust feature (reason → record value → ✓ / ⚠ / ✗); one place for the rule; decisions that are final and traceable; the human decides, the copilot only suggests.

**Research or validation still required:** the 4 assumptions of the brief (D17) – weights are useful; analysts want everything on one screen; "funds available yes / no" helps; the claim check reduces wrong blocks like A-1042.

**Data, architecture, testing, accessibility, security, or governance work that would be needed:** a real weighting method that reacts to failed checks (D22, D46); real or realistic record data and a model that returns structured claims; storage with an audit trail; login with roles, incl. the team-lead reopen (E1, D27); automated browser and screen-reader tests; privacy and access rules for customer data; a card-owner version must never reveal fraud rules (D10).

**Recommended next product experiment (Claude Cowork proposal):** a short usability test with 3–5 fraud analysts on A-1042-like cases, with and without the claim check – success criterion: fewer wrong blocks and the same or shorter decision time.

---
© 2026 Mohammad Bajbouj. All rights reserved. Decisions by Mohammad Bajbouj (AI PM) (D-IDs as cited); drafted with Claude by Anthropic (Claude Cowork); app, tests and evidence by Claude Code; reviewed by Gemini (Google); no ownership of AI-generated text is claimed. Practice project for the neuefische AI PM bootcamp. All data is synthetic.
