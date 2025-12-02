# TODO

This file tracks future work, improvements, and testing tasks for Bodzify API.

**Note for Contributors**: 
- **Do NOT modify this file directly** - Contributors should not edit the TODO list
- **Suggest tasks via issues** - If you'd like to suggest a new task or work on an existing one, please open a GitHub issue first for discussion
- **Maintainers manage the TODO list** - Project maintainers are responsible for maintaining and updating this file
- **Updated during releases** - Maintainers align and update the TODO list when releasing new versions based on project priorities, completed work, and community feedback

## Table of Contents

- [Features](#features)
  - [High Priority](#high-priority)
  - [Medium Priority](#medium-priority)
  - [Low Priority](#low-priority)
- [Testing & Quality](#testing--quality)
  - [High Priority](#high-priority-1)
  - [Medium Priority](#medium-priority-1)
  - [Low Priority](#low-priority-1)
- [Infrastructure](#infrastructure)
  - [High Priority](#high-priority-2)
  - [Medium Priority](#medium-priority-2)
  - [Low Priority](#low-priority-2)
- [Documentation](#documentation)
  - [High Priority](#high-priority-3)
  - [Medium Priority](#medium-priority-3)
  - [Low Priority](#low-priority-3)
- [Contributing](#contributing)

## Features

### High Priority

- [ ] **Modernize Models with Django 5.2 Features**
  - **CRITICAL**: Replace `CheckConstraint.check` with `.condition` (14 warnings, blocks Django 6.0)
  - **Affected**: 6 models + migration file (see `FEATURE_MODERNIZE_DJANGO_5_2.md` for details)
  - **Effort**: 2-4 hours
  - **Optional Django 5.2 Features**:
    - **Composite Primary Keys**: Evaluate if any models could benefit from `CompositePrimaryKey` (e.g., relationship tables)
    - **AlterConstraint Migration**: Use new `AlterConstraint` operation instead of drop/recreate for constraint changes
    - **JSONArray Function**: Consider using new `JSONArray` database function for JSON operations
    - **Async Auth Methods**: Leverage new async authentication methods if using async views (`aauthenticate`, `alogin`, etc.)
    - **Query/Fragment in reverse()**: Use new `query` and `fragment` arguments in `reverse()` for cleaner URL generation
    - **HttpResponse.text**: Use new `.text` property instead of decoding `.content` manually
    - **Simple Block Tags**: Consider `simple_block_tag()` decorator for custom template tags
    - **Automatic Shell Imports**: Models auto-import in Django shell (already working, no action needed)
  - **Priority 3 - Review for Compatibility (CHECK)**:
    - **MySQL utf8mb4**: Connection now defaults to `utf8mb4` instead of `utf8` (verify no issues)
    - **VALUES() ordering**: `values()` and `values_list()` now preserve order (verify queries using union/intersection)
    - **Built-in aggregate validation**: Single-argument aggregates now raise TypeError if called incorrectly (good for catching bugs)
  - **Documentation**: Main focus should be Priority 1 (CheckConstraint deprecation fix). Other features are nice-to-have improvements.

- [ ] **Complete API documentation**
  - Document all API endpoints in README.md
  - Add usage examples for common operations
  - Document authentication flow and token management
  - Add request/response examples for each endpoint

- [ ] **Audio format support expansion**
  - Add support for additional audio formats (OGG, M4A, etc.)
  - Test audio fingerprinting compatibility across formats

- [ ] **Enhanced search functionality**
  - Implement advanced filtering options
  - Add full-text search capabilities
  - Support search across multiple fields simultaneously
  - Add search result ranking and relevance scoring

### Medium Priority

- [ ] **Batch operations API**
  - Add endpoints for bulk track upload
  - Implement batch tagging operations

- [ ] **Advanced genre hierarchy features**
  - Support for multiple genre hierarchies per user

- [ ] **Track metadata enhancement**
  - Add support for additional metadata fields (composer, conductor, etc.)
  - Add metadata import from external sources (MusicBrainz, Discogs)

- [ ] **Spotify integration improvements**
  - Add Spotify playlist synchronization
  - Implement Spotify track matching and linking

- [ ] **Play tracking enhancements**
  - Add play statistics and analytics
  - Implement play history with filtering

### Low Priority

- [ ] **Album artwork management**
  - Add album artwork upload and storage
  - Implement artwork extraction from audio files
  - Add artwork API endpoints
  - Support for multiple artwork sizes and formats

- [ ] **Export and backup features**
  - Add library export functionality (JSON, CSV)
  - Implement backup and restore API
  - Add scheduled backup options
  - Support for incremental backups

- [ ] **Social features**
  - Add user profiles and public libraries
  - Implement track sharing between users
  - Add community playlists
  - Support for user following and activity feeds

- [ ] **Mobile API optimizations**
  - Add mobile-specific endpoints with reduced payloads
  - Implement pagination improvements for mobile
  - Add offline sync capabilities
  - Optimize response times for mobile networks

- [ ] **Rate limiting and API quotas**
  - Implement per-user rate limiting
  - Add API usage tracking
  - Support for tiered API access levels
  - Add rate limit headers to responses

## Testing & Quality

### High Priority

- [ ] **Comprehensive test coverage**
  - Achieve 90%+ test coverage across all modules
  - Add integration tests for all API endpoints
  - Implement end-to-end tests for critical workflows
  - Add tests for edge cases and error handling
  - Add unit tests for all codebase
  - Add e2e tests for all critical workflows

- [ ] **Authentication and authorization testing**
  - Test JWT token expiration and refresh
  - Add tests for Spotify OAuth flow

### Medium Priority

- [ ] **Performance testing**
  - Load testing for high-traffic endpoints
  - Database query optimization analysis
  - Test response times under various loads
  - Identify and fix N+1 query problems

- [ ] **API contract testing**
  - Validate OpenAPI schema accuracy
  - Test backward compatibility for API changes
  - Verify request/response format consistency
  - Add contract tests for external integrations

- [ ] **Error handling validation**
  - Test all error response formats
  - Verify error codes and messages are consistent
  - Test error handling for edge cases
  - Validate AppValidationException usage across codebase

- [ ] **Database migration testing**
  - Test migration rollback scenarios
  - Verify data integrity after migrations
  - Test migration performance on large datasets
  - Add tests for complex migration dependencies

### Low Priority

- [ ] **Code quality metrics**
  - Set up code complexity analysis
  - Implement code duplication detection
  - Add security vulnerability scanning
  - Track technical debt metrics

- [ ] **Accessibility testing**
  - Test API responses for accessibility compliance
  - Verify error messages are clear and actionable
  - Test API documentation accessibility
  - Add accessibility guidelines to documentation

## Infrastructure

### High Priority

- [ ] **CI/CD pipeline improvements**
  - Add automated dependency updates (Dependabot)
  - Implement automated security scanning
  - Add performance regression testing
  - Set up automated deployment to staging environment

- [ ] **Database optimization**
  - Review and optimize database indexes
  - Implement database query monitoring
  - Add database connection pooling configuration
  - Set up database backup automation

- [ ] **Monitoring and logging**
  - Implement structured logging
  - Add application performance monitoring (APM)
  - Set up error tracking and alerting
  - Add health check endpoints

### Medium Priority

- [ ] **Caching strategy**
  - Implement Redis caching for frequently accessed data
  - Add cache invalidation strategies
  - Optimize cache key naming conventions
  - Add cache hit/miss monitoring

- [ ] **API versioning**
  - Implement API versioning strategy
  - Add version negotiation endpoints
  - Document version deprecation policy
  - Create migration guides between versions

- [ ] **Documentation infrastructure**
  - Set up automated API documentation generation
  - Add interactive API documentation (Swagger/ReDoc)
  - Implement documentation versioning
  - Add code examples generator

### Low Priority

- [ ] **Python version updates**
  - Monitor Python 3.15 release and compatibility
  - Test library compatibility with future Python versions
  - Update CI/CD workflows for new Python versions
  - Update project dependencies

- [ ] **Django version updates**
  - Monitor Django 5.1+ releases and new features
  - Test compatibility with future Django versions
  - Update deprecated Django features
  - Leverage new Django REST Framework features

- [ ] **Third-party service integrations**
  - Research additional metadata source integrations
  - Add support for multiple authentication providers
  - Implement service health monitoring

## Documentation

### High Priority

- [ ] **API usage guide**
  - Complete README.md with usage examples
  - Add authentication guide
  - Document common workflows and use cases
  - Create API endpoint reference documentation

- [ ] **Development setup guide**
  - Enhance CONTRIBUTING.md with troubleshooting section
  - Add common development issues and solutions
  - Document local development best practices
  - Create developer onboarding checklist

### Medium Priority

- [ ] **Architecture documentation**
  - Document system architecture and design decisions
  - Create data model diagrams
  - Document API design patterns used
  - Add integration flow diagrams

- [ ] **Deployment documentation**
  - Document production deployment process
  - Add environment-specific configuration guides
  - Create deployment checklist
  - Document rollback procedures

### Low Priority

- [ ] **Video tutorials**
  - Create video walkthrough of API usage
  - Add developer setup video tutorial
  - Create genre hierarchy management tutorial
  - Add playlist creation workflow video

- [ ] **Community resources**
  - Create FAQ document
  - Add troubleshooting guide
  - Document known issues and workarounds
  - Create glossary of terms

## Contributing

If you'd like to work on any of these items:

1. Check if there's already an open issue for the task
2. Create a new issue using the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml) if needed
3. Fork the repository and create a feature branch following our [Git Flow workflow](CONTRIBUTING.md#2-branching)
4. Implement your changes with appropriate tests following our [testing guidelines](CONTRIBUTING.md#4-testing)
5. Submit a pull request using our [PR template](.github/pull_request_template.md)

For questions about specific tasks, please open an issue for discussion or refer to our [Contributing Guidelines](CONTRIBUTING.md).

