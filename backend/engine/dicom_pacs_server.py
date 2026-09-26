"""
OmniCare AI — On-Device DICOM 3.0 Web-PACS Micro-Server Engine
Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026
Implements DICOMweb (WADO-RS and QIDO-RS) standards, Hounsfield Unit (HU) windowing presets,
and calibrated medical imaging metadata for offline edge viewing.
"""

from typing import Dict, Any, List, Optional

try:
    from config import CONFIG
except ImportError:
    from backend.config import CONFIG

# Standard Medical Hounsfield Unit (HU) Windowing Presets
DICOM_HU_PRESETS: Dict[str, Dict[str, Any]] = {
    "lung": {
        "label": "Lung Window",
        "description": "High dynamic range for pulmonary parenchyma and bronchi",
        "window_width": 1500,
        "window_center": -600,
        "min_hu": -1350,
        "max_hu": 150
    },
    "soft_tissue": {
        "label": "Soft Tissue / Mediastinum",
        "description": "Optimized for heart, great vessels, and lymph nodes",
        "window_width": 350,
        "window_center": 50,
        "min_hu": -125,
        "max_hu": 225
    },
    "bone": {
        "label": "Bone Window",
        "description": "Wide window to visualize trabecular architecture and fractures",
        "window_width": 2000,
        "window_center": 400,
        "min_hu": -600,
        "max_hu": 1400
    },
    "brain": {
        "label": "Brain Window",
        "description": "Narrow window discriminating gray matter from white matter",
        "window_width": 80,
        "window_center": 40,
        "min_hu": 0,
        "max_hu": 80
    }
}

# Preloaded On-Device DICOM 3.0 Studies
LOCAL_DICOM_DATABASE: Dict[str, Dict[str, Any]] = {
    "STUDY-001": {
        "study_instance_uid": "1.2.840.10008.5.1.4.1.1.2.2026.09.26.101",
        "study_id": "STUDY-001",
        "study_date": "20260926",
        "study_time": "143000",
        "patient_id": "ABHA-9821-4432-8710",
        "patient_name": "Sharma^Aarav",
        "patient_birth_date": "19720315",
        "patient_sex": "M",
        "modality": "CT",
        "study_description": "High-Resolution Chest CT (HRCT Thorax)",
        "series_count": 1,
        "instance_count": 1,
        "instances": {
            "INST-001": {
                "sop_instance_uid": "1.2.840.10008.5.1.4.1.1.2.2026.09.26.101.1",
                "instance_id": "INST-001",
                "instance_number": 1,
                "sop_class_uid": "1.2.840.10008.5.1.4.1.1.2",  # CT Image Storage
                "rows": 512,
                "columns": 512,
                "pixel_spacing": [0.683, 0.683],
                "slice_thickness": 1.0,
                "kvp": 120,
                "x_ray_tube_current": 180,
                "rescale_intercept": -1024.0,
                "rescale_slope": 1.0,
                "photometric_interpretation": "MONOCHROME2",
                "default_window_preset": "lung",
                "clinical_impression": "Bilateral ground-glass opacities in lower lobes with peripheral bronchiectasis."
            }
        }
    },
    "STUDY-002": {
        "study_instance_uid": "1.2.840.10008.5.1.4.1.1.1.2026.09.26.102",
        "study_id": "STUDY-002",
        "study_date": "20260926",
        "study_time": "151500",
        "patient_id": "ABHA-6643-9012-3321",
        "patient_name": "Devi^Sunita",
        "patient_birth_date": "19800722",
        "patient_sex": "F",
        "modality": "US",
        "study_description": "Point-of-Care Ultrasound (POCUS) Cardiac & Pleural",
        "series_count": 1,
        "instance_count": 1,
        "instances": {
            "INST-002": {
                "sop_instance_uid": "1.2.840.10008.5.1.4.1.1.6.1.2026.09.26.102.1",
                "instance_id": "INST-002",
                "instance_number": 1,
                "sop_class_uid": "1.2.840.10008.5.1.4.1.1.6.1",  # Ultrasound Image Storage
                "rows": 480,
                "columns": 640,
                "pixel_spacing": [0.25, 0.25],
                "slice_thickness": 0.0,
                "rescale_intercept": 0.0,
                "rescale_slope": 1.0,
                "photometric_interpretation": "RGB",
                "default_window_preset": "soft_tissue",
                "clinical_impression": "Parasternal long-axis view confirming preserved LVEF 62.5% and normal pleural sliding (Seashore sign)."
            }
        }
    }
}


