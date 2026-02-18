"""
Load Knowledge - Loads research documents into the vector database.

Usage:
    python -m app.load_knowledge             # Upsert (skip existing)
    python -m app.load_knowledge --recreate  # Drop and reload all
"""

import argparse
from pathlib import Path

RESEARCH_DIR = Path(__file__).parent.parent / "research"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load research into vector database")
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Drop existing knowledge and reload from scratch",
    )
    args = parser.parse_args()

    from agents.settings import committee_knowledge

    if args.recreate:
        print("Recreating knowledge base (dropping existing data)...\n")
        if committee_knowledge.vector_db:
            committee_knowledge.vector_db.drop()
            committee_knowledge.vector_db.create()

    print(f"Loading research from: {RESEARCH_DIR}\n")

    for subdir in ["companies", "sectors"]:
        path = RESEARCH_DIR / subdir
        if not path.exists():
            print(f"  {subdir}/: (not found)")
            continue

        files = [f for f in path.iterdir() if f.is_file() and not f.name.startswith(".")]
        print(f"  {subdir}/: {len(files)} files")

        if files:
            committee_knowledge.insert(name=f"research-{subdir}", path=str(path), skip_if_exists=True)

    print("\nDone!")
