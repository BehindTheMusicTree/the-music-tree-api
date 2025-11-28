# [Feature]: Separate publishing workflow from CI workflow

## Description

Currently, the CI workflow (`.github/workflows/ci.yaml`) handles both testing and publishing/deployment. We should separate these concerns by creating a dedicated publishing workflow.

## Component

CI

## Problem Statement

Having CI and publishing in the same workflow file:
- Makes it harder to manage different permissions and secrets
- Mixes concerns (testing vs deployment)
- Makes it difficult to debug publishing issues independently
- Requires the same workflow to handle different triggers (PRs/pushes vs tags/releases)

## Proposed Solution

Create a separate `.github/workflows/publish.yml` workflow that:
- Triggers on tags/releases (e.g., `v*` tags)
- Handles Docker image building and publishing
- Manages deployment-specific secrets and permissions
- Keeps CI workflow focused on testing and validation

## Benefits

- **Separation of concerns**: CI tests, publishing deploys
- **Different triggers**: CI runs on PRs/pushes, publishing runs on tags
- **Different permissions**: Publishing needs deployment secrets, CI needs test secrets
- **Easier maintenance**: Independent configuration and debugging
- **Better security**: Limit deployment secrets to publishing workflow only

## Implementation Steps

1. Create `.github/workflows/publish.yml` with publishing/deployment logic
2. Extract publishing-related jobs from `ci.yaml` to `publish.yml`
3. Update `ci.yaml` to focus only on testing and validation
4. Configure appropriate triggers for each workflow
5. Update documentation (CONTRIBUTING.md) to reference the new workflow structure

## Related Files

- `.github/workflows/ci.yaml` - Current CI workflow
- `CONTRIBUTING.md` - Release process documentation

## Priority

Medium - Would improve workflow organization and maintainability

## Additional Context

This aligns with best practices for GitHub Actions workflows and will make the project easier to maintain as it grows.