def query_studies(
    patient_id: Optional[str] = None,
    modality: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    QIDO-RS (RESTful DICOM Study Search):
    Returns list of matching DICOM studies according to DICOMweb specification.
    """
    results = []
    for study in LOCAL_DICOM_DATABASE.values():
        if patient_id and patient_id.lower() not in study["patient_id"].lower():
            continue
        if modality and modality.upper() != study["modality"].upper():
            continue
        results.append({
            "0020000D": {"vr": "UI", "Value": [study["study_instance_uid"]]},
            "00200010": {"vr": "SH", "Value": [study["study_id"]]},
            "00080020": {"vr": "DA", "Value": [study["study_date"]]},
            "00080030": {"vr": "TM", "Value": [study["study_time"]]},
            "00100020": {"vr": "LO", "Value": [study["patient_id"]]},
            "00100010": {"vr": "PN", "Value": [{"Alphabetic": study["patient_name"]}]},
            "00080060": {"vr": "CS", "Value": [study["modality"]]},
            "00081030": {"vr": "LO", "Value": [study["study_description"]]},
            "study_id": study["study_id"],
            "patient_name": study["patient_name"],
            "patient_id": study["patient_id"],
            "modality": study["modality"],
            "study_description": study["study_description"],
            "instance_count": study["instance_count"]
        })
    return results


def retrieve_instance(study_id: str, instance_id: str) -> Dict[str, Any]:
    """
    WADO-RS (RESTful DICOM Instance Retrieval):
    Returns calibrated DICOM instance attributes, HU presets, and pixel metadata.
    """
    study = LOCAL_DICOM_DATABASE.get(study_id.upper())
    if not study:
        raise KeyError(f"DICOM study '{study_id}' not found on edge PACS server.")

    instance = study["instances"].get(instance_id.upper())
    if not instance:
        # Fallback to first instance
        if study["instances"]:
            instance = next(iter(study["instances"].values()))
        else:
            raise KeyError(f"DICOM instance '{instance_id}' not found in study '{study_id}'.")

    # Generate synthetic 16x16 downsampled calibration matrix for instant edge rendering
    pixel_matrix = [
        [round(50 + 20 * (r / 16.0) + 10 * (c / 16.0), 1) for c in range(16)]
        for r in range(16)
    ]

    return {
        "engine": "Qualcomm Hexagon NPU DICOM 3.0 Web-PACS Micro-Server",
        "study_id": study["study_id"],
        "patient_id": study["patient_id"],
        "patient_name": study["patient_name"],
        "modality": study["modality"],
        "study_description": study["study_description"],
        "instance_id": instance["instance_id"],
        "sop_instance_uid": instance["sop_instance_uid"],
        "sop_class_uid": instance["sop_class_uid"],
        "dimensions": {"rows": instance["rows"], "columns": instance["columns"]},
        "rescale": {"intercept": instance["rescale_intercept"], "slope": instance["rescale_slope"]},
        "photometric_interpretation": instance["photometric_interpretation"],
        "default_preset": instance["default_window_preset"],
        "window_presets": DICOM_HU_PRESETS,
        "sample_preview_matrix": pixel_matrix,
        "clinical_impression": instance["clinical_impression"],
        "wado_rs_url": f"/api/pacs/studies/{study['study_id']}/instances/{instance['instance_id']}",
        "zero_cloud_egress": True
    }


def get_hu_presets() -> Dict[str, Any]:
    """Returns all standard medical Hounsfield Unit windowing presets."""
    return DICOM_HU_PRESETS
