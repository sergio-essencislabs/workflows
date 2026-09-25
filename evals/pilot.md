# Live pilot runbook

Use a separate disposable GitHub repository/project with actual configured RoadS
planning input. Its creation and mutations require the user's explicit scope.
Do not use GuardianS or a production repository as a fixture. Record run timestamp,
CLI/plugin version, session identity, repository/issue URLs, commits and outputs.

1. Load with `--plugin-dir`, inspect `/help`, invoke `/workflows:workflows` and
   verify one public entry and five internal helper skills. Native static validation
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
10. Restart without the plugin and verify GuardianS and project data remain intact.

Only after all required checks pass, present the linked evidence and separately
ask about default-workflow switching and GuardianS deactivation via AskUserQuestion.
