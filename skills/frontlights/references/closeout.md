# Closing finished issues

Read this when the stage 1 closeout question is answered yes, when a family worked in stage 6 is
reported merged, or when the user asks to close or move finished issues. Everything the user reads
stays in Portuguese. Closing is a write on GitHub with **its own approval**: no implementation
authorization, no merged PR and no green test stands in for it. The helper only reads; the session
writes, with its own `gh`, and only what the user approved.

## 1. Find the candidates (read only)

```powershell
python "${CLAUDE_PLUGIN_ROOT}/scripts/closeout.py" candidates --config <config> --root <project>
python "${CLAUDE_PLUGIN_ROOT}/scripts/closeout.py" candidates --config <config> --root <project> --issues 12,13
```

By default the scope is the issues this project worked on with Frontlights (the folders of
`.frontlights/issues/`, the `issue_ids` of the authorizations and the ids of `plan.json`) plus all
their sub-issues, down the tree. `--issues` names an explicit list. `--all` sweeps every open issue of the
repository and is used only when the user asks for it. With no repository or no `gh`, say in one line that
the check could not run and go on.

An open issue is a **candidate** only when it has an acceptance-criteria section and every criterion of it is
ticked, and every one of its sub-issues is closed or a candidate in the same batch (children close before
their parents). A closed issue whose card is not in Done is a candidate to be moved only. Each candidate
carries its `action` (`close`, `close_and_move`, `move_only`), the criteria count, its PRs (state and
whether merged), its card status and `cautions`: `open_pr`, `no_pr`, `not_on_board`, `already_done_card`.
The cautions inform; they never block, and an `open_pr` is called out in the question.

`excluded` lists what is not ready and why (`unchecked_criteria` and `no_criteria` with the counts,
`open_children` with the children, `truncated` when a list was cut, `not_found` and `unreadable`): that
needs work or a decision, not closing. `order` is 1-based and is the order to close in. `closedUnchecked`
counts closed issues whose card could not be checked because the board was not readable, and `alreadyDone`
counts the closed ones that need nothing. Tell the user briefly, never propose it. Ticking a criterion belongs
to the verification of the issue, with evidence (a test, a measured result, a reviewed diff), under the
authorization for routine issue updates; this step trusts the ticks and never ticks one itself.

`board.status` says whether cards can be moved: `unconfigured` (no board: close only), `not_read` (nothing in
scope, so the board was not read), `unavailable` (a `gh`
without the `project` scope: say so, give `gh auth refresh -s project`, close only),
`done_option_missing` (the board has no option named as `project.done`: show the field and its real options
and ask which one is Done; recording the answer in `.frontlights/config.json` as `project.done` is a local
write, shown first). Without `project.done` the pair is `Status` / `Done`.

## 2. Show the list and ask

Show in the conversation, in full and in the user's language, one table with a row per candidate (number,
title, top-level or sub-issue, criteria n/n, children, PRs, card status → Done, action, cautions) in the
`order` of the result, and the exact `commands` that will run. Send the same text as a file with the host's
file-sending tool when one exists, and put it in the `preview` of the approve option (show-before-approval,
`SKILL.md`). Then ask with `AskUserQuestion`: "Fechar estas <N> issues e mover os cartões para Done?" with
"Sim, fechar e mover tudo" first and recommended (recommend "Escolher quais" instead when some candidate has
`open_pr`), "Escolher quais" (a follow-up question with the candidates, at most four per call), "Só fechar,
sem mover" and "Não agora". "Não agora" writes nothing and the question comes back in a later
session only if the list changed. Record the answer verbatim with a reference; never answer for the user.

## 3. Write what was approved

In the `order` of the result, for each approved issue run the `commands` exactly as given, each value as one
double-quoted argument: first `gh issue close <n> --repo <repo> --reason completed`, then, when the card
moves, `gh project item-edit <number> --owner <owner> --url <issue-url> --field <field> --value <value>`.
Never close a parent before every one of its children is closed. A failed write is recorded and only the
missing ones are retried, never by repeating a close that already landed; a child that fails to close holds
its parent back and both are reported. Pause a few seconds between writes when the batch is large, to stay
under the secondary rate limit. Add no comment: the closing is already on the issue.

## 4. Verify

```powershell
python "${CLAUDE_PLUGIN_ROOT}/scripts/closeout.py" verify --config <config> --root <project> --issues 12,13
```

Report per issue whether it is closed and its card is in Done; list every `ok: false` (the command then exits
with code 1). GitHub is the source
of truth: the local `.frontlights/issues/<n>/` snapshots are updated to closed with the time of the read,
never the other way round. Put the approved list, the user's literal answer, the results and the verify
output in the handoff.

## 5. Let RoadS see it

RoadS reads only the **Status** of the card in the Project, never whether the issue is closed: closing an issue
without moving its card changes nothing there, and a completed item stays in its sprint, marked done, until the
sprint rotation removes it. RoadS also refreshes only when it syncs, and a sync within 30 s of the previous one
returns the old snapshot. So, when cards were moved and the roadmap sync of stage 1 is configured, tell the user
this in one line and offer a new sync (a question with options, "Sincronizar agora" and "Deixar para depois");
on yes run the roadmap sync again as `references/roadmap-sync.md` describes. Without the board (`board.status`
`unconfigured` or `unavailable`) say plainly that the close-only fallback will not show in RoadS.

## Never

- Close an issue that has no criteria section or an unticked criterion in this flow. A user who asks for a
  specific one anyway gets the unticked items shown first, and the answer is theirs, outside this list.
- Reopen, delete, transfer or archive an issue, or edit its body, here.
- Merge a pull request, deploy or release: the closeout never does.
