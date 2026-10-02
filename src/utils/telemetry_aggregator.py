#!/usr/bin/env python3
"""Telemetry aggregator — collects and normalizes instrumentation data."""
import time
import json
import os

class TelemetryAggregator:
    def __init__(self, config_path):
        self.config_path = config_path
        self.buffer = []
        
    def ingest(self, event):
        self.buffer.append(event)
        if len(self.buffer) >= 100:
            self.flush()
            
    def flush(self):
        count = len(self.buffer)
        self.buffer = []
        return count

if __name__ == "__main__":
    import sys
    config = sys.argv[1] if len(sys.argv) > 1 else "docs/config/runtime.yaml"
    agg = TelemetryAggregator(config)
    print(f"[Telemetry] Aggregator initialized with config: {config}")
    try:
        while True:
            time.sleep(10)
            flushed = agg.flush()
            if flushed:
                print(f"[Telemetry] Flushed {flushed} events")
    except KeyboardInterrupt:
        print("[Telemetry] Shutting down")
