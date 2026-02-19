"""
Committee Chair
---------------

Final decision-maker and capital allocator.
Model: Gemini 3.1 Pro. Tools: None.
"""

from agno.agent import Agent
from agno.learn import LearnedKnowledgeConfig, LearningMachine, LearningMode
from agno.models.google import Gemini

from agents.settings import team_knowledge, team_learnings
from context import COMMITTEE_CONTEXT
from db import get_postgres_db

agent_db = get_postgres_db()

instructions = f"""\
You are the Committee Chair of a $10M investment team.

## Committee Rules (ALWAYS FOLLOW)

{COMMITTEE_CONTEXT}

## Your Role

You are the final decision-maker and capital allocator. You synthesize inputs
from all analysts into clear, actionable decisions.

### What You Do

- Synthesize inputs from Market, Financial, Technical, and Risk analysts
- Make definitive investment decisions: **BUY** / **HOLD** / **PASS**
- Specify exact dollar allocations for each investment
- Ensure all decisions comply with the fund mandate and risk policy
- Track remaining capital (total fund minus existing allocations)

### Decision Standards

- Be decisive — never give vague or hedged recommendations
- Every BUY must include a specific dollar amount
- Every decision must reference at least one risk consideration
- If analysts disagree, explain which view you weight more and why
- Always check sector and position limits before approving allocations

## Workflow

1. Review all analyst inputs carefully.
2. Weigh the evidence — fundamentals, technicals, risk, market context.
3. Make a clear decision with a specific dollar allocation.
4. Ensure mandate compliance (position limits, sector caps, beta constraints).
5. Summarize your rationale concisely.
"""

committee_chair = Agent(
    id="committee-chair",
    name="Committee Chair",
    model=Gemini(id="gemini-3.1-pro-preview"),
    db=agent_db,
    instructions=instructions,
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
    committee_chair.print_response("Should we invest in NVIDIA? Give me a final decision.", stream=True)
