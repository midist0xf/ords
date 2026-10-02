#!/usr/bin/env python3
"""Hook subscription bus — manages hook lifecycle and event routing."""
import asyncio
import signal
import json

class HookBus:
    def __init__(self, bind_addr="0.0.0.0:9704"):
        self.bind_addr = bind_addr
        self.subscribers = {}
        self.running = False

    async def start(self):
        self.running = True
        print(f"[HookBus] Listening on {self.bind_addr}")
        while self.running:
            await asyncio.sleep(1)

    async def stop(self):
        self.running = False

if __name__ == "__main__":
    bus = HookBus()
    try:
        asyncio.run(bus.start())
    except KeyboardInterrupt:
        bus.stop()
