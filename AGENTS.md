# Project guidance

The Music Tree API is a Django/DRF service with PostgreSQL and optional audio
fingerprinting. Read `README.md`, `DEVELOPMENT.md` and `CONTRIBUTING.md` for
setup, validation and Gitflow. Read the relevant project rules listed below
before working. Apply each only within its stated scope; `**/` includes root files.
Verify guidance against the code and current configuration.

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

## Project rules

Rules scoped to `**/*` are general project instructions: read them for every
task, including Git and GitHub operations without file edits.

- For `**/*`, read `.agents/rules/changelog-best-practices.md`.
- For `**/*`, read `.agents/rules/commit-message-convention.md`.
- For `**/*`, read `.agents/rules/dependency-pinning.md`.
- For `**/*`, read `.agents/rules/divide-test-cases.md`.
- For `**/*`, read `.agents/rules/field-name-constants.md`.
- For `**/*`, read `.agents/rules/git-flow-workflow.md`.
- For `**/*`, read `.agents/rules/issue-description-in-separate-file.md`.
- For `**/*`, read `.agents/rules/issue-template-usage.md`.
- For `**/*`, read `.agents/rules/no-useless-comments.md`.
- For `**/*`, read `.agents/rules/one-class-per-file.md`.
- For `**/*`, read `.agents/rules/pr-description-in-separate-file.md`.
- For `**/*`, read `.agents/rules/pre-pr-checklist.md`.
- For `**/*`, read `.agents/rules/private-resource-filtering.md`.
- For `**/*`, read `.agents/rules/pull-request-convention.md`.
- For `**/*`, read `.agents/rules/test-naming-convention.md`.
- For `**/*`, read `.agents/rules/test-structure.md`.
- For `**/*`, read `.agents/rules/use-assert-not-assertequal.md`.
- For `**/*`, read `.agents/rules/use-custome-validation-exception.md`.
- For `**/*.py`, read `.agents/rules/use-pipe-none.md`.
