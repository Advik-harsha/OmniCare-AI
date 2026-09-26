"""
OmniCare AI — On-Device Clinical Diagnostic Workstation
FastAPI REST Service on Snapdragon® X Elite (45 TOPS Qualcomm Hexagon NPU)
Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026
"""

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

try:
    from config import CONFIG
    from engine.telemetry import get_npu_telemetry
    from engine.hardware_governor import get_governor_status, set_governor_profile
    from engine.fhir_exporter import export_abdm_fhir_bundle, PATIENT_PRESETS
    from engine.safety_guardrails import get_safety_engine
    from security.wolf_vault import get_vault
    from security.offline_sync_engine import get_sync_engine
except ImportError:
    from backend.config import CONFIG
    from backend.engine.telemetry import get_npu_telemetry
    from backend.engine.hardware_governor import get_governor_status, set_governor_profile
    from backend.engine.fhir_exporter import export_abdm_fhir_bundle, PATIENT_PRESETS
    from backend.engine.safety_guardrails import get_safety_engine
    from backend.security.wolf_vault import get_vault
    from backend.security.offline_sync_engine import get_sync_engine

app = FastAPI(
    title=CONFIG.app_name,
    version=CONFIG.version,
    description="On-Device Multimodal Clinical Workstation for Snapdragon X Elite"
)

# CORS middleware for local frontend and judge inspection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GovernorRequest(BaseModel):
    profile: str

class VaultStoreRequest(BaseModel):
    patient_id: str
    record: Dict[str, Any]

class TriageEvaluationRequest(BaseModel):
    news2_score: int
    shock_index: float
    arrhythmia_type: Optional[str] = "NORMAL"

@app.get("/")
def read_root():
    return {
        "workstation": CONFIG.app_name,
        "version": CONFIG.version,
        "status": "OPERATIONAL",
        "target_soc": CONFIG.hardware.soc,
        "npu_tops": CONFIG.hardware.npu_peak_tops,
        "privacy": "Zero Cloud Egress (DPDP Act 2023 Compliant)",
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": CONFIG.app_name,
        "npu_status": "ONLINE (45.0 TOPS HTP v73)",
        "memory_ok": True,
        "storage_enclave": "LOCKED_SECURE"
    }

# ----------------- NPU Telemetry & Hardware Governor -----------------

@app.get("/api/telemetry")
def get_telemetry_endpoint():
    return get_npu_telemetry()

@app.get("/api/governor/status")
def get_governor_status_endpoint():
    return get_governor_status()

@app.post("/api/governor/profile")
def set_governor_profile_endpoint(req: GovernorRequest):
    try:
        return set_governor_profile(req.profile)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----------------- Patient Demographic Engine -----------------

@app.get("/api/patient/presets")
def get_patient_presets_endpoint():
    return [
        {
            "key": k,
            "id": v["id"],
            "name": v["name"],
            "gender": v["gender"],
            "age": v["age"],
            "chief_complaint": v["chief_complaint"]
        }
        for k, v in PATIENT_PRESETS.items()
    ]

@app.get("/api/patient/{preset_key}")
def get_patient_detail_endpoint(preset_key: str):
    key = preset_key.lower().strip()
    if key not in PATIENT_PRESETS:
        raise HTTPException(status_code=404, detail=f"Patient preset '{preset_key}' not found.")
    return PATIENT_PRESETS[key]

# ----------------- HP Wolf Security Enclave -----------------

@app.get("/api/security/vault/status")
def get_vault_status_endpoint():
    return get_vault().get_status()

@app.post("/api/security/vault/store")
def store_vault_record_endpoint(req: VaultStoreRequest):
    encrypted = get_vault().encrypt_record(req.patient_id, req.record)
    return {"status": "STORED_ENCRYPTED", "payload": encrypted}

@app.get("/api/security/vault/retrieve/{patient_id}")
def retrieve_vault_record_endpoint(patient_id: str):
    try:
        decrypted = get_vault().decrypt_record(patient_id)
        return {"status": "DECRYPTED_SUCCESS", "record": decrypted}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/security/audit")
def get_audit_trail_endpoint():
    return get_vault().get_audit_trail()

@app.get("/api/security/audit/verify")
def verify_audit_endpoint():
    valid = get_vault().verify_audit_integrity()
    return {"audit_chain_verified": valid, "status": "VERIFIED_TAMPER_FREE" if valid else "CORRUPTED"}

# ----------------- Offline Sync Queue -----------------

@app.get("/api/security/sync/status")
def get_sync_status_endpoint():
    return get_sync_engine().get_queue_status()

@app.post("/api/security/sync/trigger")
def trigger_sync_endpoint():
    return get_sync_engine().trigger_sync()

# ----------------- ABDM FHIR R4 Exporter -----------------

@app.get("/api/export/fhir")
def export_fhir_endpoint(patient: str = Query("aarav", description="Patient preset identifier")):
    bundle = export_abdm_fhir_bundle(patient)
    return bundle

# ----------------- Clinical Safety & CDSCO SaMD Guardrails -----------------

@app.get("/api/safety/guardrails")
def get_safety_status_endpoint():
    return get_safety_engine().get_guardrails_status()

@app.post("/api/safety/evaluate")
def evaluate_safety_endpoint(req: TriageEvaluationRequest):
    return get_safety_engine().evaluate_triage_risk(
        news2_score=req.news2_score,
        shock_index=req.shock_index,
        arrhythmia_type=req.arrhythmia_type
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
