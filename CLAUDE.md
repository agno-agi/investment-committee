# CLAUDE.md

This file provides context for Claude Code when working with this repository.

## Project Overview

Agentic Investment Committee (AIC) — A multi-agent system built with Agno that simulates a professional investment committee deploying $10M into public equities. Demonstrates 5 multi-agent architectures, three-layer knowledge, and institutional learning.

## Architecture

```
AgentOS (app/main.py)
├── Agents (7 reusable specialists)
│   ├── Market Analyst          — macro trends, sector analysis, news (Exa + YFinance)
│   ├── Financial Analyst       — fundamentals, valuation, financials (YFinance)
│   ├── Technical Analyst       — price action, momentum, entry/exit (YFinance)
│   ├── Risk Officer            — downside scenarios, portfolio exposure (YFinance)
│   ├── Knowledge Agent         — research library (RAG) + memo archive (FileTools)
│   ├── Memo Writer             — synthesizes analysis into formal memos (FileTools)
│   └── Committee Chair         — final decisions, capital allocation (Opus 4.6)
│
├── Teams (4 architectures)
│   ├── Coordinate Team         — Chair orchestrates analysts dynamically
│   ├── Route Team              — routes questions to the right specialist
│   ├── Broadcast Team          — all analysts evaluate simultaneously
│   └── Task Team               — autonomous task decomposition
│
├── Workflows (1 architecture)
│   └── Investment Workflow     — deterministic pipeline with parallel steps
│
├── Three-Layer Knowledge
│   ├── Layer 1: Static Context     — mandate, risk policy, process (always in prompt)
│   ├── Layer 2: Research Library   — company profiles, sector analysis (PgVector RAG)
│   └── Layer 3: Memo Archive       — past investment memos (FileTools)
│
└── Institutional Learning          — patterns, corrections, insights (LearningMachine)
```

All specialist agents use:
- Claude Sonnet 4.6 model (`claude-sonnet-4-6`)
- PostgreSQL database (pgvector) for persistence
- Committee context (Layer 1) in system prompt
- Shared knowledge base (Layer 2) for RAG
- Shared learnings (institutional learning)

Committee Chair and team leaders use:
- Claude Opus 4.6 model (`claude-opus-4-6`)

## Key Files

| File | Purpose |
|------|---------|
| `app/main.py` | AgentOS entry point, registers all agents/teams/workflows |
| `app/load_knowledge.py` | Loads research documents into PgVector (run once) |
| `app/config.yaml` | Quick prompts for each agent, team, and workflow |
| `agents/settings.py` | Shared instances: knowledge, learnings, paths, URLs |
| `agents/market_analyst.py` | Market Analyst — Exa MCP + YFinance |
| `agents/financial_analyst.py` | Financial Analyst — YFinance |
| `agents/technical_analyst.py` | Technical Analyst — YFinance |
| `agents/risk_officer.py` | Risk Officer — YFinance |
| `agents/knowledge_agent.py` | Knowledge Agent — RAG + FileTools |
| `agents/memo_writer.py` | Memo Writer — FileTools (save) |
| `agents/committee_chair.py` | Committee Chair — Opus 4.6, no tools |
| `teams/coordinate_team.py` | Coordinate team (dynamic orchestration) |
| `teams/route_team.py` | Route team (single dispatch) |
| `teams/broadcast_team.py` | Broadcast team (parallel evaluation) |
| `teams/task_team.py` | Task team (autonomous decomposition) |
| `workflows/investment_workflow.py` | Deterministic 5-step pipeline |
| `context/loader.py` | Loads `*.md` context files into `COMMITTEE_CONTEXT` |
| `context/mandate.md` | Fund rules: $10M, public equities, limits |
| `context/risk_policy.md` | Position sizing, portfolio risk, rebalancing |
| `context/process.md` | 6-step evaluation pipeline |
| `db/session.py` | `get_postgres_db()` and `create_knowledge()` helpers |
| `db/url.py` | Builds database URL from environment |
| `compose.yaml` | Local development with Docker |

## Development Setup

### Virtual Environment

```bash
./scripts/venv_setup.sh
source .venv/bin/activate
```

### Format & Validation

```bash
source .venv/bin/activate && ./scripts/format.sh
source .venv/bin/activate && ./scripts/validate.sh
```

## Conventions

