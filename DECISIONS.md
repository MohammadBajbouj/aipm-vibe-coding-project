# Product and Build Decisions

Six decisions that shaped the fraud-alert claim check prototype. Full log with all 54 decisions (D1–D54): kept locally in `my_notes/decision_log.md`. "D" = decision ID in that log; quotes are Mohammad (AI PM)'s approval words, copied from the log.

*Status: drafted by Claude Cowork, confirmed by Mohammad (AI PM) (D58).*

### 1. Check every copilot reason against its record (core of the product)

- **Context:** In the synthetic case A-1042 a wrong copilot reason led to blocking a genuine customer's card. The analyst could not see whether the reasons were supported by the records (D11, D12).
- **Claude Code proposal:** none – the idea came from Mohammad (AI PM)'s earlier AI Architecture handout; Claude Cowork proposed the "claim check" wording.
- **Decision (D12):** "It would point to this is what I was looking for in terms of improvement, and this is what was missing in the AI architecture repo. So include point two too."
- **Reason:** The missing check was the gap found in the previous handout.
- **Consequence:** Each reason shows ✓ matches / ⚠ not available / ✗ mismatch next to its record value; the analyst decides.

### 2. Claim-check rule: 25 % tolerance instead of 50 %

- **Context:** When does a number in a reason count as a mismatch?
- **Claude Code proposal:** ✗ if more than 50 % away from the record value.
- **Decision (D19):** "Yes, approved." – with the tolerance changed to 25 % (Claude Cowork's change).
- **Reason:** 50 % would let clearly wrong reasons pass as "matches".
- **Consequence:** Rules: yes/no facts – different = ✗; numbers – ✗ above 25 %; record missing = ⚠; else ✓. A-1042 shows 2 × ✗.

### 3. Simplest stack: one Python rule, one self-contained HTML file

- **Context:** The app must open on Mac, Windows and phones without installs, so coaches and recruiters can open it (D21); no Node.js (D8).
- **Claude Code proposal:** Option C of three – the rule exists only in Python; a build script writes one self-contained `index.html`.
- **Decision (D30):** "I said already. OD11, option C, approved."
- **Reason:** The rule exists in one place only, so it cannot drift between two languages; no server, no packages.
- **Consequence:** Standard-library Python only; an installed mobile app is a later expansion.

### 4. Fixed, mocked weights with a warning line

- **Context:** The suggestion (release / block / call) needs weights, but there is no real model.
- **Claude Code proposal:** keep the weights fixed and pre-written per alert (no recalculation), add a warning line above the suggestion ("Based on the copilot's reasons – 2 of 3 not confirmed by the records"), label reasons and weights "mocked".
- **Decision (D22):** "Okay, we make this for the simulation. We give a weight, fixed weight, not dropping it, and the message. Like in the future, if this app to be used, there will be weighting method"
- **Reason:** A prototype should not pretend to compute weights it cannot justify.
- **Consequence:** Weights labelled "mocked". Known limitation: A-1042 still suggests "Block 70 %" under 2 unconfirmed reasons (D46) – a real weighting method is a Capstone question.

### 5. A saved decision is final and read-only

- **Context:** Can the analyst change a decision after saving?
- **Claude Code proposal:** all three decisions mark the alert done; reason required (empty → "Please enter a reason"); saved decisions final and read-only.
- **Decision (D23):** "especially like C, which is save decision is final with no editing for the traceability. So I approve all."
- **Reason:** Traceability (Mohammad (AI PM)); the required reason also gives the app an error state.
- **Consequence:** Short reason required ("Please enter a reason"); decided alerts stay viewable as "done" (D37). Team-lead reopen = extension E1, later (D27).

### 6. Phone test shares only the app, never the repo

- **Context:** The own phone test served the whole repo folder on the home Wi-Fi, including notes and git data.
- **Claude Code proposal:** review finding R4 – serve a folder that contains only `index.html`.
- **Decision (D43):** "b" – fix in M5 together with the README.
- **Reason:** No private project files on the network.
- **Consequence:** README and `CLAUDE.md` use the safe command.

---
© 2026 Mohammad Bajbouj. All rights reserved. Decisions by Mohammad Bajbouj (AI PM) (D-IDs as cited); drafted with Claude by Anthropic (Claude Cowork); proposals by Claude Code; no ownership of AI-generated text is claimed. Practice project for the neuefische AI PM bootcamp. All data is synthetic.
