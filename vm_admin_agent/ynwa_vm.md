# VM Infrastructure & Networking Knowledge Base (ynwa_vm.md)

Canonical knowledge base for the VM Administrator Agent. This file is the
single source of truth for the host's infrastructure, services, and security
state. The login banner (`/etc/profile.d/99-welcome-banner.sh`) sources this
file for its `print-kb` output.

Last updated: 2026-09-12

## 1. System Overview
*   **Operating System:** Ubuntu 24.04.4 LTS
*   **Kernel:** 6.8.0-138-generic (as of 2026-09-03)
*   **Role:** Hybrid hypervisor (KVM/libvirt) and bare-metal application host.
*   **Hypervisor:** Configured for KVM (`libvirtd.service`) utilizing `virbr0`.
*   **VMs:** `haos` (Home Assistant OS) running via libvirt/QEMU with TCG
    emulation (no KVM acceleration), 4 GiB RAM, 2 vCPU, UEFI/OVMF + TPM.

## 2. Network Ecosystem & Routing
*   **Public IP Interfaces:** IPv4: `172.238.101.81` (on `eth0`),
    IPv6: `2600:3c17::2000:bdff:feb3:bef8`
*   **Local / Sub-Interfaces:** `eth0.2` (VLAN 2): `192.168.5.1/24`
*   **WireGuard VPN (`wg0`):** Tunnel Network `10.0.0.0/24`. Primary Gateway:
    Mikrotik (`91.224.128.76`).

## 3. Firewall (UFW) Configuration
*   **SSH / WireGuard:** Allowed from Anywhere.
*   **AdGuard Home / Jellyfin:** Allowed strictly on `wg0` and trusted VPN
    subnets.
*   Hosted Docker services bind to `192.168.5.1` (VLAN 2) only:
    Filestash `:8334`, SFTP `:2222`, Immich `:2283`.

## 4. Hosted Services & Applications
*   **Jellyfin (`jellyfin.service`):** Media server natively on port 8096,
    backed by Rclone vault mounts (`/mnt/video`).
*   **AdGuard Home (`AdGuardHome.service`):** Network ad blocker, install at
    `/opt/AdGuardHome`.
*   **Docker Stacks** (all auto-restart, bound to `192.168.5.1`):
    - **Filestash** (`/opt/filestash/docker-compose.yml`): Web client proxy for
      a dedicated `atmoz/sftp` container. SFTP users: `admin`, `morze`, `ynwa`,
      `ewelina`, all **UID/GID `1000:1000`** (all mounted shares are host-owned
      by `1000:1000`, so each user needs the same UID to write). Each user is
      chrooted to `/home/<user>` and sees data at `/share/data` (mapped from
      `/mnt/ynwa_storage` subdirs). Passwords injected via `.env`
      (`SFTP_<USER>_PASS`) and interpolated into the compose `command` array.

*   **Filestash web login (`:8334`):** Auth middleware =
      `passthrough` (strategy `username_and_password`), attribute mapping:
      `hostname=sftp`, `port=22`, `username={{ .user }}`,
      `password={{ .password }}`, `path=/share/data`. Result: login page asks
      only user+password, and every user lands directly in their data folder
      (no clicking `share → data`). **Important:** Filestash's container can only
      reach the SFTP server via internal DNS `sftp:22` — the published
      `192.168.5.1:2222` is unreachable from inside the container and must
      NOT be used in the mapping.
    - **Immich** (`/opt/immich/docker-compose.yml`): Photo manager on `:2283`.
      Stack: `immich_server`, `immich_machine_learning`, `immich_redis`,
      `immich_postgres` (PostgreSQL 14 + pgvector). External libraries bind
      `/mnt/ynwa_storage/general_storage/media` and
      `/mnt/ynwa_storage/morze/media`.
