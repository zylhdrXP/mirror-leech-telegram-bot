#!/bin/bash

# Remove previous error.log if any
rm -f error.log

# Ensure local bin directory exists and is in PATH
mkdir -p bin
export PATH="$(pwd)/bin:$PATH"

# Auto-download aria2c static binary if not present
if ! command -v aria2c &> /dev/null; then
    echo "[MLTB-AutoSetup] aria2c not found. Downloading static binary..."
    curl -sL https://github.com/P3TERX/Aria2-Pro-Core/releases/download/1.36.0_2021.08.22/aria2-1.36.0-static-linux-amd64.tar.gz | tar -xz -C bin/
    chmod +x bin/aria2c 2>/dev/null || true
    echo "[MLTB-AutoSetup] aria2c installed to bin/aria2c"
fi

# Auto-download qbittorrent-nox static binary if not present
if ! command -v qbittorrent-nox &> /dev/null; then
    echo "[MLTB-AutoSetup] qbittorrent-nox not found. Downloading static binary..."
    curl -sL -o bin/qbittorrent-nox https://github.com/userdocs/qbittorrent-nox-static/releases/download/release-5.3.0_v2.1.2/x86_64-qbittorrent-nox
    chmod +x bin/qbittorrent-nox 2>/dev/null || true
    echo "[MLTB-AutoSetup] qbittorrent-nox installed to bin/qbittorrent-nox"
fi

# Activate virtualenv if present
if [ -d "mltbenv" ]; then
    source mltbenv/bin/activate
fi

# Run update.py, capturing stderr to error.log if any error occurs
python3 update.py 2> >(while IFS= read -r line; do echo "$line" >> error.log; echo "$line" >&2; done)
UPDATE_EXIT=$?
if [ $UPDATE_EXIT -ne 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: update.py exited with code $UPDATE_EXIT" >> error.log
    exit $UPDATE_EXIT
fi

# Run bot, capturing stderr to error.log if any error occurs
python3 -m bot 2> >(while IFS= read -r line; do echo "$line" >> error.log; echo "$line" >&2; done)
BOT_EXIT=$?
if [ $BOT_EXIT -ne 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: bot exited with code $BOT_EXIT" >> error.log
    exit $BOT_EXIT
fi

# Clean up error.log if empty
[ -s error.log ] || rm -f error.log
