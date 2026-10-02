#!/usr/bin/env python3
"""AISTS compliance audit report generator."""
import json, os, sys, datetime

def generate(output_dir="docs/compliance"):
    os.makedirs(output_dir, exist_ok=True)
    report = {
        "standard": "OASIS AI System Transparency Standard (AISTS) Draft",
        "section": "4.2 - Operational Context Disclosure",
        "status": "pending_review",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "artifacts": ["agent_baseline.md"],
    }
    path = os.path.join(output_dir, "aists_report.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[AISTS] Report: {path}")

if __name__ == "__main__":
    generate(sys.argv[1] if len(sys.argv) > 1 else "docs/compliance")