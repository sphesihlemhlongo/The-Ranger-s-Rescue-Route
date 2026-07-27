# PLAN — Ranger's Rescue Route (handoff from planning session)

## Status
- [x] Step 1: Scaffold + CLAUDE.md + data/level1.json + data/level2.json
- [x] Step 3: dijkstra.py + validate.py + solve.py --level 1
      DONE. pytest green, validator passes, local score 100.
      Answer: A -> D -> E -> B, cost 9. Written to out/level1_answer.{json,txt}
- [x] scripts/package.py per the Submission Contract (built early, out of
      order, because Level 1 needed repackaging after the data fix)
- [ ] Package + submit Level 1 (target: local score 100 before upload)
      Package DONE: submission_level1.zip, local score 100, verified to
      reproduce from a clean extract. Remaining: upload it plus
      out/level1_answer.json to the hackathon site.
      STALE ARTIFACTS: the old submission1/ folder and submission1.zip
      predate the data fix and contain the WRONG route (A -> D -> B,
      cost 7). Delete them so they cannot be uploaded by mistake.
- [ ] Step 4: Level 2 — parse-time weight collapse (time + risk) is DONE
      in graph.py design; verify tests cover it
- [ ] Step 5: Station ordering — brute-force all 24 permutations of
      S1..S4, Dijkstra per leg, pick min total. NO heuristics — 24 perms
      is exhaustive and provably optimal at this size
- [ ] Step 6: Leg concatenation — joint node appears ONCE
      (leg1 ends X, leg2 starts X → drop duplicate). Validator must pass
      before any answer file is written
- [ ] Step 7: Local scorer — DONE for L1 (src/solve.py report_score, using
      OPTIMA constants from the spec). Confirm it covers L2.
- [ ] Step 8: submit L2

## RESOLVED: data/level1.json was corrupted
Fixed 2026-07-27 against the spec PDF (p.5 "Edge List (travel time only)").
The committed file had wrong weights (C-D 3 vs 1, C-E 3 vs 5, E-F 1 vs 2,
B-F 6 vs 7), was missing D-E 3, D-F 6 and B-E 4, and carried a spurious
B-D 5 edge that created a fake 7-cost shortcut. The solver was correct all
along; only the input data was wrong.

tests/test_graph.py now pins the full L1 edge list to the spec and asserts
both graphs are undirected, so this class of corruption fails loudly.

## OPEN: data/level2.json does not match the spec either
Verified against spec p.7. The file is a different graph entirely: it
contains nodes P13-P17, which do not exist in the spec (nodes are A, B,
S1-S4, P1-P12). 18 of 20 edges are wrong or missing. Rebuild it from the
spec adjacency list (PDF p.7) before starting Step 4.

Also note the spec names the stations S1..S4, which is what the adjacency
list uses. data/level3.json is an empty placeholder.

## Decisions already made (do not relitigate)
- Stdlib only (heapq, itertools, json, argparse)
- One codebase, thin entry point: solve.py --level {1|2}
- Levels are independent deliverables; L1 submitted before L2 work
- Dijkstra with heapq + lazy deletion; predecessors for path reconstruction
- Level 2 legs: A → [best perm of S1..S4] → B, effective weight = time+risk

## Definition of done, every step
pytest -q green → solve runs → validator passes → local score printed