# Live acceptance runbook

Use a separate disposable GitHub repository/project with actual configured RoadS
planning input, or a real project the user names for it. Creation and mutations require
the user's explicit scope. Do not use a production environment as a fixture. Record run timestamp,
CLI/plugin version, session identity, repository/issue URLs, commits and outputs.

1. Load with `--plugin-dir`, inspect `/help`, invoke `/frontlights` and
   verify a single plugin skill, hidden from the menu, whose stage files live in
   `skills/frontlights/references/`. Confirm stage 0 asks nothing and only shows
   the `claude rc` guidance when no host runs,
   every question has options, and all user-facing text is in Portuguese. Native static validation
   alone is not proof of interactive skill invocation.
2. Read real observations and existing issues; include an unavailable-source case
   and a duplicate proposed outcome. Verify no mutation occurred during discovery.
3. Interview, approve a PRD revision and inspect the proposed issues. Decline one
   publication approval; confirm no issues were written. Approve the final plan.
4. Run the horizontal-ticket input from `vertical-slices.md`; inspect the revised
   vertical outcomes before publication. Record the actual transcript and judgment.
5. Authorize two independent slices plus a third dependent/overlapping slice with
   concurrency two. Confirm distinct worktrees and overlapping execution of the
   first pair. Confirm the third waits for verified integration and no slot overrun.
6. Inspect real red/green/broader/type-check output and exact-diff independent
   review. Change a file after review and verify completion waits for re-review.
7. Trigger early renewal; read fresh issue, diff and durable handoff in a new
   session. Exercise changed issue scope. If trustworthy token telemetry and
   pre-limit renewal cannot be enforced, mark hard-cap acceptance blocked.
8. Connect the phone with native Remote Control in the current session. Ask a
   queued decision and exercise a native permission prompt. A human confirms
   receipt and response; visible prompts alone are not approval.
9. Attempt harmless simulations of unauthorized issue/repository/branch writes,
   merge, deploy, release and unrelated external mutations. Do not execute real
   destructive commands. Verify native controls stop these, not just helper
   predicates. Where exact scoping is unavailable, record the limit and keep
   external writes gated; do not label full AFK acceptance passed.
10. Restart without the plugin and verify the project data and its Git history remain intact
    (this plugin does not depend on GuardianS or alter it; nothing of it is checked here).
11. Learning mode. Answer "Ligado" to "Ativar o modo aprendizado?" in the same
    call as the depth. Confirm `references/learning.md` was read before the first
    explanation, and that each technical question is preceded by chat text with
    the concept in plain words, why the project does it that way, a commented
    excerpt with its path (about fifteen lines, no secrets) and what each option
    changes. Confirm one "Ficou claro?" shares the call with at most three
    decisions, and that no call ever holds more than four questions. Answer
    "Entendi" once and confirm the decisions stand. Pick "Explicar de outro
    jeito" twice: the decisions in that call are asked again, and "Seguir a
    recomendação" (its description says the decision is marked "a revisar")
    appears only after the second re-explanation and records the decision as
    "tomada pela recomendação, a revisar" under Decisions and Open decisions,
    and as the first branch offered at the closing. Repeat with "Desligado": the solution round shows exactly
    three approaches plus "Explicar antes de decidir". Pick that option on one
    of several questions in a call: the explanation comes, the same question
    returns without the option together with the check, and the other answers
    stand. Confirm no explanation or excerpt contains a secret, the discovery
    log records the mode and one row per concept, and the explanations are
    readable on the phone. The textual tests only prove these rules are written
    down; this step proves they are followed.
12. Issue family and stacked branches. Start from a disposable issue with three open
    sub-issues (one depends on the parent, one labelled `needs-decision`) and one
    closed. Confirm the stage 2 line names the open ones, the grilling gives the
    pending one its own solution round, every body has `## Camadas da fatia`, and the
    stage 6 call carries the stacking question with the recommended option first and
    a concurrency equal to the independent children. Authorize stacking and confirm
    the child worktree starts from the parent's branch (`git merge-base --is-ancestor`),
    its draft PR has that branch as base, and nothing is merged. After a human merges the
    parent, confirm the PR is retargeted and the base comes in by merge, with no rebase
    or force-push.
13. Watched browser run. On an issue that touches the frontend, confirm the "pronto
    para assistir?" question comes before any window opens, the window is a visible
    Chrome, the strip reads "ANTES: main" and then "DEPOIS: branch <name>", each case
    runs twice, popups stay long enough to read, and the window stays open about
    45 s at the end. Move a test user to a restricted profile through the product's
    endpoint and confirm the row is identical after the undo. Confirm another
    session's server on a fixed port is left running and the question is asked.

14. Closeout. After a human merges a worked family, start `/frontlights`: the closeout question of stage 1 appears
    only when open issues of this project have every acceptance criterion ticked (and their children closed or
    listed). Confirm the table lists children before parents with the PRs (open, merged or none), the current card
    status and the exact commands. Answer "Não agora" once and confirm nothing was written. Approve and confirm
    each issue is closed as completed and its card is in Done, children first, and that `closeout.py verify`
    reports every issue ok. An issue with an unticked criterion, no criteria section or an open child that is not itself
    in the list must never appear in the list, and a `gh` without the project scope must be reported with the close-only fallback.

15. Completed items in the files. With roadmap sync configured and an item of the current sprint in Done on the board, press
    Sincronizar in RoadS, then run `/frontlights` and answer yes to the roadmap question. Confirm the diff shows the item as
    "concluída" with the sync date in the ROADMAP.md and in the sprint file, that nothing is acknowledged to RoadS when only
    completions are in the plan (`ack: not_needed`), that approving writes them with backup and verified markers, that a
    second sync does not propose them again, and that `markCompleted: false` stops it.

Only after all required checks pass, present the linked evidence and ask, via AskUserQuestion,
whether to declare the version accepted. Items the environment cannot enforce (an exact
scope for external writes, a measured context cap) are recorded as documented limits, never as passed.
