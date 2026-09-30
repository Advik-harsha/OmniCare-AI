"""
OmniCare AI — On-Device Clinical Diagnostic Workstation
FastAPI REST Service on Snapdragon® X Elite (45 TOPS Qualcomm Hexagon NPU)
Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026
"""

import os
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

try:
    from config import CONFIG
    from engine.execution_mode import get_execution_environment
    from engine.telemetry import get_npu_telemetry

    from engine.hardware_governor import get_governor_status, set_governor_profile
    from engine.fhir_exporter import export_abdm_fhir_bundle, PATIENT_PRESETS
    from engine.safety_guardrails import get_safety_engine
    from engine.qnn_vision import analyze_dermatology_lesion, screen_retinal_fundus
    from engine.xai_abcd import evaluate_abcd_rule, compute_optical_iqa
    from engine.qnn_audio import analyze_pulmonary_sound, get_stethoscopy_presets
    from engine.qnn_transcribe import transcribe_medical_audio, get_dictation_presets
    from engine.clinical_scribe import generate_soap_note
    from engine.qnn_rppg import extract_rppg_vitals
    from engine.cardiac_ecg import analyze_cardiac_ecg, digitize_paper_ecg, get_ecg_presets
    from engine.news2_calculator import calculate_news2_score
    from engine.drug_guardian import get_jan_aushadhi_catalog, get_generic_substitution, check_drug_interactions
    from engine.council_of_specialists import deliberate_case
    from engine.pocus_ultrasound import analyze_cardiac_pocus, analyze_pleural_pocus, get_pocus_presets
    from engine.regional_counselor import get_supported_languages, synthesize_counseling
    from engine.dicom_pacs_server import query_studies, retrieve_instance, get_hu_presets
    from engine.federated_privacy import get_privacy_budget, sanitize_weight_delta
    from security.wolf_vault import get_vault
    from security.offline_sync_engine import get_sync_engine
except ImportError:
    from backend.config import CONFIG
    from backend.engine.execution_mode import get_execution_environment
    from backend.engine.telemetry import get_npu_telemetry

    from backend.engine.hardware_governor import get_governor_status, set_governor_profile
    from backend.engine.fhir_exporter import export_abdm_fhir_bundle, PATIENT_PRESETS
    from backend.engine.safety_guardrails import get_safety_engine
    from backend.engine.qnn_vision import analyze_dermatology_lesion, screen_retinal_fundus
    from backend.engine.xai_abcd import evaluate_abcd_rule, compute_optical_iqa
    from backend.engine.qnn_audio import analyze_pulmonary_sound, get_stethoscopy_presets
    from backend.engine.qnn_transcribe import transcribe_medical_audio, get_dictation_presets
    from backend.engine.clinical_scribe import generate_soap_note
    from backend.engine.qnn_rppg import extract_rppg_vitals
    from backend.engine.cardiac_ecg import analyze_cardiac_ecg, digitize_paper_ecg, get_ecg_presets
    from backend.engine.news2_calculator import calculate_news2_score
    from backend.engine.drug_guardian import get_jan_aushadhi_catalog, get_generic_substitution, check_drug_interactions
    from backend.engine.council_of_specialists import deliberate_case
    from backend.engine.pocus_ultrasound import analyze_cardiac_pocus, analyze_pleural_pocus, get_pocus_presets
    from backend.engine.regional_counselor import get_supported_languages, synthesize_counseling
    from backend.engine.dicom_pacs_server import query_studies, retrieve_instance, get_hu_presets
    from backend.engine.federated_privacy import get_privacy_budget, sanitize_weight_delta
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

# Mount static directories for interactive Cockpit UI & Judge Showcase Portal
_frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
_showcase_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "showcase"))

if os.path.exists(_frontend_dir):
    app.mount("/cockpit", StaticFiles(directory=_frontend_dir, html=True), name="cockpit")
    app.mount("/frontend", StaticFiles(directory=_frontend_dir, html=True), name="frontend")

