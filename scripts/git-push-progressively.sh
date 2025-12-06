#!/bin/bash

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source ${SCRIPTS_DIR}utils.sh

# Check if the commit message is passed as an argument
if [ $# -eq 0 ]; then
    log "ERROR: please provide a commit message as an argument." >&2
    exit 1
fi

commit_message=$1
max_retries=3
retry_delay=5
push_timeout=1200

push_with_timeout() {
    log "Starting git push (timeout: ${push_timeout}s = $((push_timeout / 60)) minutes)..."
    
    local output_file=$(mktemp)
    git push --verbose --progress > "$output_file" 2>&1 &
    local push_pid=$!
    local elapsed=0
    local last_line_count=0
    
    while kill -0 $push_pid 2>/dev/null; do
        if [ $elapsed -ge $push_timeout ]; then
            log "Push timed out after ${push_timeout} seconds ($((push_timeout / 60)) minutes). Killing process..." >&2
            kill $push_pid 2>/dev/null
            wait $push_pid 2>/dev/null
            tail -n +$((last_line_count + 1)) "$output_file" 2>/dev/null
            rm -f "$output_file"
            return 124
        fi
        
        local current_line_count=$(wc -l < "$output_file" 2>/dev/null || echo 0)
        if [ $current_line_count -gt $last_line_count ]; then
            tail -n +$((last_line_count + 1)) "$output_file" 2>/dev/null | while IFS= read -r line; do
                log "$line"
            done
            last_line_count=$current_line_count
        fi
        
        if [ $elapsed -ge 30 ] && [ $((elapsed % 30)) -eq 0 ]; then
            if grep -q "POST git-receive-pack" "$output_file" 2>/dev/null; then
                log "[Waiting for GitHub to process push... ${elapsed}s/${push_timeout}s elapsed]"
            else
                log "[Still uploading... ${elapsed}s elapsed]"
            fi
        fi
        
        sleep 1
        elapsed=$((elapsed + 1))
    done
    
    wait $push_pid
    local exit_code=$?
    
    local current_line_count=$(wc -l < "$output_file" 2>/dev/null || echo 0)
    if [ $current_line_count -gt $last_line_count ]; then
        tail -n +$((last_line_count + 1)) "$output_file" 2>/dev/null | while IFS= read -r line; do
            log "$line"
        done
    fi
    
    local output_content=""
    if [ -f "$output_file" ]; then
        output_content=$(cat "$output_file")
        rm -f "$output_file"
    fi
    
    if echo "$output_content" | grep -qiE "(RPC failed|curl.*55|Recv failure|unexpected disconnect|hung up|fatal.*remote)" && [ $exit_code -ne 0 ]; then
        log "Network error detected in push output. This will be retried." >&2
        return 130
    fi
    
    if echo "$output_content" | grep -qi "Everything up-to-date"; then
        if [ $exit_code -ne 0 ]; then
            log "Push reported 'Everything up-to-date' but exited with error. Verifying..." >&2
            if git fetch origin --quiet 2>/dev/null; then
                local current_branch=$(git rev-parse --abbrev-ref HEAD)
                local local_commit=$(git rev-parse HEAD)
                local remote_commit=$(git rev-parse "origin/${current_branch}" 2>/dev/null || echo "")
                if [ "$local_commit" = "$remote_commit" ]; then
                    log "Verified: local and remote are in sync. Push succeeded." >&2
                    return 0
                fi
            fi
            return 130
        else
            return 0
        fi
    fi
    
    if [ $exit_code -eq 124 ] || [ $exit_code -eq 143 ]; then
        log "Push timed out after ${push_timeout} seconds." >&2
        log "Large pushes can take 5-15 minutes for GitHub to process after upload completes." >&2
        log "If this persists, consider pushing in smaller batches or increasing push_timeout." >&2
    fi
    
    return $exit_code
}

push_with_retry() {
    local retry_count=0
    local network_error_retries=0
    local max_network_retries=5
    
    while [ $retry_count -lt $max_retries ]; do
        if push_with_timeout; then
            if ! git fetch origin --quiet 2>/dev/null; then
                log "WARNING: Could not verify push with fetch. Assuming success." >&2
            fi
            return 0
        else
            local exit_code=$?
            retry_count=$((retry_count + 1))
            
            if [ $exit_code -eq 130 ]; then
                network_error_retries=$((network_error_retries + 1))
                if [ $network_error_retries -le $max_network_retries ]; then
                    local backoff=$((retry_delay * network_error_retries))
                    log "Network error detected. Retrying in ${backoff} seconds... (network retry $network_error_retries/$max_network_retries)"
                    sleep $backoff
                    retry_count=$((retry_count - 1))
                    continue
                else
                    log "Too many network errors. Treating as regular failure." >&2
                fi
            fi
            
            if [ $exit_code -eq 124 ] || [ $exit_code -eq 143 ]; then
                log "Push timed out after ${push_timeout} seconds." >&2
            fi
            
            if [ $retry_count -lt $max_retries ]; then
                log "Push failed. Retrying in ${retry_delay} seconds... (attempt $retry_count/$max_retries)"
                sleep $retry_delay
            else
                log "ERROR: Push failed after $max_retries attempts." >&2
                return 1
            fi
        fi
    done
}

while true; do
    # Get a list of modified files
    IFS=$'\n'
    files=($(git status --porcelain | awk 'BEGIN{srand()} {print rand() "\t" $0}' | sort -n | cut -f2-))

    # Check if the file list is empty
    if [ ${#files[@]} -eq 0 ]; then
        log "No files to add. Ending script."
        break
    fi

    # Add the files to the git index
    for file in "${files[@]}"; do
        status=$(echo "$file" | awk '{print $1}')
        file_path=$(echo "$file" | awk '{print substr($0, index($0,$2))}')
        file_path=${file_path%\"}
        file_path=${file_path#\"}
        if [ -n "$file_path" ]; then
            if [ "$status" == "D" ]; then
                if git ls-files --error-unmatch "$file_path" >/dev/null 2>&1; then
                    git rm --cached "$file_path"
                    if [ $? -ne 0 ]; then
                        log "ERROR: Failed to remove $file_path from git index." >&2
                        exit 1
                    fi
                fi
            elif [ "$status" == "??" ]; then
                git add "$file_path"
                if [ $? -ne 0 ]; then
                    log "ERROR: Failed to add $file_path to git index." >&2
                    exit 1
                fi
            else
                git add "$file_path"
                if [ $? -ne 0 ]; then
                    log "ERROR: Failed to add $file_path to git index." >&2
                    exit 1
                fi
            fi
            
            log "Committing $file_path..."
            if ! git commit -m "$commit_message"; then
                log "ERROR: Failed to commit $file_path." >&2
                exit 1
            fi
            
            log "Pushing $file_path..."
            remote=$(git config --get remote.origin.url 2>/dev/null || echo "origin")
            log "Remote: $remote"
            
            current_branch=$(git rev-parse --abbrev-ref HEAD)
            local_commit_before=$(git rev-parse HEAD)
            
            if ! push_with_retry; then
                log "ERROR: Failed to push after retries. Stopping script." >&2
                log "Check your network connection and remote repository access." >&2
                exit 1
            fi
            
            sleep 2
            if git fetch origin --quiet 2>/dev/null; then
                remote_commit=$(git rev-parse "origin/${current_branch}" 2>/dev/null || echo "")
                if [ "$local_commit_before" = "$remote_commit" ]; then
                    log "Successfully pushed $file_path (verified)"
                else
                    log "WARNING: Could not verify push, but git reported success. Continuing..." >&2
                fi
            else
                log "WARNING: Could not fetch to verify push. Assuming success." >&2
            fi
        fi
    done
done