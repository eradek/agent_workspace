# Host profile: work-muc-lhv582

Owner agent: `vm_admin_agent`
Status: **observed** (initial enrollment; no service-level verification yet)
Observed at: 2026-09-14 (UTC)
Verification method: local execution of `scripts/host_facts.py`, `uname -a`,
`id`, `/etc/os-release` read. Hostname is a hint, confirmed out of band by the
user selecting the logical ID.
Revalidation trigger: any system change, OS upgrade, tool install, or before
proposing a mutation on this host.

## 1. Identity and scope

- **Logical ID:** `work-muc-lhv582`
- **User's shorthand:** `work-vm` refers to this host (confirmed 2026-10-05);
  it is distinct from `ynwa-vm`.
- **Hostname hint:** `muc-lhv582`
- **Purpose:** Work laptop / interactive workstation (user-confirmed via
  enrollment request; specific role beyond terminal + dev tooling not yet
  established).
- **Environment boundary:** Personal work machine of `rochalsk`. NOT part of the
  `ynwa-vm` environment. Private/business tools from `ynwa_vm.md` MUST NOT be
  copied here without separate approval.
- **Execution context:** Local process host. No SSH controller/target
  separation for this record.

## 2. Observed state

### Operating system

- Distribution: Ubuntu 24.04.4 LTS (`PRETTY_NAME`, `/etc/os-release`)
- Version ID: `24.04`
- Kernel: `6.8.0-117-generic` (`uname -r`)
- Architecture: `x86_64`
- Init: systemd (inferred from `systemctl` present; not health-checked)

### User and privilege

- Interactive user: `rochalsk` (uid 34349, gid 34349)
- Group membership: `adm`, `sudo`, `staff`, `users`, `docker`
- Effective root during enrollment: no
- Sudo: available (not exercised during enrollment)

### Tools on PATH (presence only, no version/health check)

| Tool        | Present | Notes |
| ----------- | ------- | ----- |
| `apt-get`   | yes     | System package manager (Ubuntu native) |
| `docker`    | yes     | User is in `docker` group; daemon health not verified |
| `git`       | yes     | Used by dotfiles workflow |
| `herdr`     | yes     | Terminal multiplexer (ecosystem tool) |
| `opencode`  | yes     | This agent runtime |
| `python3`   | yes     | Used by `scripts/host_facts.py` |
| `ssh`       | yes     | Client present; server status not verified |
| `sudo`      | yes     | See privilege section |
| `systemctl` | yes     | systemd is present |
| `tmux`      | yes     | Ecosystem tool |
| `ufw`       | yes     | Binary present; ruleset / active state NOT verified |
| `brew`      | no      | Confirms non-macOS |
| `launchctl` | no      | Confirms non-macOS |
| `virsh`     | no      | No libvirt hypervisor role |
| `code`      | no      | VS Code CLI not on PATH |
| `claude`    | no      | Claude CLI not present |

### Dotfile ecosystem (verified 2026-09-14)

The `~/.tmux` symlink map documented in `ynwa_vm.md` §7 is fully deployed here:

- `~/.tmux.conf` → `~/.tmux/.tmux.conf`
- `~/.config/herdr/config.toml` → `~/.tmux/herdr/config.toml`
- `~/.config/opencode/opencode.jsonc` → `~/.tmux/opencode/opencode.jsonc`
- `~/.zshrc` → `~/.tmux/zsh/.zshrc`
- `~/.gitconfig` → `~/.tmux/git/.gitconfig`
- Default shell: `/usr/bin/zsh`
- SSH-agent forwarding support via `~/.zprofile` / `~/.zshenv` stable socket
  symlink pattern for herdr panes and new ssh logins.
- Interactive shell alias: `r` → `rtrsh` in `~/.tmux/zsh/.zshrc`.
- SSH-agent forwarding/herdr follow-up (observed 2026-10-05; see change log):
  on this work VM, SSH-forwarded identities from the user's Mac were available
  in the SSH login shell, but a herdr pane used a different, empty agent socket.
  In that pane, explicitly exporting
  `SSH_AUTH_SOCK="$HOME/.ssh-agent-forward/socket"` made `ssh-add -l` show the
  forwarded identities. `~/.zprofile` maintains this stable symlink on SSH
  login, and `~/.zshenv` only falls back to it if an inherited socket is absent
  or not a socket; it does not replace a different live socket. The herdr server
  launch environment and automatic inheritance behavior have not been verified.
- Git config on this machine mirrors `/u0/rochalsk/.gitconfig`:
  `user.name=Radek Ochalski`, `user.email=rochalsk@akamai.com`,
  `push.default=simple`, and `remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*`.
- Powerlevel10k branch display is customized to preserve the beginning of long
  branch names and truncate the tail in `~/.tmux/zsh/.p10k.zsh`.

Not verified: `~/.opencode.env`, `~/.p10k.zsh`, fonts install,
  `watch-agent`, `opencode-status.sh`, `ecosystem-versions.sh`, banner, and
  `update-ecosystem.sh`.

### systemd health (observed 2026-09-14)

- **1 failed unit:** `systemd-sysctl.service` — exited `status=1/FAILURE` at
  boot on 2026-06-22 and has not been re-run since. Journal shows only the
  generic failure line; the offending sysctl key is not identified.
