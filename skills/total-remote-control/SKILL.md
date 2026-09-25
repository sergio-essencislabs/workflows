---
name: total-remote-control
description: Supports workflows by configuring a persistent Remote Control host so the user's phone can start a new session on this machine at any time.
user-invocable: false
---

# Anchored remote control

Run only inside the coordinating workflows session, after stage 1, and only after
the user chose the anchored arrangement. Everything presented to the user is in
Portuguese. Configure nothing silently and start no host on the user's behalf.

State the two conditions before anything else, and state them as requirements
rather than preferences. They are not the same kind of constraint and must not be
presented as one. The terminal window hosting the command must stay open, always:
`claude remote-control` is a terminal interface, closing its window ends the host
within seconds, and sessions hosted from a scheduled task or a background logon
died about twenty seconds after the phone connected. No power setting changes
this. The lid must stay open until the closed-lid test has passed on this machine;
the cause once observed for a dropped session has been removed, but removing a
cause is not a measurement. The PC may be locked in both cases.

Never propose boot automation of any kind: no scheduled task, no startup
shortcut, no service, no background logon host. Never call
`SetThreadExecutionState`, and never present sleep or display timeouts set to
"never" as protection; both were instrumented on this machine and neither
prevented standby on lock. Only S0 Modern Standby exists here, so there is no
deeper sleep state to fall back on.

Read the machine before asking about it. `workflow.py monitoring --root <project>`
returns both power values, any candidate host process, and the exact commands it
ran. Prefer it over ad-hoc parsing: the lock-display setting is hidden, `powercfg
/q` reports no value for it, and only `/qh` with the raw identifiers shows it. A
value of zero means "never blank on lock" and "do nothing on lid close". A missing
value reads as unknown, never as zero. Quote the measured values back to the user
before proposing any change.

Explain the lever honestly whenever the display setting comes up. Blanking the
display kills no process; standby does. On this machine locking alone was measured
to enter standby even with every timeout set to "never", and a zero lock-display
value is an attempt to break that chain, not a fix for a known cause. A screen
that stays on is not evidence that the session survives.

Label every limit and never promise past it. That a zero lock-display value on AC
holds through a long lock is unproven: the only measured survival was about ninety
seconds, and it was on battery. That a zero lid value makes a closed lid safe is
untested. The result of the preflight is a recommendation, not proof of authority.

Ask at most three `AskUserQuestion` calls and stop at the first refusal. The first
carries two questions: header `Condições`, asking acceptance of a locked PC with
the terminal window and the lid open, options `Concordo` and `Não posso`; and
header `Energia`, asking whether the machine stays on AC power while unattended,
options `Na tomada`, `Na bateria` and `Não sei`. `Não posso` ends this skill and
returns mode `local` or `alternative` to the coordinator. Battery and uncertainty
both continue, carrying the measured battery profile as a stated caveat and no
claim that the arrangement survives.

Make the second call only when a measured value is not zero, on either profile.
Present the exact `powercfg` lines to be run and the current values, then ask with
header `Ajuste de energia` and options `Aplicar`, `Deixar como está` and `Só
mostrar`. Changing a power scheme is a system change and requires this approval
every time. Record the previous values before any change, never modify a scheme
other than the active one, and never widen the change beyond the two settings
named here.

Make the third call after the user has started the host. Instruct the user to open
a terminal that will stay open, in the project directory, and run `claude
remote-control --name <nome-curto>`. Keep `--spawn`, `--capacity` and
`--permission-mode` at their defaults. Never propose `bypassPermissions`,
`acceptEdits`, `auto` or `dontAsk` to make unattended work easier; a wider
permission mode is a separate human decision with its own authorization and is
refused here. Then ask, header `Conexão`, whether the phone opened the session and
answered a test question, options `Confirmo pelo celular`, `Não conectou` and
`Prefiro local`; and header `Nova sessão`, whether a session started from the
phone works in the same directory or a separate worktree. Only `Confirmo pelo
celular` records `phone_connected: true`. A running process, a printed URL, a QR
code or a displayed prompt is never that evidence.

Describe detection as asymmetric, because it is. No candidate process means no
persistent host, and that conclusion is safe. A candidate means a process: the
host may be listening with no phone attached, the terminal may be about to close,
and the argument also appears in a help invocation. Whether the phone is attached,
whether the tunnel is healthy and whether a session is recorded inside the
reattachment window are all outside what any local check can answer; report them
as unknown rather than as false.

After a restart, in a new session, or whenever the user reports a disconnection,
detect first and offer this configuration again when no host is found. Do not
reuse an earlier confirmation. Where a session was recorded for this directory or
one of its worktrees, `claude remote-control -c` reattaches to it and fails when
nothing was recorded there within roughly the last four hours. Offer that path
before a fresh host, describe the window as documented rather than verified here,
and never plan around it as a guarantee.

Record mode `phone`, `confirmed_by`, `phone_connected`, the session identity, the
measured power values and the time in the authorization's `monitoring` block and
in the handoff's monitoring field. Write no scheduled task, no shortcut, no
startup entry and no file outside `.workflows/`. Return the recorded arrangement
and every unresolved condition to `/workflows:workflows`; an unconfirmed phone
blocks each phase that depends on reaching the user.
