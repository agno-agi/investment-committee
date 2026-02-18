"""
Coordinate Team
---------------

Chair (Opus) dynamically orchestrates analysts based on the question.
Best for: open-ended investment questions.
"""

from agno.learn import LearnedKnowledgeConfig, LearningMachine, LearningMode
from agno.models.anthropic import Claude
from agno.team import Team, TeamMode

from agents import (
    financial_analyst,
    knowledge_agent,
    market_analyst,
    memo_writer,
    risk_officer,
    technical_analyst,
)
from agents.settings import committee_learnings

coordinate_team = Team(
    id="coordinate-team",
    name="Investment Committee - Coordinate",
    mode=TeamMode.coordinate,
    model=Claude(id="claude-opus-4-6"),
    members=[
        market_analyst,
        financial_analyst,
        technical_analyst,
        risk_officer,
        knowledge_agent,
        memo_writer,
    ],
    instructions=[
        "You are the Committee Chair of a $10M investment committee.",
        "Dynamically decide which analysts to consult based on the question.",
        "For investment evaluations: start with Financial + Market analysts, then Risk, then Memo Writer.",
        "Always consult the Risk Officer before making allocation decisions.",
        "Provide a final recommendation with a specific dollar allocation.",
        "Ensure all decisions comply with the fund mandate.",
    ],
    learning=LearningMachine(
        knowledge=committee_learnings,
        learned_knowledge=LearnedKnowledgeConfig(
            mode=LearningMode.AGENTIC,
            namespace="global",
        ),
    ),
    show_members_responses=True,
    markdown=True,
)
