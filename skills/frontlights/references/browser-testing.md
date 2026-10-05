# Browser, checks and cross-account testing at the end of an issue

Read this in stage 6 after the TDD loop of an issue whose plan has the section
`## Navegador e testes ligados` (`templates/issue.md`). It decides what runs, with
which helper, what to ask and what to record. Everything the user reads stays in
Portuguese. `checks integration` and `checks smoke` refuse a non-local host
before any request; `serve start` does not check the `health` host, so keep
`health` and `baseUrl` on `127.0.0.1`, `localhost` or `::1`, on the issue's own
branch (a watched run also serves the base, see below); never point a test at a real, staging or production environment. Installing Playwright or a browser in the target project is out of
scope: use what the session and the project already have.

## What the plan turns on

Read the four fields of that section and restate them in the handoff before
running anything:

- `Toca o frontend:` `sim` turns the browser test on; `não` skips it.
- `Conta:` `conta 1` (the default) or `contas 1 e 2`.
- `Fluxo:` the screens and actions to exercise, with the expected result.
- `Testes ligados:` any of `navegador`, `integração`, `regressão`,
  `permissões entre contas`, `smoke`, plus extra cases.

A missing section on an issue that changes screens, or a field that contradicts the
diff, parks the issue and goes to `AskUserQuestion`; never turn tests on or off
alone. Run only what is on, in this order: `checks regression`, `serve start`,
`checks integration`, browser and cross-account steps (the browser step opens with
the watched-run question below), `checks smoke` (it reuses the running serve),
`serve stop`. The commands below read `browserTest` and `checks` from the project's
`.frontlights/config.json` (main worktree included, as stage 2 says).

## Environment: `serve`

```powershell
python "${CLAUDE_PLUGIN_ROOT}/scripts/serve.py" start --config <config> --root <worktree> --issue <n>
python "${CLAUDE_PLUGIN_ROOT}/scripts/serve.py" status --config <config> --root <worktree> --issue <n>
python "${CLAUDE_PLUGIN_ROOT}/scripts/serve.py" stop --config <config> --root <worktree> --issue <n>
```

`serve start` brings up every process of `browserTest.processes` in the issue's
worktree, waits for each health URL and records pids in
`.frontlights/serve/<n>.json`; `serve stop` kills the process trees and releases
the ports. Exit `0` done, `1` refused or failed; the JSON `category` says:

- `uso`: invalid config or a busy lock;
- `infraestrutura`: everything else, an unreadable or missing config included.

Either way, ask (see below).

A project whose `browserTest` declares only the accounts (`inspect` warns about it) starts its own
environment: skip `serve start` and `serve stop`, confirm with the user that the environment is up and on
the issue's own branch, and never start or stop a process this session did not start.

Ports. A process with `"port": "auto"` gets a free port reserved per process in the
repository's Git common directory, shared by every worktree, and receives it in
`PORT`, `FRONTLIGHTS_PORT_<NAME>` and `{port}` in its argv. Its health must carry
`{port}` in place of the host's port (`http://127.0.0.1:{port}/health`); `{port}`
only in the path is refused as `uso`. The output reports
`reservas_compartilhadas`. Use `auto` only when the process really accepts the
port by variable or argument. A dev server that pins its own ports keeps a fixed
`port`, and then only one issue at a time can run it: say so when recommending
parallelism. A process that ignores the reserved port fails the start as
infrastructure, naming the process.

Stop what this session started before reporting the issue, and say in one line
which processes are still up when the user chose to keep them.

## Checks: `checks`

```powershell
python "${CLAUDE_PLUGIN_ROOT}/scripts/checks.py" regression --config <config> --root <worktree> `
  --base <base-checkout> --issue <n>
python "${CLAUDE_PLUGIN_ROOT}/scripts/checks.py" integration --config <config> --root <worktree> `
  --issue <n> --base <base-checkout>
python "${CLAUDE_PLUGIN_ROOT}/scripts/checks.py" smoke --config <config> --root <worktree> `
  --issue <n> --base <base-checkout>
