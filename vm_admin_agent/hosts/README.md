# Host knowledge registry

A host profile is a record of one explicitly identified system, not an install
recipe. Never select a profile just because the operating system matches.

| Logical host ID | Canonical profile | Scope / status |
| --- | --- | --- |
| `ynwa-vm` | [../ynwa_vm.md](../ynwa_vm.md) | Original VM; historical observations; target binding must be confirmed |

The current checkout host is **not enrolled** by cloning this repository. No
Linux/macOS host is implicitly mapped to the legacy VM.

## Enrolling another system

1. Agree on a stable user-selected ID (for example `work-linux-01`), repository
   privacy boundary, and approved read-only discovery commands.
2. Run `scripts/host_facts.py` from the workspace on the intended host. Confirm
   the machine identity out of band; do not store machine IDs, SSH keys, or
   fingerprints in shared discovery output. For remote operation, identify
   local controller and remote target separately.
3. Review facts and inspect only the relevant services/configs. Do not collect
   environment variables, credential files, full process arguments, or full
   container configuration dumps that might expose secrets.
4. With approval, create `<host-id>/profile.md` and `<host-id>/changes.md` here
   and add the profile link above. Until then, observations are provisional.
5. Verify the profile and allowed operations with the user. Enrollment does not
   approve changes, package installation, or administrator privileges.

## Profile format

Each profile should contain:

- **Identity/scope:** logical ID, owner agent, OS, purpose, environment boundary;
  confirmed target and observation date (UTC). Hostname is a hint, not identity.
- **Evidence/status:** verified versus observed versus hypothesis, verification
  commands (without secrets), and triggers for revalidation.
- **Observed state:** services, package/service managers, networking, storage,
  and existing tools relevant to the host; mark unknowns explicitly.
- **Desired state:** separately approved requirements, never mixed with facts.
- **Ownership:** config source repositories, symlink targets, runbook links,
  banner integration if any, and secret-store references (no secret values).
- **Safety:** allowed operations, approval requirements, recovery access, and
  rollback/verification procedures.

The changes file holds dated action/result/verification entries, not raw logs.
Store reusable Ubuntu/macOS/service procedures once in a runbook library, link
them from profiles, and distinguish tested OS versions. Refresh volatile facts
on demand rather than generating constant Git churn.

## Concurrent writers

The administrator agent owns host profiles. Other agents may propose changes or
make explicitly authorized evidence-backed edits in their own branch/worktree.
Conflicting observations require revalidation; never select the newest text
automatically. Preserve the old evidence as superseded when useful.