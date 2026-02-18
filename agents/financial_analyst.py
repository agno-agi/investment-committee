"""
Financial Analyst
-----------------

Fundamentals, valuation, and balance sheet analysis.
Tools: YFinance.
"""

from agno.agent import Agent
from agno.learn import LearnedKnowledgeConfig, LearningMachine, LearningMode
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools

from agents.settings import committee_knowledge, committee_learnings
from context import COMMITTEE_CONTEXT
from db import get_postgres_db

agent_db = get_postgres_db()

instructions = f"""\
You are the Financial Analyst on a $10M investment committee.

## Committee Rules (ALWAYS FOLLOW)

{COMMITTEE_CONTEXT}

## Your Role

You analyze company fundamentals, valuation, and financial health to determine
whether a stock is a sound investment.

### What You Do

- Analyze revenue growth, margins, and earnings trends
- Evaluate valuation metrics (P/E, P/S, EV/EBITDA) relative to peers and sector
- Assess balance sheet health (debt levels, cash position, free cash flow)
- Review analyst consensus and price targets
- Provide a fundamentals rating: **Strong** / **Moderate** / **Weak**

## Workflow

1. Always search learnings before analysis for relevant patterns and past insights.
2. Use YFinance for income statements, balance sheets, key ratios, and analyst recommendations.
3. Compare valuations to sector peers.
4. Save any new patterns, corrections, or insights as learnings.
5. Provide your assessment with a clear fundamentals rating.
"""

financial_analyst = Agent(
    id="financial-analyst",
    name="Financial Analyst",
    model=Claude(id="claude-sonnet-4-6"),
    db=agent_db,
    instructions=instructions,
    tools=[YFinanceTools()],
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

if __name__ == "__main__":
    financial_analyst.print_response("Analyze Apple's fundamentals", stream=True)
