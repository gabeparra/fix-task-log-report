# log-report — fixed Terminal-Bench 2 (Harbor) task

A repaired version of the broken `log-report` Harbor task. The task itself: parse
an Apache-style access log into a small JSON report at `/app/report.json`.

## Verified

```
harbor run -p log-report -a oracle   # reward 1.0 (4/4 pytest tests pass, ctrf.json written)
harbor run -p log-report -a nop      # reward 0.0
```

Tested with harbor 0.17.1.

## Defects found and fixed

### task.toml
- `artifacts = "/app/out.json"` was a **string** — the Harbor schema requires a
  **list** (`artifacts: list[str | ArtifactConfig]`), so `TaskConfig` validation
  failed and Harbor silently refused to load the task at all
  (`ValueError: Either datasets or tasks must be provided.`). Now
  `artifacts = ["/app/report.json"]`.
- The declared artifact pointed at `/app/out.json`, but the task (solution and
  verifier) produces `/app/report.json`. Declaration now matches reality.
- `verification_explanation = "Check the report file."` described the dishonest
  existence-only verifier; rewritten to describe the real exact-value checks.
- All tb2-template metadata fields retained (`category`, `subcategory`,
  `task_objective`, `artifact_type`, `expert_time_estimate_hours`,
  `model_tested`, `agent_tested`, and the three explanation fields), plus the
  full `[environment]` block including `allow_internet` and `mcp_servers`.

### environment/Dockerfile
- `FROM python:latest` was unpinned — not reproducible. Now pinned by digest:
  `python:3.13-slim@sha256:eb43ff12…`.
- `COPY solution_hint.py /app/solution_hint.py` **leaked the full reference
  solution into the agent's container** (its own comment admitted it). The file
  is deleted and the COPY removed.
- The pinned `pytest`/`pytest-json-ctrf` install stays: the verifier runs in the
  shared environment and needs them.

### tests/test.sh
- Wrote the reward to `/app/reward.txt`; Harbor reads
  `/logs/verifier/reward.txt`, so **every run errored with a missing reward
  file** regardless of what the agent did. Fixed path, plus `mkdir -p
  /logs/verifier` for safety.
- No CTRF report was produced even though `pytest-json-ctrf` was installed.
  pytest now runs with `--ctrf /logs/verifier/ctrf.json`.
- The reward file is written unconditionally on both code paths, overwriting
  anything an agent might have pre-staged.

### tests/test_outputs.py
- The old tests only checked that `/app/report.json` **exists and is non-empty**
  — `echo hi > /app/report.json` would have scored 1.0. The tests now parse the
  JSON and assert the exact ground-truth values: `total_requests == 6`,
  `unique_ips == 3`, `top_path == "/index.html"`.
- Ground truth is hardcoded in `tests/` (never agent-visible) instead of being
  recomputed from `/app/access.log`, which the agent could rewrite to make a
  bogus report self-consistent.
- Tests map 1:1 onto the numbered success criteria in `instruction.md`; each
  test's docstring names the criterion it verifies.

### instruction.md
- Was vague ("summarize what you find… save your findings") — it never named the
  output file, the format, or the keys, so even a perfect agent could not know
  the verifier wanted `/app/report.json` with those three keys. Rewritten with
  the exact output path, key names/types, and numbered success criteria that
  match the verifier one-for-one.

## Layout

```
log-report/
├── task.toml
├── instruction.md
├── environment/
│   ├── Dockerfile
│   └── access.log
├── solution/
│   ├── solve.sh
│   └── solve.py
└── tests/
    ├── test.sh
    └── test_outputs.py
```
