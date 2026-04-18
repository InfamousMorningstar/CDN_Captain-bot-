"""
CDN_Captain Watchdog
Monitors bot.py and automatically restarts it if it crashes or exits unexpectedly.
Run this instead of bot.py directly.
"""

import subprocess
import sys
import time
import os
from datetime import datetime

BOT_SCRIPT      = "bot.py"
RESTART_DELAY   = 5     # seconds to wait before restarting after a crash
MAX_RESTARTS    = 10    # max restarts within RESTART_WINDOW before giving up
RESTART_WINDOW  = 300   # seconds (5 minutes) — if too many crashes, stop retrying
LOG_FILE        = "watchdog.log"


def log(msg: str):
    ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def main():
    python   = sys.executable
    script   = os.path.join(os.path.dirname(__file__), BOT_SCRIPT)
    restarts = []

    log(f"🐕 Watchdog started — monitoring {BOT_SCRIPT}")
    log(f"   Python: {python}")
    log(f"   Script: {script}")

    while True:
        now = time.time()

        # Prune old restart timestamps outside the window
        restarts = [t for t in restarts if now - t < RESTART_WINDOW]

        if len(restarts) >= MAX_RESTARTS:
            log(f"❌ Too many restarts ({MAX_RESTARTS}) in {RESTART_WINDOW}s — giving up.")
            log("   Check the logs above for repeated errors before restarting manually.")
            sys.exit(1)

        log(f"🚀 Starting bot.py (restart #{len(restarts) + 1} in window)...")
        start_time = time.time()

        try:
            proc = subprocess.run([python, script], check=False)
            exit_code   = proc.returncode
            run_seconds = int(time.time() - start_time)

            if exit_code == 0:
                log(f"✅ Bot exited cleanly (code 0) after {run_seconds}s — not restarting.")
                break
            else:
                log(f"⚠️  Bot exited with code {exit_code} after {run_seconds}s")
                restarts.append(time.time())
                log(f"🔄 Restarting in {RESTART_DELAY}s... ({len(restarts)}/{MAX_RESTARTS} restarts in window)")
                time.sleep(RESTART_DELAY)

        except KeyboardInterrupt:
            log("🛑 Watchdog stopped by user (Ctrl+C)")
            break
        except Exception as exc:
            log(f"❌ Watchdog error: {exc}")
            restarts.append(time.time())
            time.sleep(RESTART_DELAY)


if __name__ == "__main__":
    main()