if os.path.exists(_showcase_dir):
    app.mount("/showcase", StaticFiles(directory=_showcase_dir, html=True), name="showcase")


class GovernorRequest(BaseModel):
    profile: str

class VaultStoreRequest(BaseModel):
    patient_id: str
    record: Dict[str, Any]

class TriageEvaluationRequest(BaseModel):
    news2_score: int
    shock_index: float
    arrhythmia_type: Optional[str] = "NORMAL"

class DermAnalysisRequest(BaseModel):
    preset_lesion: Optional[str] = "melanoma_suspect"
    custom_mst: Optional[int] = None

class RetinaAnalysisRequest(BaseModel):
    preset_fundus: Optional[str] = "moderate_npdr"

class StethoscopyAnalysisRequest(BaseModel):
    preset_audio: Optional[str] = "pneumonia_crackles"

class DictationRequest(BaseModel):
    preset_audio: Optional[str] = "copd_consultation"

class SoapGenerationRequest(BaseModel):
    consultation_text: Optional[str] = ""
    vitals: Optional[Dict[str, Any]] = None
    modality_findings: Optional[Dict[str, Any]] = None

class RPPGAnalysisRequest(BaseModel):
    patient_state: Optional[str] = "normal"
    sbp: Optional[int] = 120

class ECGAnalysisRequest(BaseModel):
    preset_strip: Optional[str] = "stemi_anterior"

class News2Request(BaseModel):
    rr: Optional[int] = 16
    spo2: Optional[int] = 98
    on_o2: Optional[bool] = False
    sbp: Optional[int] = 120
    hr: Optional[int] = 72
    avpu: Optional[str] = "A"
    temp_c: Optional[float] = 36.8
    spo2_scale: Optional[int] = 1

class GenericSubstituteRequest(BaseModel):
    prescriptions: List[str] = ["Augmentin 625mg", "Atorva 20mg"]

class DrugInteractionsRequest(BaseModel):
    drugs: List[str] = ["Clopidogrel", "Omeprazole"]

class CouncilDeliberateRequest(BaseModel):
    patient_context: Dict[str, Any] = {}

class CardiacPOCUSRequest(BaseModel):
    edv_ml: Optional[float] = 120.0
    esv_ml: Optional[float] = 45.0
    hr_bpm: Optional[int] = 72
    preset_key: Optional[str] = None

class PleuralPOCUSRequest(BaseModel):
    m_mode_variance: Optional[float] = 0.08
    b_lines: Optional[int] = 0
    preset_key: Optional[str] = None

class CounselorSynthesizeRequest(BaseModel):
    condition: Optional[str] = "Hypertension & Cardiovascular Health"
    language_code: Optional[str] = "hi-IN"
    medications: Optional[List[str]] = None
    lifestyle_tips: Optional[List[str]] = None

class DPSGDDeltaRequest(BaseModel):
    weight_delta: Optional[List[float]] = None
    epsilon: Optional[float] = 1.2
    delta: Optional[float] = 1e-5

