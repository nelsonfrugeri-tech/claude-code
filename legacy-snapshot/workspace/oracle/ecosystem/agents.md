# Agent Registry

## Core Agents (Ecosystem)

| Agent | File | Role | Model | Skills | Tools |
|-------|------|------|-------|--------|-------|
| **oracle** | oracle.md | Ecosystem Manager | opus | arch-py, ai-engineer, product-manager, review-py | All |
| **architect** | architect.md | Software Architect | opus | arch-py | Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch |
| **dev-py** | dev-py.md | Python Developer | opus | arch-py | Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch |
| **review-py** | review-py.md | Code Reviewer | opus | review-py, arch-py | Read, Grep, Glob, Bash, Write |
| **tech-pm** | tech-pm.md | Product Manager | opus | product-manager | Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch |
| **explorer** | explorer.md | Codebase Analyzer | opus | — | Read, Grep, Glob, Bash, Write, WebSearch, WebFetch |
| **builder** | builder.md | Infra Builder | opus | — | Read, Glob, Grep, Bash, Task, AskUserQuestion |
| **debater** | debater.md | Skills Debater | opus | — | Glob, Read, Grep, WebSearch, WebFetch, Write, AskUserQuestion, Bash |
| **executor** | executor.md | Skills Executor | opus | — | Glob, Read, Grep, Edit, Write, Bash, AskUserQuestion |

## bike-shop Agents (Slack Personas)

| Agent | File | Persona | Slack App Name |
|-------|------|---------|----------------|
| **elliot-alderson** | elliot-alderson.md | Brilliant dev, obsessive about clean code & security | Elliot Alderson |
| **mr-robot** | mr-robot.md | Senior architect, direct, blunt, zero tolerance for BS | Mr. Robot |
| **tyrell-wellick** | tyrell-wellick.md | Ambitious PM, organized, strategic, obsessed with execution | Tyrell Wellick |
| **slack-monitor** | slack-monitor.md | Monitors Slack agent processes | — |

## Agent Creation Checklist

When creating a new agent:

1. Create `~/.claude/agents/{name}.md` with frontmatter (name, description, tools, model, skills)
2. Define persona and workflow in the body
3. Register in this file
4. If Slack agent: create Slack App (see `procedures/slack-app-setup.md`)
5. If needs GitHub: create GitHub App (see `procedures/github-app-setup.md`)
6. Test with `claude --agent {name}`
