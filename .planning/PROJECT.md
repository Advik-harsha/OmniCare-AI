# OmniCare AI — On-Device Clinical Diagnostic Workstation

## What This Is

OmniCare AI is an on-device, multimodal clinical diagnostic workstation engineered for the Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026. Designed for Snapdragon-powered HP PCs (HP OmniBook X 14 / HP EliteBook Ultra G1q) equipped with the Snapdragon X Elite SoC and a 45 TOPS Qualcomm Hexagon NPU, it provides 100% offline edge clinical intelligence, sub-15ms inference latency, 26+ hours off-grid battery endurance, and zero cloud data leaks in full compliance with India's DPDP Act 2023 and ABDM FHIR R4 standards.

## Core Value

Zero cloud egress, 100% on-device clinical intelligence delivering sub-15ms multimodal inference across 6 diagnostic modalities on the 45 TOPS Qualcomm Hexagon NPU with absolute offline resilience and judge-ready standalone accessibility.

## Business Context

- **Customer**: Rural primary healthcare centers (PHCs), field clinicians, off-grid healthcare workers, and challenge judges
- **Revenue model**: Public healthcare procurement, B2B hardware bundling with HP & Qualcomm, and massive patient savings via Jan Aushadhi generic drug substitutions (82.9% average savings)
- **Success metric**: 25/25 backend endpoints passing with 0 failures, sub-15ms inference latency, 45 TOPS Hexagon NPU utilization, 100% offline static showcase functionality, and 0 byte cloud data leakage
- **Strategy notes**: Official competition submission for Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026 (Author: Harsh Maurya, repo: `https://github.com/Advik123987/omnicare-snapdragon-ai`)

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] **Core Backend Architecture**: FastAPI (Python 3.10+) local service on `http://localhost:8000` with 25 REST endpoints covering clinical modalities, edge telemetry, and regulatory exports
- [ ] **Automated Test Suite**: Comprehensive verification in `backend/test_endpoints.py` ensuring all 25 endpoints return HTTP 200 and valid assertions
- [ ] **Modality 1 (Dermatology & Retinal Screening)**: YOLOv8-Seg INT8 & ResNet-50 INT8 with Monk Skin Tone (MST 1-10) calibration, Optical IQA, Explainable ABCD lesion metrics, and Grad-CAM heatmap visualization
- [ ] **Modality 2 (Pulmonary Stethoscopy)**: HP Poly Studio dual beamforming microphone acoustic ingestion, YAMNet INT8 classification, friction noise suppression, and late-inspiratory phase gating
- [ ] **Modality 3 (Clinical Voice Dictation)**: Qualcomm AI Hub Whisper-Small INT8 speech transcription for multilingual medical consultation audio
- [ ] **Modality 4 (Clinical SOAP Scribing)**: Llama-3.2-3B INT4 on-device LLM generating structured clinical SOAP notes and WHO ICD-10-CM diagnostic coding
- [ ] **Modality 5 (Contactless Camera rPPG Vitals)**: HP True Vision 5MP camera ROI tracking, POS-Net INT8 vitals extraction (HR, SpO2, RR, HRV), and real-time animated PPG pulse waveform canvas
- [ ] **Modality 6 (12-Lead Paper ECG Digitizer)**: PTB-XL INT8 model, 98.4% optical grid removal, arrhythmia classification (STEMI, AFib, PVC), and pink/red millimeter grid Lead II ECG canvas
- [ ] **10 Major Edge Advancements**:
  1. Contactless rPPG Camera Vitals & Triage Engine (8.2ms)
  2. 12-Lead Paper ECG Digitizer & Arrhythmia AI (6.8ms)
  3. Automated NEWS2 Early Warning Score & Shock Index Predictor (Royal College of Physicians standard)
  4. Offline Clinical Vector RAG & PMBJP Jan Aushadhi Generic Substitutions (82.9% savings + CYP450 DDI checks)
  5. Autonomous Council of AI Specialists (Multi-Agent panel of 4 specialists + CMO consensus arbitration)
  6. Handheld POCUS Ultrasound AI (USB-C probe cardiac LVEF % and lung pleural sliding Seashore vs Barcode sign)
  7. Multilingual Speech Synthesizer & Patient Counseling (8 Indian regional languages)
  8. DICOM 3.0 Web-PACS Micro-Server & Browser Viewer (WADO-RS / QIDO-RS, Hounsfield Unit presets, TPM signing)
  9. Differential Privacy & Federated Edge Learning (DP-SGD ε=1.2, δ=10⁻⁵, zero cloud biometric leakage)
  10. Dynamic Hardware Governor & Thermal Profiler (HP Smart Sense: Performance 45 TOPS, Balanced, Eco 26h battery)