@app.get("/")
def read_root():
    env = get_execution_environment()
    return {
        "workstation": CONFIG.app_name,
        "version": CONFIG.version,
        "status": "OPERATIONAL",
        "execution_mode": env["execution_mode"],
        "mode_label": env["mode_label"],
        "is_hardware_accelerated": env["is_hardware_accelerated"],
        "is_simulation_fallback": env["is_simulation_fallback"],
        "target_soc": CONFIG.hardware.soc,
        "target_npu": CONFIG.hardware.npu,
        "npu_tops": CONFIG.hardware.npu_peak_tops,
        "privacy": "Zero Cloud Egress (Privacy-Preserving Edge Architecture)",
        "privacy_notice": env["regulatory_notice"],
        "clinical_safety_notice": env["clinical_safety_notice"],
        "cockpit_ui": "/cockpit",
        "showcase_portal": "/showcase",
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    env = get_execution_environment()
    return {
        "status": "healthy",
        "service": CONFIG.app_name,
        "execution_mode": env["execution_mode"],
        "mode_label": env["mode_label"],
        "npu_status": f"ONLINE ({env['mode_label']})",
        "memory_ok": True,
        "storage_enclave": "LOCKED_SECURE"
    }

@app.get("/api/system/mode")
def get_system_mode_endpoint():
    return get_execution_environment()


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

# ----------------- Modality 1: Dermatology & Retina Vision -----------------

@app.post("/api/vision/dermatology/analyze")
def analyze_dermatology_endpoint(req: DermAnalysisRequest = Body(default=DermAnalysisRequest())):
    return analyze_dermatology_lesion(preset_lesion=req.preset_lesion, custom_mst=req.custom_mst)

@app.post("/api/vision/retina/screen")
def screen_retina_endpoint(req: RetinaAnalysisRequest = Body(default=RetinaAnalysisRequest())):
    return screen_retinal_fundus(preset_fundus=req.preset_fundus)

# ----------------- Modality 2: Pulmonary Stethoscopy -----------------

@app.get("/api/audio/stethoscopy/presets")
def get_stethoscopy_presets_endpoint():
    return get_stethoscopy_presets()

@app.post("/api/audio/stethoscopy/analyze")
def analyze_stethoscopy_endpoint(req: StethoscopyAnalysisRequest = Body(default=StethoscopyAnalysisRequest())):
    return analyze_pulmonary_sound(preset_key=req.preset_audio)

# ----------------- Modality 3: Clinical Voice Dictation -----------------

@app.get("/api/transcribe/presets")
def get_dictation_presets_endpoint():
    return get_dictation_presets()

@app.post("/api/transcribe/dictation")
def transcribe_dictation_endpoint(req: DictationRequest = Body(default=DictationRequest())):
    return transcribe_medical_audio(preset_key=req.preset_audio)

# ----------------- Modality 4: Clinical SOAP Scribe & ICD-10 -----------------

@app.post("/api/scribe/soap/generate")
def generate_soap_endpoint(req: SoapGenerationRequest = Body(default=SoapGenerationRequest())):
    return generate_soap_note(
        consultation_text=req.consultation_text,
        vitals=req.vitals,
        modality_findings=req.modality_findings
    )

# ----------------- Modality 5: Contactless Camera rPPG Vitals -----------------

@app.get("/api/vitals/rppg/live")
def get_live_rppg_endpoint(state: str = Query("normal", description="Patient physiological state"), sbp: int = Query(120)):
    return extract_rppg_vitals(patient_state=state, sbp=sbp)

@app.post("/api/vitals/rppg/analyze")
def analyze_rppg_endpoint(req: RPPGAnalysisRequest = Body(default=RPPGAnalysisRequest())):
    return extract_rppg_vitals(patient_state=req.patient_state, sbp=req.sbp)

# ----------------- Modality 6: 12-Lead Paper ECG Digitizer -----------------

@app.get("/api/cardiac/ecg/presets")
def get_ecg_presets_endpoint():
    return get_ecg_presets()

@app.post("/api/cardiac/ecg/digitize")
def digitize_ecg_endpoint(req: ECGAnalysisRequest = Body(default=ECGAnalysisRequest())):
    return digitize_paper_ecg(preset_strip=req.preset_strip)

@app.post("/api/cardiac/ecg/analyze")
def analyze_ecg_endpoint(req: ECGAnalysisRequest = Body(default=ECGAnalysisRequest())):
    return analyze_cardiac_ecg(preset_strip=req.preset_strip)

# ----------------- Phase 4: NEWS2 Calculator & Shock Index -----------------

@app.post("/api/clinical/news2/calculate")
def calculate_news2_endpoint(req: News2Request = Body(default=News2Request())):
    return calculate_news2_score(
        rr=req.rr or 16,
        spo2=req.spo2 or 98,
        on_o2=req.on_o2 or False,
        sbp=req.sbp or 120,
        hr=req.hr or 72,
        avpu=req.avpu or "A",
        temp_c=req.temp_c or 36.8,
        spo2_scale=req.spo2_scale or 1
    )

# ----------------- Phase 4: PMBJP Jan Aushadhi & CYP450 DDI -----------------

@app.get("/api/drugs/jan_aushadhi/catalog")
def get_jan_aushadhi_catalog_endpoint():
    return get_jan_aushadhi_catalog()

@app.post("/api/drugs/jan_aushadhi/substitute")
def substitute_generic_endpoint(req: GenericSubstituteRequest = Body(default=GenericSubstituteRequest())):
    return get_generic_substitution(prescribed_drugs=req.prescriptions)

@app.post("/api/drugs/interactions/check")
def check_interactions_endpoint(req: DrugInteractionsRequest = Body(default=DrugInteractionsRequest())):
    return check_drug_interactions(drugs=req.drugs)

# ----------------- Phase 4: Council of AI Specialists -----------------

@app.post("/api/clinical/council/deliberate")
def deliberate_council_endpoint(req: CouncilDeliberateRequest = Body(default=CouncilDeliberateRequest())):
    return deliberate_case(patient_context=req.patient_context)

# ----------------- Phase 4: Handheld POCUS Ultrasound AI -----------------

@app.get("/api/pocus/presets")
def get_pocus_presets_endpoint():
    return get_pocus_presets()

@app.post("/api/pocus/cardiac/ejection_fraction")
def cardiac_pocus_endpoint(req: CardiacPOCUSRequest = Body(default=CardiacPOCUSRequest())):
    return analyze_cardiac_pocus(
        edv_ml=req.edv_ml,
        esv_ml=req.esv_ml,
        hr_bpm=req.hr_bpm,
        preset_key=req.preset_key
    )

@app.post("/api/pocus/lung/sliding_sign")
def lung_pocus_endpoint(req: PleuralPOCUSRequest = Body(default=PleuralPOCUSRequest())):
    return analyze_pleural_pocus(
        m_mode_variance=req.m_mode_variance,
        b_lines=req.b_lines,
        preset_key=req.preset_key
    )

# ----------------- Phase 4: Regional Speech Counselor (8 Languages) -----------------

@app.get("/api/clinical/counselor/languages")
def get_counselor_languages_endpoint():
    return get_supported_languages()

@app.post("/api/clinical/counselor/synthesize")
def synthesize_counselor_endpoint(req: CounselorSynthesizeRequest = Body(default=CounselorSynthesizeRequest())):
    return synthesize_counseling(
        condition=req.condition or "Hypertension & Cardiovascular Health",
        language_code=req.language_code or "hi-IN",
        medications=req.medications,
        lifestyle_tips=req.lifestyle_tips
    )

# ----------------- Phase 4: DICOM 3.0 Web-PACS Micro-Server -----------------

@app.get("/api/pacs/studies")
def query_pacs_studies_endpoint(patient_id: Optional[str] = Query(None), modality: Optional[str] = Query(None)):
    return query_studies(patient_id=patient_id, modality=modality)

@app.get("/api/pacs/studies/{study_id}/instances/{instance_id}")
def retrieve_pacs_instance_endpoint(study_id: str, instance_id: str):
    try:
        return retrieve_instance(study_id=study_id, instance_id=instance_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/pacs/presets")
def get_pacs_presets_endpoint():
    return get_hu_presets()

# ----------------- Phase 4: Differential Privacy (DP-SGD) Federated Learning -----------------

@app.get("/api/federated/privacy/budget")
def get_federated_budget_endpoint():
    return get_privacy_budget()

@app.post("/api/federated/privacy/sanitize_delta")
def sanitize_federated_delta_endpoint(req: DPSGDDeltaRequest = Body(default=DPSGDDeltaRequest())):
    return sanitize_weight_delta(
        weight_delta=req.weight_delta,
        epsilon=req.epsilon or 1.2,
        delta=req.delta or 1e-5
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
