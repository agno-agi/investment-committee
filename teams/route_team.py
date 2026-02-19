"""
Route Team
----------

Routes each question to exactly one specialist.
Best for: quick, targeted questions.
"""

from agno.models.google import Gemini
from agno.team import Team, TeamMode

from agents import (
    committee_chair,
    financial_analyst,
    knowledge_agent,
    market_analyst,
    memo_writer,
    risk_officer,
    technical_analyst,
)

route_team = Team(
    id="route-team",
    name="Investment Team - Route",
    mode=TeamMode.route,
    model=Gemini(id="gemini-3.1-pro-preview"),
    members=[
        market_analyst,
        financial_analyst,
        technical_analyst,
        risk_officer,
        knowledge_agent,
        memo_writer,
        committee_chair,
    ],
    instructions=[
        "Route each question to exactly one specialist:",
        "- Macro/sector/news questions → Market Analyst",
        "- Fundamentals/valuation/financials → Financial Analyst",
        "- Price action/charts/momentum → Technical Analyst",
        "- Risk/downside/position sizing → Risk Officer",
        "- Research/past analysis/company deep dives → Knowledge Agent",
        "- Write a memo → Memo Writer",
        "- Final decisions/allocations → Committee Chair",
    ],
    show_members_responses=True,
    markdown=True,
)
