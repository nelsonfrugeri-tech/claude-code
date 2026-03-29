# Skills Registry

| Skill | Path | Trigger | Purpose |
|-------|------|---------|---------|
| **arch-py** | `~/.claude/skills/arch-py/` | `/arch-py`, `/arch` | Python architecture, design patterns, type system, testing |
| **ai-engineer** | `~/.claude/skills/ai-engineer/` | `/ai-engineer` | LLM engineering, RAG, agents, multi-provider, caching |
| **review-py** | `~/.claude/skills/review-py/` | review-py skill | Code review templates, checklist, severity criteria |
| **product-manager** | `~/.claude/skills/product-manager/` | `/product-manager`, `/pm` | Product management, user stories, roadmap, backlog |

## Skill Dependencies

- `ai-engineer` complements `arch-py` (AI layer on top of Python foundation)
- `review-py` references `arch-py` for technical quality criteria
- All agents in AI projects should have `ai-engineer` as baseline skill
