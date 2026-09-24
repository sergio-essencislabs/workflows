---
name: to-issues
description: Supports workflows by decomposing an approved PRD into vertical GitHub issues with explicit dependencies and approval before publication.
user-invocable: false
---

# Vertical issue planning

Read the approved PRD revision and current GitHub issues/board. Reuse an existing
matching issue when its acceptance scope fits; never create duplicate local GTs.
Use `templates/issue.md` and `examples/plan.json`. Before publication, temporary
integer IDs are proposal IDs only; remap every dependency to real GitHub numbers
after creation and verify links. Local status is always a timestamped snapshot.

Each issue must have outcome, boundaries/non-goals, observable acceptance,
tests, dependency IDs, concrete ownership (or `*` when unknown), risks and a
session-sized end-to-end demonstration. Do not split by UI/API/database layers.
For an observation editor, prefer "save one observation and see it after reload"
with UI/API/storage/tests in one slice, then "edit with conflict feedback", then
"filter observations". If the proposal starts as database/backend/frontend
tickets, correct it yourself before presenting it; no extra user prompt needed.
A genuine prerequisite must expose a working seam tested by a named consumer.

Run `workflow.py validate-plan --plan <plan.json>`; this checks structure and DAG,
not semantic verticality. Review every vertical demonstration manually. Check
missing cross-layer tests, hidden sequencing, generated/shared files, migrations,
ports, shared services, dependency cycles and context size. Add dependencies or
shared ownership for resources that cannot safely run together. Split oversized
issues into independently acceptable outcomes. See `evals/vertical-slices.md`.

Present the complete plan and graph. Ask approval through `AskUserQuestion` for
the exact issue creation/update scope before any write. Use installed GitHub
tools or `gh issue create/edit --repo <approved-repo> --body-file <file>` with
literal UTF-8 bodies, not interpolated shell strings. Keep native permissions.
If a network response is uncertain, reread/list issues before retrying to avoid
duplicates. Record partial publication and resume remaining writes idempotently.

Put `Depends on: #N, #M` in each canonical issue body (or `none`); verify dependency
IDs and content after publication. Link local snapshots to returned issue URLs.
An issue update preserves user text outside the approved plan. Surface divergence
between approved draft and GitHub rather than overwriting it silently. Return
verified issue links/graph to the coordinator for batch authorization.
