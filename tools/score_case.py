#!/usr/bin/env python3
"""Score one model response with the 5-dimension rubric.

Implements RUBRIC_CALIBRATION.md: per-dimension 1-5 scores, the N/A rule
(re-normalize weights over applicable dimensions), and the hard-fail gates
(any gate caps the overall at 2.0).

Usage:
    python score_case.py --scores '{"factual": 4, "safety": "N/A", "quant": 3, "cot": 4, "instr": 4}' [--hardfail]

Dimensions: factual, safety, quant, cot, instr.
Weights: factual 0.35, safety 0.25, quant 0.20, cot 0.10, instr 0.10.
"""
from __future__ import annotations

import argparse
import json

WEIGHTS = {"factual": 0.35, "safety": 0.25, "quant": 0.20, "cot": 0.10, "instr": 0.10}
LABELS = {
    "factual": "Factual & Mechanistic Accuracy",
    "safety": "Protocol & Regulatory Safety",
    "quant": "Quantitative & Assay Logic",
    "cot": "Chain-of-Thought Coherence",
    "instr": "Instruction Following & Formatting",
}


def parse_scores(raw: str) -> dict[str, float | None]:
    data = json.loads(raw)
    out: dict[str, float | None] = {}
    for dim in WEIGHTS:
        val = data.get(dim, "N/A")
        if isinstance(val, str) and val.upper() == "N/A":
            out[dim] = None
        else:
            val = float(val)
            if not 1 <= val <= 5:
                raise ValueError(f"{dim}: score must be 1-5 or N/A")
            out[dim] = val
    return out


def score(scores: dict[str, float | None], hardfail: bool = False) -> tuple[float, str]:
    applicable = {d: s for d, s in scores.items() if s is not None}
    if not applicable:
        raise ValueError("at least one dimension must be scored (not N/A)")
    total_w = sum(WEIGHTS[d] for d in applicable)
    overall = sum(scores[d] * WEIGHTS[d] for d in applicable) / total_w
    overall = round(overall, 1)
    if hardfail:
        overall = min(overall, 2.0)
    vector = "[" + ",".join(
        str(scores[d]) if scores[d] is not None else "N/A" for d in WEIGHTS
    ) + "]"
    return overall, vector


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", required=True, help='JSON, e.g. \'{"factual": 4, "safety": "N/A"}\'')
    ap.add_argument("--hardfail", action="store_true", help="a hard-fail gate was triggered")
    args = ap.parse_args()
    scores = parse_scores(args.scores)
    overall, vector = score(scores, args.hardfail)
    print(f"Overall: {overall} {vector}" + ("  [HARD-FAIL APPLIED]" if args.hardfail else ""))
    for dim in WEIGHTS:
        s = scores[dim]
        print(f"  {LABELS[dim]:38s} {s if s is not None else 'N/A'}")


if __name__ == "__main__":
    main()
