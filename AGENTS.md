# Project guidance

The Music Tree API is a Django/DRF service with PostgreSQL and optional audio
fingerprinting. Read `README.md`, `DEVELOPMENT.md` and `CONTRIBUTING.md` for
setup, validation and Gitflow. The repository's existing `.cursor/rules/` and
`.cursorrules` contain project conventions; consult relevant rules and verify
against the code and current repository configuration.

The local startup skill is shared at `.agents/skills/launch/SKILL.md` and linked
from `.claude/skills/launch`. Preserve existing environment files and databases;
only run destructive reinitialization when explicitly requested.
