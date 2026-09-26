# Roadmap: OmniCare AI

## Overview

OmniCare AI is an on-device, multimodal clinical diagnostic workstation engineered for the Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026. The roadmap is structured as a 6-phase Vertical MVP progression: starting with core hardware telemetry, Wolf Security enclave, and Ralph/CodeRabbit harness, building out the 6 diagnostic AI modalities and 10 edge advancements, crafting the futuristic clinical cockpit and standalone judge showcase with 100% offline fallback resilience, and culminating in full automated test verification (25/25 endpoints) and submission document generation.

## Phases

- [ ] **Phase 1: Core Architecture, Hardware Governor, Security & Harness** - Establish FastAPI backend, Hexagon NPU telemetry, HP Smart Sense governor, Wolf Security AES-256 vault, ABDM FHIR exporter, and Ralph/CodeRabbit harness.
- [ ] **Phase 2: Diagnostic Audio, Vision & NLP Engines** - Build on-device multimodal diagnostic AI modules for Dermatology/Retina, Pulmonary Stethoscopy, Multilingual Voice Dictation, and Clinical SOAP Scribing.
- [ ] **Phase 3: Contactless rPPG Vitals & 12-Lead Paper ECG Digitizer** - Implement camera photoplethysmography (POS-Net INT8) and 12-lead paper ECG digitizer with 98.4% grid removal and PTB-XL INT8 arrhythmia detection.
- [ ] **Phase 4: Advanced Clinical Intelligence & Distributed Edge Services** - Implement NEWS2 early warning scoring, PMBJP Jan Aushadhi generic substitutions + CYP450 DDIs, Multi-Agent Council of Specialists, POCUS ultrasound, 8-language speech synthesis, and DICOM 3.0 Web-PACS.
- [ ] **Phase 5: Futuristic Clinical Cockpit UI & Standalone Judge Showcase** - Construct futuristic clinical cockpit dashboard and offline Judge Showcase Portal & pitch deck with 100% offline fallback resilience and live canvases.
- [ ] **Phase 6: Automated Verification, Submission Package & Code Review** - Pass all 25 automated backend tests (exit code 0), generate official competition submission artifacts (.docx, .pptx, .pdf), and enforce review gates.

## Phase Details

### Phase 1: Core Architecture, Hardware Governor, Security & Harness
**Goal**: Establish local FastAPI backend, Snapdragon X Elite Hexagon NPU telemetry, HP Smart Sense dynamic governor, HP Wolf Security AES-256 vault, ABDM FHIR exporter, patient preset profiles, and Ralph/CodeRabbit autonomous execution & review harness.  
**Mode**: mvp  
**Depends on**: Nothing (first phase)  
**Requirements**: CORE-01, CORE-02, CORE-03, CORE-04, CORE-05, SEC-01, SEC-02, SEC-03, HARN-01, HARN-02  
**Success Criteria** (what must be TRUE):
  1. FastAPI server launches locally on `http://localhost:8000` via `launch_omnicare.bat` and `launch_omnicare.ps1` with dual-import engine portability.
  2. NPU profiler reports 45.0 TOPS peak, sub-15ms latency, and switches across HP Smart Sense profiles (Performance, Balanced, Eco).
  3. HP Wolf Security vault encrypts and validates patient records with AES-256-GCM and SHA-256 chaining.
  4. ABDM FHIR R4 JSON clinical bundle exporter generates compliant NRCeS India standard records.
  5. Ralph iterative harness (`prd.json`, `ralph.ps1`) and `.coderabbit.yaml` review configuration are active.
**Plans**: 3 plans

Plans:
- [ ] 01-01: Backend core infrastructure, config, launcher scripts, and Hexagon NPU telemetry governor.
- [ ] 01-02: HP Wolf Security encrypted patient vault, ABDM FHIR R4 exporter, and patient preset demographics.
- [ ] 01-03: Ralph autonomous loop harness (`prd.json`, loop scripts) and CodeRabbit review configuration (`.coderabbit.yaml`).

