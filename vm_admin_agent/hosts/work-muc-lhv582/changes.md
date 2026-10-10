# Change log: work-muc-lhv582

Dated entries only. Each entry: action, result, verification, rollback status.
Do not paste raw command output or secrets here; link to evidence stored in an
approved location if needed.

## 2026-10-05 — Herdr pane used a different SSH agent (observed; pane corrected manually)

- **Scope/host:** `work-muc-lhv582` (`work-vm`), SSH-forwarded agent access from
  the user's Mac to herdr panes. Owner: `vm_admin_agent`.
- **Status:** Observed; the manual pane correction was verified for that pane.
- **Finding:** `ssh-add -l` in the SSH login shell listed forwarded identities,
  while a herdr pane used another agent socket with no identities. Pointing the
  pane's `SSH_AUTH_SOCK` at `~/.ssh-agent-forward/socket` made those identities
  visible. No private key was copied to the VM.
- **Evidence/verification:** User-provided command results, followed by a
  successful `ssh-add -l` after exporting the stable socket path in the pane.
  No socket values or key fingerprints are retained here.
- **Existing configuration:** `~/.tmux/zsh/.zprofile` refreshes the stable
  symlink from a qualifying SSH login; `~/.tmux/zsh/.zshenv` only uses it when
  the inherited socket is absent or not a socket. Thus a different but live
  agent socket is not automatically overridden. Herdr server environment and
  automatic behavior for newly created panes remain unverified.
- **Revalidation trigger:** After reconnecting SSH, restarting/re-attaching
  herdr, changing shell startup files, or if pane `ssh-add -l` no longer lists
  the forwarded identities.
- **Rollback:** No configuration or system state was changed; the temporary
  pane export can be discarded by closing that shell/pane or restoring its
  previous `SSH_AUTH_SOCK` value.
- **Publication:** No commit or push.

## 2026-09-15 — Prompt branch truncation customized (documentation + p10k)

- **Action:** Updated `~/.tmux/zsh/.p10k.zsh` so long branch names preserve the
  beginning and truncate the tail instead of truncating the middle.
- **Scope:** User prompt customization only. No system services or packages
  changed.
- **Evidence:** The previous formatter truncated `VCS_STATUS_LOCAL_BRANCH` with
  `branch[13,-13]="…"`; the new edit switches to `branch[33,-1]="…"`.
- **Verification:** Fresh zsh sessions should show long branch names starting
  with the initial branch prefix, e.g. `bugfix/RCMTM…` rather than a middle cut.
- **Rollback:** Restore the previous `branch[13,-13]="…"` line.
- **Publication:** Not committed or pushed.

## 2026-09-15 — Git config aligned to `/u0/rochalsk/.gitconfig` (documentation + dotfiles)

- **Action:** Updated `~/.tmux/git/.gitconfig` to mirror the referenced machine
  settings: `user.name=Radek Ochalski`, `user.email=rochalsk@akamai.com`,
  `push.default=simple`, and `remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*`.
- **Scope:** User-level git config in the dotfiles repo and host knowledge only.
  No repositories were rewritten and no commits were created.
- **Evidence:** User supplied the canonical settings from `/u0/rochalsk/.gitconfig`.
- **Verification:** `git config --global --list --show-origin` should report the
  four settings from `~/.gitconfig` → `~/.tmux/git/.gitconfig`.
- **Rollback:** Restore the previous values in `~/.tmux/git/.gitconfig`.
- **Publication:** Not committed or pushed.

## 2026-09-15 — Git identity reset to Akamai values (documentation + dotfiles)

- **Action:** Updated `~/.tmux/git/.gitconfig` user identity to
  `rochalsk <rochalsk@akamai.com>` so this machine uses the Akamai identity for
  git operations.
- **Scope:** User-level git config in the dotfiles repo and host knowledge only.
  No remote repositories changed and no commits were created.
- **Evidence:** `git config --global --list --show-origin` previously resolved
  `user.name=R4d3k` and `user.email=rochalski@gmail.com` from the symlinked
  `~/.gitconfig`.
- **Verification:** Future `git config --global user.name` / `user.email` calls
  should report `rochalsk` and `rochalsk@akamai.com`; `--show-origin` should
  point to `~/.gitconfig` → `~/.tmux/git/.gitconfig`.
