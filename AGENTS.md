<!-- GSD:project-start source:PROJECT.md -->

## Project

**OmniCare AI — On-Device Clinical Diagnostic Workstation**

OmniCare AI is an on-device, multimodal clinical diagnostic workstation engineered for the Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026. Designed for Snapdragon-powered HP PCs (HP OmniBook X 14 / HP EliteBook Ultra G1q) equipped with the Snapdragon X Elite SoC and a 45 TOPS Qualcomm Hexagon NPU, it provides 100% offline edge clinical intelligence, sub-15ms inference latency, 26+ hours off-grid battery endurance, and zero cloud data leaks in full compliance with India's DPDP Act 2023 and ABDM FHIR R4 standards.

**Core Value:** Zero cloud egress, 100% on-device clinical intelligence delivering sub-15ms multimodal inference across 6 diagnostic modalities on the 45 TOPS Qualcomm Hexagon NPU with absolute offline resilience and judge-ready standalone accessibility.

### Constraints

- **Security & Privacy (DPDP Act 2023)**: Zero cloud egress. All biometric, audio, and imaging data stays strictly on device.
- **Judge Inspection Resilience**: Every single frontend fetch call must contain an offline fallback so judges viewing static HTML files experience 100% interactive responsiveness without Python running.
- **Verification Integrity**: All 25 endpoints in `backend/test_endpoints.py` must pass cleanly (exit code 0).
- **Import Path Portability**: Dual import (`from engine.x import ... except ImportError: from backend.engine.x import ...`) pattern in all backend engine files.
- **Submission Document Sync**: Whenever features update, regenerate `.docx`, `.pptx`, and `.pdf` official submission artifacts.

<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->

## Technology Stack

Technology stack not yet documented. Will populate after codebase mapping or first phase.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->

## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

No project skills found. Add skills to any of: `.agents/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