### Phase 2: Diagnostic Audio, Vision & NLP Engines
**Goal**: Build on-device multimodal diagnostic AI modules for Dermatology/Retinal screening (YOLOv8/ResNet-50 INT8 + Monk Skin Tone + ABCD/Grad-CAM), Pulmonary Stethoscopy (HP Poly Studio + YAMNet INT8), Multilingual Voice Dictation (Whisper-Small INT8), and Clinical SOAP Scribing (Llama-3.2-3B INT4 + ICD-10).  
**Mode**: mvp  
**Depends on**: Phase 1  
**Requirements**: DERM-01, DERM-02, DERM-03, DERM-04, PULM-01, PULM-02, PULM-03, PULM-04, DICT-01, DICT-02, DICT-03, SCRIBE-01, SCRIBE-02, SCRIBE-03  
**Success Criteria** (what must be TRUE):
  1. Dermatology & retinal screening outputs lesion classification, Monk Skin Tone rating (MST 1-10), optical IQA, and explainable ABCD rule evaluation with Grad-CAM heatmap visualization.
  2. Pulmonary stethoscopy classifies respiratory acoustics into Wheezes, Crackles, Stridor, and Normal breath sounds with acoustic friction suppression.
  3. Voice dictation engine transcribes multilingual medical speech into consultation transcripts.
  4. Clinical scribe structures transcripts into standardized SOAP notes with WHO ICD-10-CM diagnostic codes.
**Plans**: 3 plans

Plans:
- [ ] 02-01: Dermatology and retinal screening engine with Monk Skin Tone calibration, optical IQA, and ABCD/Grad-CAM explainability.
- [ ] 02-02: HP Poly Studio pulmonary stethoscopy engine with YAMNet INT8 classification and late-inspiratory phase gating.
- [ ] 02-03: Whisper-Small INT8 multilingual voice dictation and Llama-3.2-3B INT4 clinical SOAP & ICD-10 scribing engine.

### Phase 3: Contactless rPPG Vitals & 12-Lead Paper ECG Digitizer
**Goal**: Implement contactless camera photoplethysmography (POS-Net INT8) delivering real-time vitals (HR, SpO2, RR, HRV) and 12-lead paper ECG digitizer with 98.4% optical grid suppression and PTB-XL INT8 arrhythmia detection.  
**Mode**: mvp  
**Depends on**: Phase 2  
**Requirements**: RPPG-01, RPPG-02, RPPG-03, RPPG-04, ECG-01, ECG-02, ECG-03, ECG-04  
**Success Criteria** (what must be TRUE):
  1. Contactless rPPG engine extracts HR, SpO2, RR, and Shock Index in 8.2ms with real-time waveform data stream.
  2. ECG digitizer strips background grid lines from paper photos with 98.4% optical suppression and reconstructs Lead II voltage traces.
  3. Arrhythmia classifier identifies STEMI, AFib, and PVC within 6.8ms latency and computes PR/QRS/QTc intervals.
**Plans**: 2 plans

Plans:
- [ ] 03-01: Contactless rPPG vital signs engine with POS-Net INT8 and hemodynamic shock index prediction.
- [ ] 03-02: 12-Lead paper ECG digitizer, PTB-XL arrhythmia classifier, and electrophysiological interval calculator.

### Phase 4: Advanced Clinical Intelligence & Distributed Edge Services
**Goal**: Implement 8 advanced edge engines: NEWS2 early warning scoring, PMBJP Jan Aushadhi generic substitution (82.9% savings) + CYP450 DDI checks, Autonomous Multi-Agent Council of AI Specialists with CMO arbitration, Handheld POCUS ultrasound (LVEF % & Pleural sliding), Multilingual speech synthesizer (8 Indian languages), DICOM 3.0 Web-PACS micro-server, and Differential Privacy (DP-SGD) federated learning.  
**Mode**: mvp  
**Depends on**: Phase 3  
**Requirements**: ADV-01, ADV-02, ADV-03, ADV-04, ADV-05, ADV-06, ADV-07, ADV-08  
**Success Criteria** (what must be TRUE):
  1. Royal College of Physicians NEWS2 score breakdown and clinical escalation protocols are accurately calculated.
  2. PMBJP Jan Aushadhi engine matches branded prescriptions to generic equivalents with transparent cost savings and DDI warnings.
  3. Council of AI Specialists renders consensus opinion with 4 specialist testimonials and CMO arbitration.
  4. POCUS ultrasound evaluates cardiac ejection fraction and lung pleural sliding signs.
  5. DICOM 3.0 server serves calibrated medical images via WADO-RS / QIDO-RS.
  6. Differential privacy engine applies DP-SGD (ε=1.2, δ=10⁻⁵) to model update deltas.
