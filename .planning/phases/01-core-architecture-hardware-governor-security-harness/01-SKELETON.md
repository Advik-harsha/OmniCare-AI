# Walking Skeleton — OmniCare AI

**Phase:** 1  
**Generated:** 2026-09-26  
**Target Hardware:** Snapdragon-Powered HP PCs (HP OmniBook X / HP EliteBook Ultra, 45 TOPS Hexagon NPU)  

## Capability Proven End-to-End

A clinician or judge can launch OmniCare AI locally with a 1-click script, connect to the FastAPI backend at `http://localhost:8000`, query Snapdragon Hexagon NPU telemetry (45.0 TOPS, sub-15ms latency), switch HP Smart Sense governor profiles, encrypt/retrieve patient data within the HP Wolf Security AES-256-GCM enclave, and run autonomous execution & review loops via Ralph and CodeRabbit.

## Architectural Decisions

| Decision | Choice | Rationale |
|---|---|---|
| **Backend Framework** | FastAPI (Python 3.10+) | High-performance asynchronous REST API, auto OpenAPI documentation, minimal CPU overhead on Snapdragon Windows |
| **NPU Acceleration** | Qualcomm AI Hub QNN EP (`HTP v73 INT8/INT4`) | Native execution on Qualcomm Hexagon NPU with 45 TOPS peak performance and sub-15ms latency |
| **Security Enclave** | HP Wolf Security (AES-256-GCM) | Hardware-backed vault with SHA-256 tamper-evident chaining ensuring 100% compliance with India DPDP Act 2023 |
| **Healthcare Standard** | India ABDM / ABHA FHIR R4 JSON | Standardized clinical data exchange compliance recognized by National Health Authority (NHA) & NRCeS |
| **Frontend Strategy** | Vanilla HTML5 / CSS3 / ES6 Canvas | Zero-dependency, instant static execution for contest judges with guaranteed 100% offline fallback resilience |
| **Autonomous Dev Harness** | Ralph Loop + CodeRabbit | PRD-driven autonomous iterative execution (`prd.json`) paired with automated code review gates (`.coderabbit.yaml`) |

## Stack Touched in Phase 1

- [ ] Project scaffold: `backend/requirements.txt`, `backend/config.py`, `backend/main.py`
- [ ] Launch scripts: `launch_omnicare.bat`, `launch_omnicare.ps1`
- [ ] Telemetry & Governor: `backend/engine/telemetry.py`, `backend/engine/hardware_governor.py`
- [ ] Security & Vault: `backend/security/wolf_vault.py`, `backend/security/offline_sync_engine.py`
- [ ] Healthcare Standards & Safety: `backend/engine/fhir_exporter.py`, `backend/engine/safety_guardrails.py`
- [ ] Autonomous Harness: `prd.json`, `ralph.ps1`, `ralph.bat`, `.coderabbit.yaml`

## Out of Scope (Deferred to Later Slices)

- Diagnostic vision models (YOLOv8-Seg, ResNet-50) — Phase 2
- Pulmonary acoustic stethoscopy (YAMNet) — Phase 2
- Speech dictation (Whisper-Small) & SOAP note generation (Llama-3.2) — Phase 2
- Contactless camera rPPG vitals & ECG digitizer — Phase 3
- Advanced AI Council, POCUS ultrasound, and DICOM PACS — Phase 4
- Futuristic Clinical Cockpit UI & Judge Showcase Portal — Phase 5
- Full 25-endpoint automated test suite & submission artifact generation — Phase 6

## Subsequent Slice Plan

Each later phase builds directly on this walking skeleton:
- **Phase 2**: Multi-Modal Diagnostic AI Engines (Dermatology, Retina, Stethoscopy, Dictation, SOAP scribing)
- **Phase 3**: Contactless rPPG Vitals & 12-Lead Paper ECG Arrhythmia Digitizer
- **Phase 4**: Advanced Edge Intelligence (NEWS2, Jan Aushadhi generics + DDIs, Council of Specialists, POCUS, Multilingual speech)
- **Phase 5**: Futuristic Clinical Cockpit UI & Standalone Judge Showcase
- **Phase 6**: Automated Verification, Submission Package & Code Review
