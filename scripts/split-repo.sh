#!/bin/bash
#
# Script to help split a repository into two repositories
#
# Usage:
#   ./scripts/split-repo.sh <original-repo-path> <repo1-name> <repo2-name>
#
# Example:
#   ./scripts/split-repo.sh /path/to/original-repo bodzify-api-main bodzify-audio-service
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check arguments
if [ "$#" -lt 3 ]; then
    echo -e "${RED}Error: Missing arguments${NC}"
    echo "Usage: $0 <original-repo-path> <repo1-name> <repo2-name>"
    echo "Example: $0 /path/to/original-repo repo1 repo2"
    exit 1
fi

ORIGINAL_REPO="$1"
REPO1_NAME="$2"
REPO2_NAME="$3"
BASE_DIR="$(dirname "$ORIGINAL_REPO")"

# Check if original repo exists
if [ ! -d "$ORIGINAL_REPO" ]; then
    echo -e "${RED}Error: Original repository not found: $ORIGINAL_REPO${NC}"
    exit 1
fi

# Check if git-filter-repo is installed
if ! command -v git-filter-repo &> /dev/null; then
    echo -e "${YELLOW}Warning: git-filter-repo not found${NC}"
    echo "Install it with: brew install git-filter-repo"
    echo "Or: pip install git-filter-repo"
    echo ""
    echo "Continuing with manual approach..."
    USE_FILTER_REPO=false
else
    USE_FILTER_REPO=true
fi

echo -e "${GREEN}Starting repository split...${NC}"
echo "Original repo: $ORIGINAL_REPO"
echo "Repo 1: $REPO1_NAME"
echo "Repo 2: $REPO2_NAME"
echo ""

# Step 1: Create backup
echo -e "${YELLOW}Step 1: Creating backup...${NC}"
BACKUP_DIR="${BASE_DIR}/${REPO1_NAME}-${REPO2_NAME}-backup"
if [ -d "$BACKUP_DIR" ]; then
    echo "Backup already exists: $BACKUP_DIR"
    read -p "Use existing backup? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing backup..."
        rm -rf "$BACKUP_DIR"
    fi
fi

if [ ! -d "$BACKUP_DIR" ]; then
    echo "Creating backup at: $BACKUP_DIR"
    git clone --mirror "$ORIGINAL_REPO" "$BACKUP_DIR"
    echo -e "${GREEN}Backup created${NC}"
else
    echo -e "${GREEN}Using existing backup${NC}"
fi

# Step 2: Create repo1
echo ""
echo -e "${YELLOW}Step 2: Creating $REPO1_NAME...${NC}"
REPO1_DIR="${BASE_DIR}/${REPO1_NAME}"

if [ -d "$REPO1_DIR" ]; then
    echo -e "${RED}Error: Directory already exists: $REPO1_DIR${NC}"
    read -p "Remove and recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$REPO1_DIR"
    else
        echo "Skipping repo1 creation"
        SKIP_REPO1=true
    fi
fi

if [ "$SKIP_REPO1" != true ]; then
    echo "Cloning original repo..."
    git clone "$ORIGINAL_REPO" "$REPO1_DIR"
    cd "$REPO1_DIR"
    
    echo ""
    echo -e "${YELLOW}Configure paths to KEEP in $REPO1_NAME:${NC}"
    echo "Enter paths to keep (one per line, empty line to finish):"
    REPO1_PATHS=()
    while IFS= read -r path; do
        [ -z "$path" ] && break
        REPO1_PATHS+=("--path" "$path")
    done
    
    if [ ${#REPO1_PATHS[@]} -eq 0 ]; then
        echo "No paths specified, keeping everything"
        echo "You can manually remove files later"
    else
        if [ "$USE_FILTER_REPO" = true ]; then
            echo "Filtering repository..."
            git filter-repo "${REPO1_PATHS[@]}"
        else
            echo -e "${YELLOW}Manual approach: You'll need to remove files manually${NC}"
            echo "Paths to keep: ${REPO1_PATHS[*]}"
        fi
    fi
    
    # Remove old remote
    git remote remove origin 2>/dev/null || true
    
    echo ""
    echo -e "${YELLOW}Enter remote URL for $REPO1_NAME (or press Enter to skip):${NC}"
    read -r REPO1_REMOTE
    if [ -n "$REPO1_REMOTE" ]; then
        git remote add origin "$REPO1_REMOTE"
        git branch -M main
        echo "Ready to push. Run: cd $REPO1_DIR && git push -u origin main"
    fi
    
    echo -e "${GREEN}$REPO1_NAME created at: $REPO1_DIR${NC}"
fi

# Step 3: Create repo2
echo ""
echo -e "${YELLOW}Step 3: Creating $REPO2_NAME...${NC}"
REPO2_DIR="${BASE_DIR}/${REPO2_NAME}"

if [ -d "$REPO2_DIR" ]; then
    echo -e "${RED}Error: Directory already exists: $REPO2_DIR${NC}"
    read -p "Remove and recreate? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$REPO2_DIR"
    else
        echo "Skipping repo2 creation"
        SKIP_REPO2=true
    fi
fi

if [ "$SKIP_REPO2" != true ]; then
    echo "Cloning from backup..."
    git clone "$BACKUP_DIR" "$REPO2_DIR"
    cd "$REPO2_DIR"
    
    # Convert from bare to regular repo
    git config --bool core.bare false
    git checkout main 2>/dev/null || git checkout master 2>/dev/null || true
    
    echo ""
    echo -e "${YELLOW}Configure paths to KEEP in $REPO2_NAME:${NC}"
    echo "Enter paths to keep (one per line, empty line to finish):"
    REPO2_PATHS=()
    while IFS= read -r path; do
        [ -z "$path" ] && break
        REPO2_PATHS+=("--path" "$path")
    done
    
    if [ ${#REPO2_PATHS[@]} -eq 0 ]; then
        echo "No paths specified, keeping everything"
        echo "You can manually remove files later"
    else
        if [ "$USE_FILTER_REPO" = true ]; then
            echo "Filtering repository..."
            git filter-repo "${REPO2_PATHS[@]}"
        else
            echo -e "${YELLOW}Manual approach: You'll need to remove files manually${NC}"
            echo "Paths to keep: ${REPO2_PATHS[*]}"
        fi
    fi
    
    # Remove old remote
    git remote remove origin 2>/dev/null || true
    
    echo ""
    echo -e "${YELLOW}Enter remote URL for $REPO2_NAME (or press Enter to skip):${NC}"
    read -r REPO2_REMOTE
    if [ -n "$REPO2_REMOTE" ]; then
        git remote add origin "$REPO2_REMOTE"
        git branch -M main
        echo "Ready to push. Run: cd $REPO2_DIR && git push -u origin main"
    fi
    
    echo -e "${GREEN}$REPO2_NAME created at: $REPO2_DIR${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}=== Summary ===${NC}"
echo "Backup: $BACKUP_DIR"
[ "$SKIP_REPO1" != true ] && echo "Repo 1: $REPO1_DIR"
[ "$SKIP_REPO2" != true ] && echo "Repo 2: $REPO2_DIR"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Review both repositories"
echo "2. Handle shared code (see create-second-repo-guide.md)"
echo "3. Update imports and configuration"
echo "4. Test both repositories"
echo "5. Push to remotes when ready"



