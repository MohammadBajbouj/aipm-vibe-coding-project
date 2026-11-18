# Product Brief

> **Reasoning by Mohammad (AI PM), structured by Claude Cowork (D3).** Every line traces to a decision in the project's decision log (D-IDs). v1 approved (D18); updated with Claude Code's challenge (D19–D27). Points that Claude Cowork proposed and Mohammad (AI PM) accepted are marked *(Cowork proposal, accepted)*. Everything in the product is **synthetic** – no real bank, customer or AI-model data.

## Product Summary

**Working name:** Fraud-Alert Explanation Copilot – analyst screen (D1)

**One-sentence value proposition:** The fraud analyst sees everything on one screen – the alert, the copilot's explanation with each reason checked against its record (mismatches flagged), and a non-binding suggestion for release, block or call – so wrong reasons no longer lead to wrong decisions unnoticed (D12).

## User and Problem

**Primary user:** Fraud analyst in a bank's fraud operations team (D10).
Secondary (same screen, no own journey): team lead of the analysts; AI engineer interested in the flagged mismatches (D10). Secondary users get no own features in this mini-project (D27). Extension E1, only after the core slice and quality gate: the team lead reopens a decision after a customer complaint or audit – a new, linked decision, the original stays unchanged (D27).

**Situation and current behavior:** A fraud alert arrives and the analyst gets a notification. They open the app, read the alert and the copilot's explanation, and decide: release, block or call the customer (D11).

**Problem or unmet need:** The analyst cannot see whether the copilot's reasons are supported by the records. In the AI Architecture case (alert A-1042, synthetic) the copilot said "new, unknown device" and "6 times the average", while the records showed a device known for 8 months and about 2 times – the analyst trusted it and blocked a genuine customer's card (D12; case from the AI Architecture handout).

**Evidence we have:** Only the synthetic AI Architecture case (system map, diagnostic register, recovery plan – recovery action 4 "claim check"). No real user research.

**Assumptions that still require research (D17):**
1. Weights for release / block / call are useful to analysts (Mohammad (AI PM)'s assumption). Doubt recorded: no real reference for weights yet – a real weighting method is a capstone question (D22).
2. Analysts want everything on one screen instead of several tools *(Cowork proposal, accepted)*.
3. "Funds available: yes / no" helps the fraud decision *(Cowork proposal, accepted)*.
4. The claim check reduces wrong blocks like A-1042 *(Cowork proposal, accepted)*.

## Core Journey

**Starting point:** Alert list with 3 synthetic alerts (D24): A-1042 (2 × ✗), one with all ✓, one with device data missing (⚠).

**Key user actions (D13, Cowork proposal, accepted):**
1. Alert list – the analyst clicks an alert (e.g. A-1042).
2. Alert screen – payment details, "funds available: yes / no" (D16), the copilot's reasons; next to each reason the record value and a mark: ✓ matches / ⚠ not available / ✗ mismatch.
3. Suggestion – release, block or call, with fixed, pre-written weights labelled "mocked" (D22); above it a warning line, e.g. "Based on the copilot's reasons – 2 of 3 not confirmed by the records" (D22).
4. Decision – the analyst clicks release, block or call and enters a short reason (required, D23).

**Successful outcome:** "Decision saved"; the status is shown ("payment released" / "call planned" / "card blocked") and the alert is marked done in the list (D13, D14). All three decisions mark the alert done; a saved decision is final and read-only, for traceability (D23).

**Important empty or failure state (D13):**
- No open alerts – empty list with a clear message; appears once all 3 alerts are decided (D24).
- Empty reason – saving blocked, message "Please enter a reason" (D23).
- Note on screen: "Demo – decisions are lost when the page is reloaded"; reload = reset (D24).
- Record value missing – "device data not available"; the customer's previously known devices are shown for comparison, labelled "previous devices, not from this payment" (Mohammad (AI PM)'s idea) – plain list of at most 3 devices (name + "known since"), no matching, no marks (D25).

## Scope

### Must Demonstrate

- The core journey above, from alert list to saved decision (D13).
- Claim check per reason: record value next to the copilot's reason, ✓ / ⚠ / ✗ (D12). Rules (D19): yes/no facts – different = ✗; numbers – ✗ if more than 25 % away from the record value; record value missing = ⚠; otherwise ✓.
- Traffic-light colours, always with word + symbol (D15): claim check green ✓ matches / orange ⚠ not available / red ✗ mismatch; status green released / orange call planned / red blocked.
- Non-binding suggestion with mocked weights; only the analyst's click sets a status (D12, D14).
- Empty state and "device data not available" state (D13).

### Explicit Non-Goals (D16)

- Login / authentication (D11).
- Card-owner version (D10) – capstone idea.
- Balance amounts (only "funds available: yes / no").
- Connection to real bank systems – synthetic alerts only *(Cowork proposal, accepted)*.
- Real AI-model call – explanations pre-written and labelled "mocked" *(Cowork proposal, accepted)*.
- Database – decisions kept only while the page is open *(Cowork proposal, accepted)*.
- Real notifications – the alert list is the starting point *(Cowork proposal, accepted)*.

## Acceptance Evidence

| Criterion | How we will verify it |
|---|---|
| After the decision the screen shows the new status: "card blocked" / "payment released" / "call planned" (D14) | Manual walkthrough in Chrome (D9), all three decisions |
| A-1042: "new device" and "6 times" both show ✗ mismatch next to the record values (D14, Cowork proposal, accepted) | Manual walkthrough + one automated check of the claim-check logic (D9) |
| The copilot never sets a status by itself – only the analyst's click (D14, Cowork proposal, accepted) | Manual walkthrough: open an alert, no click → status unchanged |
| Empty, "device data not available" and "Please enter a reason" states appear (D13, D23, D24) | Manual walkthrough with the 3 synthetic alerts |
| At phone width the alert screen stacks into one column and stays readable; decision buttons and reason field reachable with the Tab key (D26) | Chrome at phone width + test on a real phone (D20) |

## Constraints and Risks

- **Data and privacy:** synthetic data only; no balance amounts (D16); analyst IDs instead of names (as in the AI Architecture case).
- **Accessibility:** colour never alone – always word + symbol (D15).
- **Technical constraints:** no new system installs on the MacBook, no Node.js (D8); no browser-test tool – manual tests in Chrome + one automated logic check (D9); the app should also run on other computers, e.g. Windows (D8), and open on a real phone (D20); preferred: one self-contained HTML file, so coaches and recruiters can open it without setup (D21); the claim-check logic must be testable without a browser and without Node.js (D20). Stack decided in M2.
- **Product or trust risks:** mocked explanations and weights could be mistaken for real AI output – they must be labelled "mocked" on screen (D12, D16); weights may increase over-trust in the copilot (assumption 1, D17).

## Capstone Potential

**Why this direction may deserve further investment:** It turns a planned safety measure (claim check, recovery action 4 of the AI Architecture handout) into something an analyst can see and use – a concrete answer to "how do we stop an AI copilot's unsupported claims from reaching a decision".

**What must be learned before treating it as a Capstone candidate:** the four assumptions (D17) with real fraud analysts; a real weighting method (D22); the team-lead reopen journey (D27); whether a card-owner version is possible without revealing fraud rules (D10); how a real AI model and real records would feed the claim check.

---
© 2026 Mohammad Bajbouj. All rights reserved. Reasoning and decisions by Mohammad Bajbouj (AI PM); structured with Claude by Anthropic (Claude Cowork); no ownership of AI-generated text is claimed. Practice document for the neuefische AI PM bootcamp. Case and data are synthetic.
