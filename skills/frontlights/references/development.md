# Bounded implementation

Read the recorded authorization, current GitHub issues and `docs/security.md`.
Without exact issue IDs, concurrency, permitted worktree/repository operations,
verification commands, monitoring arrangement and stop conditions, return the
missing decision to the coordinator's `AskUserQuestion`. Never infer permission
for external writes from local shell access. Run structured authorization checks
where applicable; they are advisory preflight, not sandbox enforcement.

## Dispatch and ownership

Inspect Git status/remotes/worktrees and current issue acceptance criteria. The
scope of a dispatch is the family: the issue and all its open sub-issues
(`SKILL.md`, "An issue and its sub-issues move together"), each with its own branch
and worktree; the parent never goes alone unless the user chose that. Create one
isolated branch/worktree per issue from its approved base (the approved base
branch, or its dependency's branch when stacked, see below) using native
Git tooling; verify the resolved path, actual branch and common repository before
editing. Never reuse a dirty shared checkout, discard changes or write a protected
branch. Recheck branch/worktree identity before each mutation boundary.

Branches use the charter's `branch_prefix` (default `claude/`). Choose the
worktree base before asking the authorization: when `inspect` reports
`path_risk` other than `ok`, propose a short base such as `C:/wt/<project>` in
the authorization question itself instead of discovering a
`'$GIT_DIR' too big` failure afterwards. Any other change of base after
approval goes back to the user through `AskUserQuestion`.

Refresh the plan from GitHub and run `frontlights.py schedule --plan <file> --limit
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
base. An unmerged PR alone does not meet this condition, unless the dependent's
approved base is that very branch (stacking, below). Cherry-picks and stacked bases
need the recorded repository-operation authorization; without it, park the
dependents. `schedule` only reads `status`, so it cannot see an issue that depends
on two unmerged branches: that check is manual (below). With many ready issues that
share ownership or use `*`, its exact search can take minutes (about 150 s for 23
issues), so give the command a longer timeout.

## Stacked branches: parent and children without waiting for the merge

Making children wait for the parent's merge serializes the family behind a human
step. So, whenever an issue of the family depends on another one (a child that
lists its parent in `Depends on`, or a sibling chain), stage 6 offers to **stack**
the dependent on its dependency's branch, in the same `AskUserQuestion` call as
the concurrency and the authorization. The question is "Como as filhas se apoiam
no pai?", with "Empilhadas no pai (Recomendada)" first (each child branches from the
parent's branch and its PR targets that branch) and "Esperar o merge do pai" second
(each child starts from the approved base once the parent is merged). Its text warns
that a squash-merge of the parent makes the later merge of the base conflict on the
hunks the child shares with it, and that merging the parent PR with a merge commit
avoids that; how to merge stays with the human. Record the answer verbatim in the
authorization, with the repository operations it needs: branch from a branch that is
not the base, push it (and the dependency's branch), open a draft PR whose base is the
dependency's branch, retarget that PR, `git merge` of a base into the issue's own branch, and `git merge` of a family's verified
branches into a local integration branch that is never pushed. Those are the only merges it allows: it never covers merging a PR, writing
the base branch, deploying or releasing. Without the stacking answer, a dependent
stays parked until its dependency is in the approved base.

**Concurrency.** Recommend as ceiling the number of independent children whose
`ownership` does not overlap, and never less than the first wave. Read the stacked
wave from `schedule --limit 24` run on a throwaway copy of the plan in which the
parent is marked `verified`; the real plan is not edited. Children whose
ownership overlaps do not run together: `schedule` serializes them, and the
question says so.

**Rules.**

- A child leaves its dependency's branch once the dependency is `verified` on it
  (acceptance evidence current for that branch's HEAD, tests green); an independent
  review still pending does not hold it back. Create the child's worktree from that
  exact commit (`git worktree add -b <branch_prefix><name> <path> <sha>`), record the
  `<sha>` in the handoff and in the plan, and only `"base": "<dependency-branch>"` in
  its worktree entry of the authorization (the commit does not exist when the
  authorization is approved, so it never goes there). Confirm with `git merge-base
  --is-ancestor <sha> HEAD`.
- Stack on one dependency only. An issue that depends on two unmerged branches, unless
  one already contains the other (a sibling stacked on the parent, say), is
  parked and the question goes to the user; `schedule` does not detect it, so read
  each dependent's `Depends on` yourself. Children of one parent stack on the
  parent, never on each other; a child that needs a sibling's code lists it in
  `Depends on` and stacks on that sibling's branch.
- Push the dependency's branch before the child's PR: the base must exist on the
  remote and be current, or the child's diff would carry the dependency's unpushed
  commits. The child's draft PR has that branch as base (`gh pr create --draft --base
  <dependency-branch>`) and names in its body the PR it is stacked on, so the review
  sees only the child's own diff. Draft PRs keep the permission and native approval of
  the charter.
- When the dependency's branch moves after the child started (review fixes), the
  child brings it in with `git merge <dependency-branch>`, reruns its tests and
  refreshes the evidence; the new hashes invalidate the earlier review. Check
  `git merge-base --is-ancestor` at each material boundary.
- After a human merges the parent PR, run `git fetch origin` and retarget each child
  PR to the base the parent's PR merged into (`<parent-pr-base>`, which is the
  approved base branch and not always the default one). GitHub usually does it when
  the parent branch is deleted on merge; reread the PR's base to confirm, otherwise
  `gh pr edit <child-pr> --base <parent-pr-base>`. Then bring the base in with `git
  merge origin/<parent-pr-base>` and rerun the tests. Use a merge, never a rebase or a
  force-push. A merge commit of the parent merges cleanly; a squash or rebase merge
  rewrites its commits, so conflicts on the hunks the child shares with the parent are
  expected: resolve them in the merge commit, keeping the child's own changes on top of
  the parent's content that the base already has, and show those hunks to the reviewer.
  The merge changes HEAD, so refresh the evidence and have the reviewer look again; what
  remains to review is the child's own diff.
- A conflict on anything beyond the parent's own content already in the base, or a
  dependency closed without being merged, is a stop condition: park the child and ask.

## Integrating a family before its PRs

Each branch passing alone does not prove the family works together: a test of one child
can assert the very behavior another child changes on purpose, and a clean Git merge
does not make a green suite. Before any PR of a family with more than one branch is
opened, integrate it locally: an integration worktree from the parent's branch that
merges every verified child branch (local only: never pushed, never a PR), then run
the full relevant suite, the type checks and, when a member turns it on, the browser
test on it. Findings follow the destination ladder; a fix goes to the branch that owns
the file, never to the integration branch, and the integration is redone after it.
The PRs open only after an integration with a green suite, and each branch still needs
its own current review (`review-gate`). Record the integration worktree, the merged
HEADs and the results in the handoff. The integration branch is evidence, never delivered.

## Test-driven development

TDD is the red → green loop. This section is the reference that makes that loop
produce tests worth keeping: what a good test is, where tests go, the
anti-patterns and the rules of the loop. Every subsection applies on every cycle:
consult them before and during the loop, not after.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and
interface vocabulary match the project's domain language, and respect ADRs in the
area you're touching.

Follow the conventions recorded in the issue's `## Approach and conventions` and
in the discovery log: structure, naming, error handling, libraries and test
style of the surrounding code. Break a convention only where that section names
the approved break. Finding mid-work that the pattern is concretely worse, or
that the approved approach does not fit, parks the issue and returns the
question to the coordinator's `AskUserQuestion`; never switch approach or
pattern silently.

### What a good test is

Tests verify behavior through public interfaces, not implementation details. Code
can change entirely; tests shouldn't. A good test reads like a specification:
"user can checkout with valid cart" tells you exactly what capability exists, and
it survives refactors because it doesn't care about internal structure. See
[tdd-tests.md](tdd-tests.md) for examples and [tdd-mocking.md](tdd-mocking.md) for mocking
guidelines.

### Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe
behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** The seams under test are part of each issue
(`## Seams under test` in `templates/issue.md`) and were approved when the issues
were published. You can't test everything; agreeing the seams up front is how
testing effort lands on the critical paths and complex logic instead of every
edge case. Before the first test, restate the issue's seams in the handoff. No
test is written at an unconfirmed seam. If the issue lists none, a listed seam
does not exist or cannot observe the acceptance behavior, or the shape of the
interface is itself in question (how deep the module is, where the seam belongs,
what it should expose), park the issue and return the question "What's the public
interface, and which seams should we test?" to the coordinator's
`AskUserQuestion`. Continue independent issues meanwhile.

### Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private
  methods, or verifies through a side channel (querying the database instead of
  using the interface). The tell: the test breaks when you refactor but behavior
  hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code
  does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way,
  a constant asserted equal to itself), so it passes by construction and can
  never disagree with the code. Expected values must come from an independent
  source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk
  tests verify _imagined_ behavior: you test the _shape_ of things rather than
  user-facing behavior, the tests go insensitive to real changes, and you commit
  to test structure before understanding the implementation. Work in **vertical
  slices** instead: one test → one implementation → repeat, each test a **tracer
  bullet** that responds to what the last cycle taught you.