**Plans**: 3 plans

Plans:
- [ ] 04-01: NEWS2 calculator, PMBJP Jan Aushadhi generic substitution, and CYP450 drug interaction checker.
- [ ] 04-02: Council of AI Specialists multi-agent deliberation panel and Handheld POCUS ultrasound AI engine.
- [ ] 04-03: Multilingual regional speech synthesizer, DICOM 3.0 Web-PACS server, and federated DP-SGD privacy engine.

### Phase 5: Futuristic Clinical Cockpit UI & Standalone Judge Showcase
**Goal**: Construct futuristic clinical cockpit dashboard and offline Judge Showcase Portal & pitch deck with 100% offline fallback resilience and live canvases.  
**Mode**: mvp  
**UI hint**: yes  
**Depends on**: Phase 4  
**Requirements**: UI-01, UI-02, UI-03, UI-04, UI-05  
**Success Criteria** (what must be TRUE):
  1. Clinical Cockpit displays real-time telemetry HUD (45 TOPS, latency, battery, Smart Sense selector) and 6 modality panels.
  2. All 6 modals (NEWS2, Council, Jan Aushadhi, POCUS, FHIR, Wolf Vault) open and render dynamic data.
  3. Opening `showcase/index.html` directly from disk with 0 backend servers running provides 100% interactive UI via seamless offline fallbacks.
  4. Live animated cyan PPG pulse waveform and pink/red millimeter grid Lead II ECG render cleanly on HTML5 canvases.
  5. Pitch deck (`showcase/pitch-deck.html`) presents 11 interactive slides with clinical metrics and NPU benchmarks.
**Plans**: 2 plans

Plans:
- [ ] 05-01: Futuristic Clinical Cockpit frontend with Cyan/Cobalt HUD, Web Audio synth, live canvases, and offline fallbacks.
- [ ] 05-02: Standalone Judge Showcase Portal (`showcase/index.html`) and 11-slide interactive executive pitch deck (`showcase/pitch-deck.html`).

### Phase 6: Automated Verification, Submission Package & Code Review
**Goal**: Pass all 25 automated backend tests (exit code 0), generate official competition submission artifacts (.docx, .pptx, .pdf), and enforce review gates.  
**Mode**: mvp  
**Depends on**: Phase 5  
**Requirements**: VERIF-01, VERIF-02  
**Success Criteria** (what must be TRUE):
  1. Automated test suite in `backend/test_endpoints.py` asserts all 25 clinical, hardware, and regulatory endpoints pass with code 0.
  2. Automated submission file generator (`backend/scripts/generate_submission_files.py`) outputs `.docx`, `.pptx`, and `.pdf` files.
  3. CodeRabbit review criteria and Ralph loop verification pass all safety and offline resilience gates.
**Plans**: 2 plans

Plans:
- [ ] 06-01: 25-endpoint comprehensive automated test suite and regression runner in `backend/test_endpoints.py`.
- [ ] 06-02: Automated submission document generator script and competition documentation package in `docs/`.

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Architecture, Hardware Governor, Security & Harness | 0/3 | Not started | - |
| 2. Diagnostic Audio, Vision & NLP Engines | 0/3 | Not started | - |
| 3. Contactless rPPG Vitals & 12-Lead Paper ECG Digitizer | 0/2 | Not started | - |
| 4. Advanced Clinical Intelligence & Distributed Edge Services | 0/3 | Not started | - |
| 5. Futuristic Clinical Cockpit UI & Standalone Judge Showcase | 0/2 | Not started | - |
| 6. Automated Verification, Submission Package & Code Review | 0/2 | Not started | - |