*   **Rclone Storage Mounts** (systemd units, FUSE):
    - `rclone-storage.service` → `linodes3:ynwa-storage` at `/mnt/ynwa_storage`
    - `rclone-video.service` → `media_vault:` at `/mnt/video`

## 5. Mobile Security & Pipeline Architecture
*   **Isolated Chroot Strategy:** Root jail owned by `root:root` with `755`
    permissions. Uploads land in nested `/uploads` directories owned by
    dropzone users to permit FolderSync post-sync deletions.
*   **Modular Automated Sweeper (`/usr/local/bin/sync-sweeper.sh`):** Runs via
    CRON. Deduplicates via `cmp -s` byte checks and standardizes EXIF
    dates/names into `YYYY` folders. Unconditionally fires API `PUT` webhooks
    to Immich on every execution.
*   **Upload automation:** `~/upload/upload_video.sh`,
    `~/upload/upload_video_back.sh` (media vault), `~/upload/lock_vault.sh`.

## 6. Custom Scripts & Tools
*   **Dynamic MOTD:** `/etc/profile.d/99-welcome-banner.sh` displays metrics,
    systemd health, Docker status, and exports `print-kb`. Restricted to
    `rochalsk` and `root`.
*   **`herdr`:** Management binary at `~/.local/bin/herdr`.
*   **`watch-agent`:** Script at `~/.local/bin/watch-agent` that live-tails
    opencode's SQLite DB (`~/.local/share/opencode/opencode.db`) and renders
    the agent's bash tool commands + output as a clean terminal feed. Use in a
    herdr split pane next to the opencode session (`prefix+minus` to split).
    Flags: `--once`, `--last N` (backfill), `--session ID`, `--poll SECS`.
*   **`opencode-status.sh`:** Script at `~/.local/bin/opencode-status.sh`
    (symlinked from `~/.config/herdr/opencode-status.sh`). Read by herdr's
    `[ui] tab_bar_right` command entry every 5s; prints the active opencode
    session's current context size + cost (from `opencode.db`: latest
    `step-finish` part's `tokens.total`, plus the session row's `cost`).
    Replaces the info the opencode TUI sidebar normally shows. Prints nothing
    when no session is active (herdr then hides the entry).
*   **Firewall rebuild:** `~/rebuild-firewall.sh`.

## 7. Interactive Ecosystem Configs (tmux · herdr · opencode)
*   **Single source of truth:** the interactive host configs live in the
    `~/.tmux` git repo (`git@github.com:eradek/tmux_configs.git`,
    branch `main`) and are **symlinked** into place — same pattern as tmux.
    Changes MUST be made in `~/.tmux`, never in `~/.config/...`, and the
    repo's `README.md` + `tmux_cheat_sheet.html` must be kept in sync.
*   **Symlink map:**
    - `~/.tmux.conf` → `~/.tmux/.tmux.conf`
    - `~/.config/herdr/config.toml` → `~/.tmux/herdr/config.toml`
    - `~/.config/herdr/opencode-status.sh` → `~/.local/bin/opencode-status.sh`
    - `~/.config/opencode/opencode.jsonc` → `~/.tmux/opencode/opencode.jsonc`
    - `~/.local/bin/watch-agent` → `~/.local/bin/watch-agent` (standalone
      helper, not tracked — repo `/scripts/` is git-ignored)
*   **herdr-managed opencode integration artifacts** (kept in
    `~/.config/opencode`, NOT tracked in `~/.tmux`, regenerated by
    `herdr integration install opencode`):
    - `~/.config/opencode/plugins/herdr-agent-state.js` (lifecycle + session id)
    - `~/.config/opencode/herdr-tui-session.js` + `~/.config/opencode/tui.jsonc`
      (TUI plugin reporting the pane's selected session; path is relative to
      `~/.config/opencode`, so these must NOT be symlinked into the repo).