### Rules of the loop

- **Red before green.** Write the failing test first, run it and capture the
  actual expected failure, then write only enough code to pass it and rerun the
  focused tests. Don't anticipate future tests or add speculative features.
- **The red must be behavioral.** An import error or broken harness is not the
  intended red. Fix the harness and obtain a meaningful failing assertion.
- **One slice at a time.** One seam, one test, one minimal implementation per
  cycle, each tied to one acceptance behavior.
- **Refactoring is not part of the loop.** It belongs to the review stage below,
  not the red → green implementation cycle.
- **Evidence is real.** Preserve commands, exit codes, counts and output paths.
  Never invent failure evidence for a nontestable documentation change; state the
  exception and verify the relevant behavior another way.

### After the loop

Run relevant broader tests and actual type checks discovered from repository/CI;
do not assume npm scripts. If no type checker exists, say so and record applicable
syntax/build checks. Inspect the full vertical behavior, diff, regressions and
acceptance coverage. Tests may execute arbitrary code; native permission and
sandbox controls still apply. Unexpected effects stop the affected issue.

When the issue's `## Navegador e testes ligados` turns tests on, follow
[browser-testing.md](browser-testing.md) before review, starting with its question
"pronto para assistir?" and, after a watched run, ending with the user's choice of
watching again, approving, asking for a change or going on; its records join the
evidence below.

