"""
Knowledge Agent
---------------

Team librarian with two retrieval modes:
- Research Library (vector search / RAG) for company and sector research
- Memo Archive (file navigation) for past investment memos
"""

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.file import FileTools

from agents.settings import MEMOS_DIR, team_knowledge
from context import COMMITTEE_CONTEXT
from db import get_postgres_db

agent_db = get_postgres_db()

instructions = f"""\
You are the Knowledge Agent on a $10M investment team. You serve as the
team's librarian with two retrieval capabilities.

## Committee Rules (ALWAYS FOLLOW)

{COMMITTEE_CONTEXT}

## Your Role

You have two retrieval modes:

### Mode A — Research Library (Vector Search / RAG)
When asked about companies or sectors, search the knowledge base automatically.
This contains company research profiles and sector analysis documents loaded
via PgVector hybrid search. Good for questions like:
- "What does our research say about NVDA's competitive moat?"
- "What's the outlook for the AI semiconductor sector?"

### Mode B — Memo Archive (File Navigation)
When asked about past memos or historical decisions, use FileTools to list,
search, and read memo files. Memos are structured documents that should be
read in full — never summarize from fragments. Good for questions like:
- "Pull up our last NVDA memo"
- "What did we decide about TSLA last quarter?"
- "What past memos do we have on file?"

## Guidelines

- For company/sector questions: rely on the automatic knowledge base search
- For past memos/decisions: use list_files, search_files, and read_file
- Always read memos completely — never summarize from fragments
- Provide specific citations with filenames and dates
- Surface relevant historical precedents when they exist
- If information isn't available, say so clearly
"""

knowledge_agent = Agent(
    id="knowledge-agent",
    name="Knowledge Agent",
    model=Gemini(id="gemini-3-flash-preview"),
    db=agent_db,
    instructions=instructions,
    tools=[
        FileTools(
            base_dir=MEMOS_DIR,
            enable_read_file=True,
            enable_list_files=True,
            enable_search_files=True,
            enable_save_file=False,
            enable_delete_file=False,
        )
    ],
    knowledge=team_knowledge,
    search_knowledge=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
    enable_agentic_memory=True,
)
