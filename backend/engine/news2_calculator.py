"""
OmniCare AI — Royal College of Physicians NEWS2 (National Early Warning Score 2) Engine
Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026
Implements 7 standard physiological parameters, clinical escalation pathways, and shock index correlation.
"""

from typing import Dict, Any, Optional

try:
    from config import CONFIG
except ImportError:
    from backend.config import CONFIG


def score_respiration_rate(rr: int) -> int:
    """Royal College of Physicians NEWS2 RR scoring."""
    if rr <= 8:
        return 3
    elif 9 <= rr <= 11:
        return 1
    elif 12 <= rr <= 20:
        return 0
    elif 21 <= rr <= 24:
        return 2
    else:  # rr >= 25
        return 3


def score_spo2(spo2: int, scale: int = 1, on_oxygen: bool = False) -> int:
    """Royal College of Physicians NEWS2 SpO2 scoring (Scale 1 standard or Scale 2 hypercapnic)."""
    if scale == 2:
        if spo2 <= 83:
            return 3
        elif 84 <= spo2 <= 85:
            return 2
        elif 86 <= spo2 <= 87:
            return 1
        elif 88 <= spo2 <= 92:
            return 0
        elif 93 <= spo2 <= 94:
            return 1 if on_oxygen else 0
        elif 95 <= spo2 <= 96:
            return 2 if on_oxygen else 0
        else:  # >= 97
            return 3 if on_oxygen else 0
    else:  # Scale 1 standard
        if spo2 <= 91:
            return 3
        elif 92 <= spo2 <= 93:
            return 2
        elif 94 <= spo2 <= 95:
            return 1
        else:  # >= 96
            return 0


def score_supplemental_oxygen(on_oxygen: bool) -> int:
    """Supplemental oxygen score: Room air = 0, Any supplemental O2 = 2."""
    return 2 if on_oxygen else 0


def score_systolic_bp(sbp: int) -> int:
    """Systolic blood pressure scoring."""
    if sbp <= 90:
        return 3
    elif 91 <= sbp <= 100:
        return 2
    elif 101 <= sbp <= 110:
        return 1
    elif 111 <= sbp <= 219:
        return 0
    else:  # sbp >= 220
        return 3


def score_pulse_rate(hr: int) -> int:
    """Pulse rate scoring."""
    if hr <= 40:
        return 3
    elif 41 <= hr <= 50:
        return 1
    elif 51 <= hr <= 90:
        return 0
    elif 91 <= hr <= 110:
        return 1
    elif 111 <= hr <= 130:
        return 2
    else:  # hr >= 131
        return 3


def score_consciousness(avpu: str) -> int:
    """Consciousness scoring: Alert = 0, Voice / Pain / Unresponsive / Confused = 3."""
    code = avpu.strip().upper()
    if code in ["A", "ALERT"]:
        return 0
    return 3


def score_temperature(temp_c: float) -> int:
    """Temperature (°C) scoring."""
    if temp_c <= 35.0:
        return 3
    elif 35.1 <= temp_c <= 36.0:
        return 1
    elif 36.1 <= temp_c <= 38.0:
        return 0
    elif 38.1 <= temp_c <= 39.0:
        return 1
    else:  # >= 39.1
        return 2


