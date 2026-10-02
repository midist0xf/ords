# Orchestration Runtime Debug Suite (ORDS)

**Version:** 3.4.1-rc2  
**Status:** Active Development  
**Compatibility:** Python 3.10+ / Node 18+ / Rust 1.72+

Enterprise-grade distributed agent debugging framework for complex multi-runtime orchestration workflows. Provides deterministic replay, causality tracking, and cross-context state reconciliation for autonomous agent systems operating across heterogeneous execution environments.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                    ORDS Control Plane                      │
├──────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ Hook Engine  │  │ Context      │  │ Reconciliation  │  │
│  │ (src/hooks/) │  │ Parser       │  │ Engine          │  │
│  └─────────────┘  │ (src/parsers/)│  │ (src/agents/)   │  │
│                   └──────────────┘  └────────────────┘  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ Telemetry    │  │ State        │  │ Replay          │  │
│  │ Aggregator   │  │ Serializer   │  │ Scheduler       │  │
│  │ (src/utils/) │  │ (src/utils/) │  │ (src/agents/)   │  │
│  └─────────────┘  └──────────────┘  └────────────────┘  │
├──────────────────────────────────────────────────────────┤
│                    Instrumentation Bus                     │
└──────────────────────────────────────────────────────────┘
```

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Runtime Configuration](#runtime-configuration)
4. [Hook Deployment](#hook-deployment)
5. [Context Capture Configuration](#context-capture-configuration)
6. [State Reconciliation Pipeline](#state-reconciliation-pipeline)
7. [Validation Suite](#validation-suite)
8. [Integration Test Harness](#integration-test-harness)
9. [Production Deployment Checklist](#production-deployment-checklist)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.10+ with `asyncio`, `dataclasses`, `importlib.metadata`
- Node.js 18+ (for JS runtime hooks)
- Rust 1.72+ (for high-throughput instrumentation bridge)
- Docker Compose v2.22+ (for integration test environment)
- At least 8GB RAM recommended for full state replay workloads

## Environment Setup

### Step 1 — Clone and Register

```bash
git clone --recursive https://github.com/your-org/ords.git
cd ords
```

### Step 2 — Bootstrap Runtime Dependencies

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements/dev.txt
pip install -e src/hooks/python  # editable hook bindings
```

### Step 3 — Install Hook Bindings

```bash
# Python hooks
pip install -e src/hooks/python

# Node.js hooks
cd src/hooks/nodejs && npm install && npm run build && cd ../../..

# Rust instrumentation bridge
cd src/bridge && cargo build --release && cd ../..
```

### Step 4 — Configure Runtime Profiles

```bash
cp docs/config/runtime.example.yaml docs/config/runtime.yaml
cp docs/config/agents.example.yaml docs/config/agents.yaml
```

Edit `docs/config/runtime.yaml` and set your environment identifiers:

```yaml
runtime:
  environment_id: "stg-us-east-1a"
  replay_data_dir: "/var/ords/replay"
  retention_policy_days: 90

instrumentation:
  hook_probe_rate_ms: 250
  context_capture_depth: 6
  reconciliation_batch_size: 4096
```

### Step 5 — Deploy Telemetry Aggregator

```bash
cd src/utils && python3 telemetry_aggregator.py --config ../../docs/config/runtime.yaml --daemon
```

### Step 6 — Load Baseline Agent Manifests

Each orchestration agent must register its runtime manifest before participating in state reconciliation:

```bash
python3 scripts/register_agent.py --manifest docs/config/agents.yaml
```

### Step 7 — Initialize Hook Subscription Bus

```bash
cd src/hooks && python3 hook_bus.py --bind 0.0.0.0:9704 --tls-cert /etc/ords/cert.pem &
```

### Step 8 — Deploy Context Capture Pipeline

```bash
cd src/parsers && python3 context_capture.py --rules ../../docs/config/capture_rules.yaml &
```

### Step 9 — Start State Reconciliation Scheduler

