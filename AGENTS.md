# Project guidance

The Music Tree API is a Django/DRF service with PostgreSQL and optional audio
fingerprinting. Read `README.md`, `DEVELOPMENT.md` and `CONTRIBUTING.md` for
setup, validation and Gitflow. Read the relevant project conventions in
`.claude/rules/` before working; apply their `paths` metadata only within its
stated scope. Verify guidance against the code and current configuration.

The local startup skill is shared at `.agents/skills/launch/SKILL.md` and linked
from `.claude/skills/launch`. Preserve existing environment files and databases;
only run destructive reinitialization when explicitly requested.

## Knowledge graph

When `graphify-out/graph.json` exists, use `graphify query "<question>"` for
codebase questions, `graphify path "<A>" "<B>"` for relationships, and
`graphify explain "<concept>"` for focused concepts. If available, use
`graphify-out/wiki/index.md` for broad navigation. Consult
`graphify-out/GRAPH_REPORT.md` for broad architecture review or when those
queries do not provide enough context. After modifying code, run
`graphify update .` to keep the local graph current.
