#!/bin/bash
# Finlo Critical Files Protection Hook - FAST VERSION
# Pure bash, no Python overhead
# Blocks deletion/modification of: Finlo.db, .env, .encryption.key, uv.lock

input=$(cat)

# Extract command or file_path from JSON using pure bash
# Look for either "command":"..." or "file_path":"..."
target=$(echo "$input" | grep -oP '("command"|"file_path")\s*:\s*"\K[^"]*' | head -1)

# Check if target matches protected files
if echo "$target" | grep -qiE '(Finlo\.db|\.env|\.encryption\.key|uv\.lock)'; then
    echo "BLOCKED: Cannot delete or modify critical files (Finlo.db, .env, .encryption.key, uv.lock)" >&2
    exit 2
fi

# Safe - allow execution
exit 0


