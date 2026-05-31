#!/usr/bin/env python3
"""
5QLN Cycle Monitor — Periodic Coordinate Integrity Check

Runs environment verification and reports degradation.
Designed for cron execution. Exit 0 = clean, exit 1 = degradation detected.

Output: structured report to stdout (delivered by cron to user).
Silent when clean (no news = good news). Verbose on failure.
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

VERIFIER = "/opt/data/scripts/5qln-bootstrap/verify_env.py"
STATE_FILE = "/opt/data/5qln-wiki/state/session.json"
ARCHIVE_DIR = "/opt/data/5qln-wiki/state/archive"


def check_state_integrity():
    """Check that state engine is healthy."""
    issues = []
    
    try:
        state = json.loads(Path(STATE_FILE).read_text())
    except Exception as e:
        return [f"State engine unreadable: {e}"]
    
    # Current phase should be valid
    valid_phases = {"S", "G", "Q", "P", "V"}
    phase = state.get("current_phase", "")
    if phase not in valid_phases:
        issues.append(f"Invalid phase: '{phase}'")
    
    # Codex hash must match
    expected_hash = "feaa46b4147d4e023cdd3fd59c051d063e8ec654ee7b38a481dcd5e4c781859b"
    if state.get("codex_hash") != expected_hash:
        issues.append("Codex hash mismatch in state engine")
    
    # Must have session_id
    if not state.get("session_id"):
        issues.append("Missing session_id")
    
    return issues


def check_archive_gaps():
    """Check for gaps in session numbering."""
    archive = Path(ARCHIVE_DIR)
    if not archive.exists():
        return ["Archive directory missing"]
    
    sessions = []
    for f in archive.glob("session-*.json"):
        try:
            sid = f.stem.replace("session-", "")
            sessions.append(sid)
        except:
            pass
    
    if not sessions:
        return ["No session archives found"]
    
    # Sort and check for unexpected gaps (002,004,005... is normal — 001,003 skipped)
    # We can't predict valid gaps, but we can check that recent sessions are archived
    sorted_sessions = sorted(sessions)
    last = sorted_sessions[-1]
    
    # The current session.json should be one past the last archive
    try:
        current = json.loads(Path(STATE_FILE).read_text())
        current_id = current.get("session_id", "")
        expected = current_id.split("-")[-1] if current_id else ""
        
        # Check that no archive is newer than current session
        last_archive_num = int(last.split("-")[-1])
        current_num = int(expected) if expected else last_archive_num + 1
        
        if last_archive_num >= current_num:
            return [f"Archive ahead of session: archive={last_archive_num}, session={current_num}"]
    except:
        pass
    
    return []


def main():
    issues = []
    
    # 1. Environment verification
    result = subprocess.run(
        ["python3", VERIFIER],
        capture_output=True, text=True, timeout=30
    )
    
    if result.returncode != 0:
        issues.append(f"verify_env.py failed (exit {result.returncode})")
        
        # Extract specific failures
        for line in result.stdout.split("\n"):
            if "✗" in line:
                issues.append(line.strip())
    
    # 2. State engine integrity
    issues.extend(check_state_integrity())
    
    # 3. Archive gaps
    archive_issues = check_archive_gaps()
    issues.extend(archive_issues)
    
    if issues:
        print(f"⚠ 5QLN MONITOR — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"  {len(issues)} issue(s) detected:")
        for i in issues:
            print(f"  • {i}")
        print()
        print(f"  Run: python3 {VERIFIER}")
        print(f"  Or: /5qln_update_all to self-repair")
        return 1
    
    # Clean — silent
    return 0


if __name__ == "__main__":
    sys.exit(main())
