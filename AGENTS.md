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