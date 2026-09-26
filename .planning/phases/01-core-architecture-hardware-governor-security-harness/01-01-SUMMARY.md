---
phase: 01-core-architecture-hardware-governor-security-harness
plan: 01
subsystem: core-backend
tags: [fastapi, snapdragon, npu, telemetry, governor]
provides:
  - FastAPI local backend running on localhost:8000
  - Hexagon NPU telemetry profiler reporting 45.0 TOPS peak and sub-15ms latency
  - HP Smart Sense dynamic governor with Performance, Balanced, and Eco profiles
  - 1-click Windows and PowerShell launchers
affects: [Phase 2, Phase 3, Phase 4, Phase 5]
actuals:
  tasks: 2
  commits: 1
tech-stack:
  added: [fastapi, uvicorn, pydantic, numpy]
  patterns: [dual-import portability, dynamic hardware profiling]
key-files:
  created:
    - backend/requirements.txt
    - backend/config.py
    - backend/engine/telemetry.py
    - backend/engine/hardware_governor.py
    - backend/main.py
    - launch_omnicare.bat
    - launch_omnicare.ps1
duration: 4min
completed: 2026-09-26
status: complete
---

# Plan 01-01 Summary: Core Backend Infrastructure & NPU Telemetry

Established foundational FastAPI service, Snapdragon X Elite NPU hardware profiling engine, HP Smart Sense governor, and 1-click execution scripts.

## Accomplishments
- Implemented `backend/config.py` declaring Snapdragon X Elite specs (45 TOPS Hexagon NPU, sub-15ms target latency, 26h battery life).
- Implemented `backend/engine/telemetry.py` modeling live 45.0 TOPS NPU compute profiling.
- Implemented `backend/engine/hardware_governor.py` modeling HP Smart Sense profiles (Performance 45 TOPS, Balanced 32 TOPS, Eco 20 TOPS with <20 dBA fan noise).
- Built `backend/main.py` mounting CORS, health check, telemetry, and governor REST endpoints.
- Created `launch_omnicare.bat` and `launch_omnicare.ps1` for 1-click launch.
