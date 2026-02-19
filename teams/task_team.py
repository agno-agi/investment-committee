"""
Task Team
---------

Chair autonomously decomposes complex tasks with dependencies.
Best for: multi-step portfolio construction and analysis.
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

task_team = Team(
    id="task-team",
    name="Investment Team - Tasks",
    mode=TeamMode.tasks,
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
        "Decompose complex investment tasks into sub-tasks with dependencies.",
        "Assign each sub-task to the most appropriate analyst.",
        "Parallelize independent tasks (e.g., fundamentals + technicals).",
        "Ensure risk assessment happens after fundamental + technical analysis.",
        "Memo writing should be the final step after all analysis is complete.",
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
