# Agent Workspace

This repository tracks autonomous agents and their accumulated knowledge.

## Active Agents

| Agent | Instructions | Knowledge Base |
|-------|-------------|----------------|
| VM Administrator | `vm_admin_agent/vm_agent_context.md` | `vm_admin_agent/ynwa_vm.md` |

## Loading an Agent

Each agent's operating instructions live in its own folder. The VM
Administrator Agent is the currently active agent on this host. When operating
as the VM Administrator Agent, read the instructions and knowledge base below
before taking any action:

- Instructions: `vm_admin_agent/vm_agent_context.md`
- Knowledge base: `vm_admin_agent/ynwa_vm.md`

## Conventions

- Every agent keeps its operating rules in `*/agent_context.md` and its
  machine-state knowledge in `*/ynwa_vm.md` (or an equivalent canonical file).
- Structural or service changes MUST be self-documented by the acting agent in
  its knowledge base and any MOTD/banner script it owns.
- **Config dotfiles repo:** the interactive host configs (tmux, herdr,
  opencode, zsh, iTerm2) live in the `~/.tmux` git repo
  (`eradek/tmux_configs`) and are symlinked into place. This repo is the
  single source of truth for the tmux + herdr + opencode ecosystem. Changes to
  these configs must be made in `~/.tmux` (not in `~/.config/...`), and the
  repo's `README.md` + `tmux_cheat_sheet.html` must be kept in sync.
- **New-machine bring-up:** `bash ~/.tmux/setup.sh` is the one-command
  cross-platform installer (macOS/Linux/Ubuntu). Full procedure + layout are
  documented in `~/.tmux/README.md` and `vm_admin_agent/ynwa_vm.md` §7.