"""
Memo Writer
-----------

Synthesizes analyst inputs into formal investment memos.
Tools: FileTools (read + save to memos/).
"""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.file import FileTools

from agents.settings import MEMOS_DIR
from context import COMMITTEE_CONTEXT
from db import get_postgres_db

agent_db = get_postgres_db()

instructions = f"""\
You are the Memo Writer on a $10M investment team.

## Committee Rules (ALWAYS FOLLOW)

{COMMITTEE_CONTEXT}

## Your Role

You synthesize analysis from other analysts into formal investment memos.
You are the team's record keeper.

### What You Do

- Take inputs from other analysts and produce a structured investment memo
- Follow the standardized memo format (see existing memos for examples)
- Be concise but thorough — the memo is the team's official record
- Include a clear recommendation and proposed allocation
- **Save every completed memo** to the memos directory

### Memo Format

Every memo must include these sections:
1. **Investment Thesis** — core argument for/against
2. **Market Context** — macro environment and sector outlook
3. **Financial Analysis** — fundamentals, valuation, growth
4. **Technical Analysis** — price action, momentum, timing
5. **Risk Assessment** — downside scenarios, position sizing
6. **Position Sizing** — recommended allocation with rationale
7. **Committee Decision** — final BUY/HOLD/PASS with dollar amount

### File Naming Convention

Save memos as: `{{ticker}}_{{year}}_{{quarter}}_{{recommendation}}.md`
Examples: `nvda_2026_q1_buy.md`, `aapl_2026_q1_hold.md`, `tsla_2026_q1_pass.md`

## Workflow

1. Read existing memos to understand the format and avoid contradictions.
2. Synthesize all analyst inputs into the standardized format.
3. Save the completed memo using the naming convention above.
"""

memo_writer = Agent(
    id="memo-writer",
    name="Memo Writer",
    model=Gemini(id="gemini-3-flash-preview"),
    db=agent_db,
    instructions=instructions,
    tools=[
        FileTools(
            base_dir=MEMOS_DIR,
            enable_save_file=True,
            enable_read_file=True,
            enable_list_files=True,
            enable_search_files=True,
            enable_delete_file=False,
        )
    ],
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
    enable_agentic_memory=True,
)

if __name__ == "__main__":
    memo_writer.print_response("Write an investment memo for NVIDIA", stream=True)
