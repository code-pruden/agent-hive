# agent-hive

A controlled agent hierarchy for Claude Code. Spawn subagents with role-based prompts, depth-limited recursion, heartbeat monitoring, and timeout enforcement.

## Roles

| Role | Purpose |
|------|---------|
| `coder` | Implement specific coding, scripting, or configuration tasks |
| `fast_reviewer` | Quick sanity check — top 3-5 issues only |
| `git_maintainer` | Inspect repo state, summarize changes, suggest commit plans |
| `orchestrator` | Coordinate multi-agent workflows and task decomposition |
| `reviewer` | Full review of designs, code, configs, or agent output |
| `summarizer` | Condense agent output or task results into compact summaries |

## Basic Usage

### agent_top

Entry point for the agent hierarchy. Reads an initial prompt and spawns the orchestrator.

```
~/agent-hive/bin/agent_top "Build a feature"
```

### spawn_agent

Spawn a single subagent with a given role and task.

```
~/agent-hive/bin/spawn_agent reviewer "Review this design for failure modes"
~/agent-hive/bin/spawn_agent coder "Implement the task runner"
```

### list_tasks

List recent tasks, newest first. Optional count argument (default 20).

```
~/agent-hive/bin/list_tasks
~/agent-hive/bin/list_tasks 5
```

### show_task

Print the result of a specific task.

```
~/agent-hive/bin/show_task 20260627T200059Z-reviewer-149721
```

## Task Results

Each spawned agent creates a directory under `tasks/<task_id>/` containing:

- `prompt.md` — the full prompt sent to the agent
- `result.md` — the agent's output (on success) or failure report
- `meta.env` — task metadata (role, depth, timestamps, paths)

## Secrets

API keys and credentials live **outside the repo** in:

```
~/.config/agent-hive/deepseek.env
```

This file is sourced by `bin/with_deepseek_env` and is never committed.

## Ignored Directories

The following are runtime/local directories and are not tracked in git:

- `tasks/` — agent prompt and result artifacts
- `logs/` — agent stdout/stderr logs
- `workspaces/` — per-agent working directories
- `.claude/` — local Claude Code harness configuration

## Current Status

**v0.1 — working subagent loop.** Spawn, review, and edit subagents function correctly with depth-limited recursion, heartbeat monitoring, and timeout enforcement. The `reviewer → coder → fast_reviewer → git_maintainer` pipeline has been exercised end-to-end.
