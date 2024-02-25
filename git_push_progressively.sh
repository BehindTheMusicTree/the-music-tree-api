#!/bin/bash

# Check if commit message is passed as an argument
if [ $# -eq 0 ]; then
    echo "Please provide a commit message as an argument."
    exit 1
fi

commit_message=$1

while true; do
    # Get a list of modified files
    files=$(git status --porcelain | awk '{print $2}' | shuf | head -n 5)

    # Check if the file list is empty
    if [ -z "$files" ]; then
        echo "No files to add. Ending script."
        break
    fi

    # Add the files to git's index
    for file in $files; do
        git add "$file"
    done

    # Commit and push
    git commit -m "$commit_message"
    git push
done