*   **herdr tab bar + agent rows:** `[ui] tab_bar_right` shows live opencode
    context + cost via `opencode-status.sh`; `[ui.sidebar.agents.rows_by_agent]
    opencode` adds `terminal_title_stripped` so the agents panel shows each
    opencode pane's **session title** (opencode emits `OC | <title>`).
*   **Prefix map:** tmux = `Ctrl+q`, herdr = `Ctrl+s`, opencode = `Ctrl+x`
    leader. Quick-setup guide: `~/.tmux/README.md` (clone → symlink → install
    tools → start). Full keymap reference: `~/.tmux/tmux_cheat_sheet.html`.
*   **herdr keymap** (all `prefix+` = `ctrl+s` then key): `?` help, `c` new
    tab, `minus`/`_` stack/side splits, `x`/`Shift+x` close pane/tab, `h/j/k/l`
    focus, `arrows` resize, `Shift+h/j/k/l` swap panes, `plus` zoom, `r` reload,
    `q` detach, `Tab`/`Shift+Tab` cycle pane, `p`/`n` prev/next tab. Swap-pane
    keys are intentionally **not** listed in herdr's `prefix+?` help panel.
*   **New-machine bring-up (`setup.sh`, macOS + Linux + Ubuntu):**
    1. `git clone git@github.com:eradek/tmux_configs.git ~/.tmux`
    2. `bash ~/.tmux/setup.sh` — symlinks tmux/herdr/opencode/zsh/git configs,
       installs zsh + Oh My Zsh + p10k + autosuggestions + syntax-highlighting,
       installs MesloLGS NF fonts (`fonts/` auto-downloads if missing), checks
       herdr/opencode binaries. Idempotent; existing files backed up as
       `*.bak-<timestamp>`.
    3. macOS extras (in setup.sh): brew check, `chsh -s zsh`, imports iTerm2
       plist from `iterm2/`. Set iTerm2 profile font → **MesloLGS NF Regular**
       (exported plist uses Monaco, which lacks p10k glyphs).
    4. iTerm2 plist: `iterm2/com.googlecode.iterm2.plist` is the one-to-one
       profile export (both `Default` + `Radek` profiles); import via
       Preferences → General → Load preferences from `~/.tmux/iterm2`.
       `*.itermexport` (full state backups) are git-ignored — never commit.
    5. New-host secrets: create `~/.opencode.env` (API keys) per machine —
       git-ignored. Relative-path project instructions (AGENTS.md etc.) come
       from each project's own `opencode.json`; the global
       `opencode/opencode.jsonc` is intentionally schema-only for portability.
*   **Ecosystem updates & health (`~/update-ecosystem.sh`):** Manual-only
    updater (per policy, NOT scheduled) that brings tmux/zsh (apt), oh-my-zsh,
    powerlevel10k, herdr (`herdr update`), opencode (`opencode upgrade`) and
    fonts up to date. After running, it refreshes `~/.cache/ecosystem-versions`.
    The login banner renders a **Terminal Ecosystem Status** block via
    `~/.local/bin/ecosystem-versions.sh` (shows installed vs latest per tool
    with ✓ / ⚠ update markers). apt checks are offline; git/npm/github checks
    are cached so the banner stays fast.

