# Project Instructions for Claude Code

Replace the prompts in angle brackets as the project becomes clearer. Keep this
file concise and current.

## Product

- Target user: <specific user>
- User problem: <situation or task that needs improvement>
- Intended outcome: <what the user can accomplish>
- Core journey: <start, meaningful steps, and success state>
- Current milestone: <the next reviewable product outcome>

## Scope

Required for the current milestone:

- <requirement>
- <requirement>

Explicit non-goals:

- <non-goal>
- <non-goal>

Do not add features outside the current milestone without first explaining why
they are necessary.

## Technical Context

- Stack: <chosen stack and important versions>
- Architecture: <short description of the main components>
- Important paths: <source, tests, data, and documentation locations>
- Data: <synthetic, seeded, public, or other approved source>

## Commands

- Install: `<command>`
- Run: `<command>`
- Test: `<command>`
- Lint or format: `<command>`
- Build: `<command>`

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
