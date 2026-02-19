"""
Agent Settings
--------------

Shared instances used across all agents: knowledge bases, paths, and URLs.
Import from here — never recreate these.
"""

from os import getenv
from pathlib import Path

from db import create_knowledge

# Instantiated ONCE, imported everywhere
team_knowledge = create_knowledge("Team Knowledge", "team_knowledge")
team_learnings = create_knowledge("Team Learnings", "team_learnings")

# Memo archive directory (absolute path, safe for Docker)
MEMOS_DIR = Path(__file__).parent.parent / "memos"

# Exa MCP URL for web search (free tier available at exa.ai)
EXA_API_KEY = getenv("EXA_API_KEY", "")
EXA_MCP_URL = f"https://mcp.exa.ai/mcp?exaApiKey={EXA_API_KEY}&tools=web_search_exa"