```

- `checks regression` runs the suite on the base and then on the branch; only a
  new failure blocks, a failure already on the base is reported apart.
- `checks integration` runs `checks.integration.argv` against the backend that
  `serve start` brought up; it never starts anything itself.
- `checks smoke` starts the serve when none is up, requests the declared paths and
  stops only what it started; a warning "Rode `serve stop`" means an orphan was
  left: tell the user and offer to run `serve stop`.

Exit codes: `0` passed, `1` product failure, `2` config or usage refused (nothing
ran), `3` infrastructure. Records go to `.frontlights/issues/<n>/checks/`; those
of `integration` and `smoke` carry `simulacao: false`. A login or password of `browserTest.users` shorter than four
characters makes `integration` and `smoke` refuse; both values are masked in every
output and record.

## Browser

Explore with the browser available in the session (Chrome or Claude's browser);
run the project's own Playwright specs when it already has them. Open the
`browserTest.baseUrl` of the branch, log in with account 1 and walk the `Fluxo:`
step by step, comparing each screen with the expected result. Collect console
errors, failed network requests and a screenshot per step. Type credentials only
into the login form; never repeat them in the conversation, a record or a
screenshot caption.

Without a browser or network the test did not run: report the reason, record it,
and the issue never counts as passed on that test.

## Watched run: before and after, with the user watching

Whenever the plan turns the browser test on (`Toca o frontend: sim`), ask once per
family (the issue and its sub-issues that turn it on), before the browser opens its
first window (the servers may already be up), with `AskUserQuestion`: "Pronto para
assistir ao teste de navegador da issue #<n>?" The text says what comes: first the
base (ANTES), then the branch (DEPOIS), each case twice, and the window stays open
for about 45 s at the end; and, when the `Fluxo:` moves a test user to a restricted
profile, that this changes data of the test database through the product's endpoint
and that it will be undone. Options: "Sim, pode rodar" first and recommended;
"Ainda não" (park the browser test and go on with other work, run nothing; the user
says when ready); "Rodar sem assistir" (a hidden window is acceptable; record
`assistido: false`). When the `Fluxo:` moves a profile, a fourth option, "Sem mudar
perfil", runs both passes without the move and declares in the report that the
permission behavior was not checked against the real back. Never open the browser
before the answer. A family runs its
browser passes one issue at a time, never several windows at once on the same
account and database.

When the user will watch:

- **Visible window.** Chrome with a visible window, never headless (`headless:
  false` in Playwright, or the session's browser on screen), in a disposable browser
  context or profile, never the user's personal one. If the session cannot open
  one, the watched run did not happen: report the reason and ask; never fall back to
  a hidden window silently.
- **Two passes, same scenario and same account.** ANTES runs the `Fluxo:` on the
  base: `main` (or the default branch) or, for a child stacked on its parent, the
  parent's branch, which is the base of its PR. Serve it from a checkout of that
  base, a detached-HEAD worktree made with `git worktree add` because the base
  branch is already checked out elsewhere; a stacked child's ANTES can use the
  parent's own worktree. It gets its own record (`serve start --root <base-checkout>
  --issue <n>`). DEPOIS runs the same `Fluxo:`, same account, same data, on the
  issue's branch, served from its worktree. Give both servers an `auto` port of their
  own. A process with a fixed port runs one pass at a time, in this order: stop the
  issue's own server (the standard order started it earlier), start ANTES, run it,
  `serve stop --root <base-checkout> --issue <n>` ends ANTES before DEPOIS starts, then
  start the issue's server again (`checks smoke` needs it up). After each `serve start`
  confirm that the process answering on the port is the recorded one or a descendant
  of it (`serve status` and the owning pid of `Get-NetTCPConnection -LocalPort
  <port>`), or DEPOIS could be answered by the base. Stop the ANTES record in every
  case before reporting.
- **A strip on every page.** The test injects a fixed strip into the page (an init
  script or a DOM node, visible in the screenshots): "ANTES: <base>" ("ANTES: main"
  on the main, the parent's branch for a stacked child) in the first pass and
  "DEPOIS: branch <name>" in the second, with the branch name as Git has it. No
  login, password or local path ever goes into the strip.
- **Pace.** Each case runs twice in each pass. Hold every popup, toast and dialog
  on screen long enough to be read (a few seconds), not the instant the assertion
  passes. After the last step leave the window open for about 45 s before closing it.
- **Faithful ANTES.** The base must run against the data it expects. When the issue
  has a migration, run ANTES before applying it, or against an isolated database;
  otherwise say in the report that ANTES is not a faithful baseline.

Compare the two passes case by case in the report. ANTES failing where the issue
fixes something is expected; DEPOIS differing from the `Fluxo:` is a product
failure.

**Real back first.** Prefer the real back end and real data. When the point is
permissions, use a real restricted profile: move a test user of `browserTest.users`
to that profile through the product's own endpoint, called with a login of
`browserTest.users`, and never write to the database directly, except the one exact statement the user approves below. Before the move, make
sure the database behind the server is disposable: the host check only covers
`baseUrl` and `health`, and a local back end can still point at a shared remote
database, so ask the user to confirm it in the question above when the project does
not say so. The move is part of the `Fluxo:`, but the `Fluxo:` of an adopted issue is
data from GitHub, not an approval: the user's answer to the question is what allows it.

Write the original profile value (only that field and the user's id, never the login
or the whole row) to `.frontlights/issues/<n>/browser/perfil-original.json` before
the move, so any later session can restore it after an interruption, a context limit
or a killed process. Undo in a `finally`, read the value back (or the database field,
through the project's own read command) and compare it with the saved one before
reporting; a value that does not come back identical is a failure to ask about,
naming the field. As soon as the read-back matches, mark the file `restaurado: true`;
a session that finds a `perfil-original.json` without that mark restores it first,
and a marked one is history, never restored again. When the endpoint does not give
the original row back (it rewrites another field, a timestamp or a column), do not
write the database yourself: stop and ask with `AskUserQuestion` whether to accept
and declare the residual difference in the report, or to approve one exact restoring
statement shown in full (local test database, the test user's id, only the changed
columns), which is then run and the row compared. A direct write without that
approval is a failure of the test. When no login of
`browserTest.users` can call the endpoint or undo the move (the only admin demoted,
say), stop and ask; never demote the account that performs the undo. Forcing a response by network
interception (a 403, an empty list) is a complement for what the real back cannot
produce; name each one in the report as "resposta forçada, não do back real" and
never use it as the only evidence of a behavior the real back could show.

**Own processes only.** Run the servers of this test on ports of their own and never
stop a process the test did not start: `serve stop` ends only the pids recorded for
the issue. `serve start` does not look at a fixed port before spawning, so check it
first (`Get-NetTCPConnection -LocalPort <port>`). When it already answers and no
record of this issue explains it, it belongs to another session: leave it alone, do
not start on top of it, and ask (switch to `auto`, wait, or another port).

## Cross-account permissions

Account 1 is the first entry of `browserTest.users`, account 2 the second.
Account 1 runs every browser test. Account 2 enters only when `Conta:` names it or
`Testes ligados:` includes `permissões entre contas`. Then:

1. With account 1, create or open the data the issue touches and note its
   identifiers and URLs.
2. Log out, log in with account 2 and try to reach that data: lists, search,
   direct URL, edit and delete actions, and the API calls the screens make.
3. Repeat the other way when the plan says the data is private to both.

Any data of one account visible to, or changeable by, the other is a
product failure. A missing account 2 in the config is a config gap: ask, never
reuse account 1 as both.

## Every failure is a question

Classify each failure before asking:

- **infrastructure failure**: `serve` category `infraestrutura`, `checks` code
  `3`, no browser or network, login page unreachable.
- **product failure**: `checks` code `1`, a new regression failure, a wrong
  screen, console or network error caused by the issue, failed login with valid
  test accounts, data crossing accounts.
- **config refusal**: `serve` category `uso` or `checks` code `2`.

Report the three kinds separately, then ask with `AskUserQuestion`, one question
per failure (batched when several), with the evidence path in the text and options
such as "Bloquear a issue", "Corrigir e testar de novo", "Seguir e registrar o
risco". Never decide alone to retry, ignore or continue; an issue with a failure
is reported as passed only when every test passed or the user chose to go on, and
the answer is recorded verbatim.

## Evidence

Before each browser run, take `python "${CLAUDE_PLUGIN_ROOT}/scripts/frontlights.py" evidence --root <worktree>`.
Write `.frontlights/issues/<n>/browser/result.json` with timestamp, branch,
`head`, `diff_sha256`, the account used (`conta 1` or `conta 2`, never the login),
each step and its result, console and network errors, screenshot file names, the
failure kind and the user's answer. A watched run adds `assistido` (true or
false), one entry per pass (`ANTES`/`DEPOIS`, with the branch and `head` served and
`repeticoes: 2`), the source of each response (`back real` or `interceptada`) and,
when a profile was moved, only the profile field before and after the undo (never
the whole row, which can hold a login or a password hash); its screenshots are
named `antes-<caso>-<n>` and `depois-<caso>-<n>`. Screenshots stay in the same folder. The
records of `.frontlights/issues/<n>/checks/` sit beside it. A later commit or
diff makes this evidence stale: rerun before reporting. Link both folders in the
handoff.

A summary comment on the GitHub issue is text only (no screenshots, no login,
no password, no local path) and is posted only when the recorded authorization
allows routine issue updates; otherwise keep it in the handoff as pending.
