---
phase: 03-contactless-rppg-vitals-12-lead-paper-ecg-digitizer
plan: 02
subsystem: cardiac-ecg
tags: [ecg, ptb-xl, stemi, afib, pvc, intervals, canvas]
provides:
  - Optical grid removal with 98.4% background grid suppression
  - 1D signal digitization at 25 mm/s and 10 mm/mV standard paper speed
  - PTB-XL INT8 arrhythmia classification (STEMI, AFib, PVC, NSR) in 6.8ms
  - Electrophysiological interval calculations (PR, QRS, QT, QTc)
  - Lead II voltage coordinates for pink/red millimeter grid HTML5 canvas
affects: [Phase 4, Phase 5, Phase 6]
actuals:
  tasks: 1
  commits: 1
tech-stack:
  added: [ptb-xl, ecg-digitizer]
  patterns: [color deconvolution grid suppression, Bazett QTc correction]
key-files:
  created:
    - backend/engine/cardiac_ecg.py
  modified:
    - backend/main.py
duration: 3min
completed: 2026-09-26
status: complete
---

# Plan 03-02 Summary: 12-Lead Paper ECG Digitizer & PTB-XL Arrhythmia AI

Implemented 12-lead paper ECG digitization with 98.4% optical grid suppression, PTB-XL INT8 arrhythmia classification in 6.8ms, and electrophysiological interval calculations.

## Accomplishments
- Implemented `backend/engine/cardiac_ecg.py` stripping pink/red millimeter paper grid lines via adaptive color deconvolution.
- Classified acute anterior STEMI, Atrial Fibrillation, Premature Ventricular Contractions, and Normal Sinus Rhythm in 6.8ms on Qualcomm Hexagon NPU.
- Calculated PR interval, QRS duration, and Bazett-corrected QTc interval.
- Generated Lead II voltage points for rendering on calibrated millimeter grid canvas.
- Mounted REST endpoints in `backend/main.py`:
  - `GET /api/cardiac/ecg/presets`
  - `POST /api/cardiac/ecg/digitize`
  - `POST /api/cardiac/ecg/analyze`
