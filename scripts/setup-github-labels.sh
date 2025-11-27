#!/bin/bash

# Script to create GitHub labels for auto-labeler
# Run this script to set up all labels in your GitHub repository

set -e

# Colors for labels
# Component labels - various colors to distinguish features
COMPONENT_COLOR_1="#0E8A16"  # Green
COMPONENT_COLOR_2="#1D76DB"  # Blue
COMPONENT_COLOR_3="#B60205"  # Red
COMPONENT_COLOR_4="#D93F0B"  # Orange
COMPONENT_COLOR_5="#0CF574"  # Light Green
COMPONENT_COLOR_6="#0052CC"  # Dark Blue
COMPONENT_COLOR_7="#5319E7"  # Purple
COMPONENT_COLOR_8="#FBCA04"  # Yellow

# Type labels - standard colors
TYPE_COLOR_DOCS="#0052CC"     # Blue for documentation
TYPE_COLOR_TEST="#0E8A16"     # Green for tests
TYPE_COLOR_CI="#FBCA04"        # Yellow for CI/CD
TYPE_COLOR_DEPS="#D93F0B"      # Orange for dependencies
TYPE_COLOR_DOCKER="#0CF574"    # Light Green for Docker
TYPE_COLOR_OTHER="#B60205"     # Red for other

echo "Creating GitHub labels..."

# Component labels
gh label create "track" --description "Track-related changes" --color "$COMPONENT_COLOR_1" --force 2>/dev/null || echo "Label 'track' already exists or created"
gh label create "artist" --description "Artist-related changes" --color "$COMPONENT_COLOR_2" --force 2>/dev/null || echo "Label 'artist' already exists or created"
gh label create "album" --description "Album-related changes" --color "$COMPONENT_COLOR_3" --force 2>/dev/null || echo "Label 'album' already exists or created"
gh label create "genre" --description "Genre/criteria-related changes" --color "$COMPONENT_COLOR_4" --force 2>/dev/null || echo "Label 'genre' already exists or created"
gh label create "tag" --description "Tag-related changes" --color "$COMPONENT_COLOR_5" --force 2>/dev/null || echo "Label 'tag' already exists or created"
gh label create "playlist" --description "Playlist-related changes" --color "$COMPONENT_COLOR_6" --force 2>/dev/null || echo "Label 'playlist' already exists or created"
gh label create "play" --description "Play-related changes" --color "$COMPONENT_COLOR_7" --force 2>/dev/null || echo "Label 'play' already exists or created"
gh label create "user" --description "User-related changes" --color "$COMPONENT_COLOR_8" --force 2>/dev/null || echo "Label 'user' already exists or created"
gh label create "spotify" --description "Spotify integration changes" --color "$COMPONENT_COLOR_1" --force 2>/dev/null || echo "Label 'spotify' already exists or created"
gh label create "musicbrainz" --description "MusicBrainz integration changes" --color "$COMPONENT_COLOR_2" --force 2>/dev/null || echo "Label 'musicbrainz' already exists or created"
gh label create "audio-fingerprinting" --description "Audio fingerprinting changes" --color "$COMPONENT_COLOR_3" --force 2>/dev/null || echo "Label 'audio-fingerprinting' already exists or created"
gh label create "filtering" --description "Filtering/search changes" --color "$COMPONENT_COLOR_4" --force 2>/dev/null || echo "Label 'filtering' already exists or created"
gh label create "middleware" --description "Middleware changes" --color "$COMPONENT_COLOR_5" --force 2>/dev/null || echo "Label 'middleware' already exists or created"
gh label create "serializer" --description "Serializer changes" --color "$COMPONENT_COLOR_6" --force 2>/dev/null || echo "Label 'serializer' already exists or created"
gh label create "model" --description "Model changes" --color "$COMPONENT_COLOR_7" --force 2>/dev/null || echo "Label 'model' already exists or created"
gh label create "view" --description "View/viewset changes" --color "$COMPONENT_COLOR_8" --force 2>/dev/null || echo "Label 'view' already exists or created"
gh label create "exception" --description "Exception handling changes" --color "$COMPONENT_COLOR_1" --force 2>/dev/null || echo "Label 'exception' already exists or created"
gh label create "utils" --description "Utility functions changes" --color "$COMPONENT_COLOR_2" --force 2>/dev/null || echo "Label 'utils' already exists or created"

# Type labels
gh label create "test" --description "Test files" --color "$TYPE_COLOR_TEST" --force 2>/dev/null || echo "Label 'test' already exists or created"
gh label create "documentation" --description "Documentation changes" --color "$TYPE_COLOR_DOCS" --force 2>/dev/null || echo "Label 'documentation' already exists or created"
gh label create "ci" --description "CI/CD workflow changes" --color "$TYPE_COLOR_CI" --force 2>/dev/null || echo "Label 'ci' already exists or created"
gh label create "dependencies" --description "Dependency updates" --color "$TYPE_COLOR_DEPS" --force 2>/dev/null || echo "Label 'dependencies' already exists or created"
gh label create "docker" --description "Docker configuration changes" --color "$TYPE_COLOR_DOCKER" --force 2>/dev/null || echo "Label 'docker' already exists or created"
gh label create "scripts" --description "Script changes" --color "$TYPE_COLOR_OTHER" --force 2>/dev/null || echo "Label 'scripts' already exists or created"
gh label create "migration" --description "Database migration changes" --color "$TYPE_COLOR_OTHER" --force 2>/dev/null || echo "Label 'migration' already exists or created"
gh label create "settings" --description "Settings configuration changes" --color "$TYPE_COLOR_OTHER" --force 2>/dev/null || echo "Label 'settings' already exists or created"
gh label create "admin" --description "Admin configuration changes" --color "$TYPE_COLOR_OTHER" --force 2>/dev/null || echo "Label 'admin' already exists or created"
gh label create "fixtures" --description "Test fixtures changes" --color "$TYPE_COLOR_OTHER" --force 2>/dev/null || echo "Label 'fixtures' already exists or created"
gh label create "logging" --description "Logging configuration changes" --color "$TYPE_COLOR_OTHER" --force 2>/dev/null || echo "Label 'logging' already exists or created"
gh label create "management" --description "Django management commands" --color "$TYPE_COLOR_OTHER" --force 2>/dev/null || echo "Label 'management' already exists or created"
gh label create "validator" --description "Validator changes" --color "$TYPE_COLOR_OTHER" --force 2>/dev/null || echo "Label 'validator' already exists or created"

# Standard GitHub labels (if not already present)
gh label create "bug" --description "Something isn't working" --color "$COMPONENT_COLOR_3" --force 2>/dev/null || echo "Label 'bug' already exists or created"
gh label create "enhancement" --description "New feature or request" --color "$COMPONENT_COLOR_1" --force 2>/dev/null || echo "Label 'enhancement' already exists or created"
gh label create "feature" --description "New feature" --color "$COMPONENT_COLOR_1" --force 2>/dev/null || echo "Label 'feature' already exists or created"

echo ""
echo "✅ Labels created successfully!"
echo ""
echo "You can verify labels by running: gh label list"