- `/etc/sysctl.d/` contains ten `10-*.conf` drop-ins (looks corporate-managed:
  `10-akamai.conf`, `10-kernel-hardening.conf`, `10-bufferbloat.conf`, etc.)
  plus `99-sysctl.conf` and `/etc/sysctl.conf`. Ownership and origin of these
  drop-ins are not yet confirmed. Do NOT edit without approval and clarity on
  who manages them (likely corporate config-management).
- Other units not probed.

### Docker (observed 2026-09-14)

Two long-running containers (up ~2 months), not documented in the knowledge
base, origin unconfirmed by the user:

| Container | Image | Restart | Ports (unpublished) | Volumes |
| --- | --- | --- | --- | --- |
| `rcm-db` | `mariadb:10` | `no` ⚠️ | `3306/tcp` | named `rcm_db_volume` → `/var/lib/mysql` |
| `rcm-zookeeper` | `zookeeper` | `always` | `2181, 2888, 3888, 8080` | 3 anonymous volumes → `/data`, `/datalog`, `/logs` |

Both attached to the default `bridge` network. No `docker compose` project file
located yet. `rcm-db`'s `restart=no` means it will NOT come back after a
reboot; flagged for user confirmation of intent.

Networks: only stock `bridge`, `host`, `none`.

### Firewall

`ufw` binary is installed but active-state/ruleset checks require root.
`sudo -n` was refused (interactive password required), which is the expected
security posture. Not verified.

### Explicitly unknown (not yet probed)

- Firewall active state and rule set (`ufw status verbose`)
- Full systemd unit inventory beyond failed units
- Network interfaces, routes, DNS resolvers
- Storage layout, mount points, disk usage
- Docker daemon config, image list, other stopped containers
- Pending apt updates, unattended-upgrades configuration
- SSH server presence and configuration
- Origin/manager of `/etc/sysctl.d/*` drop-ins (corporate MDM? Ansible? manual?)
- Purpose of the `rcm-*` container stack and its owning compose file (if any)
- Presence of `~/.opencode.env` and other secret files

Do NOT infer any of the above from `ynwa_vm.md`.

## 3. Desired state

Not yet defined. Enrollment does not imply any desired configuration.
Any target state must be proposed and approved as a separate change.

## 4. Ownership and integrations

- **Dotfiles / interactive configs:** The current working directory of this
  session is `/home/rochalsk/.tmux`, which matches the `~/.tmux` git-repo
  symlink pattern documented for `ynwa-vm`. Whether the full symlink map
  (`.tmux.conf`, herdr `config.toml`, opencode `opencode.jsonc`, zsh, git,
  fonts) is deployed here has **not been verified**. To be checked before any
  edits.
- **Agent workspace repository:** `/home/rochalsk/agent_workspace` on branch
  `main`, clean tree at enrollment time.
- **Banner integration:** Unknown. `ynwa_vm.md` mentions
  `/etc/profile.d/99-welcome-banner.sh` and a `print-kb` function; presence on
  this host is NOT confirmed and MUST NOT be assumed.
- **Secret store references:** None recorded. No secrets have been read or
  stored during enrollment.

## 5. Safety and allowed operations

Enrollment authorizes only:

- Read-only discovery via approved commands agreed with the user.
- Writing this profile and its `changes.md` inside
  `vm_admin_agent/hosts/work-muc-lhv582/`.
- Updating the host registry table in `vm_admin_agent/hosts/README.md`.

Enrollment does NOT authorize:

- Package installation, upgrades, or removal.
- Enabling, disabling, starting, or stopping services.
- Editing firewall rules, SSH configuration, or network settings.
- Modifying files outside the agent workspace repository.
- Committing or pushing any git repository.
- Copying tools, scripts, or configuration from the `ynwa-vm` profile to this
  host.
- Elevation with `sudo` for any purpose.

Each future mutation requires: exact target, exact commands, expected impact,
verification method, rollback plan, and explicit user approval.

## 6. Recovery / rollback

Not applicable for enrollment (documentation only). No system state was
changed.

## 7. Open questions for the user

1. Intended role and scope of this machine (workstation only, or does it host
   services? — note: two `rcm-*` docker containers are running).
2. Which parts of the `~/.tmux` ecosystem (herdr, opencode, zsh, p10k, fonts,
   `watch-agent`, `ecosystem-versions.sh`, banner) are desired here and which
   are explicitly out of scope for a work machine. (Symlinks verified in
   place; auxiliary scripts and banner not yet checked.)
3. Whether `sudo`-scoped administration is on the table for this host, or
   whether this agent should remain user-scope only. Password-sudo is
   currently the only path (non-interactive sudo refused).
4. Whether a private/business boundary applies (e.g. work-only content policy,
   no personal cloud mounts).
5. **`rcm-db` / `rcm-zookeeper`:** what is this stack, who owns it, is
   `rcm-db`'s `restart=no` intentional, and where is its compose file?
6. **`systemd-sysctl.service` failure since 2026-06-22:** who manages the
   `/etc/sysctl.d/10-*.conf` drop-ins (corporate MDM, Ansible, manual)? Should
   this be diagnosed and fixed, or left to corporate IT?