def calculate_news2_score(
    rr: int = 16,
    spo2: int = 98,
    on_o2: bool = False,
    sbp: int = 120,
    hr: int = 72,
    avpu: str = "A",
    temp_c: float = 36.8,
    spo2_scale: int = 1
) -> Dict[str, Any]:
    """
    Computes complete Royal College of Physicians NEWS2 score breakdown,
    clinical risk stratification, shock index, and clinical escalation pathway.
    """
    rr_score = score_respiration_rate(rr)
    spo2_score = score_spo2(spo2, scale=spo2_scale, on_oxygen=on_o2)
    o2_score = score_supplemental_oxygen(on_o2)
    sbp_score = score_systolic_bp(sbp)
    hr_score = score_pulse_rate(hr)
    avpu_score = score_consciousness(avpu)
    temp_score = score_temperature(temp_c)

    scores = {
        "respiration_rate": {"value": rr, "unit": "breaths/min", "score": rr_score},
        "oxygen_saturation": {"value": spo2, "unit": "%", "scale": spo2_scale, "score": spo2_score},
        "supplemental_oxygen": {"value": "Yes" if on_o2 else "Room Air", "score": o2_score},
        "systolic_blood_pressure": {"value": sbp, "unit": "mmHg", "score": sbp_score},
        "pulse_rate": {"value": hr, "unit": "bpm", "score": hr_score},
        "consciousness_avpu": {"value": avpu.upper(), "score": avpu_score},
        "temperature": {"value": temp_c, "unit": "°C", "score": temp_score}
    }

    total_score = sum(item["score"] for item in scores.values())
    has_extreme_single_score = any(item["score"] >= 3 for item in scores.values())

    # Shock Index calculation (HR / SBP)
    shock_index = round(hr / sbp, 2) if sbp > 0 else 0.0
    if shock_index > 0.9:
        shock_status = "CRITICAL_HYPOPERFUSION"
        shock_interpretation = "Severe occult hypoperfusion / hemodynamic collapse risk"
    elif shock_index > 0.7:
        shock_status = "ELEVATED_RISK"
        shock_interpretation = "Mild shock or early compensatory phase"
    else:
        shock_status = "NORMAL_PERFUSION"
        shock_interpretation = "Normal physiological perfusion"

    # Clinical Risk Stratification
    if total_score >= 7:
        clinical_risk = "HIGH_CLINICAL_RISK"
        urgency = "EMERGENCY_IMMEDIATE"
        color = "#EF4444"
        escalation_pathway = {
            "response_level": "Emergency response (ICU / Critical Care Outreach)",
            "timeframe": "Immediate (<15 minutes)",
            "actions": [
                "Continuous monitoring of vital signs",
                "Senior medical officer bedside assessment",
                "Immediate consultation with ICU / acute response team",
                "Prepare for airway stabilization and intravenous resuscitation"
            ]
        }
    elif total_score in [5, 6]:
        clinical_risk = "MEDIUM_CLINICAL_RISK"
        urgency = "URGENT_1_HOUR"
        color = "#F59E0B"
        escalation_pathway = {
            "response_level": "Urgent medical review by registered doctor",
            "timeframe": "Within 1 hour",
            "actions": [
                "Increase vital signs monitoring frequency to minimum 1 hour",
                "Urgent clinical review by ward doctor",
                "Assess whether treatment escalation is needed"
            ]
        }
    elif has_extreme_single_score:
        clinical_risk = "LOW_MEDIUM_CLINICAL_RISK"
        urgency = "URGENT_WARD_REVIEW"
        color = "#F59E0B"
        escalation_pathway = {
            "response_level": "Urgent review by registered nurse / resident",
            "timeframe": "Within 30 minutes",
            "actions": [
                "Specific single physiological parameter is critically abnormal (score 3)",
                "Increase monitoring frequency to minimum 4 hours",
                "Inform nurse in charge and duty doctor"
            ]
        }
    else:
        clinical_risk = "LOW_CLINICAL_RISK"
        urgency = "ROUTINE_WARD_CARE"
        color = "#10B981"
        escalation_pathway = {
            "response_level": "Ward-based routine response",
            "timeframe": "Next routine ward round (every 4-12 hours)",
            "actions": [
                "Continue standard 12-hourly or 4-hourly routine monitoring",
                "Standard nursing clinical care"
            ]
        }

    return {
        "engine": "Royal College of Physicians NEWS2 (On-Device)",
        "total_score": total_score,
        "max_score": 20,
        "clinical_risk": clinical_risk,
        "urgency": urgency,
        "indicator_color": color,
        "parameter_breakdown": scores,
        "shock_index": {
            "value": shock_index,
            "status": shock_status,
            "interpretation": shock_interpretation
        },
        "escalation_pathway": escalation_pathway,
        "guideline_reference": "Royal College of Physicians National Early Warning Score 2 (NEWS2) 2017/2020 Update"
    }
