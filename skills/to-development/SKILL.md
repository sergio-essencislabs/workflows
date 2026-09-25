---
name: to-development
description: Supports workflows with authorized TDD delivery, isolated worktrees, dependency-aware concurrency and evidence-based handoff.
user-invocable: false
---

# Bounded implementation

Read the recorded authorization, current GitHub issues and `docs/security.md`.
Without exact issue IDs, concurrency, permitted worktree/repository operations,
verification commands, monitoring arrangement and stop conditions, return the
missing decision to the coordinator's `AskUserQuestion`. Never infer permission
for external writes from local shell access. Run structured authorization checks
where applicable; they are advisory preflight, not sandbox enforcement.

## Dispatch and ownership

Inspect Git status/remotes/worktrees and current issue acceptance criteria.
Create one isolated branch/worktree per issue from the approved base using native
Git tooling; verify the resolved path, actual branch and common repository before
editing. Never reuse a dirty shared checkout, discard changes or write a protected
branch. Recheck branch/worktree identity before each mutation boundary.

Branches use the charter's `branch_prefix` (default `claude/`). Choose the
worktree base before asking the authorization: when `inspect` reports
`path_risk` other than `ok`, propose a short base such as `C:/wt/<project>` in
the authorization question itself instead of discovering a
`'$GIT_DIR' too big` failure afterwards. Any other change of base after
approval goes back to the user through `AskUserQuestion`.

Refresh the plan from GitHub and run `workflow.py schedule --plan <file> --limit
<approved-limit>`. The result is a recommendation, not proof of authority. Start
all eligible non-conflicting issues up to the ceiling with supported generic
subagents or separate supported sessions. Give each a bounded outcome, owned
paths, tests, checkpoint path and no authority to expand scope. Tell workers they
share the codebase and must preserve others' changes. Hide internal worker names.
If concurrent sessions/tools are unavailable, report the capacity limitation.
Do not silently serialize for convenience. Isolate ports, databases and test data
as well as Git. Recompute readiness and refill free slots after each completion.

An issue is `verified` for dependency readiness only when its acceptance evidence
is current and its required changes are present in the dependent issue's approved
base. An unmerged PR alone does not meet this condition. Stacked bases/cherry-picks
need the recorded repository-operation authorization; otherwise park dependents.

## TDD loop

For one acceptance behavior: write/adjust the test, run it, capture the actual
expected failure, implement the minimum change, then rerun focused tests. An
import error or broken harness is not the intended behavioral red. Fix the harness
and obtain a meaningful failing assertion. Preserve commands, exit codes, counts
and output paths. Never invent failure evidence for a nontestable documentation
change; state the exception and verify the relevant behavior another way.

Run relevant broader tests and actual type checks discovered from repository/CI;
do not assume npm scripts. If no type checker exists, say so and record applicable
syntax/build checks. Inspect the full vertical behavior, diff, regressions and
acceptance coverage. Tests may execute arbitrary code; native permission and
sandbox controls still apply. Unexpected effects stop the affected issue.

## Review, checkpoints and renewal

Require an independent reviewer to inspect the current diff and test evidence.
They must not author the changes under review. Bind review to `workflow.py
evidence --root <worktree>` hashes/HEAD; any change invalidates review. If no
independent reviewer is available, report "implemented, awaiting independent
review", not completed. Do not manufacture reviewer identities or approvals.

Save compact `templates/handoff.md` and a machine-readable checkpoint before each
session renewal. Include the issue URL and acceptance snapshot, repository map,
decisions, changed files, commands/results, review evidence, blockers and next
concrete step. `workflow.py checkpoint` records the issue snapshot, handoff and
current Git evidence; `workflow.py resume` detects drift without overwriting it.
Read both the human handoff and current issue/diff in the fresh session.

Check context using measured accumulated session usage plus a conservative next
step reserve, not remaining context after compaction. Target renewal near 100k;
stop before 150k. Unknown telemetry means no unattended continuation. The helper
checks reported numbers, not the host's actual token meter. If the host cannot
enforce renewal, explicitly report that hard-cap AFK acceptance is unproven.

Update GitHub checkpoints/status only if authorized and supported by current
evidence. Draft PRs also require charter permission and native approval. Never
merge, deploy, release, delete data or close issues as routine AFK work. Park
blocked issues with the precise pending question and continue independent ones.
Report each issue's state, branch/PR, exact tests/results, review evidence,
remaining risk and next action. Leave worktrees and evidence intact for recovery.
