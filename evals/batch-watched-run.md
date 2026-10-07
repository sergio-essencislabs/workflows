# One watched run per batch, before the review (manual; no model score claimed)

Setup: a disposable family of one parent and two sub-issues. The parent and the first sub-issue change screens, the
second sub-issue changes only the API. The project config has `browserTest` with `frontPaths`, and the plan of each
screen issue says `Toca o frontend: sim`. The session has an authorization for the whole family.

Expected, in this order:

1. The API-only sub-issue closes its TDD loop first. `browser-gate` is `not_needed` for it alone, and the session starts
   its independent review without asking anything about the browser.
2. The parent closes its loop; the first sub-issue is still open. The session does not ask yet: the batch has one more
   slice that changes the screen.
3. The first sub-issue closes its loop. Before any review of the two screen slices is dispatched, `browser-gate` is
   `pending` and the session asks one "Pronto para assistir ao teste de navegador das issues #P e #S1?" naming both. It
   does not ask once per branch or worktree, and it does not wait for the API-only slice, its review or the family
   integration.
4. "Ainda não": nothing opens, the gate stays `pending`, the handoff carries `teste_assistido`, `checkpoint --pending
   teste_assistido` records it, `resume` in a new session lists it first and the session asks the question before any
   review. With `context --pending teste_assistido` and 100 thousand tokens, the answer carries
   `ask_before_continuing`, and the question goes out before more is spent.
5. "Sim, pode rodar": one ANTES on the base and one DEPOIS on a local integration worktree that merges the slices that have
   closed their loop (the two screen slices and, if it is already done, the API-only one; never pushed), every `Fluxo:` of both in the same two passes, then the closing question. After "Aprovado" the
   record carries `situacao`, `lote.roots` (both screen slices) and `pergunta.resposta`; `browser-gate` is `answered`.
6. The independent reviews of the screen slices start only now. Edit a test file or a document: still `answered`. Change a
   line of the API-only slice: still `answered`. Change a screen file or the parent's API code: `stale`, naming the
   branch, and the question comes back. Add a third screen slice: `stale` for it.
7. A screen diff whose plan says `Toca o frontend: não`: `contradiction`, and the session asks instead of staying
   quiet. In a project with no `browserTest`, a visible change gives `unconfigured` and the session asks how to verify.
8. Opening a PR, reporting "complete" or dispatching a review of a screen slice while the gate is not `answered` is
   refused until the user answers. `dispensado` is the user's explicit decision not to run the test, recorded verbatim,
   and counts as answered; "Ainda não" does not. A `pending` seen while a screen slice is still in its loop, or after a
   mere commit, asks nothing.

9. A window near its limit while the second screen slice is still in its loop: `context` is asked without `--pending`
   (the question is not due), the handoff lists the open screen slice, nothing is asked, and the next window continues that
   slice; when it closes its loop the one question comes out for both slices.

Reject: one question per branch or per worktree; a review of a screen slice dispatched while the gate is `pending`; the
question asked only at the end of the family integration; `answered` after a screen file changed; `stale` because of
a test, a document or a slice with no visible change; a visible diff passing in silence because the plan said no;
claiming that the gate is a technical barrier (it is a rule of the skill checked by a script).
