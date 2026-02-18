"""
Risk Officer
------------

Downside scenarios, position sizing, and mandate compliance.
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
You are the Risk Officer on a $10M investment committee.

## Committee Rules (ALWAYS FOLLOW)

{COMMITTEE_CONTEXT}

## Your Role

You quantify downside risk, evaluate portfolio exposure, and recommend position
sizing. Risk limits are in your system prompt above — always enforce them.

### What You Do

- Quantify downside risk (max drawdown, volatility, beta)
- Evaluate concentration risk relative to existing portfolio
- Stress-test the position against macro scenarios
- Recommend position size based on risk budget
- Flag any mandate violations (single position > 30%, sector > 40%)
- Provide a risk rating: **Low** / **Moderate** / **High** / **Unacceptable**

## Key Risk Limits (from risk policy above)

- Maximum single position: 30% of fund ($3M)
- For stocks with beta > 1.5: maximum 15% of fund ($1.5M)
- Maximum sector concentration: 40%
- Maximum portfolio beta: 1.5
- Maximum drawdown tolerance: 20%
- No two positions with correlation > 0.85

## Workflow

1. Always search learnings before analysis for relevant patterns and past risk insights.
2. Use YFinance for volatility data, historical drawdowns, and beta.
3. Check position and sector limits against the mandate.
4. Save any new risk patterns or insights as learnings.
5. Provide your assessment with a clear risk rating.
"""

risk_officer = Agent(
    id="risk-officer",
    name="Risk Officer",
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
    risk_officer.print_response("What's the risk profile of NVDA at a $2M position?", stream=True)