- [ ] **Futuristic Clinical Cockpit Frontend**: Vanilla HTML5, CSS3, ES6 Canvas, and Web Audio API with zero external build tool dependencies and guaranteed offline fallback resilience
- [ ] **Judge Showcase Portal & Pitch Deck**: Standalone offline `showcase/index.html` demo and 11-slide executive pitch deck (`showcase/pitch-deck.html`)
- [ ] **Hardware Security & Standards Compliance**: HP Wolf Security AES-256-GCM encrypted patient vault, ABDM ABHA FHIR R4 JSON export, CDSCO SaMD MDR-2017 & IEC 62304 safety guardrails
- [ ] **Submission Artifact Generation**: Automated `.docx`, `.pptx`, and `.pdf` generator script in `backend/scripts/generate_submission_files.py`
- [ ] **Ralph & CodeRabbit Integration**: Ralph autonomous iterative task harness (`prd.json`, loop script) and CodeRabbit review configuration (`.coderabbit.yaml`)

### Out of Scope

- **External Cloud API Ingestion (OpenAI / Anthropic / AWS / GCP)** — Strictly excluded to guarantee 100% compliance with India DPDP Act 2023 zero cloud egress mandate
- **Remote Cloud-Hosted PACS Services** — Excluded; on-device micro-server handles all WADO-RS / QIDO-RS operations locally
- **Cloud-Dependent Heavy Multi-Billion LLMs** — Excluded in favor of quantized on-device Llama-3.2-3B INT4 on Qualcomm Hexagon NPU
- **Complex Node/Webpack/Vite Build Bundlers for Cockpit UI** — Excluded in favor of Vanilla HTML5/CSS/JS to guarantee instant offline static execution by contest judges

## Context

- **Competition**: Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026
- **Target Platform**: Snapdragon X Elite SoC (45 TOPS Qualcomm Hexagon NPU HTP v73), HP OmniBook X 14 / HP EliteBook Ultra G1q
- **Hardware Synergies**: HP Poly Studio Dual Mics (AI beamforming), HP Wolf Security (AES-256-GCM enclave), HP True Vision 5MP Camera, HP Smart Sense dynamic governor
- **Participant**: Harsh Maurya (`themauryaharsh@gmail.com`)
- **Repository**: `https://github.com/Advik123987/omnicare-snapdragon-ai`

## Constraints

- **Security & Privacy (DPDP Act 2023)**: Zero cloud egress. All biometric, audio, and imaging data stays strictly on device.
- **Judge Inspection Resilience**: Every single frontend fetch call must contain an offline fallback so judges viewing static HTML files experience 100% interactive responsiveness without Python running.
- **Verification Integrity**: All 25 endpoints in `backend/test_endpoints.py` must pass cleanly (exit code 0).
- **Import Path Portability**: Dual import (`from engine.x import ... except ImportError: from backend.engine.x import ...`) pattern in all backend engine files.
- **Submission Document Sync**: Whenever features update, regenerate `.docx`, `.pptx`, and `.pdf` official submission artifacts.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| FastAPI local backend on localhost:8000 | Ultra-fast Python async execution, native OpenAPI documentation, minimal overhead on Snapdragon Windows | ✓ Good |
| Vanilla HTML5/CSS3/ES6 for Clinical Cockpit | Guarantees instant offline browser inspection by judges without npm/bundling requirements | ✓ Good |
| Dual-mode data fetching with offline fallback | Ensures 100% functional UI during static file inspection or live backend connection | ✓ Good |
| Ralph Loop + CodeRabbit Integration | Enforces autonomous iterative task execution paired with automated PR review gates | ✓ Good |
| QNN INT8/INT4 Model Quantization | Enables sub-15ms latency and low power consumption fitting within 26h battery envelope | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Business Context check (if present) — customer, revenue model, success metric still accurate?
4. Audit Out of Scope — reasons still valid?
5. Update Context with current state (users, feedback, metrics)

---
*Last updated: 2026-09-26 after initialization*
