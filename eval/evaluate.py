"""
Measures how well the authorship analysis works on texts whose true origin you know.

  python eval/evaluate.py            # all samples
  python eval/evaluate.py human      # only folders whose name contains "human"

Each sub-folder of eval/samples/ is a true label; every .txt file inside is one test text.
Prints each verdict, a confusion matrix, and the numbers that matter most - above all, how often
real human writing gets wrongly flagged as AI. Full details are saved to eval/results.json.
Costs roughly $0.03-0.08 per text.
"""

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import server  # noqa: E402

HERE = Path(__file__).resolve().parent
LABELS = server.CATEGORIES
SHORT = {"human_written": "human", "ai_assisted": "assisted", "ai_written_human_edited": "ai+edit",
         "ai_generated": "ai-gen", "uncertain": "unsure"}
PRICE_IN, PRICE_OUT = 4 / 1e6, 20 / 1e6  # claude-opus-5-5, $ per token


def run_one(item):
    label, path = item
    try:
        r = server.ai_check(path.read_text(encoding="utf-8")[:server.MAX_CHARS])
        return {"file": f"{label}/{path.name}", "truth": label, "predicted": r["verdict"],
                "probabilities": r["probabilities"], "ai_involvement": r["ai_involvement"],
                "confidence": r["confidence"], "summary": r["summary"], "usage": r["usage"]}
    except Exception as e:  # noqa: BLE001
        return {"file": f"{label}/{path.name}", "truth": label, "error": str(e)}


def main():
    if server.client is None:
        sys.exit("No API key - add it to .env first.")
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    items = [(d.name, f) for d in sorted((HERE / "samples").iterdir()) if d.is_dir() and d.name in LABELS
             and only in d.name for f in sorted(d.glob("*.txt"))]
    if not items:
        sys.exit("No samples found in eval/samples/<label>/*.txt")
    print(f"Evaluating {len(items)} texts...\n")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run_one, items))

    ok = [r for r in results if "error" not in r]
    for r in results:
        if "error" in r:
            print(f"  ERROR  {r['file']}: {r['error']}")
            continue
        mark = "✓" if r["predicted"] == r["truth"] else "✗"
        p = r["probabilities"]
        print(f"  {mark} {r['file']:<48} -> {SHORT[r['predicted']]:<8} "
              f"(human {p['human_written']:>3}% | assisted {p['ai_assisted']:>3}% | ai+edit "
              f"{p['ai_written_human_edited']:>3}% | ai-gen {p['ai_generated']:>3}%)  {r['confidence']}")

    # Confusion matrix
    cols = LABELS + ["uncertain"]
    print("\nConfusion matrix (rows = truth, columns = verdict)")
    print(" " * 10 + "".join(f"{SHORT[c]:>10}" for c in cols))
    for t in LABELS:
        row = [r for r in ok if r["truth"] == t]
        if row:
            print(f"{SHORT[t]:<10}" + "".join(f"{sum(r['predicted'] == c for r in row):>10}" for c in cols))

    # Headline numbers
    exact = sum(r["predicted"] == r["truth"] for r in ok)
    is_ai = lambda lab: lab not in ("human_written", "uncertain")
    binary = sum((r["truth"] != "human_written") == is_ai(r["predicted"]) for r in ok)
    humans = [r for r in ok if r["truth"] == "human_written"]
    false_flags = [r for r in humans if is_ai(r["predicted"])]
    machines = [r for r in ok if r["truth"] != "human_written"]
    missed = [r for r in machines if r["predicted"] == "human_written"]
    print(f"\nExact category correct:          {exact}/{len(ok)}")
    print(f"Human vs AI-involved correct:    {binary}/{len(ok)}")
    if humans:
        print(f"Human texts wrongly flagged AI:  {len(false_flags)}/{len(humans)}   <- most important: keep this near 0")
    if machines:
        print(f"AI-involved texts called human:  {len(missed)}/{len(machines)}")
    cost = sum(r["usage"]["input_tokens"] * PRICE_IN + r["usage"]["output_tokens"] * PRICE_OUT for r in ok)
    print(f"Approximate cost of this run:    ${cost:.2f}")
    (HERE / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("Details saved to eval/results.json")


if __name__ == "__main__":
    main()
