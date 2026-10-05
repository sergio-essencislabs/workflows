# Semantic decomposition evaluation (manual; no model score claimed)

Input: "Let users create, view and edit planning observations. We probably need
three tickets: a database table, backend endpoints, and frontend screens. Existing
project has authentication, an observation list shell and a storage abstraction."

Expected: silently revise the horizontal proposal before asking approval.
Slice 1 creates and retrieves one observation through UI/API/storage with tests.
Slice 2 edits with validation and concurrent-edit feedback, depends on slice 1.
Slice 3 is optional only if independently requested; do not invent work to hit a
ticket count. Each names observable outcomes and relevant test layers. No extra
question asking permission to repair an obviously horizontal decomposition.

Reject: separate database/backend/frontend issues without a working seam;
acceptance copied verbatim from the whole PRD; hidden shared-file contention;
claiming `validate-plan` semantically proved verticality; creation before approval.

Prerequisite case: if no storage abstraction exists, a tiny tested persistence
seam may be a prerequisite only with a named consumer and executable demonstration.
Prefer embedding it into the first thin vertical outcome where practical.

Family case (manual): start from an issue that has five open sub-issues, one of them
labelled `needs-decision`, and a closed one. Expected: all five open sub-issues are read
from GitHub in stage 2 and enter the same grilling (the pending one gets its own solution
round, the four decided ones are confirmed together in one question); the plan holds the
parent and the five children with `parent` set, the closed one stays out; every issue body
carries `## Camadas da fatia` with each layer handled, delegated to a named sub-issue, or
not touched with a reason; stage 6 offers stacked branches (recommended) and recommends a
concurrency equal to the number of children with disjoint `ownership`.

Reject: planning only the parent; "children after the parent's merge" as the default;
a sub-issue that is only "the API part"; a layer missing from the table; the pending
sub-issue left out of the grilling; claiming `validate-plan` checked the layers.
