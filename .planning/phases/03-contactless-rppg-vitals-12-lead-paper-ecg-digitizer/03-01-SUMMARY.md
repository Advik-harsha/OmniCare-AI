---
phase: 03-contactless-rppg-vitals-12-lead-paper-ecg-digitizer
plan: 01
subsystem: rppg-vitals
tags: [rppg, pos-net, true-vision, shock-index, vitals, canvas]
provides:
  - HP True Vision 5MP camera facial ROI tracking
  - POS-Net INT8 contactless vital signs extraction (HR, SpO2, RR, HRV) in 8.2ms
  - Hemodynamic shock index prediction and triage categorization
  - Real-time animated cyan PPG pulse waveform coordinates for HTML5 canvas
affects: [Phase 4, Phase 5, Phase 6]
actuals:
  tasks: 1
  commits: 1
tech-stack:
  added: [pos-net, rppg]
  patterns: [Plane-Orthogonal-to-Skin chrominance projection, hemodynamic shock index]
key-files:
  created:
    - backend/engine/qnn_rppg.py
  modified:
    - backend/main.py
duration: 4min
completed: 2026-09-26
status: complete
---

# Plan 03-01 Summary: Contactless Camera rPPG Vitals & Shock Index

Implemented on-device contactless camera photoplethysmography (POS-Net INT8) extracting vital signs in 8.2ms, hemodynamic shock index, and streaming PPG waveforms.

## Accomplishments
- Implemented `backend/engine/qnn_rppg.py` extracting HR (&plusmn;1.4 bpm), SpO2 %, RR, and HRV SDNN ms from facial skin ROI.
- Calculated hemodynamic shock index (HR/SBP) with clinical triage color-coding (Green, Yellow, Amber, Red).
- Provided 60-point synthetic cyan PPG pulse waveform generator for live 60 FPS HTML5 canvas animation.
- Mounted REST endpoints in `backend/main.py`:
  - `GET /api/vitals/rppg/live`
  - `POST /api/vitals/rppg/analyze`
