"""
Coordinate Team
---------------

Chair (Gemini Pro) dynamically orchestrates analysts based on the question.
Best for: open-ended investment questions.
"""

from agno.learn import LearnedKnowledgeConfig, LearningMachine, LearningMode
from agno.models.google import Gemini
from agno.team import Team, TeamMode

from agents import (
    financial_analyst,
    knowledge_agent,
    market_analyst,
    memo_writer,
    risk_officer,
    technical_analyst,
)
from agents.settings import team_learnings

coordinate_team = Team(
    id="coordinate-team",
    name="Investment Team - Coordinate",
    mode=TeamMode.coordinate,
    model=Gemini(id="gemini-3.1-pro-preview"),
    members=[
        market_analyst,
        financial_analyst,
        technical_analyst,
        risk_officer,
        knowledge_agent,
        memo_writer,
    ],
    instructions=[
        "You are the Committee Chair of a $10M investment team.",
        "Dynamically decide which analysts to consult based on the question.",
        "For investment evaluations: start with Financial + Market analysts, then Risk, then Memo Writer.",
        "Always consult the Risk Officer before making allocation decisions.",
        "Provide a final recommendation with a specific dollar allocation.",
        "Ensure all decisions comply with the fund mandate.",
    ],
    learning=LearningMachine(
        knowledge=team_learnings,
        learned_knowledge=LearnedKnowledgeConfig(
            mode=LearningMode.AGENTIC,
            namespace="global",
        ),
    ),
    show_members_responses=True,
    markdown=True,
)
