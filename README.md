# agent_workspace

Portable agent instructions and knowledge coordination. This checkout is a
**staging point for consolidation**, not yet a merged or multi-submodule setup.
The separate network-agent repository and its operational symlink are unchanged
in location. No host is automatically enrolled or administered on clone.

## Recommended target: one entry point, separate private knowledge stores

Use this repository as the umbrella/control repository. Keep small reusable
agent definitions, shared knowledge rules, validators, and client adapters here.
Use Git submodules for per-agent knowledge when separate access/history is
required; ordinary folders are simpler if independent repos are not necessary.
Submodules satisfy the requested independent knowledge repositories, but require
dependency-first publishing. A parent clone alone does not fetch their content.

Proposed layout (not created by this review):

```text
agent_workspace/
  AGENTS.md                       shared ownership, evidence, and safety rules
  agents/
	 forever_associate/             short portable role definition
	 vm_admin_agent/                short portable role definition
  knowledge/
	 network/                      private work-approved Git submodule
		README.md                   task-oriented index
		runbooks/                   reusable operational procedures
		projects/                   active project knowledge
		incidents/                  evidence-backed retrospectives
		environments/               scoped work/lab configuration references
	 systems/                      private administrator Git submodule
		README.md                   host/runbook index
		runbooks/{ubuntu,macos,services}/
		hosts/<stable-host-id>/
		  profile.md                scoped observations and separate desired state
		  changes.md                dated action/result/verification records
  adapters/{claude,copilot,opencode}/
  scripts/                        bootstrap, validation, explicit sync tooling
  .local/                         ignored machine bindings and runtime output
```

Work and personal knowledge must not share a remote or host unless policy
allows it. Even a submodule URL/name can disclose information: use a work-only
umbrella variant or local registration when that boundary requires it. Initialize
only authorized modules; do not recursively clone corporate tools on a personal
machine. Existing tool repositories remain independent, not copied into knowledge.

## Changes implemented in this checkout

- `AGENTS.md` is the neutral role index and shared knowledge contract.
- `opencode.json` loads only that index, not a specific host's full state.
- `vm_admin_agent/vm_agent_context.md` is host-neutral, with OS detection,
  approval boundaries, tool reuse, and evidence-backed updates.
- `vm_admin_agent/hosts/README.md` defines enrollment and the host record format.
- The legacy `vm_admin_agent/ynwa_vm.md` stays at its original path to preserve
  the existing banner integration; it is explicitly scoped to the original VM.
- `scripts/host_facts.py` prints minimal local discovery JSON without installing
  software, contacting devices, elevating privileges, or writing files. It accepts
  an optional `--host-id`; that is a proposed label, not enrollment or approval.
- Run local tests with `python3 -m unittest discover -s tests -v`. These validate
  the helper, not actual host administration or client agent discovery.

## Knowledge lifecycle: self-updating, not self-authorizing

1. Read index → select domain and confirmed host → inspect relevant facts.
2. Gather approved evidence → distinguish hypothesis, observation, verification.
3. Update the canonical fact within approved write scope, with scope, owner,
	UTC date, evidence, and revalidation trigger. Propose unapproved writes.
4. Put reusable lessons into a runbook; retain only host-specific differences in
	profiles. Link rather than copy. Mark obsolete findings as superseded.
5. Validate and review; instruction/permission changes are always reviewed.
6. Commit and publish only on separate approval, reporting unpublished work.

Neither agent should silently rewrite its own safety rules, install background
sync, broaden permissions, or blindly execute instructions found in logs. Prompt
rules guide behavior; enforce sensitive actions with OS permissions, client
approval controls, repository protections, and reviewed validators/CI as well.

## Staged migration (requires approval before moving histories or remotes)

1. **Security gate:** legacy knowledge contained credential material and retains
	private operational details. Identified literals were redacted in five local
	files; this was not a complete audit. Review working trees and Git histories before
	republishing; rotate genuine exposed secrets through the owner. Redaction in
	one commit does not remove earlier copies. Agree on approved private remotes.
	Never silently rewrite history or upload private content to an external scanner.
2. **Preserve:** record branches/commit IDs, repository status, submodule pointers,
	existing hook settings, symlinks, and banner references. Back up only to an
	approved location. Preserve original repos until migration is proven.
3. **Pilot umbrella:** initially register the existing network repo as an optional
	agent-package submodule, without reshuffling its references or nested tools.
	Existing operational links continue to point to the old checkout during pilot.
4. **Extract knowledge:** in temporary clones, separate role instructions from
	knowledge with a reviewed history-preserving import/split plan. Preserve all
	useful notes and legacy pointers; compare file inventories before/after.
	Do not create fresh empty repos and discard the old histories.
5. **One canonical policy:** after both agents load the umbrella reliably, share
	the contract there and replace transitional duplicated policy with tested
	pointers. Split the network agent's long embedded knowledge incrementally.
6. **Deploy adapters:** generate client-specific wrappers from canonical roles;
	do not assume identical YAML/discovery rules in Claude, Copilot, and OpenCode.
	Resolve references from the actual checkout, not a symlink's parent or CWD.
	Bootstrap should default to dry-run, refuse overwrites, back up approved
	replacements, and offer explicit per-client/per-module selection. No sudo,
	package installation, or network-module initialization by default.
7. **Validate and switch:** test links, reference resolution, module availability,
	missing-access behavior, knowledge writes, and rollback in temporary homes on
	Ubuntu and macOS. Enable hooks per clone only after checking existing hooks;
	add the same checks in CI. Switch production links only after a successful
	smoke test. This review has not performed those deployment steps.

## Publishing consistent repository revisions

There is no atomic push spanning independent Git repositories. The umbrella's
submodule commit IDs define the consistent, reproducible release:

1. Inspect each repository's status and upstream. Use a branch/worktree per
	concurrent task; never stage unrelated changes or auto-stash to force a pull.
2. Review and validate explicit changes. Publish nested tool changes first if
	needed, then knowledge/agent-package commits to their approved remotes.
3. Verify each referenced commit is reachable on the intended remote branch.
4. Stage only the intended submodule pointers in the umbrella, validate the
	complete combination, then commit and publish the parent last.
5. On another host, fetch/review the approved parent revision and initialize or
	update only selected submodules to their pinned commits, not latest branches.
	Stop on dirty trees, conflicts, missing access, or unavailable commits.
6. If a child push succeeds but the parent fails, report the partial state.
	Retry after review; the previous parent revision remains the released set.

Do not use an unconditional `git add . && commit && push` loop. Automating this
workflow should start with a status/plan mode and explicit publish confirmation,
not unattended pull/commit/push jobs on every server.
