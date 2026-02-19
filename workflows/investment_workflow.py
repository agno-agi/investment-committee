"""
Investment Workflow
------------------

Deterministic 5-step pipeline: Market → Financial+Technical (parallel) → Risk → Memo → Chair.
Best for: standardized, auditable investment reviews.
"""

from agno.workflow import Parallel, Step, Workflow

from agents import (
    committee_chair,
    financial_analyst,
    market_analyst,
    memo_writer,
    risk_officer,
    technical_analyst,
)

investment_workflow = Workflow(
    id="investment-workflow",
    name="Investment Review Pipeline",
    steps=[
        Step(name="Market Assessment", agent=market_analyst),
        Parallel(
            Step(name="Fundamental Analysis", agent=financial_analyst),
            Step(name="Technical Analysis", agent=technical_analyst),
            name="Deep Dive",
        ),
        Step(name="Risk Assessment", agent=risk_officer),
        Step(name="Investment Memo", agent=memo_writer),
        Step(name="Committee Decision", agent=committee_chair),
    ],
)
