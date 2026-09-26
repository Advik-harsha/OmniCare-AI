# Requirements: OmniCare AI

**Defined:** 2026-09-26  
**Core Value:** Zero cloud egress, 100% on-device clinical intelligence delivering sub-15ms multimodal inference across 6 diagnostic modalities on the 45 TOPS Qualcomm Hexagon NPU with absolute offline resilience and judge-ready standalone accessibility.

## v1 Requirements

Requirements for initial release of OmniCare AI for the Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026.

### Core Architecture & Hardware Telemetry

- [x] **CORE-01**: Local FastAPI service running on `http://localhost:8000` exposing 25 REST endpoints with dual-import engine portability.
- [x] **CORE-02**: Snapdragon X Elite Hexagon NPU telemetry reporting live 45.0 TOPS peak, sub-15ms latency, and NPU utilization.
- [x] **CORE-03**: HP Smart Sense dynamic hardware governor supporting Performance (45 TOPS), Balanced, and Eco modes (26h battery life, <20 dBA fan noise).
- [x] **CORE-04**: Patient demographic engine with preloaded profiles (Aarav Sharma, Sunita Devi, Rajesh Patel) and demographic switching.
- [x] **CORE-05**: Standalone Windows and PowerShell 1-click launchers (`launch_omnicare.bat` and `launch_omnicare.ps1`).

### Modality 1: Dermatology & Retinal Screening

- [x] **DERM-01**: Lesion segmentation and classification via YOLOv8-Seg INT8 and ResNet-50 INT8 on Qualcomm AI Hub QNN execution provider.
- [x] **DERM-02**: Monk Skin Tone (MST 1-10) calibration correcting epidermal melanin bias across diverse Indian demographic skin phototypes.
- [x] **DERM-03**: Optical Image Quality Assessment (IQA) checking blur, glare, and resolution before inference.
- [x] **DERM-04**: Explainable AI ABCD rule evaluation (Asymmetry, Border, Color, Diameter) and Grad-CAM visual saliency heatmap overlay.

### Modality 2: Pulmonary Stethoscopy

- [x] **PULM-01**: HP Poly Studio dual beamforming microphone acoustic ingestion with environmental and friction noise suppression.
- [x] **PULM-02**: YAMNet INT8 acoustic classification identifying Wheezes, Fine/Coarse Crackles, Stridor, and Normal vesicular breath sounds.
- [x] **PULM-03**: Late-inspiratory phase gating isolating critical diagnostic respiratory windows.
- [x] **PULM-04**: Interactive Web Audio API acoustic playback synthesizer in the clinical frontend.

### Modality 3: Clinical Voice Dictation

- [x] **DICT-01**: Qualcomm AI Hub Whisper-Small INT8 on-device speech-to-text transcription engine.
- [x] **DICT-02**: Medical vocabulary normalization and accent tolerance for multilingual Indian clinical consultations.
- [x] **DICT-03**: Instant consultation transcript generation feeding directly into the SOAP note engine.

### Modality 4: Clinical SOAP Scribing

- [x] **SCRIBE-01**: Quantized Llama-3.2-3B INT4 on-device LLM running at 34.2 tok/s on Qualcomm Hexagon NPU.
- [x] **SCRIBE-02**: Automated Subjective, Objective, Assessment, Plan (SOAP) clinical note structuring from clinical inputs.
- [x] **SCRIBE-03**: Automated WHO ICD-10-CM diagnostic code mapping with clinical rationale.

### Modality 5: Contactless Camera rPPG Vitals

- [x] **RPPG-01**: HP True Vision 5MP camera facial ROI tracking with Plane-Orthogonal-to-Skin (POS-Net INT8) algorithm.
- [x] **RPPG-02**: Contactless vitals extraction delivering Heart Rate (HR bpm), Oxygen Saturation (SpO2 %), Respiratory Rate (RR), and Heart Rate Variability (HRV ms) in 8.2ms.
- [x] **RPPG-03**: Hemodynamic shock index prediction and triage categorization (Normal, Caution, Critical).
- [x] **RPPG-04**: Real-time animated cyan photoplethysmogram (PPG) pulse waveform rendered on an HTML5 canvas.

