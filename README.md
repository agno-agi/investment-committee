# Multi-Agent Investment Team

Multi-agent investment team powered by Agno and Gemini — 7 AI analysts collaborate across 5 architectures to deploy a $10M equity portfolio

## Architecture

```
AgentOS
├── Agents (7)
│   ├── Market Analyst        ── Exa web search + YFinance
│   ├── Financial Analyst     ── YFinance fundamentals
│   ├── Technical Analyst     ── YFinance technicals
│   ├── Risk Officer          ── YFinance + mandate enforcement
│   ├── Knowledge Agent       ── RAG search + memo file navigation
│   ├── Memo Writer           ── Writes investment memos to disk
│   └── Committee Chair       ── Final decision-maker (Gemini 3.1 Pro)
│
├── Teams (4)
│   ├── Coordinate Team       ── Dynamic multi-agent orchestration
│   ├── Route Team            ── Single-agent dispatch
│   ├── Broadcast Team        ── Parallel independent evaluation
│   └── Task Team             ── Autonomous task decomposition
│
└── Workflow (1)
    └── Investment Pipeline   ── Market → Financial+Technical → Risk → Memo → Chair
```

### Three-Layer Knowledge

| Layer | What | How |
|-------|------|-----|
| **Static Context** | Fund mandate, risk policy, evaluation process | Injected into every agent's system prompt via `context/` |
| **Research Library** | Company profiles, sector analyses | PgVector hybrid search (RAG) via `research/` |
| **Memo Archive** | Past investment memos and decisions | File-based navigation via `memos/` |

## Quick Start

### 1. Clone and configure

```sh
git clone https://github.com/agno-agi/investment-team.git investment-team
cd investment-team

cp example.env .env
# Edit .env and add your API keys
# GOOGLE_API_KEY=***
# EXA_API_KEY=*** # Optional -- Exa MCP is free (thank you!)
```

### 2. Start services

```sh
docker compose up -d --build
```

This starts PostgreSQL (with pgvector) and the API server.

### 3. Load research into the knowledge base

```sh
docker exec -it investment-team-api python -m app.load_knowledge
```

This loads company profiles and sector analyses into PgVector for RAG search. Only needs to run once — documents are skipped if they already exist.

### 4. Connect the UI

