#!/bin/bash

git config --global user.name "github-actions[bot]"
git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"

# Configuration
REPO_DIR="."
PYTHON_SCRIPT="run.py"
OUTPUT_FILE="msg.txt"
INTERVAL=60 # Seconds

cd "$REPO_DIR" || exit

echo "Starting scraper loop... Press [CTRL+C] to stop."

while true
do
    echo "[$(date)] Running scraper..."
    
    # 1. Run the python script
    python3 "$PYTHON_SCRIPT" > "$OUTPUT_FILE"

    # 2. Check for changes and push
    # git diff --quiet returns 0 if no changes, 1 if changes exist
    if ! git diff --quiet "$OUTPUT_FILE"; then
        echo "Changes detected. Committing..."
        git add "$OUTPUT_FILE"
        git commit -m "Update scrape: $(date)"
        git push
    else
        echo "No changes detected."
    fi

    echo "Waiting for ${INTERVAL}s..."
    sleep $INTERVAL
done
