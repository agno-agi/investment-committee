"""
Agentic Investment Committee
-----------------------------

A multi-agent investment committee demonstrating 5 architectures.

Run:
    python -m app.main
"""

import os
from pathlib import Path

from agno.os import AgentOS

from agents import (
    committee_chair,
    financial_analyst,
    knowledge_agent,
    market_analyst,
    memo_writer,
    risk_officer,
    technical_analyst,
)
from agents.settings import committee_knowledge
from teams import broadcast_team, coordinate_team, route_team, task_team
from workflows import investment_workflow

# ---------------------------------------------------------------------------
# Load research library into vector DB at startup
# ---------------------------------------------------------------------------
research_dir = Path(__file__).parent.parent / "research"
for subdir in ["companies", "sectors"]:
    path = research_dir / subdir
    if path.exists():
        committee_knowledge.insert(name=f"research-{subdir}", path=str(path), skip_if_exists=True)

# ---------------------------------------------------------------------------
# Create AgentOS
# ---------------------------------------------------------------------------
agent_os = AgentOS(
    name="Agentic Investment Committee",
    description="A multi-agent investment committee demonstrating 5 architectures",
    agents=[
        market_analyst,
        financial_analyst,
        technical_analyst,
        risk_officer,
        knowledge_agent,
        memo_writer,
        committee_chair,
    ],
    teams=[coordinate_team, route_team, broadcast_team, task_team],
    workflows=[investment_workflow],
    config="app/config.yaml",
)

app = agent_os.get_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RUNTIME_ENV", "") == "dev"
    agent_os.serve(app="app.main:app", port=port, reload=reload)