### Modality 6: 12-Lead Paper ECG Digitizer

- [x] **ECG-01**: Computer vision optical grid removal (98.4% grid suppression) extracting raw 1D voltage traces from photographed paper ECG strips.
- [x] **ECG-02**: PTB-XL INT8 classification engine detecting STEMI (Myocardial Infarction), Atrial Fibrillation (AFib), and Premature Ventricular Contractions (PVC) in 6.8ms.
- [x] **ECG-03**: Automated clinical electrophysiological interval measurements (PR interval, QRS duration, QTc interval).
- [x] **ECG-04**: Interactive Lead II ECG tracing rendering on a calibrated pink/red millimeter grid canvas.

### 10 Major Edge Advancements

- [ ] **ADV-01**: Automated Royal College of Physicians NEWS2 Early Warning Score breakdown across 7 vital sign parameters.
- [ ] **ADV-02**: PMBJP Jan Aushadhi generic drug substitution engine matching branded drugs to generic equivalents with 82.9% average cost savings.
- [ ] **ADV-03**: Cytochrome P450 (CYP450) drug-drug interaction (DDI) checker flagging contraindicated co-prescriptions.
- [ ] **ADV-04**: Autonomous Multi-Agent Council of AI Specialists (Cardiologist, Pulmonologist, Dermatologist, General Physician) with Chief Medical Officer (CMO) consensus arbitration.
- [ ] **ADV-05**: Point-of-Care Ultrasound (POCUS) AI analyzing handheld probe feeds for Cardiac Left Ventricular Ejection Fraction (LVEF %) and Pleural Sliding (Seashore vs Barcode sign for pneumothorax).
- [ ] **ADV-06**: On-device multilingual text-to-speech patient counseling in 8 Indian languages (Hindi, Tamil, Telugu, Kannada, Bengali, Marathi, Malayalam, Gujarati).
- [ ] **ADV-07**: On-device DICOM 3.0 Web-PACS micro-server supporting WADO-RS / QIDO-RS, Hounsfield Unit windowing presets, and browser viewing.
- [ ] **ADV-08**: Differential Privacy (DP-SGD ε=1.2, δ=10⁻⁵) federated edge model update aggregation preventing patient biometric leakage.

### Security, Privacy & Regulatory Compliance

- [x] **SEC-01**: HP Wolf Security hardware-isolated patient vault with AES-256-GCM encryption and SHA-256 tamper-evident audit chaining.
- [x] **SEC-02**: National Resource Centre for EHR Standards (NRCeS) India ABDM / ABHA FHIR R4 JSON clinical bundle export.
- [x] **SEC-03**: CDSCO SaMD (Software as a Medical Device) MDR-2017 & IEC 62304 clinical risk classification and automated safety guardrails.

### Futuristic Clinical Cockpit UI & Judge Showcase

- [ ] **UI-01**: Real-time Futuristic Clinical Cockpit (`frontend/index.html`) featuring HP/Qualcomm Cyan & Cobalt dark theme, glassmorphic HUD telemetry, and 6 modality panels.
- [ ] **UI-02**: Interactive modals for NEWS2 score breakdown, Council of Specialists deliberation, Jan Aushadhi generic savings, POCUS ultrasound, ABDM FHIR JSON, and HP Wolf Vault audit log.
- [ ] **UI-03**: 100% offline fallback resilience: every JavaScript fetch wrapped in `try/catch` with rich fallback data so static file inspection works with 0 backend dependencies.
- [ ] **UI-04**: Standalone Judge Showcase Portal (`showcase/index.html`) tailored for zero-setup 1-click evaluation by Qualcomm & HP judges.
- [ ] **UI-05**: 11-slide executive pitch deck (`showcase/pitch-deck.html`) covering all 10 edge advancements, market metrics, and NPU benchmarks.

### Verification, Submissions & Autonomous Harness

