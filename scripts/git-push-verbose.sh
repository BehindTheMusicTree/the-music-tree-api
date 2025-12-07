#!/bin/bash

# Script to push with verbose output for debugging large pushes
# Usage: ./scripts/git-push-verbose.sh [branch-name] [remote]

BRANCH=${1:-$(git rev-parse --abbrev-ref HEAD)}
REMOTE=${2:-origin}
LARGE_UPLOAD_THRESHOLD_MB=10

estimate_push_size() {
    local remote_ref="${REMOTE}/${BRANCH}"
    
    if ! git rev-parse --verify "$remote_ref" >/dev/null 2>&1; then
        git fetch "$REMOTE" "$BRANCH" --quiet 2>/dev/null || true
        if ! git rev-parse --verify "$remote_ref" >/dev/null 2>&1; then
            echo 0
            return
        fi
    fi
    
    local local_commit=$(git rev-parse HEAD 2>/dev/null || echo "")
    local remote_commit=$(git rev-parse "$remote_ref" 2>/dev/null || echo "")
    
    if [ -z "$local_commit" ] || [ -z "$remote_commit" ] || [ "$local_commit" = "$remote_commit" ]; then
        echo 0
        return
    fi
    
    local size_bytes=$(git rev-list --objects "$remote_commit".."$local_commit" 2>/dev/null | \
        git cat-file --batch-check='%(objectsize)' 2>/dev/null | \
        awk '{sum+=$1} END {printf "%.0f", sum+0}')
    
    if [ -z "$size_bytes" ] || [ "$size_bytes" = "" ]; then
        echo 0
    else
        echo "$size_bytes"
    fi
}

echo "Pushing branch: $BRANCH to $REMOTE"
echo "Verbose output enabled (GIT_CURL_VERBOSE=1 GIT_TRACE=1)"
echo "Press Ctrl+C to cancel"
echo ""

# Estimate push size
push_size_bytes=$(estimate_push_size)
push_size_mb=0

if [ -n "$push_size_bytes" ] && [ "$push_size_bytes" != "0" ] && [ "$push_size_bytes" != "" ]; then
    push_size_mb=$(awk "BEGIN {printf \"%.0f\", $push_size_bytes / 1024 / 1024}")
fi

use_http11=false
http_version="HTTP/2"

if [ $push_size_mb -gt $LARGE_UPLOAD_THRESHOLD_MB ]; then
    use_http11=true
    http_version="HTTP/1.1"
    echo "Large upload detected (~${push_size_mb}MB). Using ${http_version} for better reliability..."
else
    echo "Small upload detected (~${push_size_mb}MB). Using ${http_version} for faster transfer..."
fi
echo ""

# Enable verbose output
export GIT_CURL_VERBOSE=1
export GIT_TRACE=1

# Push with verbose output, using HTTP/1.1 for large uploads
if [ "$use_http11" = true ]; then
    git -c http.version=HTTP/1.1 push "$REMOTE" "$BRANCH"
else
    git push "$REMOTE" "$BRANCH"
fi
