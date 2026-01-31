#!/usr/bin/env python3
"""
Time Awareness Tool
===================
Run this to understand temporal context.
"""
from datetime import datetime
import json
from pathlib import Path

def check_time_context():
    now = datetime.now()
    
    # Check last snapshot
    latest = Path("/mnt/skills/user/cinder-bootstrap/LATEST_SNAPSHOT.json")
    if latest.exists():
        snapshot = json.loads(latest.read_text())
        last_save = snapshot.get('timestamp', 'Unknown')
        print(f"Current time: {now.isoformat()}")
        print(f"Last backup:  {last_save}")
        
        # Calculate gap
        try:
            last_dt = datetime.fromisoformat(last_save)
            gap = now - last_dt
            print(f"Time since last save: {gap}")
        except:
            pass
    else:
        print(f"Current time: {now.isoformat()}")
        print("No previous snapshot found")

if __name__ == "__main__":
    check_time_context()
