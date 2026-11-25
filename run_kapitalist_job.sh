#!/usr/bin/env bash
set -euo pipefail

WORKDIR="/home/segvan/workers"
UV_BIN="/home/segvan/.local/bin/uv"
LOCKFILE="/tmp/kapitalist_job.lock"
LOGFILE="/home/segvan/workers/kapitalist_job.log"

cd "$WORKDIR"

# Prevent overlapping runs:
# -n: do not wait for the lock; if locked, exit immediately
# -w 1: wait up to 1 second to avoid a race with lock release
/usr/bin/flock -n -w 1 "$LOCKFILE" "$UV_BIN" run python kapitalist_job.py >> "$LOGFILE" 2>&1