- **Rollback:** Restore the previous values in `~/.tmux/git/.gitconfig`.
- **Publication:** Not committed or pushed.

## 2026-09-15 — `r` alias for rtrsh (documentation + shell config)

- **Action:** Added `alias r='rtrsh'` to `~/.tmux/zsh/.zshrc` so interactive
  zsh shells on this host resolve `r <host>` to the remote traversal wrapper.
- **Scope:** User-shell configuration and host knowledge only. No services,
  packages, or system settings changed.
- **Evidence:** `rtrsh` is present at `/usr/local/bin/rtrsh`; the active shell
  config no longer defined `r`, so zsh fell back to the builtin `r`/history
  path and produced `fc: event not found` on hostnames.
- **Verification:** Fresh zsh sessions should report `alias r='rtrsh'` and
  `r <host>` should invoke `rtrsh <host>` rather than history expansion.
- **Rollback:** Remove the alias line from `~/.tmux/zsh/.zshrc` and restart the
  shell.
- **Publication:** Not committed or pushed.

## 2026-09-14 — Initial enrollment (documentation only)

- **Action:** Created host profile `profile.md` and this change log under
  `vm_admin_agent/hosts/work-muc-lhv582/`. Added registry row for
  `work-muc-lhv582` in `vm_admin_agent/hosts/README.md`.
- **Scope:** Documentation only. No system state changed. No packages
  installed, no services touched, no files modified outside the
  `agent_workspace` repository.
- **Evidence:** Local execution of `scripts/host_facts.py`, `uname -a`, `id`,
  and read of `/etc/os-release`. Logical ID `work-muc-lhv582` confirmed by the
  user out of band.
- **Verification:** Profile fields reflect the recorded discovery output;
  fields not probed are marked as unknown in the profile.
- **Rollback:** Delete the `work-muc-lhv582/` directory and revert the registry
  row in `hosts/README.md`. No system rollback needed.
- **Publication:** Not committed or pushed. Awaiting user review of the diff.
- **Follow-ups queued (not executed):**
  - Confirm desired scope of the `~/.tmux` ecosystem on this host.
  - Decide which `ynwa-vm` tools (if any) are appropriate to port here.
  - Decide whether `sudo`-scope administration is authorized on this host.

## 2026-09-14 — Read-only verification pass (documentation only)

- **Action:** Ran three read-only batches to fill unknowns in the profile:
  dotfile symlink resolution, `systemctl --failed`, `docker ps` + `docker
  inspect` + `docker network ls`, `sysctl.d` listing, and a non-interactive
  `sudo -n ufw status` probe. Updated `profile.md` §2 with findings.
- **Scope:** Read-only. No files changed outside the `agent_workspace` repo.
  No packages, services, containers, firewall, or sysctl entries were
  modified.
- **Evidence:** Command output captured in the session; not stored here to
  avoid leaking container volume paths or corporate config filenames beyond
  what is already summarised in the profile.
- **Key findings:**
  - `~/.tmux` symlink map fully deployed; default shell `zsh`.
  - `systemd-sysctl.service` has been failed since boot on 2026-06-22.
    `/etc/sysctl.d/` contains corporate-looking drop-ins; ownership
    unconfirmed. Not diagnosed further.
  - Two undocumented containers running for ~2 months: `rcm-db` (mariadb:10,
    `restart=no`) and `rcm-zookeeper` (zookeeper, `restart=always`). No
    compose file located.
  - `ufw` status could not be read: `sudo -n` refused (interactive password
    required, as expected).
- **Verification:** Findings reflected in profile §2 "Observed state" and §7
  "Open questions"; unknowns still marked as unknown.
- **Rollback:** N/A (no system change).
- **Publication:** Not committed or pushed.
- **Follow-ups queued (awaiting user decision):**
  - Diagnose `systemd-sysctl.service` failure or defer to corporate IT.
  - Identify owner and purpose of the `rcm-*` container stack; confirm
    `rcm-db restart=no` is intentional.
  - Approve a narrow interactive `sudo` invocation to read `ufw status
    verbose`, or leave firewall state unknown.