1. Open [os.agno.com](https://os.agno.com) and sign in
2. Click **Add OS** → **Local** → enter `http://localhost:8000`
3. Click **Connect**

You'll see all 7 agents, 4 teams, and the workflow ready to use.

## What to Try

**Route a simple question** (Route Team):
```
What's AAPL's P/E ratio?
```

**Run a full committee review** (Coordinate Team):
```
Should we invest in NVIDIA?
```

**Get parallel analyst opinions** (Broadcast Team):
```
Full committee review: evaluate TSLA for $2M
```

**Autonomous portfolio construction** (Task Team):
```
Deploy $10M across the top 5 AI stocks
```

**Deterministic pipeline** (Investment Workflow):
```
Run full investment review on NVIDIA
```

**Search the knowledge base** (Knowledge Agent):
```
What does our research say about semiconductors?
```

## Agents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| Market Analyst | Gemini 3 Flash | Exa MCP, YFinance | Macro environment, news, market conditions |
| Financial Analyst | Gemini 3 Flash | YFinance | Valuation, fundamentals, analyst estimates |
| Technical Analyst | Gemini 3 Flash | YFinance | Price action, indicators, support/resistance |
| Risk Officer | Gemini 3 Flash | YFinance | Position sizing, mandate compliance, risk limits |
| Knowledge Agent | Gemini 3 Flash | FileTools (read-only) | RAG over research library + memo file browsing |
| Memo Writer | Gemini 3 Flash | FileTools (read/write) | Drafts and saves standardized investment memos |
| Committee Chair | Gemini 3.1 Pro | None | Final BUY/HOLD/PASS decisions with conviction scores |

## Teams

| Team | Mode | Members | Use Case |
|------|------|---------|----------|
| Coordinate | Dynamic orchestration | 6 analysts | Open-ended investment questions |
| Route | Single dispatch | All 7 | Direct questions to the right specialist |
| Broadcast | Parallel evaluation | 4 analysts | Independent assessments synthesized together |
| Task | Autonomous decomposition | 6 analysts | Complex multi-step portfolio tasks |

## Workflow

The **Investment Review Pipeline** runs a deterministic 5-step process:

```
Market Assessment ──→ Deep Dive (parallel) ──→ Risk Assessment ──→ Investment Memo ──→ Committee Decision
                      ├─ Fundamental Analysis
                      └─ Technical Analysis
```

Each step's output feeds into the next, producing a complete investment memo with a final committee decision.

## Project Structure

```
investment-team/
├── agents/                     # 7 specialist agents
│   ├── settings.py             # Shared knowledge instances (import, never recreate)
│   ├── market_analyst.py
│   ├── financial_analyst.py
│   ├── technical_analyst.py
│   ├── risk_officer.py
│   ├── knowledge_agent.py
│   ├── memo_writer.py
│   └── committee_chair.py
├── teams/                      # 4 team configurations
│   ├── coordinate_team.py
│   ├── route_team.py
│   ├── broadcast_team.py
│   └── task_team.py
├── workflows/                  # Deterministic pipelines
│   └── investment_workflow.py
├── context/                    # Layer 1: Static context (system prompt)
│   ├── mandate.md              # Fund rules and constraints
│   ├── risk_policy.md          # Position and portfolio risk limits
│   ├── process.md              # Evaluation pipeline and decision framework
│   └── loader.py               # Reads *.md → COMMITTEE_CONTEXT string
├── research/                   # Layer 2: Research library (PgVector RAG)
│   ├── companies/              # 7 company profiles (NVDA, AAPL, MSFT, etc.)
│   └── sectors/                # 2 sector analyses (AI semis, cloud)
├── memos/                      # Layer 3: Memo archive (FileTools)
│   ├── nvda_2025_q3_buy.md     # Seed memo: NVIDIA BUY
│   └── tsla_2025_q2_pass.md    # Seed memo: Tesla PASS
├── db/                         # Database helpers
│   ├── session.py              # get_postgres_db(), create_knowledge()
│   └── url.py                  # Builds DB URL from environment
├── app/
│   ├── main.py                 # AgentOS entry point
│   └── config.yaml             # Quick prompts for the UI
├── scripts/                    # Dev scripts
├── compose.yaml                # Docker Compose (API + PostgreSQL)
├── Dockerfile
├── pyproject.toml
└── requirements.txt
```

## Deploy to Railway

```sh
railway login

./scripts/railway_up.sh
```

### Production Operations

**Load research into knowledge base:**
```sh
railway run python -m app.load_knowledge
```

**View logs:**
```sh
railway logs --service investment-team
```

**Redeploy after changes:**
```sh
railway up --service investment-team -d
```

**Open dashboard:**
```sh
railway open
```

## Local Development

```sh
# Install uv (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup virtual environment
./scripts/venv_setup.sh
source .venv/bin/activate

# Start PostgreSQL (required)
docker compose up -d investment-team-db

# Load research
python -m app.load_knowledge

# Run the app
python -m app.main
```

### Format and lint

```sh
source .venv/bin/activate
./scripts/format.sh      # ruff format + ruff check --fix
./scripts/validate.sh    # ruff check + mypy
```

### Load research

```sh
python -m app.load_knowledge            # Upsert (skip existing)
python -m app.load_knowledge --recreate # Drop and reload all
```

### Add dependencies

1. Edit `pyproject.toml`
2. Regenerate lockfile: `./scripts/generate_requirements.sh`
3. Rebuild: `docker compose up -d --build`

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | Yes | — | Gemini models + embeddings |
| `EXA_API_KEY` | Yes | — | Web search for Market Analyst |
| `PARALLEL_API_KEY` | No | — | ParallelTools for Market Analyst |
| `RUNTIME_ENV` | No | `prd` | Set to `dev` for auto-reload |
| `DB_HOST` | No | `localhost` | PostgreSQL host |
| `DB_PORT` | No | `5432` | PostgreSQL port |
| `DB_USER` | No | `ai` | PostgreSQL user |
| `DB_PASS` | No | `ai` | PostgreSQL password |
| `DB_DATABASE` | No | `ai` | PostgreSQL database name |

## Learn More

- [Agno Github](https://github.com/agno-agi/agno)
- [Agno Documentation](https://docs.agno.com)
- [AgentOS Documentation](https://docs.agno.com/agent-os/introduction)
- [Multi-Agent Teams](https://docs.agno.com/teams)
- [Tools & Integrations](https://docs.agno.com/tools/toolkits)
- [Agno Discord](https://agno.com/discord)
