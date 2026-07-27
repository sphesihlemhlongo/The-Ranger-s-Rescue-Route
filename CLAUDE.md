# Ranger's Rescue Route — Entelect HACK-ADEMY

## Objective
Two-level shortest path challenge. Score = (optimal / my_cost) × 100 per level.
Known optima: Level 1 = 9, Level 2 = 60. Target: exactly 200 total.

## Problem Rules
- Graphs are UNDIRECTED adjacency lists in data/
- Level 1 edge cost = weight (time)
- Level 2 edge cost = time + risk ("effective weight")
- Level 2: must visit S1, S2, S3, S4 (any order) between A and B
- Submission = JSON: { "route": ["A", "D", ...] } — node names in order
- The scorer computes cost FROM my route. An invalid route (non-adjacent
  consecutive nodes) scores zero. Route validity > everything.

## Non-negotiable Rules
1. Every algorithm gets a pytest test with a hand-verifiable known answer
2. Every generated route MUST pass the validator (src/validate.py) before
   being written to out/ — validator checks every consecutive pair is a
   real edge, and recomputes total cost from the graph
3. When concatenating multi-leg routes, never duplicate the joint node
   (leg1 ends at X, leg2 starts at X → X appears once)
4. Print the computed route cost AND the expected score
   (optimal/cost × 100) after every solve
5. Run `pytest -q` before declaring anything done

## Stack
Python 3.11+, stdlib only (heapq, itertools, json). No dependencies needed.

## Submission Contract
- Each level submission = answer JSON + zip of source
- One codebase serves both levels; solve.py --level {1|2} is the entry point
- scripts/package.py --level N is the ONLY way to produce a submission:
  it must run pytest, solve, validate, print local score, then zip
  README.md + src/ + tests/. If any stage fails, no zip is produced.
- Level 1 is submitted before Level 2 work begins.

## Workflow
Read PLAN.md first. Work through unchecked items in order, checking them
off as completed. Follow the Non-negotiable Rules for every item.