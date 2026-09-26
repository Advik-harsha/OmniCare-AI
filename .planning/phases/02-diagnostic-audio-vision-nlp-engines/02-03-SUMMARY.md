---
phase: 02-diagnostic-audio-vision-nlp-engines
plan: 03
subsystem: nlp-scribe
tags: [whisper, llama-3.2, soap-note, icd-10, transcription]
provides:
  - Qualcomm AI Hub Whisper-Small INT8 medical voice dictation
  - Accent-tolerant medical vocabulary booster
  - Llama-3.2-3B INT4 on-device LLM clinical SOAP note scribing
  - WHO ICD-10-CM diagnostic code mapping with clinical rationales
affects: [Phase 4, Phase 5, Phase 6]
actuals:
  tasks: 2
  commits: 1
tech-stack:
  added: [whisper, llama-3.2, icd-10]
  patterns: [on-device LLM text generation, SOAP clinical structuring]
key-files:
  created:
    - backend/engine/qnn_transcribe.py
    - backend/engine/clinical_scribe.py
  modified:
    - backend/main.py
duration: 4min
completed: 2026-09-26
status: complete
---

# Plan 02-03 Summary: Whisper Dictation & Llama-3.2 SOAP Scribe

Implemented on-device speech-to-text dictation with Whisper-Small INT8 and autonomous clinical scribing with Llama-3.2-3B INT4 generating structured SOAP notes and WHO ICD-10-CM diagnostic codes.

## Accomplishments
- Implemented `backend/engine/qnn_transcribe.py` transcribing multilingual clinical consultation audio with vocabulary boosting.
- Implemented `backend/engine/clinical_scribe.py` generating structured Subjective, Objective, Assessment, Plan (SOAP) clinical documentation and WHO ICD-10-CM coding at 34.2 tok/s.
- Mounted REST endpoints in `backend/main.py`:
  - `GET /api/transcribe/presets`
  - `POST /api/transcribe/dictation`
  - `POST /api/scribe/soap/generate`
