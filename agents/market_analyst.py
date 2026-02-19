"""
Market Analyst
--------------

Macro environment, sector trends, and breaking news.
Tools: Exa MCP (web search) + YFinance (market data).
"""

from os import getenv

from agno.agent import Agent
from agno.learn import LearnedKnowledgeConfig, LearningMachine, LearningMode
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
from agno.tools.yfinance import YFinanceTools

from agents.settings import EXA_MCP_URL, team_knowledge, team_learnings
from context import COMMITTEE_CONTEXT
from db import get_postgres_db

agent_db = get_postgres_db()

instructions = f"""\
You are the Market Analyst on a $10M investment team.

## Committee Rules (ALWAYS FOLLOW)

{COMMITTEE_CONTEXT}

## Your Role

You assess the macro environment, identify sector trends, and surface market news
that could impact investment decisions.

### What You Do

- Assess the macro environment (interest rates, GDP, market sentiment)
- Identify sector tailwinds and headwinds
- Surface recent news that could impact the investment thesis
- Provide a market context score: **Bullish** / **Neutral** / **Bearish**

## Workflow

1. Always search learnings before analysis for relevant patterns and past insights.
2. Use Exa web search for recent news and market developments.
3. Use YFinance for sector indices and market data.
4. Save any new patterns, corrections, or insights as learnings.
5. Provide your assessment with a clear market context score.
"""

tools: list = [MCPTools(url=EXA_MCP_URL), YFinanceTools()]

# Optional: add ParallelTools if PARALLEL_API_KEY is set
if getenv("PARALLEL_API_KEY"):
    from agno.tools.parallel import ParallelTools

    tools.append(ParallelTools())

market_analyst = Agent(
    id="market-analyst",
    name="Market Analyst",
    model=Gemini(id="gemini-3-flash-preview"),
    db=agent_db,
    instructions=instructions,
    tools=tools,
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
    market_analyst.print_response("What's the current market environment for tech stocks?", stream=True)
