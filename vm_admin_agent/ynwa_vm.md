# VM Infrastructure & Networking Knowledge Base (ynwa_vm.md)

Canonical knowledge base for the VM Administrator Agent. This file is the
single source of truth for the host's infrastructure, services, and security
state. The login banner (`/etc/profile.d/99-welcome-banner.sh`) sources this
file for its `print-kb` output.

Last updated: 2026-09-03

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
      `ewelina` (UIDs 1000-1003), each with isolated paths under
      `/mnt/ynwa_storage`. Passwords injected via `.env`.
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
*   **Firewall rebuild:** `~/rebuild-firewall.sh`.

## 7. Security Notes
*   `/opt/filestash/.env` is `600 root:root` (SFTP credentials).
*   `/opt/immich/.env` is `600 root:root` (DB credentials) — hardened
    2026-09-03.
*   SFTP passwords for `atmoz/sftp` are injected from `.env` via
    environment variable interpolation in the compose `command` array.

## 8. Maintenance Log
*   **2026-09-03:** Recreated repo `agent_workspace` as a fresh git repo
    (branch `main`). Created `ynwa_vm.md` as canonical KB, added `AGENTS.md`
    entry point, wired `opencode.json` instructions, refactored banner
    `print-kb` to source this file, corrected kernel version to `6.8.0-138`.
    Applied 16 pending apt updates; hardened `/opt/immich/.env` to `600`.