---
name: grilling
description: Supports the workflows coordinator with focused product discovery, decision interviews and explicit assumptions.
user-invocable: false
---

# Discovery interview

Relentlessly stress-tests plans and designs through systematic questioning.

Conducts deep-dive questioning across all aspects of a plan, walking through decision trees branch-by-branch until shared understanding is reached
Automatically explores the codebase to answer questions where code context is available, reducing redundant back-and-forth
Designed for design reviews, architecture validation, and pre-implementation planning where thorough vetting prevents downstream issues

Use only within the coordinating workflows session. Read approved decisions and
current planning input before asking anything. Use `AskUserQuestion` for every
question; workers without it return questions to the coordinator.

1. Summarize the observation, source/timestamp, affected users and observed pain.
2. Separate evidence from inference and untested assumptions. Read relevant code
   and existing issues; identify duplicates, contradictions and missing context.
3. Batch at most four related material decisions per interview: desired outcome,
   success measure, boundaries, constraints, priority, compatibility, risks and
   significant alternatives. Explain recommendations and trade-offs concretely.
4. Record answers in `templates/discovery.md`, including rejected alternatives,
   unresolved questions, approval references and evidence. Never re-ask settled
   decisions unless new evidence invalidates them; explain such changes.
5. Continue until implementation-changing ambiguities are resolved. If a small
   research/prototype step is needed, bound it and obtain permission for any
   changes beyond existing authority. Do not start product implementation here.

Return approved decisions and unresolved items to `/workflows:workflows` for PRD
drafting. A decision log is planning evidence, never an issue status database.
