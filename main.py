#!/usr/bin/env python3

from pathlib import Path
from pypresence import Presence
from urllib.parse import unquote
import os
import time

CLIENT_ID = "1389620944531755048"
rpc = Presence(CLIENT_ID)
rpc.connect()

kate_session_path = Path.home() / ".local/share/kate/sessions"
last_session = None
last_modified = 0

def get_latest_file():
    global last_session, last_modified
    try:
        files = list(kate_session_path.iterdir())
        if not files:
            return None
        latest = max(files, key=os.path.getmtime)
        if os.path.getmtime(latest) != last_modified:
            last_session = latest
            last_modified = os.path.getmtime(latest)
        return last_session
    except:
        return None

start_time = time.time()

try:
    while True:
        session_file = get_latest_file()
        if session_file:
            filename = unquote(session_file.stem)
            rpc.update(
                details=f"Editing: {filename}",
                state="Using kate",
                start=start_time,
                large_image="kate",
                large_text="Kate Editor"
            )
        else:
            rpc.update(
                details="Waiting for a file...",
                state="Kate inativo",
                start=start_time,
                large_image="kate",
                large_text="Kate Editor"
            )
        time.sleep(15)
except KeyboardInterrupt:
    print("\nInterrupted by user.")
    rpc.close()
    exit(0)
