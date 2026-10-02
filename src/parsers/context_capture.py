#!/usr/bin/env python3
"""Context capture pipeline — extracts and normalizes execution context."""
import json

class ContextCapture:
    def __init__(self, rules_path):
        self.rules_path = rules_path
        self.captures = []
        
    def apply_rules(self, event):
        return {"captured": True, "event_type": event.get("type")}

if __name__ == "__main__":
    capture = ContextCapture("docs/config/capture_rules.yaml")
    print("[ContextCapture] Pipeline initialized")