### Agent Pattern

All agents follow this structure:

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.learn import LearningMachine, LearnedKnowledgeConfig, LearningMode

from context import COMMITTEE_CONTEXT
from agents.settings import committee_knowledge, committee_learnings
from db import get_postgres_db

agent_db = get_postgres_db()

instructions = f"""\
You are the [Role] on a $10M investment committee.

## Committee Rules (ALWAYS FOLLOW)

{COMMITTEE_CONTEXT}

## Your Role
[Role-specific instructions...]
"""

my_agent = Agent(
    id="my-agent",
    name="My Agent",
    model=Claude(id="claude-sonnet-4-6"),
    db=agent_db,
    instructions=instructions,
    tools=[...],
    knowledge=committee_knowledge,
    search_knowledge=True,
    learning=LearningMachine(
        knowledge=committee_learnings,
        learned_knowledge=LearnedKnowledgeConfig(
            mode=LearningMode.AGENTIC,
            namespace="global",
        ),
    ),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
    enable_agentic_memory=True,
)
```

### Critical Rules

1. **Never duplicate knowledge instances** — always import from `agents.settings`
2. **All instructions include `COMMITTEE_CONTEXT`** via f-string (Layer 1)
3. **Opus for Chair/team leaders, Sonnet for specialists**
4. **Memos = files (FileTools), Research = vectors (PgVector)** — never mix
5. **`committee_chair` is NOT a member** of Coordinate/Broadcast/Task teams (the team `model=` acts as chair). It IS a member of Route team and the final Workflow step.
6. **No learning config** on: Memo Writer, Committee Chair, Knowledge Agent, Route team
7. **Agent IDs are kebab-case** and match `config.yaml` keys
8. **`skip_if_exists=True`** on research loading to prevent re-indexing

### Database

- Use `get_postgres_db()` from `db` module
- Knowledge bases use `create_knowledge()` from `db` module
- The `contents_table` parameter is only needed when provided to a Knowledge base

```python
# Shared knowledge instances (import from agents.settings)
from agents.settings import committee_knowledge, committee_learnings

# Agent database (no contents_table needed)
agent_db = get_postgres_db()
```

### Imports

```python
# Database
from db import db_url, get_postgres_db, create_knowledge

# Context
from context import COMMITTEE_CONTEXT

# Shared settings
from agents.settings import committee_knowledge, committee_learnings, MEMOS_DIR, EXA_MCP_URL

# Agents
from agents import (
    market_analyst, financial_analyst, technical_analyst,
    risk_officer, knowledge_agent, memo_writer, committee_chair,
)

# Teams
from teams import coordinate_team, route_team, broadcast_team, task_team

# Workflows
from workflows import investment_workflow
```

## Commands

```bash
# Setup virtual environment
./scripts/venv_setup.sh
source .venv/bin/activate

# Local development with Docker
docker compose up -d --build

# Load research into knowledge base
python -m app.load_knowledge
python -m app.load_knowledge --recreate  # Drop and reload

# Format & validation
./scripts/format.sh
./scripts/validate.sh

# Generate requirements
./scripts/generate_requirements.sh
```

## Environment Variables

Required:
- `ANTHROPIC_API_KEY` — for Claude models
- `OPENAI_API_KEY` — for embeddings
- `EXA_API_KEY` — for Exa web search

Optional:
- `PARALLEL_API_KEY` — for ParallelTools web search
- `RUNTIME_ENV` — set to `dev` for auto-reload
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASS`, `DB_DATABASE`

## Ports

- API: 8000
- Database: 5432

## Data Storage

| What | Layer | Storage | Table/Location |
|------|-------|---------|----------------|
| Investment mandate, risk policy | Layer 1 | Filesystem → prompt | `context/*.md` |
| Company research, sector analysis | Layer 2 | PgVector | `committee_knowledge` |
| Research document contents | Layer 2 | PostgreSQL | `committee_knowledge_contents` |
| Past investment memos | Layer 3 | Filesystem | `memos/*.md` |
| Discovered patterns, corrections | Learning | PgVector | `committee_learnings` |
| Learning contents | Learning | PostgreSQL | `committee_learnings_contents` |
| Session history | — | PostgreSQL | Automatic (Agno) |
| Agent memory | — | PostgreSQL | Automatic (Agno) |
