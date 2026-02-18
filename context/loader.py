from pathlib import Path

CONTEXT_DIR = Path(__file__).parent


def load_context() -> str:
    """Load all static context files into a single string for system prompt injection."""
    sections = []
    for file in sorted(CONTEXT_DIR.glob("*.md")):
        sections.append(file.read_text())
    return "\n\n---\n\n".join(sections)


COMMITTEE_CONTEXT = load_context()
