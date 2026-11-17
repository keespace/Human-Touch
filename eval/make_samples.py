"""
Builds the AI-written part of the test set (uses your API credit - roughly $0.10-0.30 per run).

  python eval/make_samples.py

- ai_generated/   : texts Claude writes from scratch, including ones told to imitate a real person's voice
- ai_assisted/    : each file in human_written/ polished by Claude, the way people commonly "improve" their writing
Existing files are never overwritten, so you can re-run it after adding more human texts.

ai_written_human_edited/ can't be generated honestly: it needs a person to edit an AI draft. See eval/README.md.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import server  # noqa: E402  (reuses the API client and model)

SAMPLES = Path(__file__).resolve().parent / "samples"

GENERATE = {
    "kids_story_plain": "Write a 250-word children's picture-book story about a shy hedgehog who wants to join the forest choir.",
    "kids_story_humanlike": "Write a 250-word bedtime story for a 5-year-old about a lost red mitten. Make it sound like it was "
                            "written by a real parent for their own child: quirky, specific, not polished, no moral at the end.",
    "personal_essay_humanlike": "Write a 300-word personal blog post about learning to drive at 40. Sound like a real person: "
                                "use contractions, a couple of tangents, one or two small typos, and avoid any neat lesson at the end.",
    "school_essay": "Write a 300-word essay for a 10th-grade class on why libraries still matter.",
    "book_review_humanlike": "Write a 250-word Goodreads-style review of a made-up cozy mystery novel. Write like an ordinary "
                             "reader, casual and opinionated, with a gripe or two.",
    "opinion_blog": "Write a 300-word opinion piece on whether kids should have smartphones before age 13.",
}

ASSIST_PROMPT = ("Please improve this text for publication: fix any errors, make it flow better and read more "
                 "professionally, but keep the author's meaning and content. Return only the improved text.\n\n{text}")


def ask(prompt: str) -> str:
    r = server.client.messages.create(
        model=server.MODEL, max_tokens=4000, output_config={"effort": "low"},
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in r.content if b.type == "text").strip()


def main():
    if server.client is None:
        sys.exit("No API key - add it to .env first.")
    for folder in ("human_written", "ai_assisted", "ai_written_human_edited", "ai_generated"):
        (SAMPLES / folder).mkdir(parents=True, exist_ok=True)

    for name, prompt in GENERATE.items():
        out = SAMPLES / "ai_generated" / f"{name}.txt"
        if not out.exists():
            out.write_text(ask(prompt), encoding="utf-8")
            print("wrote", out.relative_to(SAMPLES))

    for src in sorted((SAMPLES / "human_written").glob("*.txt")):
        out = SAMPLES / "ai_assisted" / f"polished_{src.name}"
        if not out.exists():
            out.write_text(ask(ASSIST_PROMPT.format(text=src.read_text(encoding="utf-8"))), encoding="utf-8")
            print("wrote", out.relative_to(SAMPLES))


if __name__ == "__main__":
    main()
