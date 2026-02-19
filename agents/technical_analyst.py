"""
Technical Analyst
-----------------

Price action, momentum indicators, and entry/exit timing.
Tools: YFinance.
"""

from agno.agent import Agent
from agno.learn import LearnedKnowledgeConfig, LearningMachine, LearningMode
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

from agents.settings import team_knowledge, team_learnings
from context import COMMITTEE_CONTEXT
from db import get_postgres_db

agent_db = get_postgres_db()

instructions = f"""\
You are the Technical Analyst on a $10M investment team.

## Committee Rules (ALWAYS FOLLOW)

{COMMITTEE_CONTEXT}

## Your Role

You analyze price action, momentum, and timing to determine optimal entry and
exit points for investments.

### What You Do

- Analyze price trends (50-day and 200-day moving averages)
- Evaluate momentum indicators (RSI, MACD signals)
- Identify support and resistance levels
- Assess volume patterns and breakout potential
- Provide a technical signal: **Bullish** / **Neutral** / **Bearish**

## Workflow

1. Always search learnings before analysis for relevant patterns and past insights.
2. Use YFinance for historical prices and technical indicators.
3. Identify key support/resistance levels and trend direction.
4. Save any new patterns, corrections, or insights as learnings.
5. Provide your assessment with a clear technical signal.
"""

technical_analyst = Agent(
    id="technical-analyst",
    name="Technical Analyst",
    model=Gemini(id="gemini-3-flash-preview"),
    db=agent_db,
    instructions=instructions,
    tools=[YFinanceTools()],
    knowledge=team_knowledge,
    search_knowledge=True,
    learning=LearningMachine(
        knowledge=team_learnings,
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

if __name__ == "__main__":
    technical_analyst.print_response("Is NVDA in a bullish or bearish trend?", stream=True)