## Review, checkpoints and renewal

Require an independent reviewer to inspect the current diff and test evidence.
They must not author the changes under review. Bind review to `frontlights.py
evidence --root <worktree>` hashes/HEAD and save that output with the review result
(`.frontlights/issues/<n>/review.json`). Run `frontlights.py review-gate --root
<worktree> --review <review.json>` before reporting an issue as reviewed, before
opening or updating a PR and after every commit: exit code 0 means the review still
covers the code, exit code 2 means it is stale. Any commit, edit or new file after the
review makes it stale (bringing a base into the branch included), whatever its size:
rerun the suite, take new evidence and have the independent reviewer look again. A
stale review is never reported as reviewed. If no
independent reviewer is available, report "implemented, awaiting independent
review", not completed. Do not manufacture reviewer identities or approvals.
Classify the review's findings, and those of tests and live checks, by the
destination ladder of the Follow-ups section in `issues.md` (same PR, checklist in
the source issue, sub-issue, top-level issue only for new scope), decided as one batch.

Refactoring happens here. The reviewer may recommend refactors of the green code;
the author applies them without changing behavior or adding tests at new seams,
reruns the full relevant suite and type checks, and records fresh evidence. The
new hashes invalidate the earlier review, so the independent reviewer reviews
again before the issue can be reported as reviewed.

Save compact `templates/handoff.md` and a machine-readable checkpoint before each
session renewal. Include the issue URL and acceptance snapshot, repository map,
decisions, changed files, commands/results, review evidence, blockers and next
concrete step. `frontlights.py checkpoint` records the issue snapshot, handoff and
current Git evidence; `frontlights.py resume` detects drift without overwriting it.
Read both the human handoff and current issue/diff in the fresh session.

Check context using measured accumulated session usage plus a conservative next
step reserve, not remaining context after compaction. Target renewal near 100k;
stop before 150k. Unknown telemetry means no unattended continuation. The helper
checks reported numbers, not the host's actual token meter. If the host cannot
enforce renewal, explicitly report that hard-cap AFK acceptance is unproven.

Update GitHub checkpoints/status only if authorized and supported by current
evidence; tick an acceptance criterion in the issue body only with evidence for it
(a test, a measured result, a reviewed diff), because the closeout of stage 7 trusts
the ticks. Closing an issue and moving its card are never part of this: they have
their own approval (`references/closeout.md`). Draft PRs also require charter permission and native approval. Never
merge a pull request, write the base branch, deploy, release, delete data or close
issues as routine AFK work; the only merges allowed are the ones the stacking authorization names: of a base into an issue's own
branch, and of a family's verified branches into a local integration branch that is never pushed. Park
blocked issues with the precise pending question and continue independent ones.
Report each issue's state, branch/PR, exact tests/results, review evidence,
remaining risk and next action. Leave worktrees and evidence intact for recovery.
