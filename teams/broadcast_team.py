from agno.learn import LearnedKnowledgeConfig, LearningMachine, LearningMode
from agno.models.anthropic import Claude
from agno.team import Team, TeamMode

from agents import (
    financial_analyst,
    market_analyst,
    risk_officer,
    technical_analyst,
)
from agents.settings import committee_learnings

broadcast_team = Team(
    id="broadcast-team",
    name="Investment Committee - Broadcast",
    mode=TeamMode.broadcast,
    model=Claude(id="claude-opus-4-6"),
    members=[
        market_analyst,
        financial_analyst,
        technical_analyst,
        risk_officer,
    ],
    instructions=[
        "You are the Committee Chair synthesizing independent analyst views.",
        "All analysts have evaluated this investment simultaneously.",
        "Synthesize their perspectives into a unified recommendation.",
        "Note where analysts agree and disagree.",
        "Provide a final BUY/HOLD/PASS decision with a specific dollar allocation.",
        "Weight the Risk Officer's concerns heavily in position sizing.",
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