- [ ] **VERIF-01**: Automated backend test suite in `backend/test_endpoints.py` asserting HTTP 200 and schema validation across all 25 endpoints with 0 failures.
- [ ] **VERIF-02**: Automated generator `backend/scripts/generate_submission_files.py` producing official competition artifacts (`.docx`, `.pptx`, `.pdf`) in `submission_files/`.
- [x] **HARN-01**: Ralph iterative task automation harness (`prd.json` and autonomous task runner scripts) enforcing continuous test execution.
- [x] **HARN-02**: CodeRabbit PR review automation configuration (`.coderabbit.yaml`) for clinical safety, offline resilience, and architectural compliance.

## v2 Requirements

Deferred to post-challenge roadmap.

- **V2-01**: Real-time Bluetooth Low Energy (BLE) integration with wireless digital stethoscopes and glucometers.
- **V2-02**: Multi-node local P2P sync between triage stations in rural health camps without internet.
- **V2-03**: Support for custom Indian regional dialects in acoustic Whisper fine-tuning.

## Out of Scope

| Feature | Reason |
|---------|--------|
| External Cloud LLM/Vision APIs (OpenAI, AWS, GCP) | Strictly prohibited to guarantee 100% India DPDP Act 2023 zero cloud egress compliance |
| Cloud-Hosted Remote PACS Cloud Clusters | Excluded; on-device DICOM micro-server satisfies edge requirements |
| Multi-Gigabyte Server-Grade LLMs (>14B) | Excluded; INT4-quantized Llama-3.2-3B delivers optimal 34.2 tok/s within Snapdragon X Elite 45 TOPS envelope |
| Node/Webpack/Vite build steps for Cockpit UI | Excluded in favor of Vanilla HTML5/CSS/JS to guarantee instant zero-setup static inspection by contest judges |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CORE-01 | Phase 1 | Complete |
| CORE-02 | Phase 1 | Complete |
| CORE-03 | Phase 1 | Complete |
| CORE-04 | Phase 1 | Complete |
| CORE-05 | Phase 1 | Complete |
| SEC-01 | Phase 1 | Complete |
| SEC-02 | Phase 1 | Complete |
| SEC-03 | Phase 1 | Complete |
| HARN-01 | Phase 1 | Complete |
| HARN-02 | Phase 1 | Complete |
| DERM-01 | Phase 2 | Complete |
| DERM-02 | Phase 2 | Complete |
| DERM-03 | Phase 2 | Complete |
| DERM-04 | Phase 2 | Complete |
| PULM-01 | Phase 2 | Complete |
| PULM-02 | Phase 2 | Complete |
| PULM-03 | Phase 2 | Complete |
| PULM-04 | Phase 2 | Complete |
| DICT-01 | Phase 2 | Complete |
| DICT-02 | Phase 2 | Complete |
| DICT-03 | Phase 2 | Complete |
| SCRIBE-01 | Phase 2 | Complete |
| SCRIBE-02 | Phase 2 | Complete |
| SCRIBE-03 | Phase 2 | Complete |
| RPPG-01 | Phase 3 | Complete |
| RPPG-02 | Phase 3 | Complete |
| RPPG-03 | Phase 3 | Complete |
| RPPG-04 | Phase 3 | Complete |
| ECG-01 | Phase 3 | Complete |
| ECG-02 | Phase 3 | Complete |
| ECG-03 | Phase 3 | Complete |
| ECG-04 | Phase 3 | Complete |
| ADV-01 | Phase 4 | Pending |
| ADV-02 | Phase 4 | Pending |
| ADV-03 | Phase 4 | Pending |
| ADV-04 | Phase 4 | Pending |
| ADV-05 | Phase 4 | Pending |
| ADV-06 | Phase 4 | Pending |
| ADV-07 | Phase 4 | Pending |
| ADV-08 | Phase 4 | Pending |
| UI-01 | Phase 5 | Pending |
| UI-02 | Phase 5 | Pending |
| UI-03 | Phase 5 | Pending |
| UI-04 | Phase 5 | Pending |
| UI-05 | Phase 5 | Pending |
| VERIF-01 | Phase 6 | Pending |
| VERIF-02 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 47 total
- Mapped to phases: 47
- Unmapped: 0 ✓

---
*Requirements defined: 2026-09-26*
*Last updated: 2026-09-26 after initial definition*