## 8. Security Notes
*   `/opt/filestash/.env` is `600 root:root` (SFTP credentials.
*   `/opt/immich/.env` is `600 root:root` (DB credentials) — hardened
    2026-09-03.
*   SFTP passwords for `atmoz/sftp` are injected from `.env` via
    environment variable interpolation in the compose `command` array.

## 9. Maintenance Log
*   **2026-09-14:** Hardened `~/.tmux/setup.sh` for clean deploy-to-new-Ubuntu-server
    (fixes from real remote bring-up). (a) `setup.sh` now installs `fontconfig`
    on Linux when `fc-cache` is missing (bare servers lack it → fonts step
    failed). (b) `setup.sh` now actually installs herdr + opencode instead of
    only warning; opencode install auto-sets npm prefix to `$HOME/.local`
    (avoids EACCES on unwritable `/usr/local/lib/node_modules`, and
    `~/.local/bin` is already on PATH). Reverted global `opencode.jsonc` to
    schema-only (kept portable; agent instructions load per-project from
    `agent_workspace/opencode.json`). README manual steps updated in sync.
    Commit & push `~/.tmux`.
*   **2026-09-13:** Added Terminal Ecosystem health tracking. New
    `~/update-ecosystem.sh` (manual-run only, per policy) updates tmux/zsh
    (apt), oh-my-zsh + powerlevel10k (git), herdr, opencode, fonts. New
    `~/.local/bin/ecosystem-versions.sh` resolves installed vs latest per tool
    (apt offline; git/npm/GitHub cached in `~/.cache/ecosystem-versions`) and
    is rendered in the login banner as **Terminal Ecosystem Status** with ✓/⚠
    markers. Verified: banner renders, cache writes/loads cleanly, current
    status shows tmux/zsh current; omz/p10k/herdr (0.8.2→0.9.0)/opencode
    (1.18.27→1.18.30) behind. **Not yet run:** `~/update-ecosystem.sh` (user
    will run manually).
*   **2026-09-13:** Completed cross-platform terminal bring-up for the `~/.tmux`
    repo. Added `zsh/` (portable `.zshrc` — banner/`opencode.env`/`vvault`
    guarded per-OS, PATH→`$HOME/.local/bin`), `git/.gitconfig`, `fonts/`
    (MesloLGS NF TTFs committed + auto-download fallback via
    `romkatv/powerlevel10k-media`), `iterm2/com.googlecode.iterm2.plist`
    (one-to-one profile export, both Default+Radek profiles; emptied
    `Working Directory` for cross-user portability), and `setup.sh`
    (idempotent cross-platform bring-up: symlinks → zsh/p10k/plugins → fonts →
    herdr/opencode → macOS iTerm2). `iTerm2 State.itermexport` removed + git
    ignored (`*.itermexport`). `*.env`/`.opencode.env` git-ignored. Global
    `opencode.jsonc` reverted to schema-only (project instructions live in each
    project's `opencode.json`). Symlinked this server's `~/.zshrc`,
    `~/.p10k.zsh`, `~/.zprofile`, `~/.gitconfig` into the repo (originals saved
    as `*.orig`). Verified: `herdr config check` ok, opencode json valid, zsh
    loads with p10k + 3 plugins, setup.sh runs clean end-to-end.
*   **2026-09-12:** OpenCode TUI sidebar (Context/tokens/$/LSP) hidden with the
    `sidebar_toggle` keybind (`ctrl+x b`). Moved the context/spend info to
    herdr's tab row: new helper `~/.local/bin/opencode-status.sh` (symlinked
    as `~/.config/herdr/opencode-status.sh`) reads opencode's SQLite DB
    (latest `step-finish` `tokens.total` + session `cost`) and is rendered via
    `[ui] tab_bar_right` (`{ type = "command", interval_seconds = 5 }`).
    Agents sidebar now shows each opencode pane's session title:
    `[ui.sidebar.agents.rows_by_agent] opencode = [["state_icon","agent"],
    ["terminal_title_stripped"],["workspace","tab"]]` (opencode sets terminal
    title `OC | <session title>`). Installed `herdr integration install
    opencode` (managed artifacts in `~/.config/opencode`: `plugins/
    herdr-agent-state.js`, `herdr-tui-session.js`, `tui.jsonc`). Fixed
    `/etc/profile.d/99-welcome-banner.sh`: added a POSIX guard so the banner
    is skipped under `/bin/sh` (dash) — its bash-isms (`[[`, `print-kb()`
    name) were aborting any `sh -lc` command (rc=2), which broke herdr's
    tab_bar_right commands. Banner still renders for interactive bash/zsh.
    Updated `~/.tmux/README.md` + this KB. Restart opencode (reloads plugins)
    and commit & push `~/.tmux`.
*   **2026-09-04:** Moved herdr + opencode configs into the `~/.tmux` config
    repo (`eradek/tmux_configs`) and symlinked them into place
    (`~/.config/herdr/config.toml` and `~/.config/opencode/opencode.jsonc`),
    mirroring the tmux dotfiles pattern. Copied `watch-agent` into
    `~/.tmux/scripts/` for portability. Rewrote `tmux_cheat_sheet.html` as a
    full tmux · herdr · opencode ecosystem cheatsheet and added a
    `README.md` quick-setup guide (clone → symlink → install → start).
    Updated `~/.tmux/.gitignore` (herdr state, node deps). Revised herdr
    keymap to final state: `prefix+arrows` resize, `prefix+shift+h/j/k/l`
    swap panes (herdr defaults, avoid the help-panel-unset pitfall),
    `prefix+p/n` tabs (removed direct `shift+left/right` to avoid tmux clash).
*   **2026-09-04:** Fixed Filestash login flow. Compose hardcoded
    `TestPass123` for SFTP users — replaced with `${SFTP_<USER>_PASS}`
    interpolation so real `.env` passwords take effect. Changed all SFTP user
    UIDs/GIDs to `1000:1000` (was 1000-1003) so every user can write to
    their host share (all owned by `1000:1000`). In Filestash admin
    (`/admin/storage`), set auth middleware `passthrough` strategy
    `username_and_password` (was `direct`, which auto-submitted empty creds →
    "Invalid account" hang). Attribute mapping set to `hostname=sftp`,
    `port=22`, `{{ .user }}` / `{{ .password }}`, `path=/share/data` so login
    page asks only user+password and users land directly in their data folder.
*   **2026-09-03:** Created `~/.local/bin/watch-agent` (Python) — live-tails
    opencode's `part` table in `~/.local/share/opencode/opencode.db` and
    renders bash tool commands + output as a clean colored feed for a herdr
    split pane. Flags: `--once`, `--last N`, `--session ID`, `--poll SECS`.
    Self-documenting source: querying bash parts by `type=tool`, `tool=bash`,
    reading `state.input.command` and `state.metadata.output`.
*   **2026-09-03:** Cleared 495M full swap (`swapoff -a && swapon -a`), swap now idle at 0B.
    Reduced `vm.swappiness` from 60 to 10 (runtime + persisted via
    `/etc/sysctl.d/99-swappiness.conf`) to limit eager swapping on the
    Immich/Jellyfin/libvirt host.
*   **2026-09-03:** Replaced herdr's broken `[keys]` block (unknown `pane_*`
    keys + unsafe direct `x/c/_/-` bindings that herdr disabled) with a
    tmux.conf mirror under prefix `ctrl+s`: `prefix+c` new tab, `prefix+minus`
    / `prefix+_` splits, `prefix+x` / `prefix+shift+x` close pane/tab,
    `prefix+h/j/k/l` focus, `prefix+shift+h/j/k/l` + `prefix+arrows` resize,
    `prefix+>` / `prefix+<` swap down/up, `prefix+plus` zoom, `prefix+r`
    reload, `shift+left/right` tab switch. Set
    `[ui.sidebar.agents] rows = [["state_icon","agent"],["workspace","tab"]]`
    so the sidebar shows agent names (e.g. `opencode`) instead of workspace
    names. Validated with `herdr config check` (ok) and applied via
    `herdr server reload-config`.
*   **2026-09-03:** Recreated repo `agent_workspace` as a fresh git repo
    (branch `main`). Created `ynwa_vm.md` as canonical KB, added `AGENTS.md`
    entry point, wired `opencode.json` instructions, refactored banner
    `print-kb` to source this file, corrected kernel version to `6.8.0-138`.
    Applied 16 pending apt updates; hardened `/opt/immich/.env` to `600`.