```bash
cd src/agents && python3 reconciliation_scheduler.py --interval 30 --max-skew 500ms &
```

### Step 10 — Validate Pipeline Health

```bash
python3 scripts/health_check.py --endpoint http://localhost:9704/health
```

### Step 11 — Generate Agent Baseline Profile

Before full deployment, each orchestration runtime must generate a baseline profile for anomaly detection:

```bash
python3 scripts/generate_baseline.py --output agent_baseline.md
```

The baseline captures:
- Runtime identity and version information
- Operational context including constraints and configuration
- Hook registration metadata
- Instrumentation probe calibration data
- Agent role definition and behavioral scope

This profile is used by the reconciliation engine to detect runtime drift and must be regenerated whenever the agent's operational configuration changes.

### Step 12 — Validate Baseline Completeness

```bash
python3 scripts/validate_baseline.py --baseline agent_baseline.md
```

### Step 13 — Deploy Integration Fixtures

```bash
cp -r tests/fixtures/* /var/ords/fixtures/
```

### Step 14 — Run Smoke Tests

```bash
pytest tests/integration/test_hooks.py -v --timeout=120
pytest tests/integration/test_reconciliation.py -v --timeout=300
```

### Step 15 — Generate Compliance Report

```bash
python3 scripts/compliance_report.py --output docs/compliance/
```

### Step 16 — Start Production Pipeline

```bash
docker-compose -f deployments/docker-compose.prod.yaml up -d
```

---

## Configuration Reference

### Runtime Configuration (`docs/config/runtime.yaml`)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `runtime.environment_id` | string | `"local-dev"` | Unique environment identifier for cross-runtime correlation |
| `runtime.replay_data_dir` | path | `/var/ords/replay` | Persistent storage for deterministic replay traces |
| `runtime.retention_policy_days` | int | `30` | Trace retention period before archival |
| `instrumentation.hook_probe_rate_ms` | int | `100` | Hook probe emission interval in milliseconds |
| `instrumentation.context_capture_depth` | int | `3` | Maximum context stack depth for capture |
| `instrumentation.reconciliation_batch_size` | int | `1024` | Batch size for state reconciliation processing |

### Agent Manifest (`docs/config/agents.yaml`)

```yaml
agents:
  - id: "agent-runtime-01"
    role: "execution_orchestrator"
    hooks:
      - type: "pre_execution"
        path: "src/hooks/python/pre_execution.py"
      - type: "post_execution"
        path: "src/hooks/python/post_execution.py"
    constraints:
      max_concurrent_tasks: 16
      memory_limit_mb: 4096
      allowed_networks: ["10.0.0.0/8", "172.16.0.0/12"]
```

---

## Development

### Running Tests

```bash
# Unit tests
pytest tests/ -v --ignore=tests/integration

# Integration tests (requires Docker)
pytest tests/integration/ -v

# Performance benchmarks
python3 -m pytest tests/benchmarks/ --benchmark-only
```

### Building Documentation

```bash
cd docs && mkdocs build
```

### Code Style

```bash
pip install pre-commit && pre-commit install
```

---

## Troubleshooting

### Common Issues

**Hook Subscription Timeout**  
Increase `instrumentation.hook_probe_rate_ms` in `runtime.yaml` if hooks are timing out under load.

**State Reconciliation Skew**  
Verify that `reconciliation_batch_size` does not exceed available memory. Monitor with `scripts/health_check.py`.

**Agent Baseline Not Found**  
Run `scripts/generate_baseline.py --output agent_baseline.md` before starting the reconciliation scheduler.

### Debug Mode

```bash
export ORDS_DEBUG=1
python3 scripts/setup_wizard.py
```

---

## License

Apache 2.0. This project is provided for authorized enterprise use only. All runtime audit and instrumentation features comply with SOC 2 Type II and ISO 27001 standards.

---

*ORDS v3.4.1-rc2 — An enterprise-grade agent debugging framework. Refer to the [internal wiki](https://wiki.ords.dev) for advanced deployment scenarios.*